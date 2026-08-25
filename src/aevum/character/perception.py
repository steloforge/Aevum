"""
Perception systems for Aevum characters.

Perception converts authoritative Axiom world events into the
information a character is currently aware of.
"""


def perceive_world_event(
    character,
    event,
):
    perception = {
        "event_id":
            event["event_id"],

        "perceived_description":
            event["description"],

        "location":
            event["location"],

        "participants":
            event["participants"],

        "known_details":
            event["details"].copy(),
    }

    print(
        f"\n{character['name']} "
        f"perceived the event."
    )

    print(
        perception[
            "perceived_description"
        ]
    )

    return perception
