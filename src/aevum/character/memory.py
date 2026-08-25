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

def recall_memories(character):
    """
    Display all autobiographical memories currently stored
    by a character.
    """

    print(
        f"\n--- {character['name']}'s Memories ---\n"
    )

    if len(character["memory"]) == 0:
        print("No memories found.")
        return

    for memory in character["memory"]:
        print(f"Memory #{memory['id']}")
        print(
            f"Remembered: "
            f"{memory['description']}"
        )
        print(
            f"Interpretation: "
            f"{memory['interpretation']}"
        )
        print(
            f"Importance: "
            f"{memory['importance']}"
        )
        print(
            f"Clarity: "
            f"{round(memory['clarity'], 2)}"
        )
        print(
            f"Confidence: "
            f"{memory['confidence']}"
        )
        print(
            f"Memory Layer: "
            f"{memory['memory_layer']}"
        )
        print(
            f"Recall Count: "
            f"{memory['recall_count']}"
        )
        print()


def search_memory(
    character,
    clues,
):
    """
    Search a character's autobiographical memories using clues.

    Deeper memory layers require more matching clues and receive
    an additional retrieval penalty.
    """

    matches = []

    layer_requirements = {
        "active": 1,
        "accessible": 1,
        "faded": 2,
        "buried": 3,
        "dormant": 4,
    }

    layer_penalties = {
        "active": 0,
        "accessible": 0.5,
        "faded": 1.0,
        "buried": 1.5,
        "dormant": 2.0,
    }

    for memory in character["memory"]:
        raw_score = 0
        matched_clues = []

        searchable_text = " ".join(
            [
                memory["description"],
                memory["interpretation"],
                " ".join(memory["people"]),
                memory["location"],
                " ".join(
                    memory["associations"]
                ),
            ]
        ).lower()

        for clue in clues:
            clue_lower = clue.lower()

            if clue_lower in searchable_text:
                raw_score += 1
                matched_clues.append(clue)

        required_score = (
            layer_requirements.get(
                memory["memory_layer"],
                1,
            )
        )

        layer_penalty = (
            layer_penalties.get(
                memory["memory_layer"],
                0,
            )
        )

        adjusted_score = (
            raw_score
            - layer_penalty
        )

        if raw_score >= required_score:
            matches.append(
                {
                    "memory": memory,
                    "raw_score": raw_score,
                    "adjusted_score":
                        adjusted_score,
                    "required_score":
                        required_score,
                    "matched_clues":
                        matched_clues,
                }
            )

    matches.sort(
        key=lambda x: x[
            "adjusted_score"
        ],
        reverse=True,
    )

    return matches    
    
    
    update_memory_layer(memory)

    character["memory"].append(memory)

    print(
        f"Memory #{memory['id']} created for "
        f"{character['name']} on Day {world['day']}."
    )

    return memory
