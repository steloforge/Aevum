import json
from pathlib import Path


def save_game_state(
    character,
    world,
    filepath,
):
    """
    Save character and world state to JSON.
    """

    path = Path(filepath)

    # Create the parent directory if needed.
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_data = {
        "character": character,
        "world": world,
    }

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            save_data,
            file,
            indent=4,
        )

    print(
        f"Game state saved to: {path}"
    )


def load_game_state(filepath):
    """
    Load character and world state from JSON.
    """

    path = Path(filepath)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        save_data = json.load(file)

    character = save_data["character"]
    world = save_data["world"]

    print(
        "Game state loaded successfully."
    )
    print(
        f"Character: {character['name']}"
    )
    print(
        f"World Day: {world['day']}"
    )
    print(
        f"Memories: "
        f"{len(character.get('memory', []))}"
    )

    return character, world


def autosave(
    character,
    world,
    filepath,
):
    """
    Convenience wrapper for saving committed simulation state.
    """

    save_game_state(
        character,
        world,
        filepath,
    )

    print("Autosave complete.")
