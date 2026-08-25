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
    # 5. SELF-CONCEPT
    # --------------------------------------------------------

    self_concept = update_self_concept(
        character,
        perception,
        interpretation,
    )

    # --------------------------------------------------------
    # 6. BELIEFS
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
    # 7. AUTOSAVE
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
    }
