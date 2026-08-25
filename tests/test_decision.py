from aevum.character.decision import (
    calculate_need_pressure,
    calculate_need_urgency,
    calculate_sleep_pressure,
    calculate_time_of_day_effect,
)


def test_low_physical_need_has_normal_urgency():
    assert (
        calculate_need_urgency(
            "hunger",
            22,
        )
        == 1.0
    )


def test_physical_need_urgency_increases_with_pressure():
    assert (
        calculate_need_urgency(
            "hunger",
            30,
        )
        == 1.25
    )

    assert (
        calculate_need_urgency(
            "hunger",
            50,
        )
        == 1.75
    )

    assert (
        calculate_need_urgency(
            "hunger",
            70,
        )
        == 2.5
    )

    assert (
        calculate_need_urgency(
            "hunger",
            85,
        )
        == 4.0
    )


def test_nonphysical_need_has_normal_urgency():
    assert (
        calculate_need_urgency(
            "training_drive",
            95,
        )
        == 1.0
    )


def test_eating_reproduces_ryuk_day_34_hunger_pressure():
    character = {
        "needs": {
            "hunger": 22.0,
        },
    }

    action = {
        "name":
            "Eat a meal",

        "action_type":
            "eat",

        "satisfies": {
            "hunger": 45,
        },
    }

    result = calculate_need_pressure(
        character,
        action,
    )

    assert (
        result["score"]
        == 9.9
    )

    assert (
        result["reasons"]
        == [
            (
                "hunger pressure: "
                "+9.9 "
                "(urgency x1.0)"
            )
        ]
    )


def test_action_can_satisfy_multiple_needs():
    character = {
        "needs": {
            "family_responsibility":
                0.8,

            "social":
                0.6,
        },
    }

    action = {
        "name":
            "Help at the family shop",

        "action_type":
            "family_duty",

        "satisfies": {
            "family_responsibility":
                35,

            "social":
                10,
        },
    }

    result = calculate_need_pressure(
        character,
        action,
    )

    # 0.8 × .35 = .28
    # 0.6 × .10 = .06
    assert (
        result["score"]
        == 0.34
    )

    assert len(
        result["reasons"]
    ) == 2

def test_sleep_pressure_is_zero_below_fatigue_threshold():
    character = {
        "needs": {
            "fatigue": 10,
        },
    }

    action = {
        "action_type":
            "sleep",
    }

    result = calculate_sleep_pressure(
        character,
        action,
    )

    assert result["score"] == 0


def test_sleep_pressure_uses_only_fatigue_above_twenty():
    character = {
        "needs": {
            "fatigue": 34.5,
        },
    }

    action = {
        "action_type":
            "sleep",
    }

    result = calculate_sleep_pressure(
        character,
        action,
    )

    assert (
        result["score"]
        == 12.69
    )


def test_sleep_pressure_reproduces_high_fatigue_behavior():
    character = {
        "needs": {
            "fatigue": 37.33,
        },
    }

    action = {
        "action_type":
            "sleep",
    }

    result = calculate_sleep_pressure(
        character,
        action,
    )

    # Effective fatigue:
    # 37.33 - 20 = 17.33
    #
    # Urgency at 37.33 fatigue:
    # 1.25
    #
    # 17.33 * 0.70 * 1.25
    # = 15.16375
    assert (
        result["score"]
        == 15.16
    )


def test_non_sleep_action_gets_no_sleep_pressure():
    character = {
        "needs": {
            "fatigue": 90,
        },
    }

    action = {
        "action_type":
            "rest",
    }

    result = calculate_sleep_pressure(
        character,
        action,
    )

    assert result == {
        "score": 0,
        "reasons": [],
    }


def test_sleep_is_discouraged_in_morning():
    world = {
        "hour": 9,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "sleep",
        )
    )

    assert (
        result["period"]
        == "morning"
    )

    assert (
        result["effect"]
        == -12
    )

    assert (
        result["reason"]
        == (
            "The character would "
            "normally be awake"
        )
    )


def test_sleep_is_encouraged_at_night():
    world = {
        "hour": 21,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "sleep",
        )
    )

    assert (
        result["period"]
        == "night"
    )

    assert (
        result["effect"]
        == 10
    )

    assert (
        result["reason"]
        == "Natural sleeping hours"
    )


def test_sleep_is_strongly_encouraged_late_at_night():
    world = {
        "hour": 2,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "sleep",
        )
    )

    assert (
        result["period"]
        == "late_night"
    )

    assert (
        result["effect"]
        == 20
    )


def test_family_shop_matches_normal_shop_hours():
    world = {
        "hour": 10,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "family_duty",
        )
    )

    assert (
        result["effect"]
        == 3
    )

    assert (
        result["reason"]
        == "Normal shop hours"
    )


def test_family_shop_is_discouraged_at_night():
    world = {
        "hour": 22,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "family_duty",
        )
    )

    assert (
        result["effect"]
        == -8
    )

    assert (
        result["reason"]
        == "Shop is likely closed"
    )


def test_secret_training_gets_night_privacy_bonus():
    world = {
        "hour": 21,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "train",
        )
    )

    assert (
        result["effect"]
        == 3
    )

    assert (
        result["reason"]
        == "Night provides privacy"
    )


def test_eating_gets_early_morning_meal_bonus():
    world = {
        "hour": 7,
    }

    result = (
        calculate_time_of_day_effect(
            world,
            "eat",
        )
    )

    assert (
        result["effect"]
        == 2
    )

    assert (
        result["reason"]
        == "Natural meal time"
    )
