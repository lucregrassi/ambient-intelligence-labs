"""
Read a Tuya PIR motion sensor through the Tuya Cloud OpenAPI.

Ambient Intelligence — MSc in Robotics Engineering
University of Genoa

Author: Lucrezia Grassi <lucrezia.grassi@unige.it>

Run:  python3 main.py                 (one reading every 5 seconds)
      python3 main.py --interval 1    (one reading every second)
      python3 main.py --csv motion.csv
"""

import argparse
import csv
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from tuya_iot import TuyaOpenAPI
from colorama import Fore, Style

# Optional: the script must run without it. On Linux it needs espeak-ng.
try:
    import pyttsx3
    engine = pyttsx3.init()
except Exception as exc:
    print(f"Text to speech not available ({exc}) — continuing without it.")
    engine = None

parser = argparse.ArgumentParser(description="Read a Tuya PIR sensor from the cloud.")
parser.add_argument("--interval", type=float, default=5.0,
                    help="seconds between cloud requests (default: 5)")
parser.add_argument("--csv", default=None,
                    help="append every reading to this CSV file")
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

writer = None
csvfile = None
if args.csv:
    csvfile = open(args.csv, "a", newline="")
    writer = csv.writer(csvfile)
    if csvfile.tell() == 0:
        writer.writerow(["timestamp", "device_id", "pir", "battery_percentage"])
    print(f"Writing every reading to {args.csv}\n")

previous_motion_status = None
first_reading = True
calls = 0

try:
    while True:
        try:
            # One GET request = one API call against your monthly quota.
            response = openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/status")
            calls += 1

            if not response.get("success"):
                print(f"Request failed: {response.get('msg')} (code {response.get('code')})")
                time.sleep(args.interval)
                continue

            status = {item["code"]: item["value"] for item in response["result"]}

            # Not every PIR model calls motion "pir", so show the codes once.
            if first_reading:
                print(f"This device reports: {list(status.keys())}\n")
                first_reading = False

            motion_status = status.get("pir")
            battery = status.get("battery_percentage")

            if motion_status is None:
                print("No 'pir' field in the response — check the codes printed above.")
                time.sleep(args.interval)
                continue

            stamp = datetime.now().strftime("%H:%M:%S")
            colour = Fore.GREEN if motion_status == "pir" else Fore.RED
            label = "MOTION" if motion_status == "pir" else "  --  "
            print(f"{stamp}  {colour}{label}{Style.RESET_ALL}   "
                  f"battery {battery}%   [{calls} API calls this run]")

            if writer:
                writer.writerow([datetime.now().isoformat(timespec="seconds"),
                                 DEVICE_ID, motion_status, battery])
                csvfile.flush()      # without this the file stays empty until you quit

            if engine and motion_status == "pir" and previous_motion_status != "pir":
                engine.say("Motion detected!")
                engine.runAndWait()

            previous_motion_status = motion_status
            time.sleep(args.interval)

        except Exception as exc:
            # Keep polling: a dropped connection must not end the session.
            print(f"{datetime.now():%H:%M:%S} - Error: {exc}")
            time.sleep(5)

except KeyboardInterrupt:
    print(f"\nStopped after {calls} API calls.")
finally:
    if csvfile:
        csvfile.close()
