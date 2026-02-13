"""
GFS (Grandfather-Father-Son) retention policy for backup folders.

- Son (daily): keep the last N days (one backup per day, e.g. 7).
- Father (weekly): keep the last N weeks for the chosen weekday (e.g. 4 Sundays). Use 0 to disable.
- Grandfather (monthly): keep the last N months (first day of month, e.g. 12).
- Great-grandfather (yearly): keep the last N years (1st January, e.g. 4). Use 0 to disable.
"""

import re
import shlex
import shutil
from datetime import datetime
from pathlib import Path

from paramiko import SSHClient

# Folder names are expected to match: 2025-02-12_14-30
BACKUP_FOLDER_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$")


def parse_backup_folder_name(name: str) -> datetime | None:
    """Parse a backup folder name (YYYY-MM-DD_HH-MM) into a datetime. Returns None if invalid."""
    if not BACKUP_FOLDER_PATTERN.match(name):
        return None
    try:
        return datetime.strptime(name, "%Y-%m-%d_%H-%M")
    except ValueError:
        return None


def compute_folders_to_keep(
    folder_dates: list[tuple[str, datetime]],
    *,
    daily_days: int = 7,
    weekly_weeks: int = 4,
    weekly_weekday: int = 6,
    monthly_months: int = 12,
    yearly_years: int = 0,
) -> set[str]:
    """
    Compute which folder names to keep under the GFS policy.

    folder_dates: list of (folder_name, parsed_datetime), any order.
    weekly_weekday: 0=Monday, 6=Sunday.
    Use weekly_weeks=0 or yearly_years=0 to disable that tier.

    Returns the set of folder names to keep.
    """
    if not folder_dates:
        return set()

    # Sort by date descending (newest first)
    sorted_folders = sorted(folder_dates, key=lambda x: x[1], reverse=True)

    keep: set[str] = set()

    # Great-grandfather (yearly): 1st January, keep yearly_years
    if yearly_years > 0:
        yearly = [(n, d) for n, d in sorted_folders if d.month == 1 and d.day == 1]
        for name, _ in yearly[:yearly_years]:
            keep.add(name)

    # Grandfather (monthly): first day of month, keep monthly_months (excluding yearly)
    monthly = [(n, d) for n, d in sorted_folders if d.day == 1 and n not in keep]
    for name, _ in monthly[:monthly_months]:
        keep.add(name)

    # Father (weekly): chosen weekday, keep weekly_weeks (excluding already kept)
    if weekly_weeks > 0:
        weekly = [
            (n, d) for n, d in sorted_folders if d.weekday() == weekly_weekday and n not in keep
        ]
        for name, _ in weekly[:weekly_weeks]:
            keep.add(name)

    # Son (daily): one backup per day for the last daily_days (excluding already kept)
    by_day: dict[tuple[int, int, int], list[tuple[str, datetime]]] = {}
    for name, dt in sorted_folders:
        if name in keep:
            continue
        key = (dt.year, dt.month, dt.day)
        if key not in by_day:
            by_day[key] = []
        by_day[key].append((name, dt))

    # Sort days by date desc, take the latest backup per day for daily_days days
    days_sorted = sorted(by_day.keys(), reverse=True)
    for day_key in days_sorted[:daily_days]:
        # Latest backup of that day
        day_folders = sorted(by_day[day_key], key=lambda x: x[1], reverse=True)
        if day_folders:
            keep.add(day_folders[0][0])

    return keep


def list_local_backup_folders(base_path: Path) -> list[tuple[str, datetime]]:
    """List backup folders under base_path. Returns [(folder_name, datetime), ...]."""
    result: list[tuple[str, datetime]] = []
    if not base_path.exists():
        return result
    for child in base_path.iterdir():
        if not child.is_dir():
            continue
        dt = parse_backup_folder_name(child.name)
        if dt is not None:
            result.append((child.name, dt))
    return result


def list_remote_backup_folders(ssh_client: SSHClient, base_path: str) -> list[tuple[str, datetime]]:
    """List backup folders on the remote host under base_path."""
    result: list[tuple[str, datetime]] = []
    try:
        sftp = ssh_client.open_sftp()
        try:
            for entry in sftp.listdir_attr(base_path):
                if not entry.st_mode or not (entry.st_mode & 0o040000):
                    continue
                dt = parse_backup_folder_name(entry.filename)
                if dt is not None:
                    result.append((entry.filename, dt))
        finally:
            sftp.close()
    except Exception:
        pass
    return result


def apply_retention_local(
    base_path: Path,
    keep_folders: set[str],
    logger,
) -> None:
    """Delete local backup folders that are not in keep_folders."""
    for child in base_path.iterdir():
        if not child.is_dir() or child.name in keep_folders:
            continue
        if parse_backup_folder_name(child.name) is None:
            continue
        try:
            shutil.rmtree(child)
            logger.success(f"Retention: removed local folder {child.name}")
        except Exception as e:
            logger.error(f"Retention: failed to remove local folder {child.name}: {e}")


def apply_retention_remote(
    ssh_client: SSHClient,
    base_path: str,
    keep_folders: set[str],
    logger,
) -> None:
    """Delete remote backup folders that are not in keep_folders."""
    try:
        sftp = ssh_client.open_sftp()
        try:
            for entry in sftp.listdir_attr(base_path):
                if not entry.st_mode or not (entry.st_mode & 0o040000):
                    continue
                name = entry.filename
                if name in keep_folders or parse_backup_folder_name(name) is None:
                    continue
                full_path = f"{base_path.rstrip('/')}/{name}"
                stdin, stdout, stderr = ssh_client.exec_command(f"rm -rf {shlex.quote(full_path)}")
                stdout.channel.recv_exit_status()
                err = stderr.read().decode().strip()
                if err:
                    logger.error(f"Retention: failed to remove remote folder {name}: {err}")
                else:
                    logger.success(f"Retention: removed remote folder {name}")
        finally:
            sftp.close()
    except Exception as e:
        logger.error(f"Retention: failed to list/remove remote folders: {e}")


def run_retention_local(
    base_path: Path,
    logger,
    *,
    daily_days: int = 7,
    weekly_weeks: int = 4,
    weekly_weekday: int = 6,
    monthly_months: int = 12,
    yearly_years: int = 0,
) -> None:
    """Run GFS retention on local backup directory."""
    folder_dates = list_local_backup_folders(base_path)
    keep = compute_folders_to_keep(
        folder_dates,
        daily_days=daily_days,
        weekly_weeks=weekly_weeks,
        weekly_weekday=weekly_weekday,
        monthly_months=monthly_months,
        yearly_years=yearly_years,
    )
    to_remove = len(folder_dates) - len(keep)
    if to_remove <= 0:
        logger.debug("Retention: nothing to prune locally.")
        return
    logger.debug(f"Retention: keeping {len(keep)} local folders, removing {to_remove}.")
    apply_retention_local(base_path, keep, logger)


def run_retention_remote(
    ssh_client: SSHClient,
    base_path: str,
    logger,
    *,
    daily_days: int = 7,
    weekly_weeks: int = 4,
    weekly_weekday: int = 6,
    monthly_months: int = 12,
    yearly_years: int = 0,
) -> None:
    """Run GFS retention on remote backup directory."""
    folder_dates = list_remote_backup_folders(ssh_client, base_path)
    keep = compute_folders_to_keep(
        folder_dates,
        daily_days=daily_days,
        weekly_weeks=weekly_weeks,
        weekly_weekday=weekly_weekday,
        monthly_months=monthly_months,
        yearly_years=yearly_years,
    )
    to_remove = len(folder_dates) - len(keep)
    if to_remove <= 0:
        logger.debug("Retention: nothing to prune on remote.")
        return
    logger.debug(f"Retention: keeping {len(keep)} remote folders, removing {to_remove}.")
    apply_retention_remote(ssh_client, base_path, keep, logger)
