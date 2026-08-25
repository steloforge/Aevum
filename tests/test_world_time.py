from aevum.world import (
    advance_time,
    get_time_period,
)


def test_advance_time_within_same_day():
    world = {
        "day": 1,
        "hour": 8,
    }

    advance_time(
        world,
        3,
    )

    assert world["day"] == 1
    assert world["hour"] == 11


def test_advance_time_across_midnight():
    world = {
        "day": 1,
        "hour": 23,
    }

    advance_time(
        world,
        3,
    )

    assert world["day"] == 2
    assert world["hour"] == 2


def test_time_periods():
    cases = [
        (5, "early_morning"),
        (9, "morning"),
        (13, "afternoon"),
        (18, "evening"),
        (22, "night"),
        (2, "late_night"),
    ]

    for hour, expected in cases:

        world = {
            "day": 1,
            "hour": hour,
        }

        assert (
            get_time_period(world)
            == expected
        )
