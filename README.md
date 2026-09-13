# Ambient Intelligence — Labs

Lab material for **Ambient Intelligence (80188)**, MSc in Robotics Engineering, University of Genoa.

Four independent labs. Nothing in one lab depends on the output of another.

| | Lab | What you do | How to open it |
|---|---|---|---|
| **1** | [PIR from the Tuya cloud](lab1-tuya-pir/) | Pair a motion sensor, create your own cloud project, and read the sensor over a REST API from Python | [Instructions](lab1-tuya-pir/README.md) — runs on your own machine |
| **2** | [Magnetic indoor localization](lab2-magnetic-localization/) | Record the magnetic field while walking a corridor, build a map of it, and work out where you were | [Open in Colab](https://colab.research.google.com/github/lucregrassi/ambient-intelligence-labs/blob/main/lab2-magnetic-localization/Lab2_magnetic_localization.ipynb) |
| **3** | [Classroom ontology in Protégé](lab3-classroom-ontology/) | Describe the room you are sitting in as an ontology, and let the reasoner work out three things about it that nobody typed | [Instructions](lab3-classroom-ontology/README.md) — runs in Protégé on your own machine |
| **4** | Bayesian networks with pyAgrum | *(coming later in the course)* | |

## Before you start

**Lab 1** runs on your own laptop and needs Python — the instructions include the virtual-environment
setup. 

**Lab 2** runs entirely in Google Colab: nothing to install, and the recordings needed to run it
are already inside the notebook, so it works even if your own data collection went wrong. When you open a Colab notebook from here, you are looking at a copy. **Do `File → Save a copy in Drive` before you start**, otherwise your work disappears when you close the tab. You cannot modify anything in this repository, so experiment freely.

**Lab 3** runs on your own laptop too, in Protégé, which has to be installed **before** the lesson — its instructions say which download to take.

## Author

**Lucrezia Grassi** — <lucrezia.grassi@unige.it>
