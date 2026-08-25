from aevum.character.beliefs import (
    get_or_create_belief,
)

from aevum.character.processing import (
    process_outcome_for_character,
)


def make_character():
    character = {
        "name": "Test Character",

        "traits": {
            "self_control": 50,
            "rule_obedience": 70,
            "patience": 70,
        },

        "values": {
            "peace": 80,
            "family": 80,
        },

        "memory": [],

        "relationships": {},

        "current_emotions": {
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
            "stress": 0,
            "happiness": 50,
        },

        "self_concept": {
            "protector": 0,
            "peacekeeper": 0,
            "family_guardian": 0,
            "rule_follower": 0,
            "fighter": 0,
        },

        "beliefs": {},
    }

    belief = get_or_create_belief(
        character,
        "community_support",
        (
            "People in my community "
            "look out for one another."
        ),
    )

    belief["concepts"] = [
        "residents",
        "help",
        "community",
    ]

    return character


def test_world_event_flows_through_character_cognition():
    character = make_character()

    world = {
        "day": 12,
        "hour": 10,
    }

    event = {
        "event_id": "event_1",

        "day": 12,

        "event_type":
            "action_outcome",

        "description":
            (
                "Several residents helped "
                "an injured neighbor."
            ),

        "location":
            "Community Market",

        "participants": [
            "Test Character",
            "Resident",
            "Neighbor",
        ],

        "details": {
            "community_help_given":
                True,

            "resolved_peacefully":
                True,
        },
    }

    result = (
        process_outcome_for_character(
            character=character,
            world=world,
            outcome_event=event,
            autosave_after=False,
        )
    )

    # --------------------------------------------------------
    # PERCEPTION
    # --------------------------------------------------------

    assert (
        result[
            "perception"
        ]["event_id"]
        == "event_1"
    )

    # --------------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------------

    assert (
        result[
            "interpretation"
        ]["emotions"]["happiness"]
        > 0
    )

    # --------------------------------------------------------
    # LIVE EMOTIONAL STATE
    # --------------------------------------------------------

    assert (
        character[
            "current_emotions"
        ]["happiness"]
        > 50
    )

    # --------------------------------------------------------
    # MEMORY
    # --------------------------------------------------------

    assert len(
        character["memory"]
    ) == 1

    memory = character[
        "memory"
    ][0]

    assert (
        memory["description"]
        == event["description"]
    )

    assert (
        memory["clarity"]
        == 95
    )

    assert (
        "community market"
        in memory[
            "associations"
        ]
    )

    assert (
        "community help given"
        in memory[
            "associations"
        ]
    )

    # --------------------------------------------------------
    # IDENTITY
    # --------------------------------------------------------

    assert (
        character[
            "self_concept"
        ]["peacekeeper"]
        == 5
    )

    # --------------------------------------------------------
    # BELIEF
    # --------------------------------------------------------

    belief = character[
        "beliefs"
    ]["community_support"]

    assert (
        belief["confidence"]
        == 60.5
    )

    assert len(
        belief["evidence_for"]
    ) == 1

    assert (
        belief[
            "times_reconsidered"
        ]
        == 1
    )
