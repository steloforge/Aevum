from aevum.character.interpretation import (
    interpret_event,
)


def make_character():
    return {
        "name":
            "Test Character",

        "traits": {
            "rule_obedience":
                70,

            "patience":
                70,
        },

        "values": {
            "peace":
                80,

            "family":
                80,
        },

        "relationships":
            {},
    }


def make_perception(
    details=None,
):
    if details is None:
        details = {}

    return {
        "event_id":
            "event_test",

        "known_details":
            details,
    }


def test_default_interpretation():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(),
    )

    assert (
        result[
            "interpretation"
        ]
        ==
        "Something happened, but I am still deciding what it means to me."
    )

    assert (
        result["importance"]
        == 30
    )


def test_family_protection_creates_positive_interpretation():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "protected_family":
                    True,
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["happiness"]
        == 20
    )

    # Base 30 + family value 80 * 0.2
    assert (
        result[
            "importance"
        ]
        == 46
    )

    assert (
        "protected my family"
        in result[
            "interpretation"
        ]
    )


def test_peaceful_resolution_respects_peace_value():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "resolved_peacefully":
                    True,
            }
        ),
    )

    # 15 base peaceful happiness
    # +10 because peace value >= 70
    assert (
        result[
            "emotions"
        ]["happiness"]
        == 25
    )


def test_community_support_is_positive():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "community_help_given":
                    True,
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["happiness"]
        == 15
    )

    assert (
        result[
            "emotion_causes"
        ]["happiness"]
        == "Community Support"
    )


def test_community_neglect_creates_negative_emotions():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "community_help_refused":
                    True,
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["sadness"]
        == 15
    )

    assert (
        result[
            "emotions"
        ]["anger"]
        == 10
    )

    assert (
        result[
            "emotions"
        ]["stress"]
        == 5
    )


def test_blocked_violent_action_creates_guilt_for_peaceful_character():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "action_allowed":
                    False,

                "attempted_action":
                    "Attack the guard",
            }
        ),
    )

    # 15 from rule obedience
    # +15 because a peaceful character
    # moved toward violence
    assert (
        result[
            "emotions"
        ]["guilt"]
        == 30
    )

    assert (
        result[
            "emotions"
        ]["stress"]
        == 10
    )


def test_low_trust_target_increases_anger():
    character = make_character()

    character[
        "relationships"
    ]["Rival"] = {
        "trust":
            20,

        "respect":
            50,

        "familiarity":
            20,

        "affection":
            0,

        "fear":
            0,
    }

    result = interpret_event(
        character,
        make_perception(
            {
                "target":
                    "Rival",
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["anger"]
        == 10
    )

    assert (
        result[
            "emotion_causes"
        ]["anger"]
        == "Rival"
    )


def test_feared_target_increases_fear():
    character = make_character()

    character[
        "relationships"
    ]["Monster"] = {
        "trust":
            50,

        "respect":
            50,

        "familiarity":
            20,

        "affection":
            0,

        "fear":
            60,
    }

    result = interpret_event(
        character,
        make_perception(
            {
                "target":
                    "Monster",
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["fear"]
        == 15
    )


def test_successful_help_is_rewarding():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "action_success":
                    True,

                "helped_person":
                    True,

                "target":
                    "Resident",
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["happiness"]
        == 25
    )

    assert (
        result[
            "importance"
        ]
        == 50
    )


def test_training_creates_happiness_and_importance():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "trained_skill":
                    True,
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["happiness"]
        == 10
    )

    assert (
        result[
            "importance"
        ]
        == 45
    )


def test_family_time_is_rewarding():
    character = make_character()

    result = interpret_event(
        character,
        make_perception(
            {
                "spent_time_with_family":
                    True,
            }
        ),
    )

    assert (
        result[
            "emotions"
        ]["happiness"]
        == 20
    )

    assert (
        result[
            "emotion_causes"
        ]["happiness"]
        == "Family"
    )
