# Aevum Development Notes

This document tracks Aevum's current architectural state, completed
development milestones, and future work.

The document is intentionally divided into three categories:

1. **Current Architecture** — behavior that exists and is currently tested.
2. **Completed Milestones** — important architectural stages that have been
   successfully implemented.
3. **Future Development** — systems, improvements, and design questions that
   have not yet been completed.

Future work should be added to the Future Development section first.

Once a planned feature is implemented and tested, its documentation should
be moved or incorporated into Current Architecture or Completed Milestones
rather than leaving outdated future notes in place.


---

# 1. Current Architecture


## Character Cognition Pipeline

Authoritative world events are processed through the character's subjective
cognitive systems.

The current processing flow is:

World Event
→ Perception
→ Interpretation
→ Emotional Response
→ Sleep Cognitive Effects when applicable
→ Memory Creation
→ Relationship Update
→ Self-Concept Update
→ Belief Evaluation

Axiom owns canonical reality.

Character systems own subjective interpretation and psychological change.

This separation is a core architectural rule.


## Perception and Interpretation

Characters do not operate directly on canonical world events as though their
knowledge were identical to reality.

World events first pass through perception and interpretation.

This allows canonical reality and character experience to remain separate.

The intended distinction is:

Canonical World Event
→ Character Perception
→ Character Interpretation

Future systems may expand this boundary with incomplete information,
misperception, hidden information, deception, or differing perspectives.


## Emotional State

Characters maintain persistent emotional state.

Interpretations can alter current emotions through the emotional-response
system.

Emotional regulation and opposing-emotion suppression may modify the final
response before it becomes persistent character state.

Sleep provides a stronger recovery process that moves persistent emotional
state toward baseline.


## Memory

Characters form autobiographical memories from perceived and interpreted
world events.

Current memory behavior includes:

- memory creation
- clarity
- importance
- emotional associations
- retrieval
- reinforcement
- decay
- emotional reactivation
- memory-layer transitions
- sleep consolidation

Memory belongs to the character and is not canonical world state.


## Relationships

Relationship updates are integrated into character outcome processing.

Current relationship dimensions include:

- trust
- respect
- familiarity
- affection
- fear

Relationship changes are subjective consequences of a character's
experiences.

The current processing boundary is:

World Event
→ Perception
→ Interpretation
→ Emotional Response
→ Memory Creation
→ Relationship Update

Relationship targets should represent actual people involved in the event.

Abstract concepts or emotional causes such as "Community Support" or
"Family" should not accidentally become relationship targets.


## Self-Concept

Characters maintain persistent self-concept dimensions that can change
through experience.

Current dimensions include:

- protector
- peacekeeper
- family_guardian
- rule_follower
- fighter

Self-concept currently represents accumulated identity evidence.

More sophisticated identity behavior remains future work.


## Beliefs

Characters can maintain beliefs with confidence and supporting or
contradicting evidence.

Canonical events can become subjectively relevant to beliefs through
perception and judgment.

Belief processing remains character-owned rather than authoritative
world state.


## Autonomous Decision System

The autonomous decision system is divided into focused, independently
testable influences.

Current decision layers include:

- need urgency and need pressure
- special sleep pressure
- activity preference
- recent repetition / satiation
- time-of-day context
- value relevance and value-based motivation
- goal relevance
- ambition and discipline
- risk / rule-obedience hesitation
- candidate action generation
- action availability filtering
- ranked self-directed action selection

Important decision functions include:

- `calculate_need_pressure()`
- `calculate_sleep_pressure()`
- `calculate_repetition_effect()`
- `calculate_time_of_day_effect()`
- `calculate_value_effect()`
- `calculate_goal_effect()`
- `calculate_risk_effect()`
- `generate_self_directed_actions()`
- `is_self_directed_action_available()`
- `score_self_directed_action()`
- `choose_self_directed_action()`


### Desirability Is Not Availability

An action may be undesirable without being impossible.

Desirability determines how strongly a character wants to perform an action.

Availability determines whether the action can currently be considered at
all.

For example:

- "Shop is likely closed" may reduce time-of-day desirability.
- "Family shop is closed" may make the action unavailable.

These concepts should remain separate.


### Intention Is Not Outcome

The decision system determines what the character wants to do.

It does not determine canonical reality and should not directly mutate
authoritative world state.

The current boundary is:

Character State
→ Generate Possible Actions
→ Filter Unavailable Actions
→ Score Available Actions
→ Choose Intention
→ Axiom Resolution
→ Canonical World Event
→ Character Cognition


### Decision Result Schema

Scored actions preserve:

- `action` — human-readable action name
- `action_type` — structured action category
- `action_data` — complete candidate action definition

This preserves both display information and structured action metadata for
downstream Axiom resolution.


## Self-Directed Action Resolution

Aevum currently supports six baseline self-directed actions:

- `eat`
- `rest`
- `family_duty`
- `train`
- `social_family`
- `sleep`

The five ordinary waking actions share reusable authoritative resolution
mechanics.

The shared waking-action path handles:

- action satisfaction effects
- authoritative need mutation
- action duration
- world-time advancement
- normal waking need drift
- resolution results

Action-specific canonical facts remain outside the generic helper.

This allows actions such as training or family duty to share physical
resolution mechanics while still producing different canonical outcomes.


## Axiom Boundary

Axiom determines what actually happens.

For self-directed actions, Axiom owns authoritative consequences including:

- action success or failure
- need changes
- action duration
- world-time advancement
- canonical outcome events

Axiom does not own subjective consequences such as:

- interpretation
- emotional meaning
- autobiographical memory
- relationships
- self-concept
- beliefs

Those remain character cognition.


## Canonical Self-Directed Events

Successfully resolved self-directed actions are converted into canonical
`self_directed_outcome` world events.

This creates a common boundary between autonomous behavior and the existing
character cognition pipeline.

A character can therefore perceive, interpret, emotionally respond to,
remember, and psychologically incorporate actions they chose themselves.

No separate autonomous-memory system is required.


## Sleep Architecture

Sleep remains specialized rather than using normal waking-action resolution.

Sleep currently includes two distinct categories of consequences.


### Authoritative Sleep Consequences

Axiom owns:

- eight hours of world-time advancement
- sleep-specific hunger change
- strong fatigue recovery
- sleep-specific training-drive change
- canonical sleep-event creation

Social and family-responsibility pressure do not currently increase during
sleep.


### Subjective Sleep Consequences

Character cognition owns:

- stronger emotional recovery
- prior-memory consolidation

Sleep emotional recovery moves persistent emotional state toward baseline.

Negative emotions trend toward zero.

Happiness trends toward its baseline value.


### Sleep Memory Consolidation

Sleep can strengthen eligible recent memories.

Consolidation strength currently considers:

- memory importance
- emotional intensity
- reduced reinforcement for mundane memories
- a maximum consolidation boost

Sleep consolidation occurs before creation of the new sleep-event memory.

Therefore:

Prior waking memories
→ Sleep consolidation
→ New sleep-event memory

The sleep that just occurred does not immediately consolidate its own newly
created memory.


---

# 2. Completed Milestones


## Modular Character Cognition

The original prototype's character cognition behavior has been separated
into focused modules including:

- perception
- interpretation
- emotions
- memory
- relationships
- identity
- beliefs
- processing

These systems can now be tested independently while still participating in
the complete outcome-processing pipeline.


## Relationship Pipeline Integration

Relationship updates are integrated into normal character outcome
processing.

Relationship targets are derived from event participants rather than
abstract emotional concepts.

This preserves the distinction between:

- a person involved in an experience
- the concept or cause associated with that experience


## Modular Autonomous Decision System

The prototype's large autonomous scoring logic has been decomposed into
focused decision influences.

Need pressure, sleep pressure, preference, repetition, time context, values,
goals, traits, risk, availability, and ranking can now be tested and tuned
independently.


## First Autonomous Cognition Vertical Slice

The first complete autonomous vertical slice was implemented using `eat`.

The validated path established:

Character Internal State
→ Candidate Generation
→ Availability Filtering
→ Autonomous Scoring
→ Intention Selection
→ Axiom Resolution
→ Authoritative Need and Time Changes
→ Canonical World Event
→ Character Perception
→ Interpretation
→ Emotional Response
→ Memory
→ Relationships
→ Self-Concept
→ Beliefs

This proved that autonomous actions could enter the same cognition pipeline
as externally generated world events.


## Baseline Self-Directed Action Set

The original baseline action set has now been migrated through Axiom:

- `eat`
- `rest`
- `family_duty`
- `train`
- `social_family`
- `sleep`

Ordinary waking actions use shared resolution mechanics while preserving
action-specific canonical outcomes.


## Sleep Cognition Integration

Sleep now spans authoritative Axiom resolution and subjective character
cognition without violating their architectural boundary.

The completed sleep path is:

Sleep Intention
→ Axiom Resolution
→ Authoritative Time Advancement
→ Sleep-Specific Physical Recovery
→ Canonical Sleep Event
→ Character Processing
→ Emotional Recovery
→ Prior-Memory Consolidation
→ Sleep-Event Memory Creation
→ Remaining Character Cognition

The ordering ensures that the newly created sleep memory is not immediately
consolidated by the same sleep period.


## Current Test Checkpoint

**165 tests passing**

This checkpoint represents completion of the baseline self-directed action
and sleep cognition pipeline.


---

# 3. Future Development


## Data-Driven Autonomous Action System

**Status:** Planned

The current self-directed action catalog is intentionally fixed while the
baseline architecture is validated.

Future work should move autonomous actions into structured, extensible action
definitions so new actions can be introduced without modifying the core
decision scorer or continually adding hardcoded central branches.

Candidate actions should eventually be derived from:

- character skills and capabilities
- roles and professions
- equipment and resources
- current location
- known locations
- relationships
- world state
- laws and permissions
- learned knowledge
- temporary conditions
- action-specific requirements

The long-term goal is for characters to dynamically gain or lose possible
actions as their circumstances change.

The architectural boundary should remain:

Action Definitions / Character Capabilities
→ Candidate Generation
→ Availability
→ Desirability
→ Intention
→ Axiom Resolution
→ Canonical Outcome
→ Cognition

The decision system should remain responsible for desirability and selection.

Axiom should remain responsible for authoritative validation and outcomes.


## Richer Action Availability

**Status:** Planned

Availability rules are currently simple and mostly time-based.

Future availability should consider richer authoritative world state,
including:

- location
- access
- resources
- equipment
- physical capability
- knowledge
- relationships
- permissions
- laws
- environmental conditions
- other characters
- temporary world conditions

Availability should answer whether an action can actually be attempted.

It should remain separate from how desirable the action is.


## Identity / Self-Concept Development

**Status:** Revisit after core architecture migration

Self-concept currently accumulates identity evidence through character
experiences.

Current limitations include:

- no identity decay
- no upper bound
- no normalization
- no competition between identity dimensions
- no weakening from contradictory behavior
- no distinction between recent and distant identity-forming experiences

Future identity work should consider:

- diminishing returns from repeated identical behavior
- contradictory experiences
- competing identities
- identity reinforcement through important memories
- identity weakening over long periods without reinforcement
- identity thresholds or normalized scores
- identity-driven decision making
- differences between perceived identity and demonstrated behavior
- major experiences that rapidly reshape identity

The long-term goal is for identity to emerge from a character's history
rather than functioning as an indefinitely increasing counter.


## Long-Term Memory Validation

**Status:** Core behavior implemented; long-term validation pending

Current unit tests validate individual memory mechanics.

Future simulation testing should examine memory behavior across:

- weeks
- months
- years of simulated time

Important, emotional, and frequently recalled memories should generally
remain accessible longer than mundane, unrecalled memories.

Long-term testing should verify that memory decay creates believable
differences in character history rather than merely proving individual
functions execute correctly.


## Long-Running Simulation Tests

**Status:** Planned

Unit tests protect individual rules and architectural contracts.

Aevum should eventually include long-running simulation tests designed to
evaluate emergent behavior across extended world time.

Examples include:

- memory evolution over one simulated year
- identity development across repeated experiences
- relationship development across many interactions
- belief reinforcement and contradiction over time
- autonomous daily behavior over weeks or months
- sleep/wake stability across extended simulations
- repetition and preference behavior over many action cycles
- action availability under changing world conditions

These tests should focus on whether the combined systems produce believable
behavior rather than only whether individual functions execute correctly.


## Decision-System Tuning

**Status:** Functional baseline implemented; tuning deferred

Several decision parameters still preserve prototype-era assumptions.

Areas to revisit include:

- value relevance scaling
- goal relevance scaling
- sleep thresholds
- urgency curves
- repetition pressure
- preference influence
- risk sensitivity
- recent-action history window
- deterministic tie-breaking

These values should not be tuned aggressively until longer autonomous
simulations exist.

Without long-running behavioral tests, local improvements may create
unintended global behavior.


## Contextual Action Generation

**Status:** Planned

Candidate generation currently uses a fixed baseline catalog.

Future candidate generation should become contextual and world-aware.

Characters should not merely select from every action known to the engine.

Instead, possible actions should emerge from the intersection of:

- what the character knows how to do
- what the character believes is possible
- what the world actually permits
- what resources are available
- where the character currently is
- who is present
- what goals and obligations currently matter

This system should eventually allow two characters in the same world state
to perceive different possible actions because their knowledge, skills,
relationships, roles, and beliefs differ.


---

# Documentation Maintenance Rules

To keep this document useful as Aevum grows:

1. Add unimplemented ideas under **Future Development**.

2. Give significant future systems a clear status such as:
   - Planned
   - In progress
   - Revisit later
   - Validation pending

3. Once a system is implemented and tested, update **Current Architecture**
   to describe how it actually works.

4. Move historically important completed work into **Completed Milestones**.

5. Remove or rewrite future notes that are no longer true.

6. Do not leave an implemented feature described elsewhere as "pending."

7. Record important architectural boundaries, not every small code change.

8. Keep exact tuning constants primarily in code and tests unless the value
   represents an intentional architectural rule.

9. Update the test checkpoint only at meaningful architectural milestones,
   not after every individual test is added.

10. Treat this document as the current development map rather than a running
    commit log. Git history should preserve implementation-level history.
