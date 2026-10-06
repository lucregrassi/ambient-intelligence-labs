"""
Read a Tuya PIR motion sensor through the Tuya Cloud OpenAPI.

Ambient Intelligence — MSc in Robotics Engineering
University of Genoa

Author: Lucrezia Grassi <lucrezia.grassi@unige.it>

Run:  python3 main.py                 (one reading every 5 seconds)
      python3 main.py --interval 60   (one reading every minute)
"""

import argparse
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from tuya_iot import TuyaOpenAPI
from colorama import Fore, Style

parser = argparse.ArgumentParser(description="Read a Tuya PIR sensor from the cloud.")
parser.add_argument("--interval", type=float, default=5.0,
                    help="seconds between cloud requests (default: 5)")
args = parser.parse_args()

load_dotenv(override=True)


def env(name: str) -> str:
    """Read a variable from .env, and fail clearly if it is missing."""
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise SystemExit(f"Missing {name} in your .env file.")
    return value.strip()          # a trailing space in a pasted key breaks the signature


ACCESS_ID = env("ACCESS_ID")
ACCESS_SECRET = env("ACCESS_SECRET")
ENDPOINT = env("ENDPOINT")
DEVICE_ID = env("DEVICE_ID")

USERNAME = env("TUYA_USERNAME")
PASSWORD = env("TUYA_PASSWORD")
COUNTRY_CODE = env("COUNTRY_CODE").lstrip("+")     # Tuya wants "39", not "+39"

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)

try:
    # "tuyaSmart" is the schema of the Tuya app; the Smart Life app is "smartlife".
    response = openapi.connect(USERNAME, PASSWORD, COUNTRY_CODE, "tuyaSmart")
except Exception as exc:
    raise SystemExit(f"\nCould not reach {ENDPOINT}: {exc}\n"
                     "Check that you are online and that ENDPOINT is spelled correctly.\n")

response = response or {}          # the library returns None on an HTTP error
if not response.get("success"):
    raise SystemExit(
        f"\nLogin failed: {response.get('msg')} (code {response.get('code')})\n"
        "Things to check, in this order:\n"
        "  1. ENDPOINT matches the data centre of your cloud project\n"
        "     (Central Europe -> https://openapi.tuyaeu.com)\n"
        "  2. TUYA_USERNAME and TUYA_PASSWORD are the credentials of the MOBILE APP\n"
        "     account, not of the developer platform account\n"
        "  3. COUNTRY_CODE is the country you chose when you created the app account\n"
        "  4. ACCESS_ID and ACCESS_SECRET were copied whole, with no trailing space\n"
    )

print(f"Connected to {ENDPOINT} — polling every {args.interval:g} s. Ctrl-C to stop.\n")


def read_device():
    """Ask the cloud for the device's shadow: {code: (value, time in ms)}, or None.

    The shadow is the cloud's copy of the device: the last value of each property,
    with the moment the cloud received it.
    """
    r = openapi.get(f"/v2.0/cloud/thing/{DEVICE_ID}/shadow/properties") or {}
    if not r.get("success"):
        print(f"Request failed: {r.get('msg')} (code {r.get('code')})")
        return None
    return {p["code"]: (p["value"], p.get("time")) for p in r["result"]["properties"]}


def age(ms):
    """How long ago the sensor reported this value."""
    if ms is None:
        return ""
    seconds = time.time() - ms / 1000
    if seconds < 10:
        return "(just now)"
    if seconds < 90:
        return f"({seconds:.0f} s ago)"
    if seconds < 5400:
        return f"({seconds / 60:.0f} min ago)"
    return f"({seconds / 3600:.0f} h ago)"


first_reading = True
calls = 0

try:
    while True:
        try:
            # One GET request = one API call against your monthly quota.
            status = read_device()
            calls += 1

            if status is None:
                time.sleep(args.interval)
                continue

            # Not every PIR model calls motion "pir_state", so show the codes once.
            if first_reading:
                print(f"This device reports: {list(status.keys())}\n")
                first_reading = False

            motion_status, reported_at = status.get("pir_state", (None, None))

            if motion_status is None:
                print("No 'pir_state' field in the response — check the codes printed above.")
                time.sleep(args.interval)
                continue

            stamp = datetime.now().strftime("%H:%M:%S")
            colour = Fore.GREEN if motion_status == "pir" else Fore.RED
            label = "MOTION" if motion_status == "pir" else "  --  "
            print(f"{stamp}  {colour}{label}{Style.RESET_ALL}   "
                  f"{age(reported_at):<16} "
                  f"[{calls} API calls this run]")

            time.sleep(args.interval)

        except Exception as exc:
            # Keep polling: a dropped connection must not end the session.
            print(f"{datetime.now():%H:%M:%S} - Error: {exc}")
            time.sleep(5)

except KeyboardInterrupt:
    print(f"\nStopped after {calls} API calls.")
