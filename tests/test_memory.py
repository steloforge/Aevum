from aevum.character.memory import (
    create_memory,
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
