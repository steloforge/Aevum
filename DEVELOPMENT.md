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
