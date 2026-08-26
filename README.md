# Aevum

> **A world that remembers.**

Aevum is an experimental autonomous-world simulation engine written in Python.

Its long-term goal is to explore persistent interactive worlds populated by characters
who do more than wait for a player to interact with them.

Aevum characters can maintain needs, memories, emotions, relationships, beliefs,
identity, values, goals, and preferences. These systems influence what characters
choose to do and how their experiences affect future behavior.

Rather than scripting exactly what a character will do next, Aevum asks:

> **Given who this character is, what they have experienced, what they currently need,
> and what their world allows — what would they choose to do?**

The project is currently an actively developed prototype.

**Current automated test suite: 165 tests**

---

## Why Aevum?

Many game characters primarily react to player actions or follow predefined schedules
and behavior trees.

Aevum is an experiment in a different direction.

The goal is to explore characters that can:

- continue making decisions without player input
- develop from accumulated experiences
- remember important events
- form and change relationships
- maintain beliefs about their world
- develop a persistent sense of identity
- choose actions based on competing internal motivations
- experience consequences that influence later decisions

The player does not need to be the center of every simulated life.

Eventually, the same world could contain both player-controlled and autonomous
characters participating in the same persistent simulation.

---

# Axiom

At the center of Aevum is **Axiom**, the authoritative world layer.

A character may want something to happen.

A character may believe something happened.

A character may even attempt to make something happen.

None of those things automatically make it true.

Axiom determines canonical reality.

Its responsibilities include:

- maintaining authoritative world state
- enforcing simulation rules and constraints
- managing world time
- validating action availability
- resolving character intentions
- applying authoritative consequences
- creating canonical world events

Characters remain responsible for subjective cognition:

- perception
- interpretation
- emotion
- autobiographical memory
- relationships
- self-concept
- beliefs

This creates a fundamental architectural boundary:

```text
Character Intention
        ↓
      Axiom
        ↓
Canonical World Outcome
        ↓
Character Perception
        ↓
Subjective Cognition
```

The distinction allows a character's understanding of reality to eventually differ
from reality itself.

---

# Current Character Systems

## Autonomous Decision-Making

Characters evaluate competing self-directed actions using influences including:

- physical and psychological needs
- need urgency
- sleep pressure
- personality traits
- personal values
- goals
- activity preferences
- recent behavior
- repetition / satiation
- time-of-day context
- world availability
- risk and rule hesitation

Aevum intentionally separates:

**Desirability** — how much a character wants to perform an action.

from:

**Availability** — whether the action can currently be attempted.

The decision system determines intention.

It does not directly change canonical world state.

---

## Autonomous Actions

The current baseline autonomous action set includes:

- eating
- resting
- family duty
- training
- family socialization
- sleeping

Ordinary waking actions share reusable resolution mechanics while preserving
action-specific consequences.

Actions can:

- satisfy needs
- advance simulated time
- create authoritative world outcomes
- generate canonical events
- enter the character cognition pipeline
- become autobiographical memories

---

## Memory

Characters maintain autobiographical memories containing information such as:

- importance
- confidence
- clarity
- emotional associations
- people
- locations
- semantic associations
- recall history

The memory system currently supports:

- memory creation
- retrieval
- decay
- recall reinforcement
- emotional reactivation
- memory-layer transitions
- sleep consolidation

Important or emotionally significant experiences can therefore persist differently
from mundane experiences.

---

## Emotion

Characters maintain persistent emotional state.

Experiences can change emotions through interpretation, while memory recall can
reactivate emotional responses associated with earlier experiences.

The current system includes:

- event-driven emotional responses
- emotional regulation
- opposing-emotion suppression
- persistent emotional state
- emotional memory reactivation
- sleep-based emotional recovery

---

## Relationships

Characters maintain persistent relationship state toward people they encounter.

Current relationship dimensions include:

- trust
- respect
- familiarity
- affection
- fear

Relationship changes arise from a character's subjective experience of events rather
than directly modifying canonical world reality.

---

## Beliefs and Identity

Characters can maintain beliefs with confidence and supporting or contradicting
evidence.

Experiences can reinforce or challenge those beliefs.

Characters also maintain persistent self-concept dimensions that accumulate evidence
from their experiences.

These systems are intentionally separate from canonical reality: what a character
believes about themselves or the world does not have to be objectively true.

---

## Sleep

Sleep is treated differently from ordinary waking actions.

Axiom owns the physical consequences of sleep, including:

- world-time advancement
- hunger changes
- fatigue recovery
- training-drive changes
- canonical sleep-event creation

Character cognition owns subjective sleep effects, including:

- stronger emotional recovery
- consolidation of eligible prior memories

Memory consolidation occurs before creation of the new sleep-event memory, preventing
the sleep that just occurred from immediately consolidating its own memory.

---

# Simulation Pipeline

The current autonomous loop can be summarized as:

```text
Character State
      ↓
Generate Possible Actions
      ↓
Filter Unavailable Actions
      ↓
Score Available Actions
      ↓
Choose Intention
      ↓
AXIOM RESOLUTION
      ↓
Authoritative State Changes
      ↓
Canonical World Event
      ↓
Character Perception
      ↓
Interpretation
      ↓
Emotional Response
      ↓
Memory
      ↓
Relationships
      ↓
Self-Concept
      ↓
Beliefs
      ↓
Updated Character State
      ↓
Future Decisions
```

This feedback loop is central to Aevum.

A character's experiences can become part of the state that influences later behavior.

---

# Example

A simplified autonomous cycle might look like:

```text
Day 4 — 18:00

Character: Marcus

Current needs:
Hunger ............. 72
Fatigue ............ 38
Family Duty ........ 55
Training Drive ..... 41

Possible actions:
Eat a meal
Help at the family shop
Train
Rest

Decision:
Marcus chooses to eat.

Axiom resolution:
Action succeeds.
World time advances.

Canonical outcome:
Marcus ate a meal.

Character cognition:
The event is perceived and interpreted.
Emotional state may change.
A memory may be created.
Relevant relationships, identity, or beliefs may change.

The resulting character state can influence the next decision.
```

> The example above illustrates the architecture and is not yet the output of a
> dedicated public demo interface.

---

# Project Structure

Aevum is being separated into focused systems rather than maintained as one large
simulation script.

Major architectural areas currently include:

```text
aevum/
├── axiom/
│   └── authoritative world and action resolution
│
├── character/
│   ├── decision making
│   ├── perception
│   ├── interpretation
│   ├── emotions
│   ├── memory
│   ├── relationships
│   ├── identity
│   ├── beliefs
│   └── outcome processing
│
└── world / simulation systems
```

The exact project structure continues to evolve as the prototype is refactored.

---

# Testing

Aevum is developed incrementally with automated tests protecting behavioral rules and
architectural boundaries.

Current checkpoint:

```text
165 passed
```

Tests currently cover systems including:

- character cognition
- autonomous decision influences
- action availability
- self-directed action selection
- Axiom action resolution
- authoritative need changes
- world-time progression
- canonical outcome events
- relationships
- sleep cognition
- emotional recovery
- memory consolidation

Run the test suite with:

```bash
pytest -q
```

---

# Technology

Current development uses:

- **Python**
- **Pytest**
- **Git / GitHub**
- **JSON persistence**
- event-driven simulation architecture
- rule-based autonomous decision systems

Aevum does **not currently depend on a large language model** for character
decision-making.

The current focus is building the simulation architecture underneath future intelligent
behavior before introducing more advanced AI systems.

---

# Roadmap

## Near-Term

Current development priorities include:

### Data-Driven Autonomous Actions

Move beyond a fixed action catalog toward structured action definitions that allow
characters to dynamically gain or lose possible actions based on factors such as:

- skills
- capabilities
- professions and roles
- equipment
- resources
- location
- relationships
- knowledge
- permissions
- world state

### Richer Action Availability

Expand action validation beyond simple time-based rules into authoritative world
conditions.

### Runnable Demonstration

Create a small public demonstration showing:

```text
Character State
→ Available Actions
→ Action Scoring
→ Selected Intention
→ Axiom Resolution
→ World Consequences
→ Character Cognition
```

---

## Longer-Term Research and Development

Areas Aevum is intended to explore include:

- contextual action generation
- habit and routine formation
- experience-driven preference changes
- richer identity development
- long-term goals and planning
- location-aware behavior
- multi-character autonomous interaction
- relationship development over long periods
- institutions, laws, and permissions
- long-running persistent simulations
- emergent social behavior
- richer character knowledge and perception
- integration with interactive environments
- carefully bounded AI-assisted reasoning

The long-term objective is not simply to generate NPC dialogue.

It is to explore the systems required for autonomous characters to **live within a
persistent world**.

---

# Development Philosophy

Aevum is being built incrementally.

New systems are first implemented with explicit rules and tests so their behavior can
be understood before additional complexity is introduced.

A recurring architectural principle is:

> **Characters decide what they want.  
> Axiom decides what happens.  
> Experience changes who the characters become.**

---

# Project Status

**Prototype / Active Development**

Aevum is an experimental personal software-engineering project.

Its architecture is expected to evolve substantially as autonomous behavior,
world simulation, and eventually more advanced intelligent systems are developed.

For detailed architectural notes, implementation milestones, and planned work, see
[`DEVELOPMENT.md`](DEVELOPMENT.md).
