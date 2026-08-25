from aevum.persistence import (
    load_game_state,
    save_game_state,
)


def test_save_and_load_round_trip(
    tmp_path,
):
    character = {
        "name": "Test Character",
        "memory": [
            {
                "id": 1,
                "description": "Test memory",
            }
        ],
    }

    world = {
        "day": 7,
        "hour": 14,
        "next_event_id": 4,
    }

    filepath = (
        tmp_path
        / "test_save.json"
    )

    save_game_state(
        character,
        world,
        filepath,
    )

    loaded_character, loaded_world = (
        load_game_state(
            filepath
        )
    )

    assert loaded_character == character
    assert loaded_world == world
