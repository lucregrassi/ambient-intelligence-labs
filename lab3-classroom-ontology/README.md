# Lab 3 — Classroom ontology in Protégé

This lab runs on your own laptop, in **Protégé**. We start from an empty ontology and describe,
step by step, the classroom we are sitting in. Then we add definitions and rules, and let the
reasoner draw conclusions that nobody wrote.

## Protégé

Protégé 5.6 is free and runs on Windows, macOS and Linux: <https://protege.stanford.edu>

Download the **installer for your system**, not the generic ZIP: the installers come with the Java
runtime included, the ZIP expects you to have one already. The reasoner we use, **HermiT**, is
included in Protégé.

## What we build

Ontology IRI: `http://www.unige.it/ami/classroom.owl`

Every name below is used exactly as written, capital letters included, so that the result can be
compared with [`classroom_final.owl`](classroom_final.owl).

### 1 · Classes

| directly under Thing | subclasses |
|---|---|
| `Room` | `Classroom`, `Office`, `Corridor` |
| `Furniture` | `Desk`, `Chair`, `Whiteboard` |
| `Device` | `Projector`, `PresenceSensor` |
| `Person` | `Student`, `Lecturer` |
| `Activity` | `Lecture`, `Exam`, `GroupWork` |

`Room`, `Furniture`, `Device`, `Person` and `Activity` are pairwise disjoint.
`Student` and `Lecturer` are disjoint.

### 2 · Properties

| property | domain | range | |
|---|---|---|---|
| `hosts` | `Room` | `Person` | inverse: `isIn` |
| `equippedWith` | `Room` | — | inverse: `placedIn` |
| `seatedAt` | `Person` | `Desk` | |
| `usedFor` | `Room` | `Activity` | |
| `canSee` | `Person` | `Whiteboard` | |
| `hasHeadCount` | `Room` | `xsd:integer` | data property, functional |

### 3 · Individuals

| class | individuals |
|---|---|
| `Classroom` | `e2`, `e1` |
| `Corridor` | `corridor_ground_floor` |
| `Whiteboard` | `whiteboard_e2` |
| `Projector` | `projector_e2` |
| `PresenceSensor` | `pir_e2` |
| `Desk` | `desk_1`, `desk_2`, `desk_3`, `desk_4` |
| `Lecture` | `ami_lecture` |
| `Student` | `alice`, `bruno`, `chiara`, `dario` |
| `Lecturer` | `lucrezia` |

Property assertions:

```
e2        equippedWith  whiteboard_e2, projector_e2, pir_e2
e2        equippedWith  desk_1, desk_2, desk_3, desk_4
e2        usedFor       ami_lecture
e2        hasHeadCount  24
alice     seatedAt      desk_1
bruno     seatedAt      desk_2
chiara    seatedAt      desk_3
dario     seatedAt      desk_4
lucrezia  isIn          e2
```

[`classroom_checkpoint.owl`](classroom_checkpoint.owl) is exactly this state, for anyone who falls
behind.

### 4 · Defined classes

Each one is a subclass of `Room`, with the condition in **Equivalent To**:

```
TeachingRoom    Room and (equippedWith some Projector) and (equippedWith some Whiteboard)
MonitoredRoom   Room and (equippedWith some PresenceSensor)
OccupiedRoom    Room and (hosts some Person)
CrowdedRoom     Room and (hosts min 4 Person)
```

### 5 · Rules

In the Rules view (**Window ▸ Views ▸ Ontology views ▸ Rules**), atoms separated by commas:

```
Student(?s), seatedAt(?s, ?d), placedIn(?d, ?r), Room(?r) -> hosts(?r, ?s)
hosts(?r, ?p), equippedWith(?r, ?w), Whiteboard(?w) -> canSee(?p, ?w)
```

<details>
<summary><b>After the first rule, e2 hosts five people and is still not a CrowdedRoom. Why, and what is missing?</b></summary>

Five names are not five people: two names may refer to the same individual unless the ontology
says otherwise (no unique name assumption). Declare `alice`, `bruno`, `chiara` and `dario`
**different individuals**, as a single axiom.
</details>

### 6 · Break it

Give `desk_1` the additional type `Person`, synchronise the reasoner, read the explanation, then
remove it.

## Files

- [`classroom_checkpoint.owl`](classroom_checkpoint.owl) — the state at the end of step 3.
- [`classroom_final.owl`](classroom_final.owl) — the state at the end of the lab.

To download a file: click its name, then the **Download raw file** button at the top right of the
file view. Then `File → Open…` in Protégé.
