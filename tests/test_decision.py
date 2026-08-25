from aevum.character.decision import (
    calculate_need_pressure,
    calculate_need_urgency,
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
