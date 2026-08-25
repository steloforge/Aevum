from aevum.axiom.resolution import (
    create_outcome_event,
    resolve_action_outcome,
)


def make_character():
    return {
        "name":
            "Test Character",

        "traits": {
            "compassion":
                80,

            "courage":
                80,

            "self_control":
                80,

            "aggression":
                40,
        },

        "skills": {
            "discipline":
                80,
        },

        "values": {
            "personal_honor":
                70,
        },
    }


def make_world():
    return {
        "laws": {
            "safe_zones": [
                "Market",
            ],

            "no_attacking_in_safe_zones":
                True,

            "no_killing_in_safe_zones":
                True,
        }
    }


def test_capable_character_successfully_helps():
    character = make_character()

    event = {
        "location":
            "Market",
    }

    action = {
        "action":
            "Help Injured Resident",

        "action_type":
            "help_person",

        "target":
            "Injured Resident",
    }

    result = resolve_action_outcome(
        world=make_world(),
        character=character,
        chosen_action=action,
        event=event,
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result[
            "capability_score"
        ]
        >= result[
            "difficulty"
        ] + 20
    )


def test_unknown_action_is_unresolved():
    character = make_character()

    result = resolve_action_outcome(
        world=make_world(),
        character=character,
        chosen_action={
            "action":
                "Dance dramatically",

            "action_type":
                "dance",

            "target":
                None,
        },
        event={
            "location":
                "Market",
        },
    )

    assert (
        result["status"]
        == "unresolved"
    )


def test_ignore_event_always_resolves_successfully():
    character = make_character()

    result = resolve_action_outcome(
        world=make_world(),
        character=character,
        chosen_action={
            "action":
                (
                    "Ignore the situation "
                    "and continue walking"
                ),

            "action_type":
                "ignore_event",

            "target":
                None,
        },
        event={
            "location":
                "Market",
        },
    )

    assert (
        result["status"]
        == "success"
    )

def test_successful_help_creates_canonical_outcome_event():
    world = {
        "day": 12,
        "hour": 10,
        "next_event_id": 1,
        "events": [],
    }

    character = make_character()

    original_event = {
        "event_id":
            "event_original",

        "location":
            "Market",
    }

    action = {
        "action":
            "Help Injured Resident",

        "action_type":
            "help_person",

        "target":
            "Injured Resident",
    }

    outcome = {
        "status":
            "success",

        "reason":
            "Help succeeded.",
    }

    event = create_outcome_event(
        world=world,
        character=character,
        original_event=original_event,
        chosen_action=action,
        outcome=outcome,
    )

    assert (
        event["event_type"]
        == "action_outcome"
    )

    assert (
        event["location"]
        == "Market"
    )

    assert (
        event["details"][
            "source_event_id"
        ]
        == "event_original"
    )

    assert (
        event["details"][
            "action_success"
        ]
        is True
    )

    assert (
        event["details"][
            "helped_person"
        ]
        is True
    )

    assert (
        event["details"][
            "protected_other"
        ]
        is True
    )

    assert (
        event["details"][
            "resolved_peacefully"
        ]
        is True
    )


def test_partial_help_records_partial_world_state():
    world = {
        "day": 12,
        "hour": 10,
        "next_event_id": 1,
        "events": [],
    }

    event = create_outcome_event(
        world=world,
        character=make_character(),
        original_event={
            "event_id":
                "event_original",

            "location":
                "Road",
        },
        chosen_action={
            "action":
                "Help Resident",

            "action_type":
                "help_person",

            "target":
                "Resident",
        },
        outcome={
            "status":
                "partial_success",

            "reason":
                "Some assistance was provided.",
        },
    )

    assert (
        event["details"][
            "partial_success"
        ]
        is True
    )

    assert (
        event["details"][
            "action_success"
        ]
        is False
    )

    assert (
        event["details"][
            "helped_person"
        ]
        is True
    )

    assert (
        event["details"][
            "protected_other"
        ]
        is False
    )


def test_outcome_event_contains_actor_and_target():
    world = {
        "day": 12,
        "hour": 10,
        "next_event_id": 1,
        "events": [],
    }

    event = create_outcome_event(
        world=world,
        character=make_character(),
        original_event={
            "event_id":
                "event_original",

            "location":
                "Market",
        },
        chosen_action={
            "action":
                "Ignore the situation",

            "action_type":
                "ignore_event",

            "target":
                None,
        },
        outcome={
            "status":
                "success",

            "reason":
                "Continued walking.",
        },
    )

    assert event[
        "participants"
    ] == [
        "Test Character"
    ]

    assert (
        event["details"][
            "ignored_event"
        ]
        is True
    )
