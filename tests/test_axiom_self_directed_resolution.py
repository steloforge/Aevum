from aevum.axiom.resolution import (
    resolve_self_directed_action,
)


def test_unknown_self_directed_action_is_unresolved():
    character = {
        "name":
            "Test Character",
    }

    world = {
        "day": 1,
        "hour": 10,
    }

    chosen_action = {
        "action":
            "Do something mysterious",

        "action_type":
            "mysterious_action",

        "action_data": {
            "tags": [],
            "satisfies": {},
        },
    }

    result = (
        resolve_self_directed_action(
            world,
            character,
            chosen_action,
        )
    )

    assert (
        result["status"]
        == "unresolved"
    )

    assert (
        result["action"]
        == "Do something mysterious"
    )

    assert (
        result["action_type"]
        == "mysterious_action"
    )

    assert (
        result["action_data"]
        == chosen_action[
            "action_data"
        ]
    )
