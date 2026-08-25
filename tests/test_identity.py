from aevum.character.identity import (
    update_self_concept,
)


def make_character():
    return {
        "name": "Test Character",
    }


def make_perception(
    details=None,
):
    if details is None:
        details = {}

    return {
        "known_details":
            details,
    }


def test_self_concept_is_created_when_missing():
    character = make_character()

    result = update_self_concept(
        character,
        make_perception(),
        interpretation={},
    )

    assert result == {
        "protector": 0,
        "peacekeeper": 0,
        "family_guardian": 0,
        "rule_follower": 0,
        "fighter": 0,
    }


def test_protecting_family_builds_protector_and_family_guardian():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "protected_family":
                    True,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["protector"]
        == 5
    )

    assert (
        character[
            "self_concept"
        ]["family_guardian"]
        == 7
    )


def test_successfully_protecting_other_builds_protector():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "protected_other":
                    True,

                "action_success":
                    True,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["protector"]
        == 4
    )


def test_failed_protection_does_not_build_protector():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "protected_other":
                    True,

                "action_success":
                    False,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["protector"]
        == 0
    )


def test_peaceful_resolution_builds_peacekeeper():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "resolved_peacefully":
                    True,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["peacekeeper"]
        == 5
    )


def test_accepting_law_builds_rule_follower():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "accepted_law":
                    True,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["rule_follower"]
        == 3
    )


def test_family_responsibility_builds_family_guardian():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "fulfilled_responsibility":
                    True,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["family_guardian"]
        == 2
    )


def test_training_builds_fighter_identity():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "trained_skill":
                    True,
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["fighter"]
        == 1
    )


def test_actual_fighting_builds_fighter_identity():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "performed_action":
                    "Fight the attacker",
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["fighter"]
        == 2
    )


def test_training_and_fighting_can_stack():
    character = make_character()

    update_self_concept(
        character,
        make_perception(
            {
                "trained_skill":
                    True,

                "performed_action":
                    "Strike the training dummy",
            }
        ),
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["fighter"]
        == 3
    )


def test_repeated_experiences_accumulate_identity():
    character = make_character()

    perception = make_perception(
        {
            "resolved_peacefully":
                True,
        }
    )

    update_self_concept(
        character,
        perception,
        interpretation={},
    )

    update_self_concept(
        character,
        perception,
        interpretation={},
    )

    assert (
        character[
            "self_concept"
        ]["peacekeeper"]
        == 10
    )
