# Lab 3 — An ontology of this room

This lab runs on your own laptop, in **Protégé**. There is no notebook and nothing to open in the
browser, so the one thing you have to do in advance is install the software.

## Before the lesson — install Protégé

Protégé 5.6 is free and runs on Windows, macOS and Linux: <https://protege.stanford.edu>

Download the **installer for your system**, not the generic ZIP: the installers come with the Java
runtime included, the ZIP expects you to have one already.

Open it once before the lesson, just to check that it starts.

## The file

[`classroom_start.owl`](classroom_start.owl) is the room you will be sitting in, already described:
the desks, the projector, the whiteboard, the sensor above the door, and the people in it.

To get it: click the file name above, then the **Download raw file** button at the top right of the
file view. Then `File → Open…` in Protégé.

## What we do

**01 — Open the file** and find the room you are sitting in.

**02 — Define three classes.** A teaching room, a monitored room, a crowded one — written as
definitions, not as labels.

**03 — Run the reasoner** and read what it added to this room. Then look at the empty room next
door, which stays empty.

**04 — Two rules.** Where your desk is, is where you are. And whoever is in the room can see the
whiteboard.

**05 — Break it.** One assertion, and every class in the hierarchy turns red at once.

We build everything together, so there is nothing to prepare: bring your charged laptop with Protégé and the ontology file.

## The step-by-step

[`walkthrough.md`](walkthrough.md) carries every step we take in class: the expressions to type, what has to
appear after each one, and the questions with the answers hidden behind a click, so you can
try before you look. Follow it during the lab, or use it to redo the whole thing on your own.

[`classroom_final.owl`](classroom_final.owl) is the state we end at.

