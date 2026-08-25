"""
Autobiographical memory systems for Aevum characters.

Memories retain information about experiences, emotional associations,
importance, confidence, clarity, recall history, and accessibility.
"""


def update_memory_layer(memory):
    clarity = memory["clarity"]

    if clarity >= 75:
        memory["memory_layer"] = "active"

    elif clarity >= 50:
        memory["memory_layer"] = "accessible"

    elif clarity >= 25:
        memory["memory_layer"] = "faded"

    elif clarity > 0:
        memory["memory_layer"] = "buried"

    else:
        memory["memory_layer"] = "dormant"


def create_memory(
    character,
    world,
    description,
    interpretation,
    people,
    location,
    associations,
    emotions,
    importance,
    confidence,
    clarity=100,
    emotion_causes=None,
):
    if emotion_causes is None:
        emotion_causes = {}

    memory = {
        "id": len(character["memory"]) + 1,
        "description": description,
        "interpretation": interpretation,
        "people": people,
        "location": location,
        "associations": associations,
        "emotions": emotions,
        "emotion_causes": emotion_causes,
        "importance": importance,
        "confidence": confidence,
        "clarity": clarity,
        "recall_count": 0,
        "memory_layer": "active",
        "created_day": world["day"],
        "last_recalled_day": world["day"],
        "last_decay_day": world["day"],
    }

    update_memory_layer(memory)

    character["memory"].append(memory)

    print(
        f"Memory #{memory['id']} created for "
        f"{character['name']} on Day {world['day']}."
    )

    return memory
