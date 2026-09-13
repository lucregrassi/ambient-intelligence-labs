# Lab 1 — PIR from the Tuya cloud

This guide takes you from the unboxing of a PIR motion sensor to a Python script printing
`MOTION` in your terminal when somebody walks past it. The point of the exercise is
not the sensor: it is the chain between the two. A device in the room talks to the
manufacturer's cloud, the cloud exposes a REST API, and your script authenticates
against that API and asks it a question. Every commercial IoT product you own works
this way.

---

## Before you start

**Wi-Fi.** The sensor needs a **2.4 GHz network with a single shared WPA2 password**, and that
rules out every network the university runs.

- **Eduroam will not work.** It is WPA2-Enterprise: each user authenticates individually with their
  own credentials. The sensor has no way to do that.
- **Guest networks such as GenuaWiFi will not work either.** These sit behind a captive portal — a
  web page you have to accept or log into. The sensor has no browser and no screen, so it joins the
  network and then sits there with no connectivity, which looks exactly like a broken sensor.
- Use a **phone hotspot** instead. On an iPhone you must turn on **Settings → Personal Hotspot →
  Maximize Compatibility**, otherwise the hotspot runs at 5 GHz and the sensor will never find it.
  On Android, check that the hotspot band is set to 2.4 GHz.
- The phone providing the hotspot must stay on for the whole session.

A device with no screen and no browser can only join a network that has one shared password and no login page — which
excludes almost every network operated by a university, a hospital, a hotel or an airport. Those are
precisely the buildings where you would want to deploy ambient sensing, and the network is the first
thing that stops you.

---

## Prerequisites

- Python 3.9 or later.
- A phone with the Tuya app.
- A Tuya developer account (created in step 2).
- A Tuya PIR motion sensor.

---

## The step-by-step

[`walkthrough.md`](walkthrough.md) carries everything we do together in the laboratory, in order:
install the app, create the cloud project, pair the sensor, link the two accounts, set up the
Python project and run it. Follow it during the lab, or use it to redo the whole thing on your own.

Bring a charged laptop and the phone that will provide the hotspot.

