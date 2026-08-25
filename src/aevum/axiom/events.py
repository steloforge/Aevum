"""
Aevum - Axiom World Event System

Axiom is the authoritative layer of Aevum.

Characters may perceive, interpret, remember, believe, and attempt actions,
but Axiom is responsible for recording what actually occurs in canonical
world state.
"""


def create_world_event(
    world,
    event_type,
    description,
    location,
    participants,
    details=None,
):
    """
    Create a canonical event in the Aevum world.

    Parameters
    ----------
    world : dict
        Current authoritative world state.

    event_type : str
        Structured category for the event.

    description : str
        Human-readable description of what happened.

    location : str
        Location where the event occurred.

    participants : list[str]
        Characters or entities involved.

    details : dict | None
        Structured facts about the event that other systems
        can reason from.

    Returns
    -------
    dict
        Newly created canonical world event.
    """

    if details is None:
        details = {}

    # Ensure an event counter exists.
    if "next_event_id" not in world:
        world["next_event_id"] = 1

    event_id = (
        f"event_{world['next_event_id']}"
    )

    world["next_event_id"] += 1

    event = {
        "event_id": event_id,
        "day": world["day"],
        "hour": world["hour"],
        "event_type": event_type,
        "description": description,
        "location": location,
        "participants": participants,
        "details": details,
    }

    print("\n--- WORLD EVENT CREATED ---")
    print(f"ID: {event['event_id']}")
    print(f"Type: {event['event_type']}")
    print(
        f"Description: "
        f"{event['description']}"
    )
    print(
        f"Location: "
        f"{event['location']}"
    )
    print(
        f"Participants: "
        f"{event['participants']}"
    )

    return event
