#!/usr/bin/env python3
"""
System Health Monitoring Script
--------------------------------
Monitors the health of a Linux system by checking:
  - CPU usage
  - Memory usage
  - Disk space usage
  - Running processes count

If any metric exceeds the predefined threshold,
an alert is printed to the console AND written to a log file.

Author: Kishore K S
"""

import psutil
import logging
import datetime
import os

# ─────────────────────────────────────────────
# CONFIGURATION — Thresholds (in percentage %)
# ─────────────────────────────────────────────
CPU_THRESHOLD    = 80   # Alert if CPU usage exceeds 80%
MEMORY_THRESHOLD = 80   # Alert if Memory usage exceeds 80%
DISK_THRESHOLD   = 80   # Alert if Disk usage exceeds 80%
PROCESS_THRESHOLD = 300  # Alert if running processes exceed 300

# Log file location
LOG_FILE = "system_health.log"

# ─────────────────────────────────────────────
# LOGGING SETUP
# Logs to both console and a log file
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),      # Write to log file
        logging.StreamHandler()             # Print to console
    ]
)

logger = logging.getLogger(__name__)


def check_cpu():
    """Check CPU usage and alert if above threshold."""
    # interval=1 means it measures CPU over 1 second for accuracy
    cpu_usage = psutil.cpu_percent(interval=1)
    logger.info(f"CPU Usage       : {cpu_usage}%  (Threshold: {CPU_THRESHOLD}%)")

    if cpu_usage > CPU_THRESHOLD:
        logger.warning(f"⚠️  ALERT: CPU usage is HIGH! {cpu_usage}% exceeds {CPU_THRESHOLD}%")
    return cpu_usage


def check_memory():
    """Check RAM usage and alert if above threshold."""
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    used_gb  = memory.used  / (1024 ** 3)
    total_gb = memory.total / (1024 ** 3)

    logger.info(f"Memory Usage    : {memory_usage}%  ({used_gb:.2f} GB / {total_gb:.2f} GB)  (Threshold: {MEMORY_THRESHOLD}%)")

    if memory_usage > MEMORY_THRESHOLD:
        logger.warning(f"⚠️  ALERT: Memory usage is HIGH! {memory_usage}% exceeds {MEMORY_THRESHOLD}%")
    return memory_usage


def check_disk():
    """Check disk space usage and alert if above threshold."""
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    used_gb  = disk.used  / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)

    logger.info(f"Disk Usage      : {disk_usage}%  ({used_gb:.2f} GB / {total_gb:.2f} GB)  (Threshold: {DISK_THRESHOLD}%)")

    if disk_usage > DISK_THRESHOLD:
        logger.warning(f"⚠️  ALERT: Disk usage is HIGH! {disk_usage}% exceeds {DISK_THRESHOLD}%")
    return disk_usage


def check_processes():
    """Check the number of running processes and alert if above threshold."""
    process_count = len(psutil.pids())

    logger.info(f"Running Processes: {process_count}  (Threshold: {PROCESS_THRESHOLD})")

    if process_count > PROCESS_THRESHOLD:
        logger.warning(f"⚠️  ALERT: Too many processes running! {process_count} exceeds {PROCESS_THRESHOLD}")
    return process_count


def run_health_check():
    """Run all health checks and produce a summary report."""
    logger.info("=" * 60)
    logger.info("       SYSTEM HEALTH CHECK REPORT")
    logger.info(f"       {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    cpu     = check_cpu()
    memory  = check_memory()
    disk    = check_disk()
    procs   = check_processes()

    logger.info("-" * 60)

    # Overall system status
    alerts = []
    if cpu    > CPU_THRESHOLD:      alerts.append("CPU")
    if memory > MEMORY_THRESHOLD:   alerts.append("Memory")
    if disk   > DISK_THRESHOLD:     alerts.append("Disk")
    if procs  > PROCESS_THRESHOLD:  alerts.append("Processes")

    if alerts:
        logger.warning(f"🔴 System Status : UNHEALTHY — Issues detected in: {', '.join(alerts)}")
    else:
        logger.info("🟢 System Status : HEALTHY — All metrics are within normal range.")

    logger.info("=" * 60)
    logger.info(f"Log saved to: {os.path.abspath(LOG_FILE)}")


if __name__ == "__main__":
    run_health_check()
