# Reading a PIR motion sensor from the cloud — step by step

Everything we do together in the laboratory, in order. Nothing here has to be done in advance —
the accounts are created during the session on purpose, so that you see what each one is for.
Before you come, read the network section of the [README](README.md): the sensor cannot join
eduroam, and without a 2.4 GHz hotspot nothing below will work.

---

## Step 1 — Install the mobile app

Install **Tuya**, published by Tuya Smart Inc. The app used to be called *Tuya Smart* and
is now listed as **"Tuya: Smart Life, Smart Living"** — same app, same publisher, renamed.

- Android: <https://play.google.com/store/apps/details?id=com.tuya.smart>
- iOS: <https://apps.apple.com/us/app/tuya-smart/id1034649547>

Create an account in the app and **note which country you selected** — you will need it
later as `COUNTRY_CODE`.

---

## Step 2 — Create a cloud project

Go to **<https://platform.tuya.com>** and register or log in.
(The older address `iot.tuya.com` still works and shows the same platform.)

Create a **Cloud Project** with:

| Field | Value |
|---|---|
| Project name | anything |
| Description | anything |
| Industry | anything that fits — e.g. Education/Campus. It does not affect the API. |
| **Development Method** | **Smart Home** |
| **Data Center** | **Central Europe** |

The first three are yours to choose. The last two are not.

**Development Method** has two options, Custom and Smart Home. Choose **Smart Home**: it is
the one that lets you link a mobile-app account and read the devices already paired in it.
Tuya's own description of this option now says "link devices with your Smart Life app" —
ignore the app name, the option is the right one for the Tuya app too.

**Data Center** must match the region of the account you created in the app in step 1, and
it must match `ENDPOINT` in your `.env` later. If they disagree, everything appears to work
until the device list comes back empty. Central Europe corresponds to
`https://openapi.tuyaeu.com`.

You do not need to touch anything else here. Tuya has already authorised the API services a
Smart Home project needs, and that default set is enough for this exercise — ignore any guide
that tells you to subscribe to a list of extra ones. The one thing you do have to do is start
their free trial.

### Start the free trial

Go to **Cloud → Cloud Services → My Services**. For each service your project is subscribed to,
**start the free trial**. It is free and takes a moment, and until you do it every request comes
back as `No permissions`.

The trial allows **26,000 API calls and 68,000 messages a month**, with no overage billing: when the
allowance runs out the service is suspended until the month rolls over.

That is why `main.py` polls every **5 seconds** by default rather than every second. One reading per
second is 86,400 calls a day — enough to burn a month's allowance overnight, from a single script
somebody forgot to close.

---

## Step 3 — Pair the sensor

1. Open the app and make sure you are on the hotspot described above.
2. Power the sensor on.
3. Hold the side button until the green light blinks: that is pairing mode.
4. In the app, add a new device and give it the hotspot's name and password.
5. Set the work mode to **OnlyLight**, so it does not beep.

---

## Step 4 — Link the app account to the cloud project

1. In your cloud project go to **Devices** → **Link App Account** → **Add App Account**.
   Depending on the version of the console this button may read **Link Tuya App Account**
   or **Link My App**, and the second one **Add Apps**. It is the same thing.
2. A QR code appears.
3. In the mobile app tap **Me** (bottom right), then the **QR-code icon** at the top right,
   and scan it.
4. Confirm on the phone.
5. Back in the console, under **All Devices**, your sensor should now be listed. Copy its
   **Device ID**.

If the list is empty, the data centre of the project and the region of the app account do
not match. That is almost always the cause.

---

## Step 5 — Set up the project

```bash
git clone https://github.com/lucregrassi/ambient-intelligence-labs.git
cd ambient-intelligence-labs/lab1-tuya-pir
```

### Create a virtual environment

Do not skip this. On recent Ubuntu, Debian and macOS with Homebrew Python, installing
packages system-wide is refused outright with `error: externally-managed-environment`.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optionally, for the spoken "Motion detected!" announcement:

```bash
pip install -r requirements-optional.txt
```

It is optional on purpose. On macOS it installs about 170 packages, and on Linux it also
needs the system package `espeak-ng`. The script detects that it is missing and carries on
without it.

### Create your .env

```bash
cp .env.example .env
```

Then fill it in:

| Variable | Where it comes from |
|---|---|
| `ACCESS_ID`, `ACCESS_SECRET` | the **Overview** page of your cloud project |
| `ENDPOINT` | the data centre you chose — Central Europe is `https://openapi.tuyaeu.com` |
| `DEVICE_ID` | the **Devices** page, after step 4 |
| `TUYA_USERNAME`, `TUYA_PASSWORD` | the account of the **mobile app**, not of the developer platform |
| `COUNTRY_CODE` | the country you chose in the app, **without the plus sign** — Italy is `39` |

Two things that cost people twenty minutes each:

- The username and password are the **app** ones. The developer-platform login is a
  different account and will be rejected.
- Tuya wants the country code as `39`, not `+39`. `main.py` strips the plus for you, but
  every other example you find online will not.

`.env` is in `.gitignore`. Keep it that way: those four values are enough for anyone to
read your devices.

---

## Step 6 — Run it

```bash
python3 main.py
```

```
Connected to https://openapi.tuyaeu.com — polling every 5 s. Ctrl-C to stop.

This device reports: ['pir', 'battery_percentage', 'battery_state']

14:32:07     --      battery 87%   [1 API calls this run]
14:32:12   MOTION    battery 87%   [2 API calls this run]
```

The first line after connecting prints **the codes this particular device actually
reports**. Not every PIR model calls motion `pir`; some report `presence_state`. If yours
does, that line is where you find out, instead of watching a script that prints nothing.

The call counter is there so that you can watch your monthly quota being spent.

### Options

```bash
python3 main.py --interval 1          # one reading per second
python3 main.py --csv motion.csv      # also append every reading to a CSV file
```

---

Three things worth noticing:

- **The sensor never talks to your computer.** Everything goes through a server you do not
  own, in a country you did not choose. If it goes down, or the trial expires, your sensor
  is a plastic box.
- **You are polling.** You ask the cloud "anything new?" every few seconds, and almost every
  answer is "no". The alternative is push — the cloud tells you when something changes —
  which costs no quota while nothing happens and needs an address the cloud can reach.
- **Your credentials are a key to the room.** With those four values, anyone can read when
  you are in it.
