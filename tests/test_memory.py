from aevum.character.memory import (
    create_memory,
    decay_memories,
    recall_memory,
    recover_memory,
    search_memory,
    update_memory_layer,
)


def test_memory_layer_thresholds():
    cases = [
        (100, "active"),
        (75, "active"),
        (74.9, "accessible"),
        (50, "accessible"),
        (49.9, "faded"),
        (25, "faded"),
        (24.9, "buried"),
        (1, "buried"),
        (0, "dormant"),
    ]

    for clarity, expected_layer in cases:
        memory = {
            "clarity": clarity,
        }

        update_memory_layer(memory)

        assert (
            memory["memory_layer"]
            == expected_layer
        )


def test_create_memory():
    character = {
        "name": "Test Character",
        "memory": [],
    }

    world = {
        "day": 12,
        "hour": 8,
    }

    memory = create_memory(
        character=character,
        world=world,
        description="I visited the market.",
        interpretation="It was an ordinary trip.",
        people=[
            "Test Character",
            "Merchant",
        ],
        location="Market",
        associations=[
            "market",
            "merchant",
        ],
        emotions={
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
        },
        importance=15,
        confidence=90,
        clarity=60,
    )

    assert memory["id"] == 1
    assert memory["created_day"] == 12
    assert memory["last_recalled_day"] == 12
    assert memory["last_decay_day"] == 12

    assert (
        memory["memory_layer"]
        == "accessible"
    )

    assert memory["recall_count"] == 0

    assert len(character["memory"]) == 1

    assert (
        character["memory"][0]
        is memory
    )

def test_search_active_memory_with_one_clue():
    character = {
        "memory": [
            {
                "id": 1,
                "description":
                    "I bought bread from a merchant.",
                "interpretation":
                    "It was an ordinary market trip.",
                "people": [
                    "Test Character",
                    "Merchant",
                ],
                "location": "Market",
                "associations": [
                    "bread",
                    "merchant",
                    "food",
                ],
                "memory_layer": "active",
            }
        ]
    }

    results = search_memory(
        character,
        ["bread"],
    )

    assert len(results) == 1

    assert (
        results[0]["memory"]["id"]
        == 1
    )

    assert (
        results[0]["raw_score"]
        == 1
    )


def test_buried_memory_requires_three_clues():
    character = {
        "memory": [
            {
                "id": 1,
                "description":
                    "My sister was attacked by a monster.",
                "interpretation":
                    "I failed to protect her.",
                "people": [
                    "Test Character",
                    "Sister",
                ],
                "location":
                    "Outside the kingdom",
                "associations": [
                    "monster",
                    "sister",
                    "protection",
                    "failure",
                ],
                "memory_layer": "buried",
            }
        ]
    }

    weak_results = search_memory(
        character,
        ["monster"],
    )

    assert weak_results == []

    strong_results = search_memory(
        character,
        [
            "monster",
            "sister",
            "protection",
        ],
    )

    assert len(strong_results) == 1

    assert (
        strong_results[0][
            "required_score"
        ]
        == 3
    )


def test_search_ranks_stronger_match_first():
    character = {
        "memory": [
            {
                "id": 1,
                "description":
                    "I visited the market.",
                "interpretation":
                    "It was ordinary.",
                "people": [],
                "location": "Market",
                "associations": [
                    "market",
                ],
                "memory_layer":
                    "active",
            },
            {
                "id": 2,
                "description":
                    "I bought bread from a merchant at the market.",
                "interpretation":
                    "I needed food.",
                "people": [
                    "Merchant",
                ],
                "location": "Market",
                "associations": [
                    "bread",
                    "merchant",
                    "market",
                ],
                "memory_layer":
                    "active",
            },
        ]
    }

    results = search_memory(
        character,
        [
            "market",
            "bread",
            "merchant",
        ],
    )

    assert (
        results[0]["memory"]["id"]
        == 2
    )

def make_emotional_character():
    return {
        "name": "Test Character",
        "traits": {
            "self_control": 50,
        },
        "memory": [],
        "current_emotions": {
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
            "stress": 0,
            "happiness": 50,
        },
    }


def test_direct_recall_reinforces_memory():
    character = make_emotional_character()

    world = {
        "day": 20,
        "hour": 12,
    }

    memory = create_memory(
        character=character,
        world={
            "day": 10,
            "hour": 8,
        },
        description="I encountered a wolf.",
        interpretation="The encounter frightened me.",
        people=["Test Character"],
        location="Forest",
        associations=[
            "wolf",
            "forest",
            "danger",
        ],
        emotions={
            "fear": 40,
        },
        importance=50,
        confidence=90,
        clarity=60,
    )

    recalled = recall_memory(
        character=character,
        memory_id=memory["id"],
        emotional_strength=0.25,
        clarity_boost=8,
        world=world,
    )

    assert recalled is memory

    assert memory["recall_count"] == 1

    assert memory["clarity"] == 68

    assert (
        memory["last_recalled_day"]
        == 20
    )

    assert (
        memory["memory_layer"]
        == "accessible"
    )

    # Direct recall currently re-experiences
    # 25% of the stored fear:
    #
    # 40 * 0.25 = 10
    assert (
        character[
            "current_emotions"
        ]["fear"]
        == 10
    )


def test_direct_recall_can_change_memory_layer():
    character = make_emotional_character()

    memory = create_memory(
        character=character,
        world={
            "day": 1,
            "hour": 8,
        },
        description="I remember the old bridge.",
        interpretation="It mattered to me.",
        people=[],
        location="Old Bridge",
        associations=[
            "bridge",
        ],
        emotions={},
        importance=40,
        confidence=90,
        clarity=70,
    )

    assert (
        memory["memory_layer"]
        == "accessible"
    )

    recall_memory(
        character=character,
        memory_id=memory["id"],
        clarity_boost=8,
    )

    assert memory["clarity"] == 78

    assert (
        memory["memory_layer"]
        == "active"
    )


def test_recover_memory_reinforces_best_match():
    character = make_emotional_character()

    memory = create_memory(
        character=character,
        world={
            "day": 1,
            "hour": 8,
        },
        description=(
            "My sister and I encountered "
            "a monster in the forest."
        ),
        interpretation=(
            "I needed to protect my sister."
        ),
        people=[
            "Test Character",
            "Sister",
        ],
        location="Forest",
        associations=[
            "monster",
            "sister",
            "protection",
            "forest",
        ],
        emotions={
            "fear": 40,
        },
        importance=80,
        confidence=90,
        clarity=60,
    )

    world = {
        "day": 40,
        "hour": 12,
    }

    old_clarity = memory["clarity"]

    recovered = recover_memory(
        character=character,
        world=world,
        clues=[
            "monster",
            "sister",
            "protection",
        ],
    )

    assert recovered is memory

    assert memory["recall_count"] == 1

    assert (
        memory["clarity"]
        > old_clarity
    )

    assert (
        memory["last_recalled_day"]
        == 40
    )

    # recover_memory routes remembered emotion
    # through process_emotional_response().
    assert (
        character[
            "current_emotions"
        ]["fear"]
        > 0
    )

    assert (
        character[
            "current_emotions"
        ]["happiness"]
        < 50
    )


def test_failed_recovery_does_not_change_memory():
    character = make_emotional_character()

    memory = create_memory(
        character=character,
        world={
            "day": 1,
            "hour": 8,
        },
        description="I visited the harbor.",
        interpretation="It was peaceful.",
        people=[],
        location="Harbor",
        associations=[
            "water",
            "ships",
        ],
        emotions={},
        importance=20,
        confidence=90,
        clarity=80,
    )

    before = memory.copy()

    result = recover_memory(
        character=character,
        world={
            "day": 20,
            "hour": 12,
        },
        clues=[
            "dragon",
        ],
    )

    assert result is None

    assert (
        memory["recall_count"]
        == before["recall_count"]
    )

    assert (
        memory["clarity"]
        == before["clarity"]
    )

    assert (
        memory["last_recalled_day"]
        == before[
            "last_recalled_day"
        ]
    )


def test_memory_decay_reduces_clarity():
    character = make_emotional_character()

    memory = create_memory(
        character=character,
        world={
            "day": 1,
            "hour": 8,
        },
        description="I saw a tree.",
        interpretation="It was ordinary.",
        people=[],
        location="Field",
        associations=[
            "tree",
        ],
        emotions={},
        importance=0,
        confidence=90,
        clarity=80,
    )

    # Remove recent-recall protection so this
    # test isolates ordinary decay more clearly.
    memory["last_recalled_day"] = 1

    decay_memories(
        character=character,
        world={
            "day": 40,
            "hour": 8,
        },
        daily_decay=1,
    )

    assert memory["clarity"] < 80

    assert (
        memory["last_decay_day"]
        == 40
    )


def test_important_memory_decays_slower():
    ordinary_character = (
        make_emotional_character()
    )

    important_character = (
        make_emotional_character()
    )

    ordinary = create_memory(
        character=ordinary_character,
        world={
            "day": 1,
            "hour": 8,
        },
        description="An ordinary afternoon.",
        interpretation="Nothing unusual happened.",
        people=[],
        location="Home",
        associations=[
            "afternoon",
        ],
        emotions={},
        importance=0,
        confidence=90,
        clarity=100,
    )

    important = create_memory(
        character=important_character,
        world={
            "day": 1,
            "hour": 8,
        },
        description="A defining moment.",
        interpretation="This changed my life.",
        people=[],
        location="Home",
        associations=[
            "important",
        ],
        emotions={},
        importance=100,
        confidence=90,
        clarity=100,
    )

    ordinary["last_recalled_day"] = 1
    important["last_recalled_day"] = 1

    future_world = {
        "day": 101,
        "hour": 8,
    }

    decay_memories(
        ordinary_character,
        future_world,
    )

    decay_memories(
        important_character,
        future_world,
    )

    assert (
        important["clarity"]
        > ordinary["clarity"]
    )


def test_decay_can_move_memory_to_deeper_layer():
    character = make_emotional_character()

    memory = create_memory(
        character=character,
        world={
            "day": 1,
            "hour": 8,
        },
        description="A mundane memory.",
        interpretation="It was unimportant.",
        people=[],
        location="Road",
        associations=[
            "road",
        ],
        emotions={},
        importance=0,
        confidence=80,
        clarity=52,
    )

    assert (
        memory["memory_layer"]
        == "accessible"
    )

    memory["last_recalled_day"] = 1

    decay_memories(
        character=character,
        world={
            "day": 40,
            "hour": 8,
        },
        daily_decay=1,
    )

    assert memory["clarity"] < 50

    assert (
        memory["memory_layer"]
        == "faded"
    )
