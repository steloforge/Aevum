from aevum.character.relationships import (
    get_or_create_relationship,
    interpret_relationship,
    update_relationship_from_memory,
)


def make_character():
    return {
        "name": "Test Character",
        "relationships": {},
    }


def test_new_relationship_starts_neutral():
    character = make_character()

    relationship = (
        get_or_create_relationship(
            character,
            "Merchant",
        )
    )

    assert relationship == {
        "trust": 50,
        "respect": 50,
        "familiarity": 0,
        "affection": 0,
        "fear": 0,
    }


def test_existing_relationship_is_reused():
    character = make_character()

    first = get_or_create_relationship(
        character,
        "Merchant",
    )

    first["trust"] = 70

    second = get_or_create_relationship(
        character,
        "Merchant",
    )

    assert second is first
    assert second["trust"] == 70


def test_memory_increases_familiarity():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
            "Merchant",
        ],

        "emotions": {},

        "emotion_causes": {},
    }

    update_relationship_from_memory(
        character,
        memory,
    )

    relationship = character[
        "relationships"
    ]["Merchant"]

    assert (
        relationship["familiarity"]
        == 5
    )


def test_happiness_caused_by_person_improves_relationship():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
            "Friend",
        ],

        "emotions": {
            "happiness": 50,
        },

        "emotion_causes": {
            "happiness": "Friend",
        },
    }

    update_relationship_from_memory(
        character,
        memory,
    )

    relationship = character[
        "relationships"
    ]["Friend"]

    assert relationship["trust"] == 52.5
    assert relationship["affection"] == 2.0
    assert relationship["respect"] == 51.5
    assert relationship["familiarity"] == 5


def test_anger_caused_by_person_reduces_relationship():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
            "Rival",
        ],

        "emotions": {
            "anger": 50,
        },

        "emotion_causes": {
            "anger": "Rival",
        },
    }

    update_relationship_from_memory(
        character,
        memory,
    )

    relationship = character[
        "relationships"
    ]["Rival"]

    assert relationship["trust"] == 48.0
    assert relationship["affection"] == -1.5


def test_fear_caused_by_person_builds_fear_and_reduces_trust():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
            "Monster",
        ],

        "emotions": {
            "fear": 80,
        },

        "emotion_causes": {
            "fear": "Monster",
        },
    }

    update_relationship_from_memory(
        character,
        memory,
    )

    relationship = character[
        "relationships"
    ]["Monster"]

    assert relationship["fear"] == 4.0
    assert relationship["trust"] == 48.4


def test_character_does_not_create_relationship_with_self():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
        ],

        "emotions": {
            "happiness": 50,
        },

        "emotion_causes": {
            "happiness":
                "Test Character",
        },
    }

    update_relationship_from_memory(
        character,
        memory,
    )

    assert (
        "Test Character"
        not in character[
            "relationships"
        ]
    )


def test_unknown_person_is_interpreted_as_stranger():
    character = make_character()

    result = interpret_relationship(
        character,
        "Unknown Person",
    )

    assert (
        result["relationship"]
        == "Stranger"
    )

    assert (
        result["trust_level"]
        == "Unknown"
    )


def test_close_friend_interpretation():
    character = make_character()

    character["relationships"][
        "Friend"
    ] = {
        "trust": 80,
        "respect": 70,
        "familiarity": 30,
        "affection": 45,
        "fear": 0,
    }

    result = interpret_relationship(
        character,
        "Friend",
    )

    assert (
        result["relationship"]
        == "Close Friend"
    )

    assert (
        result["trust_level"]
        == "Very High"
    )

    assert (
        result["respect_level"]
        == "High"
    )

    assert (
        result["emotional_tone"]
        == "Strongly Positive"
    )


def test_hostile_relationship_interpretation():
    character = make_character()

    character["relationships"][
        "Rival"
    ] = {
        "trust": 20,
        "respect": 30,
        "familiarity": 25,
        "affection": -25,
        "fear": 5,
    }

    result = interpret_relationship(
        character,
        "Rival",
    )

    assert (
        result["relationship"]
        == "Hostile Acquaintance"
    )

    assert (
        result["trust_level"]
        == "Low"
    )

    assert (
        result["emotional_tone"]
        == "Strongly Negative"
    )

def test_relationship_effects_apply_only_once():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
            "Friend",
        ],

        "emotions": {
            "happiness": 50,
        },

        "emotion_causes": {
            "happiness":
                "Friend",
        },
    }

    first_updates = (
        update_relationship_from_memory(
            character,
            memory,
        )
    )

    relationship = character[
        "relationships"
    ]["Friend"]

    first_state = (
        relationship.copy()
    )

    second_updates = (
        update_relationship_from_memory(
            character,
            memory,
        )
    )

    assert (
        first_updates
        == ["Friend"]
    )

    assert second_updates == []

    assert (
        character[
            "relationships"
        ]["Friend"]
        == first_state
    )

    assert (
        memory[
            "relationship_effects_applied"
        ]
        is True
    )


def test_abstract_emotion_cause_does_not_become_relationship():
    character = make_character()

    memory = {
        "people": [
            "Test Character",
            "Resident",
        ],

        "emotions": {
            "happiness": 50,
        },

        "emotion_causes": {
            "happiness":
                "Community Support",
        },
    }

    update_relationship_from_memory(
        character,
        memory,
    )

    assert (
        "Community Support"
        not in character[
            "relationships"
        ]
    )

    resident = character[
        "relationships"
    ]["Resident"]

    # Resident participated in the event,
    # so familiarity increases.
    assert (
        resident["familiarity"]
        == 5
    )

    # But the abstract cause is not attributed
    # to Resident personally.
    assert resident["trust"] == 50
    assert resident["affection"] == 0
