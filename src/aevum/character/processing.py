"""
Character event-processing pipeline.

This module coordinates the cognitive systems that transform
authoritative Axiom world events into subjective character state.
"""

from aevum.character.beliefs import (
    apply_belief_judgment,
    infer_belief_relevance,
    judge_belief_evidence,
)

from aevum.character.emotions import (
    process_emotional_response,
)

from aevum.character.identity import (
    update_self_concept,
)

from aevum.character.interpretation import (
    interpret_event,
)

from aevum.character.memory import (
    create_memory_from_event,
)

from aevum.character.perception import (
    perceive_world_event,
)

from aevum.character.relationships import (
    update_relationship_from_memory,
)

# ============================================================
# SLEEP EMOTIONAL RECOVERY
# ============================================================


def recover_emotions_during_sleep(
    character,
    hours_slept,
):
    """
    Move persistent emotional state toward its baseline
    more strongly during sleep.
    """

    if "current_emotions" not in character:
        return {}

    emotions = character[
        "current_emotions"
    ]

    hourly_rate = 0.18

    recovery_strength = (
        1
        - (
            (1 - hourly_rate)
            ** hours_slept
        )
    )

    for emotion, current_value in emotions.items():

        if emotion == "happiness":
            baseline = 50
        else:
            baseline = 0

        difference = (
            baseline
            - current_value
        )

        emotions[emotion] += (
            difference
            * recovery_strength
        )

        emotions[emotion] = round(
            min(
                max(
                    emotions[emotion],
                    0,
                ),
                100,
            ),
            2,
        )

    return emotions

# ============================================================
# SLEEP MEMORY CONSOLIDATION
# ============================================================


def consolidate_recent_memories_during_sleep(
    character,
    world,
):
    """
    Consolidate memories from the character's most recent
    waking period after sleep.
    """

    memories_processed = 0

    for memory in character.get(
        "memory",
        [],
    ):

        created_day = memory.get(
            "created_day"
        )

        if created_day is None:
            continue

        age_in_days = (
            world["day"]
            - created_day
        )

        if age_in_days not in [
            0,
            1,
        ]:
            continue

        emotions = memory.get(
            "emotions",
            {},
        )

        emotional_intensity = sum(
            emotions.values()
        )

        importance = memory.get(
            "importance",
            0,
        )

        consolidation_boost = (
            importance
            * 0.03
        )

        consolidation_boost += min(
            emotional_intensity
            * 0.01,
            3,
        )

        if importance < 25:
            consolidation_boost *= 0.40

        consolidation_boost = min(
            consolidation_boost,
            6,
        )

        memory["clarity"] = (
            memory.get(
                "clarity",
                0,
            )
            + consolidation_boost
        )

        memory["clarity"] = round(
            min(
                memory["clarity"],
                100,
            ),
            2,
        )

        memories_processed += 1

    return memories_processed

# ============================================================
# SLEEP COGNITIVE EFFECTS
# ============================================================


def apply_sleep_cognitive_effects(
    character,
    world,
    outcome_event,
):
    """
    Apply subjective cognitive consequences of a completed
    sleep event.
    """

    details = outcome_event.get(
        "details",
        {},
    )

    if not details.get(
        "slept",
        False,
    ):
        return None

    hours_slept = details.get(
        "duration_hours",
        0,
    )

    emotional_recovery = (
        recover_emotions_during_sleep(
            character,
            hours_slept,
        )
    )

    memories_processed = (
        consolidate_recent_memories_during_sleep(
            character,
            world,
        )
    )

    return {
        "hours_slept":
            hours_slept,

        "emotional_recovery":
            emotional_recovery,

        "memories_processed":
            memories_processed,
    }

def apply_interpreted_emotions(
    character,
    interpretation,
    intensity_multiplier=1.0,
):
    """
    Apply an interpretation's emotional response to the
    character's persistent emotional state.
    """

    print(
        "\n--- EMOTIONAL STATE UPDATE ---"
    )

    response = process_emotional_response(
        character=character,
        emotions=interpretation[
            "emotions"
        ],
        response_strength=(
            intensity_multiplier
        ),
        use_regulation=True,
        suppress_opposing_emotions=True,
    )

    for emotion, value in (
        response[
            "current_emotions"
        ].items()
    ):
        print(
            f"{emotion}: {value}"
        )

    return response


def process_outcome_for_character(
    character,
    world,
    outcome_event,
    autosave_after=True,
    autosave_function=None,
):
    """
    Process an authoritative world outcome through a
    character's subjective cognitive systems.

    The world event remains canonical reality.

    Perception, interpretation, emotion, memory,
    self-concept, and beliefs belong to the character.
    """

    print(
        "\n=============================="
    )

    print(
        "OUTCOME PROCESSING START"
    )

    print(
        "=============================="
    )

    # --------------------------------------------------------
    # 1. PERCEPTION
    # --------------------------------------------------------

    perception = perceive_world_event(
        character,
        outcome_event,
    )

    # --------------------------------------------------------
    # 2. INTERPRETATION
    # --------------------------------------------------------

    interpretation = interpret_event(
        character,
        perception,
    )

    print(
        "\n--- OUTCOME INTERPRETATION ---"
    )

    print(
        interpretation[
            "interpretation"
        ]
    )

    # --------------------------------------------------------
    # 3. LIVE EMOTIONS
    # --------------------------------------------------------

    emotional_response = (
        apply_interpreted_emotions(
            character,
            interpretation,
        )
    )

    # --------------------------------------------------------
    # 4. MEMORY
    # --------------------------------------------------------

    memory = create_memory_from_event(
        character,
        world,
        perception,
        interpretation,
    )

    # --------------------------------------------------------
    # 5. SLEEP COGNITIVE EFFECTS
    # --------------------------------------------------------

    sleep_cognitive_effects = (
        apply_sleep_cognitive_effects(
            character,
            world,
            outcome_event,
        )
    )
    
    
    # --------------------------------------------------------
    # 6. RELATIONSHIPS
    # --------------------------------------------------------

    relationship_updates = (
        update_relationship_from_memory(
            character,
            memory,
        )
    )
    
    # --------------------------------------------------------
    # 7. SELF-CONCEPT
    # --------------------------------------------------------

    self_concept = update_self_concept(
        character,
        perception,
        interpretation,
    )

    # --------------------------------------------------------
    # 8. BELIEFS
    # --------------------------------------------------------

    belief_matches = (
        infer_belief_relevance(
            character,
            perception,
        )
    )

    belief_judgments = []

    for match in belief_matches:
        judgment = (
            judge_belief_evidence(
                character,
                perception,
                match,
            )
        )

        belief_judgments.append(
            judgment
        )

        apply_belief_judgment(
            character,
            outcome_event,
            perception,
            judgment,
        )

    # --------------------------------------------------------
    # 9. AUTOSAVE
    # --------------------------------------------------------

    if (
        autosave_after
        and autosave_function
        is not None
    ):
        autosave_function(
            character,
            world,
        )

    print(
        "\n=============================="
    )

    print(
        "OUTCOME PROCESSING COMPLETE"
    )

    print(
        "=============================="
    )

    return {
        "perception":
            perception,

        "interpretation":
            interpretation,

        "emotional_response":
            emotional_response,

        "memory":
            memory,

        "self_concept":
            self_concept,

        "belief_matches":
            belief_matches,

        "belief_judgments":
            belief_judgments,
               
        "relationship_updates":
            relationship_updates,
        
        "sleep_cognitive_effects":
            sleep_cognitive_effects,
    }
