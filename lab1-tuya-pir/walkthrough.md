# Lab 1 — PIR from the Tuya cloud, step by step

Everything we do together in the laboratory, in order. The accounts are created during the
session on purpose, so that you see what each one is for. The sensor needs a 2.4 GHz phone
hotspot, as explained in the network section of the [README](README.md): it cannot join eduroam.

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

<details>
<summary><b>No Python or no git on your laptop?</b></summary>

Check first, in a terminal (on Windows, in PowerShell):

```bash
python3 --version      # Windows: python --version
git --version
```

You need Python 3.9 or later. If one of the two is missing:

- **Windows.** Python: the installer from <https://www.python.org/downloads/> — on its first
  screen tick **Add python.exe to PATH**, otherwise the terminal will not find it. Git: the
  installer from <https://git-scm.com/downloads>, with the default options. Close and reopen
  PowerShell afterwards. On Windows the command is `python`, not `python3`, in every step below.
- **macOS.** Typing `python3 --version` or `git --version` offers to install Apple's command
  line developer tools, which include both. Accept, wait a few minutes, and run the command again.
- **Ubuntu or Debian.** `sudo apt install python3 python3-venv git`. The `python3-venv` package
  is needed for the next step and is not always installed with Python.

</details>

### Create a virtual environment

Do not skip this. On recent Ubuntu, Debian and macOS with Homebrew Python, installing
packages system-wide is refused outright with `error: externally-managed-environment`.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

On Windows, if PowerShell refuses to activate the environment because running scripts is
disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

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

`.env` is in `.gitignore`. Keep it that way: those values are enough for anyone to
read your devices.

---

## Step 6 — Run it

```bash
python3 main.py
```

```
Connected to https://openapi.tuyaeu.com — polling every 5 s. Ctrl-C to stop.

This device reports: ['pir_state', 'battery_percentage', 'alarm_time', 'charge_state', 'pwd_free_arm', 'work_mode']

10:46:29    --     (65 s ago)       [1 API calls this run]
10:46:34    --     (71 s ago)       [2 API calls this run]
10:46:39  MOTION   (just now)       [3 API calls this run]
```

The first line after connecting prints **the codes this particular device actually
reports**. The script reads `pir_state`, which is what our sensors call motion; other models
use `pir` or `presence_state`. If yours does, that line is where you find out, and the name in
the script is the one thing to change.

The time in brackets is **how long ago the sensor reported that value**, not when the script
asked: the first two lines show a value that is more than a minute old.

The call counter is there so that you can watch your monthly quota being spent.

To ask less often, give the interval in seconds:

```bash
python3 main.py --interval 60         # one reading per minute
```

---

## Step 7 — Print only the changes

As it is, the script prints a line every five seconds whatever happens, and after a few minutes
the terminal is full of identical lines. Change it so that it prints a line **only when the motion
value is different from the previous one**. You need one new variable and one condition; the time
is already at the start of every line.

Then sit completely still for a minute, and watch the terminal.

<details>
<summary><b>One way to do it</b></summary>

Before the `while True:` loop, create the variable:

```python
previous = None
```

Inside the loop, put the `print(...)` of the reading under a condition, and update the variable
after it:

```python
if motion_status != previous:
    print(...)        # the line the script already prints
previous = motion_status
```

The first reading is always printed, because at the start there is no previous value. After
that, every line is an event: motion started, or motion stopped. The original script printed
the **level** of the signal, its value at each moment; this one prints its **edges**, the moments
it changes.
</details>

<details>
<summary><b>Why did it print nothing while you were sitting still?</b></summary>

A PIR detects a change in the infrared that reaches it, not a body. A person who does not move
produces no change, and therefore no event. With this sensor alone, "nobody is here" and
"somebody is here, not moving" look exactly the same.
</details>

## If everything works: a few more tests

Each one takes a few minutes and uses only what you already have. Before trying, guess what
will happen.

**1. How long does "motion" last?** Make one movement in front of the sensor, then keep still.
How long before the value goes back to `--`? Then try moving again before it does: does the
wait start over?

<details>
<summary><b>What you should see</b></summary>

On the sensor we use, about thirty seconds. This is the **hold time**: the sensor keeps reporting
motion for a while after the last movement, which hides, for a while, the fact that a still person
disappears. Whether a new movement restarts the wait depends on the firmware, and what you have
just seen is the answer for this model.
</details>

**2. Towards the sensor, or across it?** From the far side of the room, walk slowly straight
towards the sensor. Then walk across its field of view, at the same distance.

<details>
<summary><b>What you should see</b></summary>

Walking across triggers it much more easily. The lens divides the field of view into zones, and
the sensor fires when a warm body moves from one zone into the next. Walking straight at it keeps
you in the same zones for longer. This is why a PIR at a door is mounted to look across the
doorway, not straight at it.
</details>

**3. Ask less often.** Run `python3 main.py --interval 60`. Right after a line is printed, make
one short movement and then keep still. Does the next line show it?

<details>
<summary><b>What you should see</b></summary>

Often it does not. The value goes back to `--` after about thirty seconds, before the next
request arrives a minute later: the movement happened, and the script never knew. Polling only
sees what is still true at the moment it asks. Asking more often costs more calls; the
alternative is push, where the cloud reports each change as it happens.
</details>

**4. Switch the hotspot off.** Do this one last. With the script running, turn off the phone's
hotspot for a minute, then turn it back on.

<details>
<summary><b>What you should see</b></summary>

The script keeps printing the last value as if nothing had happened: the cloud answers with what
it last received. Only the age at the end of the line gives it away, growing minute after minute,
and if you move in front of the sensor nothing changes. When the hotspot is back the sensor should
reconnect by itself (if it does not, switch it off and on). The sensor never stopped working: the
chain broke one link away from it.
</details>

---

Three things worth noticing:

- **The sensor never talks to your computer.** Everything goes through a server you do not
  own. If it goes down, or the trial expires, your sensor is a plastic box.
- **You are polling.** You ask the cloud "anything new?" every few seconds, and almost every
  answer is "no". The alternative is push — the cloud tells you when something changes —
  which costs no quota while nothing happens and needs an address the cloud can reach.
- **Your credentials are a key to the room.** With the values in your `.env`, anyone can read
  when you are in it.
