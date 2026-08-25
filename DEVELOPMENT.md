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
