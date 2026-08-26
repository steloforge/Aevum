from aevum.axiom.resolution import (
    create_self_directed_outcome_event,
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

def test_eat_resolution_creates_canonical_world_event():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_eat_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    assert (
        event["event_type"]
        == "self_directed_outcome"
    )

    assert (
        event["description"]
        == (
            "Test Character "
            "took time to eat a meal."
        )
    )

    assert (
        event["location"]
        == "Family Shop"
    )

    assert (
        event["participants"]
        == [
            "Test Character",
        ]
    )


def test_eat_world_event_contains_authoritative_details():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_eat_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    details = event[
        "details"
    ]

    assert (
        details[
            "performed_action"
        ]
        == "Eat a meal"
    )

    assert (
        details[
            "action_type"
        ]
        == "eat"
    )

    assert (
        details[
            "action_success"
        ]
        is True
    )

    assert (
        details[
            "duration_hours"
        ]
        == 1
    )

    assert (
        details[
            "self_care"
        ]
        is True
    )

    assert (
        details[
            "satisfied_hunger"
        ]
        is True
    )


def test_self_directed_event_uses_post_action_world_time():
    character = (
        make_eating_character()
    )

    world = {
        "day": 1,
        "hour": 10,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_eat_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    # Eating takes one hour.
    #
    # The canonical outcome event records
    # when the completed outcome exists.

    assert (
        event["day"]
        == 1
    )

    assert (
        event["hour"]
        == 11
    )

def make_resting_character():
    return {
        "name":
            "Test Character",

        "needs": {
            "hunger": 20,
            "fatigue": 60,
            "social": 10,
            "family_responsibility": 15,
            "training_drive": 25,
        },
    }


def make_rest_action():
    return {
        "action":
            "Rest for a while",

        "action_type":
            "rest",

        "action_data": {
            "name":
                "Rest for a while",

            "action_type":
                "rest",

            "tags": [
                "self_care",
            ],

            "satisfies": {
                "fatigue": 18,
            },
        },
    }

def test_rest_self_directed_action_succeeds():
    character = (
        make_resting_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    result = (
        resolve_self_directed_action(
            world,
            character,
            make_rest_action(),
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result["action_type"]
        == "rest"
    )

    assert (
        result["duration_hours"]
        == 2
    )


def test_rest_reduces_fatigue_then_applies_awake_drift():
    character = (
        make_resting_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    resolve_self_directed_action(
        world,
        character,
        make_rest_action(),
    )

    # 60 fatigue
    # -18 from resting
    # +3 from two waking hours
    # = 45

    assert (
        character[
            "needs"
        ][
            "fatigue"
        ]
        == 45.0
    )

    assert (
        character[
            "needs"
        ][
            "hunger"
        ]
        == 24.0
    )


def test_rest_advances_world_time_two_hours():
    character = (
        make_resting_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    resolve_self_directed_action(
        world,
        character,
        make_rest_action(),
    )

    assert (
        world["day"]
        == 1
    )

    assert (
        world["hour"]
        == 12
    )

def test_rest_resolution_creates_canonical_world_event():
    character = (
        make_resting_character()
    )

    world = {
        "day": 1,
        "hour": 10,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_rest_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    assert (
        event["event_type"]
        == "self_directed_outcome"
    )

    assert (
        event["description"]
        == (
            "Test Character "
            "took time to rest and recover."
        )
    )

    assert (
        event["location"]
        == "Family Living Quarters"
    )

    assert (
        event["participants"]
        == [
            "Test Character",
        ]
    )


def test_rest_world_event_contains_authoritative_details():
    character = (
        make_resting_character()
    )

    world = {
        "day": 1,
        "hour": 10,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_rest_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    details = event[
        "details"
    ]

    assert (
        details[
            "action_type"
        ]
        == "rest"
    )

    assert (
        details[
            "action_success"
        ]
        is True
    )

    assert (
        details[
            "duration_hours"
        ]
        == 2
    )

    assert (
        details[
            "self_care"
        ]
        is True
    )

    assert (
        details[
            "recovered_fatigue"
        ]
        is True
    )

    # Rest began at 10:00 and lasted two hours.
    assert (
        event["hour"]
        == 12
    )

# ============================================================
# FAMILY DUTY
# ============================================================


def make_family_duty_character():
    return {
        "name":
            "Test Character",

        "needs": {
            "hunger": 20,
            "fatigue": 20,
            "social": 40,
            "family_responsibility": 70,
            "training_drive": 20,
        },
    }


def make_family_duty_action():
    return {
        "action":
            "Help at the family shop",

        "action_type":
            "family_duty",

        "action_data": {
            "name":
                "Help at the family shop",

            "action_type":
                "family_duty",

            "tags": [
                "family",
                "community",
                "honor",
            ],

            "satisfies": {
                "family_responsibility": 35,
                "social": 10,
            },
        },
    }


def test_family_duty_self_directed_action_succeeds():
    character = (
        make_family_duty_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_family_duty_action(),
        )
    )

    assert (
        outcome["status"]
        == "success"
    )

    assert (
        outcome["action_type"]
        == "family_duty"
    )

    assert (
        outcome["duration_hours"]
        == 3
    )


def test_family_duty_applies_need_changes_and_time():
    character = (
        make_family_duty_character()
    )

    world = {
        "day": 1,
        "hour": 10,
    }

    resolve_self_directed_action(
        world,
        character,
        make_family_duty_action(),
    )

    # Family responsibility:
    # 70 - 35 + 1.2 = 36.2

    assert (
        character[
            "needs"
        ][
            "family_responsibility"
        ]
        == 36.2
    )

    # Social:
    # 40 - 10 + 0.9 = 30.9

    assert (
        character[
            "needs"
        ][
            "social"
        ]
        == 30.9
    )

    # Three hours of normal waking drift.

    assert (
        character[
            "needs"
        ][
            "hunger"
        ]
        == 26.0
    )

    assert (
        character[
            "needs"
        ][
            "fatigue"
        ]
        == 24.5
    )

    assert (
        character[
            "needs"
        ][
            "training_drive"
        ]
        == 21.5
    )

    assert (
        world["day"]
        == 1
    )

    assert (
        world["hour"]
        == 13
    )


def test_family_duty_creates_canonical_world_event():
    character = (
        make_family_duty_character()
    )

    world = {
        "day": 1,
        "hour": 10,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_family_duty_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    assert (
        event["event_type"]
        == "self_directed_outcome"
    )

    assert (
        event["description"]
        == (
            "Test Character spent 3 hours "
            "helping operate the family shop."
        )
    )

    assert (
        event["location"]
        == "Family Shop"
    )

    assert (
        event["participants"]
        == [
            "Test Character",
            "Ryuk's Mother",
            "Ryuk's Father",
        ]
    )

    details = event[
        "details"
    ]

    assert (
        details[
            "action_type"
        ]
        == "family_duty"
    )

    assert (
        details[
            "action_success"
        ]
        is True
    )

    assert (
        details[
            "duration_hours"
        ]
        == 3
    )

    assert (
        details[
            "helped_family"
        ]
        is True
    )

    assert (
        details[
            "supported_community"
        ]
        is True
    )

    assert (
        details[
            "fulfilled_responsibility"
        ]
        is True
    )

    assert (
        event["day"]
        == 1
    )

    assert (
        event["hour"]
        == 13
    )

# ============================================================
# TRAINING
# ============================================================


def make_training_character():
    return {
        "name":
            "Test Character",

        "needs": {
            "hunger": 20,
            "fatigue": 20,
            "social": 10,
            "family_responsibility": 15,
            "training_drive": 70,
        },
    }


def make_train_action():
    return {
        "action":
            "Practice knight techniques in secret",

        "action_type":
            "train",

        "action_data": {
            "name":
                "Practice knight techniques in secret",

            "action_type":
                "train",

            "tags": [
                "ambition",
                "discipline",
                "risk",
            ],

            "satisfies": {
                "training_drive": 40,
            },
        },
    }


def test_train_self_directed_action_succeeds():
    character = (
        make_training_character()
    )

    world = {
        "day": 1,
        "hour": 18,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_train_action(),
        )
    )

    assert (
        outcome["status"]
        == "success"
    )

    assert (
        outcome["action_type"]
        == "train"
    )

    assert (
        outcome["duration_hours"]
        == 2
    )


def test_training_applies_need_changes_and_time():
    character = (
        make_training_character()
    )

    world = {
        "day": 1,
        "hour": 18,
    }

    resolve_self_directed_action(
        world,
        character,
        make_train_action(),
    )

    # Training drive:
    #
    # 70
    # -40 from training
    # +1 from two waking hours
    # = 31

    assert (
        character[
            "needs"
        ][
            "training_drive"
        ]
        == 31.0
    )

    # Two hours of ordinary waking drift.

    assert (
        character[
            "needs"
        ][
            "hunger"
        ]
        == 24.0
    )

    assert (
        character[
            "needs"
        ][
            "fatigue"
        ]
        == 23.0
    )

    assert (
        character[
            "needs"
        ][
            "social"
        ]
        == 10.6
    )

    assert (
        character[
            "needs"
        ][
            "family_responsibility"
        ]
        == 15.8
    )

    assert (
        world["day"]
        == 1
    )

    assert (
        world["hour"]
        == 20
    )


def test_training_creates_canonical_world_event():
    character = (
        make_training_character()
    )

    world = {
        "day": 1,
        "hour": 18,
        "next_event_id": 1,
    }

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            make_train_action(),
        )
    )

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    assert (
        event["event_type"]
        == "self_directed_outcome"
    )

    assert (
        event["description"]
        == (
            "Test Character spent 2 hours secretly "
            "practicing knight martial techniques."
        )
    )

    assert (
        event["location"]
        == "Private Training Area"
    )

    assert (
        event["participants"]
        == [
            "Test Character",
        ]
    )

    details = event[
        "details"
    ]

    assert (
        details["action_type"]
        == "train"
    )

    assert (
        details["action_success"]
        is True
    )

    assert (
        details["duration_hours"]
        == 2
    )

    assert (
        details["trained_skill"]
        is True
    )

    assert (
        details["secret_training"]
        is True
    )

    assert (
        details["pursued_goal"]
        == "Become a knight"
    )

    assert (
        event["day"]
        == 1
    )

    assert (
        event["hour"]
        == 20
    )
