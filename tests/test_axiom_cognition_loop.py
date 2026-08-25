from aevum.axiom.resolution import (
    create_outcome_event,
    resolve_action_outcome,
)

from aevum.character.processing import (
    process_outcome_for_character,
)


def make_character():
    return {
        "name":
            "Test Character",

        "traits": {
            "compassion": 100,
            "courage": 100,
            "self_control": 100,
            "aggression": 20,
            "rule_obedience": 70,
            "patience": 70,
        },

        "skills": {
            "discipline": 100,
        },

        "values": {
            "personal_honor": 80,
            "peace": 80,
            "family": 80,
        },

        "memory": [],

        "relationships": {},

        "beliefs": {},

        "self_concept": {
            "protector": 0,
            "peacekeeper": 0,
            "family_guardian": 0,
            "rule_follower": 0,
            "fighter": 0,
        },

        "current_emotions": {
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
            "stress": 0,
            "happiness": 50,
        },
    }


def test_character_intention_becomes_lived_consequence():
    character = make_character()

    world = {
        "day": 20,
        "hour": 14,
        "next_event_id": 1,
        "events": [],
        "laws": {
            "safe_zones": [
                "Market",
            ],
            "no_attacking_in_safe_zones":
                True,
            "no_killing_in_safe_zones":
                True,
        },
    }

    original_event = {
        "event_id":
            "event_original",

        "event_type":
            "community_neglect",

        "description":
            (
                "An injured resident "
                "needed assistance."
            ),

        "location":
            "Market",

        "participants": [
            "Test Character",
            "Injured Resident",
        ],

        "details": {
            "target":
                "Injured Resident",
        },
    }

    chosen_action = {
        "action":
            "Help Injured Resident",

        "action_type":
            "help_person",

        "target":
            "Injured Resident",
    }

    # --------------------------------------------------------
    # CHARACTER INTENTION -> AXIOM RESOLUTION
    # --------------------------------------------------------

    outcome = resolve_action_outcome(
        world=world,
        character=character,
        chosen_action=chosen_action,
        event=original_event,
    )

    assert (
        outcome["status"]
        == "success"
    )

    # --------------------------------------------------------
    # AXIOM RESOLUTION -> CANONICAL WORLD EVENT
    # --------------------------------------------------------

    outcome_event = create_outcome_event(
        world=world,
        character=character,
        original_event=original_event,
        chosen_action=chosen_action,
        outcome=outcome,
    )

    assert (
        outcome_event[
            "details"
        ][
            "action_success"
        ]
        is True
    )

    assert (
        outcome_event[
            "details"
        ][
            "protected_other"
        ]
        is True
    )

    # --------------------------------------------------------
    # CANONICAL REALITY -> CHARACTER COGNITION
    # --------------------------------------------------------

    cognition = process_outcome_for_character(
        character=character,
        world=world,
        outcome_event=outcome_event,
        autosave_after=False,
    )

    # A memory of the actual outcome exists.
    assert (
        len(
            character[
                "memory"
            ]
        )
        == 1
    )

    assert (
        cognition[
            "memory"
        ][
            "description"
        ]
        == outcome_event[
            "description"
        ]
    )

    # Successful protection contributes to identity.
    assert (
        character[
            "self_concept"
        ][
            "protector"
        ]
        == 4
    )

    # Helping was emotionally rewarding.
    assert (
        character[
            "current_emotions"
        ][
            "happiness"
        ]
        > 50
    )

    # The target became part of lived social history.
    assert (
        "Injured Resident"
        in character[
            "relationships"
        ]
    )
