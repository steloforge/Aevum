# Aevum

> **A world that remembers.**

Aevum is a persistent autonomous-world simulation focused on characters whose behavior
and development emerge from memory, emotion, beliefs, identity, needs, goals,
preferences, relationships, and lived experience.

Rather than defining exactly what a character will do next, Aevum models who the
character is, what they have experienced, what they currently need, what they value,
and what their world allows them to do.

The project is currently an actively developed Python prototype.

---

## Axiom

At the center of Aevum is **Axiom**, the authoritative world intelligence.

Characters are responsible for their own subjective cognition: what they remember,
believe, feel, want, and attempt.

Axiom is responsible for determining what is actually true in the world.

Its responsibilities include:

- Maintaining canonical world state
- Enforcing simulation rules and constraints
- Managing world time
- Determining action availability
- Resolving character intentions
- Creating authoritative world events
- Producing consequences that characters can perceive and remember

This creates a separation between:

**Character cognition → Character intention → Axiom resolution → World outcome**

A character can believe something happened, want something to happen, or attempt to
make something happen without those subjective states automatically becoming reality.

---

## Current Systems

Aevum currently includes prototypes for:

### Autonomous Decision-Making
Characters evaluate competing actions using factors including:

- Physical and psychological needs
- Need urgency
- Personality
- Personal values
- Goals
- Activity preferences
- Recent behavior
- Repetition
- Time of day
- World availability
- Risk and rule hesitation

### Memory
Characters maintain autobiographical memories with:

- Importance
- Confidence
- Clarity
- Emotional associations
- People and locations
- Semantic associations
- Recall history
- Memory decay
- Recall reinforcement
- Emotional reactivation
- Memory layers

### Emotion
Characters maintain persistent emotional state that can:

- React to experiences
- Reactivate during memory recall
- Change through emotional regulation
- Recover gradually with time
- Recover more strongly during sleep

### Beliefs & Identity
Experiences can reinforce or contradict beliefs and gradually influence a character's
self-concept.

### Needs & Daily Life
Characters can autonomously:

- Eat
- Work
- Train
- Socialize
- Rest
- Sleep

Actions consume simulated time and alter internal state.

### Persistent State
World and character state can be serialized and restored so the simulation can continue
across sessions.

---

## Emergent Behavior

Aevum does not assign its test characters a predetermined daily schedule.

During simulation, changing needs, values, preferences, goals, recent experiences,
world constraints, and time-of-day context compete to determine what a character
chooses to do.

This has produced autonomous multi-hour routines involving work, training, meals,
family interaction, rest, and sleep.

Development focuses not only on making characters choose actions, but on understanding
and correcting *why* unrealistic behavior emerges from interacting systems.

---

## Architecture

The current conceptual simulation loop is:

```text
World State
     ↓
Character Perception
     ↓
Interpretation
     ↓
Memory / Emotion / Belief / Identity
     ↓
Needs + Goals + Preferences
     ↓
Autonomous Decision
     ↓
Character Intention
     ↓
AXIOM
     ↓
World Rules + Constraints
     ↓
Action Resolution
     ↓
Canonical World Event
     ↓
Consequences
     ↓
Character Perception
```

---

## Current Development

Aevum is in active prototype development.

Current areas of development include:

- Separating internal drives from external obligations
- Habit and routine formation
- Experience-driven preference changes
- Long-term goals and planning
- Character schedules
- Location-aware behavior
- Multi-character autonomous interaction
- Relationship development
- World institutions and rules
- Generalized action generation
- Larger persistent simulations

---

## Technology

Currently:

- **Python**
- **JSON persistence**
- Event-driven simulation architecture
- Rule-based autonomous decision systems

The architecture is being developed iteratively before expanding into larger-scale
world simulation and interactive visualization.

---

## Project Status

**Prototype / Active Development**

Aevum is an experimental personal project and its architecture is expected to evolve
substantially during development.
