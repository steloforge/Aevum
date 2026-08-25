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

def make_eating_character():
    return {
        "name":
            "Test Character",

        "needs": {
            "hunger": 60,
            "fatigue": 20,
            "social": 10,
            "family_responsibility": 15,
            "training_drive": 25,
        },
    }


def make_eat_action():
    return {
        "action":
            "Eat a meal",

        "action_type":
            "eat",

        "action_data": {
            "name":
                "Eat a meal",

            "action_type":
                "eat",

            "tags": [
                "self_care",
            ],

            "satisfies": {
                "hunger": 45,
            },
        },
    }


def test_eat_self_directed_action_succeeds():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    result = (
        resolve_self_directed_action(
            world,
            character,
            make_eat_action(),
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result["action_type"]
        == "eat"
    )

    assert (
        result["duration_hours"]
        == 1
    )


def test_eating_reduces_hunger_then_applies_time_drift():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    resolve_self_directed_action(
        world,
        character,
        make_eat_action(),
    )

    # Start hunger:
    # 60
    #
    # Meal:
    # -45
    #
    # One hour awake:
    # +2
    #
    # Final:
    # 17

    assert (
        character[
            "needs"
        ][
            "hunger"
        ]
        == 17.0
    )


def test_eating_advances_world_time():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    resolve_self_directed_action(
        world,
        character,
        make_eat_action(),
    )

    assert (
        world["day"]
        == 1
    )

    assert (
        world["hour"]
        == 11
    )


def test_eating_applies_normal_awake_need_drift():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    resolve_self_directed_action(
        world,
        character,
        make_eat_action(),
    )

    assert (
        character[
            "needs"
        ][
            "fatigue"
        ]
        == 21.5
    )

    assert (
        character[
            "needs"
        ][
            "social"
        ]
        == 10.3
    )

    assert (
        character[
            "needs"
        ][
            "family_responsibility"
        ]
        == 15.4
    )

    assert (
        character[
            "needs"
        ][
            "training_drive"
        ]
        == 25.5
    )
