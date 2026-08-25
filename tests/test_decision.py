from aevum.character.decision import (
    calculate_need_pressure,
    calculate_need_urgency,
    calculate_repetition_effect,
    calculate_sleep_pressure,
    calculate_time_of_day_effect,
    record_recent_action,
    score_self_directed_action,
    calculate_value_relevance,
    calculate_value_effect,
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

def test_neutral_activity_has_no_preference_effect():
    character = {
        "activity_preferences": {},
    }

    world = {
        "day": 1,
        "hour": 12,
    }

    result = (
        calculate_repetition_effect(
            character,
            world,
            "train",
        )
    )

    assert result["preference"] == 50
    assert result["preference_bonus"] == 0
    assert result["repetition_pressure"] == 0
    assert result["repetition_penalty"] == 0
    assert result["net_effect"] == 0


def test_liked_activity_gets_preference_bonus():
    character = {
        "activity_preferences": {
            "train": 80,
        },
    }

    world = {
        "day": 1,
        "hour": 12,
    }

    result = (
        calculate_repetition_effect(
            character,
            world,
            "train",
        )
    )

    assert result["preference"] == 80
    assert result["preference_bonus"] == 3
    assert result["net_effect"] == 3


def test_disliked_activity_gets_preference_penalty():
    character = {
        "activity_preferences": {
            "family_duty": 30,
        },
    }

    world = {
        "day": 1,
        "hour": 12,
    }

    result = (
        calculate_repetition_effect(
            character,
            world,
            "family_duty",
        )
    )

    assert result["preference_bonus"] == -2
    assert result["net_effect"] == -2


def test_recent_action_creates_repetition_pressure():
    character = {
        "activity_preferences": {
            "train": 50,
        },
        "recent_actions": [
            {
                "action_type": "train",
                "day": 1,
                "hour": 10,
                "duration_hours": 2,
            },
        ],
    }

    world = {
        "day": 1,
        "hour": 12,
    }

    result = (
        calculate_repetition_effect(
            character,
            world,
            "train",
        )
    )

    assert (
        result["repetition_pressure"]
        == 2
    )

    assert (
        result["repetition_penalty"]
        == 2.5
    )

    assert result["net_effect"] == -2.5


def test_older_repetition_has_less_influence():
    character = {
        "activity_preferences": {
            "train": 50,
        },
        "recent_actions": [
            {
                "action_type": "train",
                "day": 1,
                "hour": 10,
                "duration_hours": 2,
            },
        ],
    }

    world = {
        "day": 1,
        "hour": 20,
    }

    result = (
        calculate_repetition_effect(
            character,
            world,
            "train",
        )
    )

    assert (
        result["repetition_pressure"]
        == 0.6
    )


def test_unrelated_actions_do_not_create_repetition_pressure():
    character = {
        "activity_preferences": {
            "train": 50,
        },
        "recent_actions": [
            {
                "action_type":
                    "social_family",
                "day": 1,
                "hour": 10,
                "duration_hours": 3,
            },
        ],
    }

    world = {
        "day": 1,
        "hour": 12,
    }

    result = (
        calculate_repetition_effect(
            character,
            world,
            "train",
        )
    )

    assert (
        result["repetition_pressure"]
        == 0
    )


def test_enjoyed_activity_resists_repetition_fatigue():
    world = {
        "day": 1,
        "hour": 12,
    }

    recent_action = {
        "action_type": "train",
        "day": 1,
        "hour": 10,
        "duration_hours": 2,
    }

    neutral_character = {
        "activity_preferences": {
            "train": 50,
        },
        "recent_actions": [
            recent_action,
        ],
    }

    enthusiastic_character = {
        "activity_preferences": {
            "train": 90,
        },
        "recent_actions": [
            recent_action,
        ],
    }

    neutral = (
        calculate_repetition_effect(
            neutral_character,
            world,
            "train",
        )
    )

    enthusiastic = (
        calculate_repetition_effect(
            enthusiastic_character,
            world,
            "train",
        )
    )

    assert (
        enthusiastic[
            "repetition_penalty"
        ]
        < neutral[
            "repetition_penalty"
        ]
    )


def test_record_recent_action_stores_action_history():
    character = {}

    world = {
        "day": 4,
        "hour": 15,
    }

    record_recent_action(
        character,
        world,
        "train",
        2,
    )

    assert (
        character["recent_actions"]
        == [
            {
                "action_type": "train",
                "day": 4,
                "hour": 15,
                "duration_hours": 2,
            }
        ]
    )


def test_record_recent_action_removes_old_history():
    character = {
        "recent_actions": [
            {
                "action_type": "train",
                "day": 1,
                "hour": 10,
                "duration_hours": 2,
            },
        ],
    }

    world = {
        "day": 4,
        "hour": 12,
    }

    record_recent_action(
        character,
        world,
        "eat",
        1,
    )

    assert len(
        character["recent_actions"]
    ) == 1

    assert (
        character[
            "recent_actions"
        ][0]["action_type"]
        == "eat"
    )

def test_partial_action_score_combines_need_and_preference():
    character = {
        "needs": {
            "hunger": 22.0,
        },

        "activity_preferences": {
            "eat": 50,
        },

        "recent_actions": [],
    }

    world = {
        "day": 34,
        "hour": 10,
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

    result = (
        score_self_directed_action(
            character,
            world,
            action,
        )
    )

    assert (
        result["score"]
        == 9.9
    )

    assert (
        "hunger pressure: "
        "+9.9 (urgency x1.0)"
        in result["reasons"]
    )

    assert (
        "Activity preference: +0.0"
        in result["reasons"]
    )


def test_partial_action_score_includes_repetition_penalty():
    character = {
        "needs": {
            "hunger": 22.0,
        },

        "activity_preferences": {
            "eat": 50,
        },

        "recent_actions": [
            {
                "action_type":
                    "eat",

                "day":
                    34,

                "hour":
                    8,

                "duration_hours":
                    1,
            },
        ],
    }

    world = {
        "day": 34,
        "hour": 10,
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

    result = (
        score_self_directed_action(
            character,
            world,
            action,
        )
    )

    # Preference 50 produces:
    #
    # base repetition = 1 * 2 = 2
    # enjoyment resistance = .375
    # penalty = 2 * .625 = 1.25
    #
    # 9.9 - 1.25 = 8.65

    assert (
        result["score"]
        == 8.65
    )

    assert (
        "Recent repetition: -1.25"
        in result["reasons"]
    )


def test_partial_sleep_score_combines_sleep_and_time_pressure():
    character = {
        "needs": {
            "fatigue": 34.5,
        },

        "activity_preferences": {
            "sleep": 50,
        },

        "recent_actions": [],
    }

    world = {
        "day": 4,
        "hour": 10,
    }

    action = {
        "name":
            "Go to sleep",

        "action_type":
            "sleep",

        "satisfies": {},
    }

    result = (
        score_self_directed_action(
            character,
            world,
            action,
        )
    )

    # Sleep pressure = +12.69
    # Morning context = -12
    #
    # Net = 0.69

    assert (
        result["score"]
        == 0.69
    )

    assert (
        (
            "Sleep fatigue pressure: "
            "+12.69 (urgency x1.25)"
        )
        in result["reasons"]
    )

    assert (
        (
            "Time of day (morning): "
            "-12 - The character "
            "would normally be awake"
        )
        in result["reasons"]
    )


def test_recent_full_sleep_can_outweigh_morning_sleep_desire():
    character = {
        "needs": {
            "fatigue": 0,
        },

        "activity_preferences": {
            "sleep": 50,
        },

        "recent_actions": [
            {
                "action_type":
                    "sleep",

                "day":
                    4,

                "hour":
                    8,

                "duration_hours":
                    8,
            },
        ],
    }

    world = {
        "day": 4,
        "hour": 10,
    }

    action = {
        "name":
            "Go to sleep",

        "action_type":
            "sleep",

        "satisfies": {},
    }

    result = (
        score_self_directed_action(
            character,
            world,
            action,
        )
    )

    # Repetition:
    #
    # pressure = 8
    # base penalty = 16
    # enjoyment resistance = .375
    # repetition penalty = 10
    #
    # Morning time = -12
    #
    # Total = -22

    assert (
        result["score"]
        == -22
    )

    assert (
        "Recent repetition: -10.0"
        in result["reasons"]
    )

def test_family_duty_value_relevance_scales_with_responsibility():
    character = {
        "needs": {
            "family_responsibility": 0,
        },
    }

    result = calculate_value_relevance(
        character,
        "family_duty",
    )

    assert result == 0.25


def test_family_duty_value_relevance_reaches_full_strength():
    character = {
        "needs": {
            "family_responsibility": 100,
        },
    }

    result = calculate_value_relevance(
        character,
        "family_duty",
    )

    assert result == 1.0


def test_non_family_duty_values_have_full_relevance():
    character = {
        "needs": {
            "family_responsibility": 0,
        },
    }

    result = calculate_value_relevance(
        character,
        "social_family",
    )

    assert result == 1.0


def test_family_duty_value_effect_combines_relevant_values():
    character = {
        "needs": {
            "family_responsibility": 100,
        },

        "values": {
            "family": 80,
            "community": 60,
            "personal_honor": 70,
        },
    }

    action = {
        "name":
            "Help at the family shop",

        "action_type":
            "family_duty",

        "tags": [
            "family",
            "community",
            "honor",
        ],
    }

    result = calculate_value_effect(
        character,
        action,
    )

    assert result[
        "value_relevance"
    ] == 1.0

    assert result[
        "family_bonus"
    ] == 6.4

    assert result[
        "community_bonus"
    ] == 3.0

    assert result[
        "honor_bonus"
    ] == 3.5

    assert result[
        "total_effect"
    ] == 12.9
