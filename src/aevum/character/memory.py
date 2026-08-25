"""
Autobiographical memory systems for Aevum characters.

Memories retain information about experiences, emotional associations,
importance, confidence, clarity, recall history, and accessibility.
"""

from aevum.character.emotions import (
    process_emotional_response,
)

# ============================================================
# MEMORY LAYERS
# ============================================================


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


# ============================================================
# MEMORY CREATION
# ============================================================


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


# ============================================================
# Create Memory From Event
# ============================================================

def create_memory_from_event(
    character,
    world,
    perception,
    interpretation,
):
    associations = []

    associations.append(
        perception["location"].lower()
    )

    for person in perception["participants"]:
        if person != character["name"]:
            associations.append(
                person.lower()
            )

    details = perception["known_details"]

    for key, value in details.items():
        if isinstance(value, str):
            associations.append(
                value.lower()
            )

        elif (
            isinstance(value, bool)
            and value
        ):
            associations.append(
                key.replace(
                    "_",
                    " ",
                ).lower()
            )

    # Preserve order while removing duplicates.
    associations = list(
        dict.fromkeys(
            associations
        )
    )

    return create_memory(
        character=character,
        world=world,
        description=(
            perception[
                "perceived_description"
            ]
        ),
        interpretation=(
            interpretation[
                "interpretation"
            ]
        ),
        people=(
            perception[
                "participants"
            ]
        ),
        location=(
            perception[
                "location"
            ]
        ),
        associations=associations,
        emotions=(
            interpretation[
                "emotions"
            ]
        ),
        emotion_causes=(
            interpretation[
                "emotion_causes"
            ]
        ),
        importance=(
            interpretation[
                "importance"
            ]
        ),
        confidence=(
            interpretation[
                "confidence"
            ]
        ),
        clarity=95,
    )

# ============================================================
# MEMORY DISPLAY
# ============================================================


def recall_memories(character):
    print(
        f"\n--- {character['name']}'s Memories ---\n"
    )

    if len(character["memory"]) == 0:
        print("No memories found.")
        return

    for memory in character["memory"]:
        print(
            f"Memory #{memory['id']}"
        )

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

# ============================================================
# RECALL MEMORY
# ============================================================

def recall_memory(
    character,
    memory_id,
    emotional_strength=0.25,
    clarity_boost=8,
    world=None,
):
    for memory in character["memory"]:

        if memory["id"] == memory_id:
            memory["recall_count"] += 1

            memory["clarity"] += clarity_boost
            memory["clarity"] = min(
                memory["clarity"],
                100,
            )

            update_memory_layer(memory)

            for emotion, intensity in (
                memory["emotions"].items()
            ):
                if emotion in character[
                    "current_emotions"
                ]:
                    effect = (
                        intensity
                        * emotional_strength
                    )

                    character[
                        "current_emotions"
                    ][emotion] += effect

                    character[
                        "current_emotions"
                    ][emotion] = min(
                        character[
                            "current_emotions"
                        ][emotion],
                        100,
                    )

            if world is not None:
                memory["last_recalled_day"] = (
                    world["day"]
                )

            print(
                f"{character['name']} recalled: "
                f"{memory['description']}"
            )

            print(
                "Recall strength: "
                f"{round(emotional_strength * 100)}%"
            )

            print(
                "Memory layer: "
                f"{memory['memory_layer']}"
            )

            print("Current emotions:")

            for emotion, value in character[
                "current_emotions"
            ].items():
                print(
                    f"  {emotion}: "
                    f"{round(value, 2)}"
                )

            return memory

    print("Memory not found.")
    return None

# ============================================================
# LAYERED MEMORY SEARCH
# ============================================================


def search_memory(
    character,
    clues,
):
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
                " ".join(
                    memory["people"]
                ),
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
                matched_clues.append(
                    clue
                )

        required_score = (
            layer_requirements.get(
                memory["memory_layer"],
                1,
            )
        )

        # Faded and deeper memories become
        # progressively harder to retrieve.
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
                    "raw_score":
                        raw_score,
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


# ============================================================
# Recover Memory
# ============================================================

def recover_memory(
    character,
    world,
    clues,
    emotional_reactivation=0.20,
):
    results = search_memory(
        character,
        clues,
    )

    if not results:
        print("No memory recovered.")
        return None

    best_match = results[0]
    memory = best_match["memory"]

    print(
        f"{character['name']} recovered a memory:"
    )
    print(memory["description"])

    memory["recall_count"] += 1

    memory_age = max(
        0,
        world["day"]
        - memory["created_day"],
    )

    days_since_recall = max(
        0,
        world["day"]
        - memory["last_recalled_day"],
    )

    base_boost = 3

    importance_bonus = (
        memory["importance"]
        * 0.03
    )

    clue_bonus = (
        best_match["raw_score"]
        * 1.5
    )

    if days_since_recall > 90:
        resurfacing_bonus = 4

    elif days_since_recall > 30:
        resurfacing_bonus = 2

    else:
        resurfacing_bonus = 0

    age_penalty = min(
        memory_age * 0.01,
        3,
    )

    clarity_boost = (
        base_boost
        + importance_bonus
        + clue_bonus
        + resurfacing_bonus
        - age_penalty
    )

    clarity_boost = max(
        1,
        min(
            clarity_boost,
            15,
        ),
    )

    memory["clarity"] += clarity_boost

    memory["clarity"] = min(
        memory["clarity"],
        100,
    )

    memory["last_recalled_day"] = (
        world["day"]
    )

    update_memory_layer(memory)

    emotional_response = (
        process_emotional_response(
            character=character,
            emotions=memory.get(
                "emotions",
                {},
            ),
            response_strength=(
                emotional_reactivation
            ),
            use_regulation=True,
            suppress_opposing_emotions=True,
        )
    )

    print(
        "Matched clues:",
        best_match["matched_clues"],
    )

    print(
        "Raw match score:",
        best_match["raw_score"],
    )

    print(
        "Required score:",
        best_match["required_score"],
    )

    print(
        "Clarity boost:",
        round(
            clarity_boost,
            2,
        ),
    )

    print(
        "New clarity:",
        round(
            memory["clarity"],
            2,
        ),
    )

    print(
        "Memory layer:",
        memory["memory_layer"],
    )

    print(
        "Recall count:",
        memory["recall_count"],
    )

    print(
        "Regulation factor:",
        emotional_response[
            "regulation_factor"
        ],
    )

    print(
        "Negative emotional reactivation:",
        emotional_response[
            "negative_activation"
        ],
    )

    print(
        "Happiness reduction:",
        emotional_response[
            "happiness_reduction"
        ],
    )

    print("\nCurrent emotions:")

    for emotion, value in character[
        "current_emotions"
    ].items():
        print(
            f"  {emotion}: {value}"
        )

    return memory

# ============================================================
# Decay Memory
# ============================================================

def decay_memories(
    character,
    world,
    daily_decay=1,
):
    for memory in character["memory"]:

        if "last_decay_day" not in memory:
            memory["last_decay_day"] = (
                world["day"]
            )

        if "last_recalled_day" not in memory:
            memory["last_recalled_day"] = (
                memory["created_day"]
            )

        if "recall_count" not in memory:
            memory["recall_count"] = 0

        days_passed = (
            world["day"]
            - memory["last_decay_day"]
        )

        if days_passed <= 0:
            continue

        importance_protection = (
            memory["importance"] / 100
        ) * 0.70

        recall_strength = min(
            memory["recall_count"],
            20,
        ) / 20

        recall_protection = (
            recall_strength * 0.25
        )

        days_since_recall = (
            world["day"]
            - memory["last_recalled_day"]
        )

        if days_since_recall <= 7:
            recent_recall_protection = 0.15

        elif days_since_recall <= 30:
            recent_recall_protection = 0.08

        else:
            recent_recall_protection = 0

        emotional_intensity = sum(
            memory.get(
                "emotions",
                {},
            ).values()
        )

        emotional_strength = min(
            emotional_intensity / 400,
            1,
        )

        emotional_protection = (
            emotional_strength * 0.20
        )

        total_protection = (
            importance_protection
            + recall_protection
            + recent_recall_protection
            + emotional_protection
        )

        total_protection = min(
            total_protection,
            0.95,
        )

        decay_multiplier = (
            1 - total_protection
        )

        actual_decay = (
            daily_decay
            * days_passed
            * decay_multiplier
        )

        memory["clarity"] -= actual_decay

        memory["clarity"] = max(
            memory["clarity"],
            0,
        )

        update_memory_layer(memory)

        memory["last_decay_day"] = (
            world["day"]
        )
