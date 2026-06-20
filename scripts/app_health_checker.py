#!/usr/bin/env python3
"""
Application Health Checker
---------------------------
Checks the uptime and health of one or more applications
by sending HTTP requests and evaluating the response.

Determines if an application is:
  - UP   → HTTP 200-399 response received
  - DOWN → HTTP 400+, timeout, or connection error

Results are printed to the console AND saved to a log file.

Author: Kishore K S
"""

import requests
import logging
import datetime
import os

# ─────────────────────────────────────────────
# CONFIGURATION
# Add all application URLs you want to monitor
# ─────────────────────────────────────────────
APPLICATIONS = [
    {"name": "Wisecow App",       "url": "http://wisecow.local"},
    {"name": "Google",            "url": "https://www.google.com"},
    {"name": "GitHub",            "url": "https://www.github.com"},
    {"name": "Fake Down Service", "url": "http://localhost:9999"},  # Intentionally down
]

# Timeout in seconds for each HTTP request
REQUEST_TIMEOUT = 5

# Log file location
LOG_FILE = "app_health.log"

# ─────────────────────────────────────────────
# LOGGING SETUP
# Logs to both console and a log file
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def check_application(name, url):
    """
    Check if a single application is UP or DOWN.

    Returns a dict with:
      - name: application name
      - url: the URL checked
      - status: 'UP' or 'DOWN'
      - http_code: HTTP status code (or None if unreachable)
      - response_time: time taken in seconds (or None)
      - reason: human-readable explanation
    """
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response_time = response.elapsed.total_seconds()
        http_code = response.status_code

        # HTTP 200-399 = UP, anything else = DOWN
        if 200 <= http_code < 400:
            status = "UP"
            reason = f"HTTP {http_code} - Application is responding normally"
            logger.info(f"🟢 {name:<25} | Status: {status} | HTTP: {http_code} | Response Time: {response_time:.3f}s")
        else:
            status = "DOWN"
            reason = f"HTTP {http_code} - Application returned an error response"
            logger.warning(f"🔴 {name:<25} | Status: {status} | HTTP: {http_code} | Response Time: {response_time:.3f}s")

    except requests.exceptions.ConnectionError:
        status = "DOWN"
        http_code = None
        response_time = None
        reason = "Connection refused or host unreachable"
        logger.warning(f"🔴 {name:<25} | Status: {status} | REASON: {reason}")

    except requests.exceptions.Timeout:
        status = "DOWN"
        http_code = None
        response_time = None
        reason = f"Request timed out after {REQUEST_TIMEOUT} seconds"
        logger.warning(f"🔴 {name:<25} | Status: {status} | REASON: {reason}")

    except requests.exceptions.RequestException as e:
        status = "DOWN"
        http_code = None
        response_time = None
        reason = f"Unexpected error: {str(e)}"
        logger.warning(f"🔴 {name:<25} | Status: {status} | REASON: {reason}")

    return {
        "name": name,
        "url": url,
        "status": status,
        "http_code": http_code,
        "response_time": response_time,
        "reason": reason
    }


def run_health_check():
    """Check all configured applications and print a summary report."""
    logger.info("=" * 60)
    logger.info("       APPLICATION HEALTH CHECK REPORT")
    logger.info(f"       {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    results = []
    for app in APPLICATIONS:
        result = check_application(app["name"], app["url"])
        results.append(result)

    # Summary
    logger.info("-" * 60)
    total   = len(results)
    up      = sum(1 for r in results if r["status"] == "UP")
    down    = total - up

    logger.info(f"Total Applications : {total}")
    logger.info(f"UP                 : {up}")
    logger.info(f"DOWN               : {down}")

    if down == 0:
        logger.info("🟢 Overall Status  : ALL APPLICATIONS ARE HEALTHY")
    else:
        logger.warning(f"🔴 Overall Status  : {down} APPLICATION(S) ARE DOWN")
        logger.warning("   Applications that need attention:")
        for r in results:
            if r["status"] == "DOWN":
                logger.warning(f"   → {r['name']} ({r['url']}) — {r['reason']}")

    logger.info("=" * 60)
    logger.info(f"Log saved to: {os.path.abspath(LOG_FILE)}")


if __name__ == "__main__":
    run_health_check()
