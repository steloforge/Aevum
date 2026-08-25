# Aevum Development Notes

This document tracks known prototype limitations, architectural questions,
and systems that should be revisited as Aevum develops.

Items listed here are not necessarily bugs. Many represent intentionally
simplified behaviors preserved during the migration of the original
prototype into the modular Aevum architecture.

---

## Identity / Self-Concept

### Self-concept currently accumulates indefinitely

**Status:** Revisit after core architecture migration

The current self-concept system increases identity dimensions in response
to character experiences.

Current dimensions include:

- protector
- peacekeeper
- family_guardian
- rule_follower
- fighter

For example, repeated peaceful resolutions continually increase the
`peacekeeper` score.

Currently there is:

- no identity decay
- no upper bound
- no normalization
- no competition between identity dimensions
- no weakening from contradictory behavior
- no distinction between recent and distant identity-forming experiences

This behavior is intentionally being preserved from the original prototype
during architectural migration.

### Future questions

Consider whether self-concept should eventually support:

- diminishing returns from repeated identical behavior
- contradictory experiences
- competing identities
- identity reinforcement through important memories
- identity weakening over long periods without reinforcement
- identity thresholds or normalized scores
- identity-driven decision making
- differences between perceived identity and demonstrated behavior
- major experiences that rapidly reshape identity

The goal should be for identity to emerge from a character's history rather
than simply functioning as an indefinitely increasing counter.

---

## Memory

### Long-term memory behavior needs simulation testing

**Status:** Core behavior implemented; long-term validation pending

Current unit tests verify short-term decay, retrieval, reinforcement,
emotional reactivation, and memory-layer transitions.

Future simulation tests should examine memory behavior across:

- weeks
- months
- years of simulated time

Important, emotional, and frequently recalled memories should generally
remain accessible longer than mundane, unrecalled memories.

Long-term testing should verify that memory decay produces believable
differences in character history rather than simply confirming individual
functions execute correctly.

---

## Testing

In addition to unit tests, Aevum should eventually include long-running
simulation tests that evaluate emergent behavior over extended world time.

Examples:

- memory evolution over one simulated year
- identity development across repeated experiences
- relationship development across many interactions
- belief reinforcement and contradiction over time
- autonomous daily behavior over weeks or months

## Relationships

### Relationship updates are not yet integrated into outcome processing

**Status:** Relationship model implemented and tested; pipeline integration pending

Aevum currently contains a relationship system capable of updating:

- trust
- respect
- familiarity
- affection
- fear

from autobiographical memories and their emotional causes.

However, the original prototype's `process_outcome_for_character()` pipeline
does not call `update_relationship_from_memory()` after creating a memory.

As a result, the relationship system currently works independently but is
not automatically updated when a character processes a world event.

### Planned integration

The intended flow should be evaluated as:

World Event
→ Perception
→ Interpretation
→ Emotional Response
→ Memory Creation
→ Relationship Update

Relationship changes should remain subjective consequences of a character's
experience rather than authoritative properties of Axiom's world event.


Before integration, verify how emotional causes should map to specific
participants so abstract causes such as "Community Support" or "Family" do
not accidentally become relationship targets.

### Sleep system separation

Sleep currently spans multiple subsystems and should remain separated during migration:

- **Sleep decision scoring** determines when the character wants to sleep.
- **Sleep execution** advances world time and updates needs.
- **Sleep recovery** applies stronger emotional recovery.
- **Sleep consolidation** updates memory state.
- **Sleep outcome events** record canonical facts such as `slept`,
  `self_care`, and `recovered_energy`.

These components should be migrated and tested independently rather than
combined into one sleep function.

## Autonomous Decision System Improvements

The autonomous decision system has been migrated from the original prototype
into modular, independently tested components.

Current decision layers include:

- Need urgency and need pressure
- Special sleep pressure
- Activity preference
- Recent repetition / satiation
- Time-of-day context
- Value relevance and value-based motivation
- Goal relevance
- Ambition and discipline
- Risk / rule-obedience hesitation
- Candidate action generation
- Action availability filtering
- Ranked self-directed action selection

### Architectural improvements

The prototype handled most autonomous decision logic inside a large scoring
function. Aevum now separates that behavior into focused functions so each
cognitive influence can be tested and tuned independently.

Examples include:

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

### Important system boundaries

**Desirability is not availability.**

An action may receive a poor score because the character does not want to
perform it, while availability determines whether the action can currently be
considered at all.

For example:

- `"Shop is likely closed"` can influence time-of-day desirability.
- `"Family shop is closed"` makes the action unavailable.

**Intention is not outcome.**

The autonomous decision system produces a character intention. It does not
decide canonical reality or directly mutate world state.

The intended architecture is:

Character state
→ generate possible actions
→ filter unavailable actions
→ score available actions
→ choose intention
→ Axiom resolves the attempted action
→ canonical world event
→ character perception and cognition

### Migration improvements to revisit later

- Candidate actions are currently a fixed baseline catalog.
- Availability rules are currently simple and mostly time-based.
- Value and goal relevance use prototype-era linear scaling.
- Sleep thresholds and urgency curves may need tuning for longer simulations.
- Recent-action history currently keeps a short rolling window.
- Decision tie-breaking is currently deterministic through score ordering.
- Future action generation should become more contextual and world-aware.
- Availability should eventually use richer authoritative world state rather
  than only local decision-layer conditions.

  ### Decision result schema

Scored actions intentionally preserve both:

- `action` — human-readable action name
- `action_type` — structured action category
- `action_data` — full candidate action definition

This avoids duplicate dictionary keys and preserves both display information
and structured action metadata for downstream Axiom resolution.
