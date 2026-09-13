# Lab 3 — Classroom ontology in Protégé, step by step

Every step we take in class, so you can follow along during the lab, go over it again
afterwards, or do the whole thing on your own if you were not there.

**Six steps · about ninety minutes · Protégé 5.6 with HermiT · starting file: [`classroom_start.owl`](classroom_start.owl)**

The questions in this page are the ones asked out loud during the lab, and the answers are
hidden behind a click. Try to answer before you open them — that is where the lesson is.

---

## 01 · Before you start

Protégé installed and the starting file downloaded — the [README](README.md) says which installer
to take and how to get the file. [`classroom_final.owl`](classroom_final.owl) is where we arrive:
open that one first, run the reasoner on it, and you will know what you are aiming at.

> [!NOTE]
> If classes and properties appear with a leading colon — `:Room`, `:equippedWith` — your
> Protégé is rendering entities as qualified names, and the expression editor will accept only
> that form. Either type the colons everywhere, or turn them off once in
> **File ▸ Preferences ▸ Renderer**, choosing to render entities by their IRI short name —
> which is how they are written here.

## 02 · Getting around Protégé

There are only four places you need, and everything below happens in them.

| where | what it is for |
|---|---|
| **The class tree** — Entities ▸ Classes tab | All the classes. You create a new one by selecting its parent and clicking **Add subclass**. |
| **The Description panel** — usually on the right | Where everything is written. For a class it has the rows *Equivalent To*, *SubClass Of*, *Disjoint With*; for an individual, *Types*, the property assertions, and *Different Individuals*. The **+** at the end of a row adds one. |
| **The Individuals tab** | The things themselves: this room, the desks, the four students. |
| **The Reasoner menu** | Pick **HermiT** once, then **Start reasoner**. After every change you make, **Synchronise reasoner** — nothing you write counts until you do. |

**How to see what the reasoner concluded.** Anything the machine worked out is shown
highlighted, in a different colour from what you typed, and the class tree gains an inferred
view (*Class hierarchy (inferred)*) next to the one you edit. That colour is the whole point of
this laboratory: it separates what somebody asserted from what follows from it.

## 03 · Step 1 — Three classes that define something

A **defined class** is one where you write the condition for membership, and the reasoner finds
the members. All three are built the same way:

1. In the class tree select `Room`, then **Add subclass**, and give it the name.
2. With the new class selected, go to **Equivalent To** in the Description panel and press **+**.
3. Type the expression in the "Class expression editor" tab and confirm with **OK**.

The three expressions, exactly as we wrote them:

```
TeachingRoom    Room and (equippedWith some Projector) and (equippedWith some Whiteboard)
MonitoredRoom   Room and (equippedWith some PresenceSensor)
OccupiedRoom    Room and (hosts some Person)
```

Now **Synchronise reasoner** and look at the individual `e2`.

**What you should see:** three new lines under *Types*, highlighted — **TeachingRoom,
MonitoredRoom and OccupiedRoom**. Nobody wrote any of them. Then look at `e1`, the empty room
next door: **it stays a plain Classroom**.

> [!WARNING]
> If nothing appeared, maybe you wrote the expression in **SubClass Of** instead of
> **Equivalent To**. *SubClass Of* says: every teaching room has a projector — a necessary
> condition, which lets the reasoner check a room but never recognise one. *Equivalent To*
> says: having a projector and a whiteboard is what it means to be a teaching room — necessary
> and sufficient, so the reasoner can go and find them. In description logic, ⊑ against ≡.

<details>
<summary><b>Why is the room already occupied, when no student is in it yet?</b></summary>

Because the file says `lucrezia isIn e2`, and `isIn` is declared as the inverse of `hosts`. You
never have to write both directions: one of them is derived. It is the smallest piece of
reasoning in the file, and it matters for the next step.
</details>

## 04 · Step 2 — A class that does not fire

```
CrowdedRoom     Room and (hosts min 4 Person)
```

Same procedure, then synchronise.

**What you should see: nothing new.** There are four students sitting in that room, and a
declared head count of twenty-four, and the reasoner does not call it crowded.

<details>
<summary><b>Why not?</b></summary>

Because `hosts` is empty apart from the lecturer. Look at what the file actually says about the
students: each one is `seatedAt` a desk. Nobody ever wrote that they are *in the room*. To you
the two are obviously the same thing. To the model they are unrelated, until something connects
them — which is the next step.
</details>

> [!NOTE]
> **The number four is not a typo.** A realistic definition of a crowded lecture room would say
> twenty, and at twenty this file does not finish reasoning: the reasoner has to build models
> containing twenty distinct individuals, and the cost explodes. This is the
> expressiveness-versus-cost trade-off of the previous lecture, on your own laptop. Remember it
> when you choose cardinalities in your own ontology.

## 05 · Step 3 — A rule, and the surprise

Some things cannot be said with a class definition. *Whoever sits at a desk that stands in a
room is in that room* chains two different properties through a middle object, and that is what
SWRL rules are for.

Open the rules view — **Window ▸ Views ▸ Ontology views ▸ Rules**, then click where you want the
panel to sit — and add:

```
Student(?s), seatedAt(?s, ?d), placedIn(?d, ?r), Room(?r) -> hosts(?r, ?s)
```

**The Rules view is part of every Protégé installation and separates the atoms with commas, as
written here.** If you are using the SWRLTab instead — **Window ▸ Tabs ▸ SWRLTab**, a plugin you
may not have — the same rule wants a caret: `Student(?s) ^ seatedAt(?s, ?d) ^ placedIn(?d, ?r) ^
Room(?r) -> hosts(?r, ?s)`. Either way the rule is run by HermiT when you synchronise: you do
not need the Drools engine at the bottom of the SWRLTab.

Read it right to left: if a student sits at a desk, and that desk is in a room, then the room
hosts the student. Note `placedIn` — the file never says the desk is in the room, it says the
room is *equipped with* the desk. `placedIn` is the inverse, and the rule gets it for free.

**What you should see** after synchronising: on `e2`, four new `hosts` assertions — **alice,
bruno, chiara and dario** — derived from where they are sitting. With the lecturer, the room now
hosts five people. And *CrowdedRoom* **still does not appear.**

<details>
<summary><b>The room hosts five people. The definition asks for four. Why is it still not crowded?</b></summary>

Because nothing in the file says that alice, bruno, chiara and dario are **four different
people**. Two names are allowed to refer to the same thing unless you say otherwise — the *no
unique name assumption*. The reasoner knows there are five names. It does not know there are
five people.

This is not a quirk of the exercise: it is the normal situation whenever data comes from more
than one source — the same patient in two hospital systems, the same sensor with two
identifiers.
</details>

## 06 · Step 4 — Saying that they are different

In the **Individuals** tab select `alice`, find **Different Individuals** in the Description
panel, press **+** and add `bruno`, `chiara` and `dario`. Synchronise.

**What you should see: CrowdedRoom on `e2`** at last. And a second thing, which is easy to miss:
in the inferred class tree, **CrowdedRoom is no longer directly under Room — it has moved under
OccupiedRoom**.

Nobody wrote that. The reasoner worked out that a room hosting at least four people necessarily
hosts at least one, so every crowded room is an occupied room — **in this model and in any
other**. Every other conclusion today has been about one room; this one is about the vocabulary
itself. It is the difference between a list of names and a model, and it is the thing a taxonomy
can never do for you.

## 07 · Step 5 — The second rule, seen from a person

```
hosts(?r, ?p), equippedWith(?r, ?w), Whiteboard(?w) -> canSee(?p, ?w)
```

Synchronise, then stop looking at the room and select `alice` instead.

**What you should see:** the file says exactly one thing about alice — that she sits at desk 1.
After reasoning she also **is in e2** and **can see the whiteboard**. Two facts about a person,
derived from a piece of furniture.

This is the point of the whole afternoon for an ambient intelligence system. You never observe
that someone is in a room. You observe a desk, a chair, a sensor reading. Everything else has to
be derived, and this is what deriving looks like when it is written down instead of hidden in
code.

## 08 · Step 6 — Breaking it on purpose

Select `desk_1`, and in **Types** add `Person`. A desk that is also a person. Synchronise.

**What you should see: Protégé reports that the ontology is inconsistent**, and every class
collapses under *Nothing*.

Nothing you wrote was false in itself. You wrote one thing that cannot hold at the same time as
another: the file declares *Room, Furniture, Device, Person* and *Activity* pairwise disjoint,
so nothing can be two of them. A database would have stored your row. A log file would have
swallowed it. The reasoner refuses to answer anything at all until you fix it — and if you ask
it to explain, it will name the axioms responsible.

Then undo it (**Edit ▸ Undo**, or remove *Person* from the desk's types) and synchronise again.
You are now at [`classroom_final.owl`](classroom_final.owl): compare the two if you want to check.

## 09 · Checking yourself

After each step, this is what must be true — and if it is not, the problem is in that step and
not in a later one.

| step | what you just did | what the reasoner says about `e2` |
|---|---|---|
| **0** | Nothing — the file as downloaded | Classroom, and nothing else. The reasoner runs and has nothing to add. |
| **1** | TeachingRoom, MonitoredRoom, OccupiedRoom | All three appear. `e1` next door gains nothing. |
| **2** | CrowdedRoom | No change. `hosts` contains the lecturer only. |
| **3** | The seat-chain rule | `hosts` gains the four students. Still not crowded. |
| **4** | Different Individuals | CrowdedRoom appears, and moves under OccupiedRoom in the inferred tree. |
| **5** | The whiteboard rule | alice is in e2 and can see the whiteboard. |
| **6** | `desk_1` declared a Person | Inconsistent — everything under Nothing. |

Each of these takes the reasoner well under a second. If yours is thinking for a long time,
something is wrong with a cardinality, not with your patience.

## 10 · What will go wrong on your own ontology

These are not hypothetical: they are what actually happens, and knowing them saves you an evening.

**The reasoner concludes nothing at all**
> Your conditions are in *SubClass Of*. Necessary conditions cannot classify anything. Move them
> to *Equivalent To* and run again. (Second most common cause: you did not synchronise.)

**A rule silently does nothing**
> Check the variable names are spelled identically everywhere in the rule — `?r` in the body and
> `?r` in the head. And **never name an object property `contains`**: inside a rule it is read as
> the built-in `swrlb:contains`, and the rule quietly stops meaning what you wrote. This is why
> the property in our file is called `equippedWith`.

**"A SWRL rule uses a built-in atom…"**
> HermiT does not support built-ins, so a rule that compares numbers — `swrlb:greaterThanOrEqual`
> and friends — will not run. Express the condition as a class axiom where you can, as we did
> with `min 4`.

**The reasoner never finishes**
> Almost always a large cardinality. Keep the numbers small while you are building; raise them
> only if you have to, and expect to pay for it.

**Something classifies that should not**
> Look at your domains and ranges before blaming the reasoner. Declaring `domain Room` on a
> property does not check anything — it *tells* the reasoner that whatever has that property is a
> room, and it will happily conclude so.

**Everything is inconsistent and you do not know why**
> Ask Protégé to explain: it lists the axioms that cannot hold together. Usually it is a
> disjointness you forgot you declared, or an individual given two incompatible types.
