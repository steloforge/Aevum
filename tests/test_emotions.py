import pytest

from aevum.character.emotions import (
    drift_emotions_over_time,
    process_emotional_response,
    reset_emotions,
)


def make_character(
    self_control=50,
):
    return {
        "name": "Test Character",
        "traits": {
            "self_control":
                self_control,
        },
        "current_emotions": {
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
            "stress": 0,
            "happiness": 50,
        },
    }


def test_self_control_reduces_emotional_response():
    character = make_character(
        self_control=80,
    )

    response = process_emotional_response(
        character,
        {
            "fear": 50,
        },
    )

    # 1 - (0.80 * 0.40)
    assert (
        response["regulation_factor"]
        == pytest.approx(0.68)
    )

    # 50 * 0.68
    assert (
        response["applied_emotions"]["fear"]
        == pytest.approx(34.0)
    )


def test_negative_activation_reduces_happiness():
    character = make_character(
        self_control=50,
    )

    response = process_emotional_response(
        character,
        {
            "fear": 20,
            "anger": 10,
        },
    )

    assert (
        response["negative_activation"]
        > 0
    )

    assert (
        response["happiness_reduction"]
        > 0
    )

    assert (
        character[
            "current_emotions"
        ]["happiness"]
        < 50
    )


def test_negative_activation_increases_stress():
    character = make_character(
        self_control=50,
    )

    response = process_emotional_response(
        character,
        {
            "fear": 20,
        },
    )

    assert (
        response["stress_increase"]
        > 0
    )

    assert (
        character[
            "current_emotions"
        ]["stress"]
        > 0
    )


def test_happiness_accumulates_more_gently():
    character = make_character(
        self_control=50,
    )

    response = process_emotional_response(
        character,
        {
            "happiness": 20,
        },
    )

    # Regulation factor = 0.8
    # 20 * 0.8 * 0.5 = 8
    assert (
        response[
            "applied_emotions"
        ]["happiness"]
        == pytest.approx(8.0)
    )

    assert (
        character[
            "current_emotions"
        ]["happiness"]
        == pytest.approx(58.0)
    )


def test_emotions_drift_toward_baseline():
    character = make_character()

    character["current_emotions"] = {
        "fear": 50,
        "anger": 30,
        "guilt": 20,
        "sadness": 40,
        "stress": 25,
        "happiness": 80,
    }

    before = (
        character[
            "current_emotions"
        ].copy()
    )

    drift_emotions_over_time(
        character,
        hours_passed=2,
        sleeping=False,
    )

    after = character[
        "current_emotions"
    ]

    assert after["fear"] < before["fear"]
    assert after["anger"] < before["anger"]
    assert after["sadness"] < before["sadness"]

    # Happiness returns toward its baseline of 50.
    assert after["happiness"] < before["happiness"]
    assert after["happiness"] > 50


def test_sleep_recovers_emotions_faster():
    awake = make_character()
    sleeping = make_character()

    awake[
        "current_emotions"
    ]["fear"] = 50

    sleeping[
        "current_emotions"
    ]["fear"] = 50

    drift_emotions_over_time(
        awake,
        hours_passed=2,
        sleeping=False,
    )

    drift_emotions_over_time(
        sleeping,
        hours_passed=2,
        sleeping=True,
    )

    assert (
        sleeping[
            "current_emotions"
        ]["fear"]
        <
        awake[
            "current_emotions"
        ]["fear"]
    )


def test_reset_emotions_returns_to_baseline():
    character = make_character()

    character["current_emotions"] = {
        "fear": 80,
        "anger": 60,
        "guilt": 40,
        "sadness": 70,
        "stress": 50,
        "happiness": 10,
    }

    reset_emotions(character)

    assert character[
        "current_emotions"
    ] == {
        "fear": 0,
        "anger": 0,
        "guilt": 0,
        "sadness": 0,
        "stress": 0,
        "happiness": 50,
    }
