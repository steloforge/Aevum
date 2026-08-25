from aevum.axiom.resolution import (
    resolve_action_outcome,
)


def make_character():
    return {
        "name":
            "Test Character",

        "traits": {
            "compassion":
                80,

            "courage":
                80,

            "self_control":
                80,

            "aggression":
                40,
        },

        "skills": {
            "discipline":
                80,
        },

        "values": {
            "personal_honor":
                70,
        },
    }


def make_world():
    return {
        "laws": {
            "safe_zones": [
                "Market",
            ],

            "no_attacking_in_safe_zones":
                True,

            "no_killing_in_safe_zones":
                True,
        }
    }


def test_capable_character_successfully_helps():
    character = make_character()

    event = {
        "location":
            "Market",
    }

    action = {
        "action":
            "Help Injured Resident",

        "action_type":
            "help_person",

        "target":
            "Injured Resident",
    }

    result = resolve_action_outcome(
        world=make_world(),
        character=character,
        chosen_action=action,
        event=event,
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result[
            "capability_score"
        ]
        >= result[
            "difficulty"
        ] + 20
    )


def test_unknown_action_is_unresolved():
    character = make_character()

    result = resolve_action_outcome(
        world=make_world(),
        character=character,
        chosen_action={
            "action":
                "Dance dramatically",

            "action_type":
                "dance",

            "target":
                None,
        },
        event={
            "location":
                "Market",
        },
    )

    assert (
        result["status"]
        == "unresolved"
    )


def test_ignore_event_always_resolves_successfully():
    character = make_character()

    result = resolve_action_outcome(
        world=make_world(),
        character=character,
        chosen_action={
            "action":
                (
                    "Ignore the situation "
                    "and continue walking"
                ),

            "action_type":
                "ignore_event",

            "target":
                None,
        },
        event={
            "location":
                "Market",
        },
    )

    assert (
        result["status"]
        == "success"
    )
