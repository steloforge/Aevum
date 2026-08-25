from aevum.character.memory import (
    create_memory,
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
