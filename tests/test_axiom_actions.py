from aevum.axiom.actions import (
    generate_possible_actions,
    validate_action,
)


def test_community_neglect_generates_response_options():
    character = {
        "name":
            "Test Character",
    }

    event = {
        "event_type":
            "community_neglect",

        "details": {
            "target":
                "Injured Resident",
        },
    }

    actions = (
        generate_possible_actions(
            character,
            event,
        )
    )

    assert len(actions) == 4

    action_types = {
        action[
            "action_type"
        ]
        for action in actions
    }

    assert action_types == {
        "help_person",
        "request_help",
        "confront_person",
        "ignore_event",
    }


def test_attack_is_blocked_in_safe_zone():
    world = {
        "laws": {
            "safe_zones": [
                "Market",
            ],

            "no_attacking_in_safe_zones":
                True,
        }
    }

    action = {
        "action":
            "Attack the resident",
    }

    result = validate_action(
        world=world,
        character={},
        action=action,
        location="Market",
    )

    assert (
        result["allowed"]
        is False
    )


def test_attack_is_allowed_outside_safe_zone():
    world = {
        "laws": {
            "safe_zones": [
                "Market",
            ],

            "no_attacking_in_safe_zones":
                True,
        }
    }

    action = {
        "action":
            "Attack the resident",
    }

    result = validate_action(
        world=world,
        character={},
        action=action,
        location="Forest",
    )

    assert (
        result["allowed"]
        is True
    )
