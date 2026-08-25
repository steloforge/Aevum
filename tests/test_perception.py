from aevum.character.perception import (
    perceive_world_event,
)


def test_perception_copies_world_event():
    character = {
        "name": "Test Character",
    }

    event = {
        "event_id": "event_10",
        "description":
            "A merchant helped a resident.",
        "location":
            "Market",
        "participants": [
            "Merchant",
            "Resident",
        ],
        "details": {
            "community_help_given":
                True,
        },
    }

    perception = (
        perceive_world_event(
            character,
            event,
        )
    )

    assert (
        perception["event_id"]
        == "event_10"
    )

    assert (
        perception[
            "perceived_description"
        ]
        == event["description"]
    )

    assert (
        perception[
            "location"
        ]
        == "Market"
    )

    assert (
        perception[
            "participants"
        ]
        == event["participants"]
    )


def test_perception_copies_details_instead_of_aliasing():
    character = {
        "name": "Test Character",
    }

    event = {
        "event_id":
            "event_1",

        "description":
            "Something happened.",

        "location":
            "Road",

        "participants":
            [],

        "details": {
            "action_success":
                True,
        },
    }

    perception = (
        perceive_world_event(
            character,
            event,
        )
    )

    perception[
        "known_details"
    ][
        "action_success"
    ] = False

    assert (
        event[
            "details"
        ][
            "action_success"
        ]
        is True
    )
