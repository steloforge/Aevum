"""
Relationship systems for Aevum characters.

Relationships track trust, respect, familiarity, affection,
and fear toward known individuals.
"""


def get_or_create_relationship(
    character,
    person_name,
):
    if person_name not in character["relationships"]:
        character["relationships"][person_name] = {
            "trust": 50,
            "respect": 50,
            "familiarity": 0,
            "affection": 0,
            "fear": 0,
        }

    return character["relationships"][person_name]


def update_relationship_from_memory(
    character,
    memory,
):
    emotion_causes = memory.get(
        "emotion_causes",
        {},
    )

    for person in memory["people"]:

        if person == character["name"]:
            continue

        relationship = get_or_create_relationship(
            character,
            person,
        )

        relationship["familiarity"] += 5

        emotions = memory["emotions"]

        happiness = emotions.get(
            "happiness",
            0,
        )

        fear = emotions.get(
            "fear",
            0,
        )

        anger = emotions.get(
            "anger",
            0,
        )

        guilt = emotions.get(
            "guilt",
            0,
        )

        sadness = emotions.get(
            "sadness",
            0,
        )

        if (
            emotion_causes.get("happiness")
            == person
        ):
            relationship["trust"] += (
                happiness * 0.05
            )

            relationship["affection"] += (
                happiness * 0.04
            )

            relationship["respect"] += (
                happiness * 0.03
            )

        if (
            emotion_causes.get("anger")
            == person
        ):
            relationship["trust"] -= (
                anger * 0.04
            )

            relationship["affection"] -= (
                anger * 0.03
            )

        if (
            emotion_causes.get("fear")
            == person
        ):
            relationship["fear"] += (
                fear * 0.05
            )

            relationship["trust"] -= (
                fear * 0.02
            )

        if (
            emotion_causes.get("guilt")
            == person
        ):
            relationship["affection"] += (
                guilt * 0.01
            )

        if (
            emotion_causes.get("sadness")
            == person
        ):
            relationship["affection"] += (
                sadness * 0.01
            )

        for key in [
            "trust",
            "respect",
            "familiarity",
            "affection",
            "fear",
        ]:
            relationship[key] = round(
                relationship[key],
                2,
            )

        print(
            f"Relationship updated: {person}"
        )


def interpret_relationship(
    character,
    person_name,
):
    if person_name not in character["relationships"]:
        return {
            "relationship": "Stranger",
            "trust_level": "Unknown",
            "respect_level": "Unknown",
            "emotional_tone": "Neutral",
        }

    relationship = character[
        "relationships"
    ][person_name]

    trust = relationship["trust"]
    respect = relationship["respect"]
    familiarity = relationship["familiarity"]
    affection = relationship["affection"]
    fear = relationship["fear"]

    if familiarity < 10:
        label = "Acquaintance"

    elif (
        affection >= 40
        and trust >= 70
    ):
        label = "Close Friend"

    elif (
        affection >= 15
        and trust >= 55
    ):
        label = "Friend"

    elif (
        trust <= 30
        or affection <= -20
    ):
        label = "Hostile Acquaintance"

    elif fear >= 40:
        label = "Feared Individual"

    elif trust >= 55:
        label = "Friendly Acquaintance"

    else:
        label = "Known Individual"

    if trust >= 80:
        trust_level = "Very High"

    elif trust >= 60:
        trust_level = "High"

    elif trust >= 40:
        trust_level = "Moderate"

    elif trust >= 20:
        trust_level = "Low"

    else:
        trust_level = "Very Low"

    if respect >= 80:
        respect_level = "Very High"

    elif respect >= 60:
        respect_level = "High"

    elif respect >= 40:
        respect_level = "Moderate"

    elif respect >= 20:
        respect_level = "Low"

    else:
        respect_level = "Very Low"

    emotional_score = (
        affection - fear
    )

    if emotional_score >= 25:
        emotional_tone = (
            "Strongly Positive"
        )

    elif emotional_score >= 5:
        emotional_tone = "Positive"

    elif emotional_score <= -25:
        emotional_tone = (
            "Strongly Negative"
        )

    elif emotional_score < 0:
        emotional_tone = "Negative"

    else:
        emotional_tone = "Neutral"

    return {
        "relationship":
            label,

        "trust_level":
            trust_level,

        "respect_level":
            respect_level,

        "emotional_tone":
            emotional_tone,
    }


def show_relationship(
    character,
    person_name,
):
    if person_name not in character["relationships"]:
        print(
            f"{character['name']} "
            f"does not know {person_name}."
        )
        return

    raw = character[
        "relationships"
    ][person_name]

    interpreted = interpret_relationship(
        character,
        person_name,
    )

    print(
        f"\n--- {character['name']} "
        f"-> {person_name} ---"
    )

    print(
        "Relationship: "
        f"{interpreted['relationship']}"
    )

    print(
        f"Trust: {raw['trust']} "
        f"({interpreted['trust_level']})"
    )

    print(
        f"Respect: {raw['respect']} "
        f"({interpreted['respect_level']})"
    )

    print(
        "Familiarity: "
        f"{raw['familiarity']}"
    )

    print(
        "Affection: "
        f"{raw['affection']}"
    )

    print(
        f"Fear: {raw['fear']}"
    )

    print(
        "Emotional tone: "
        f"{interpreted['emotional_tone']}"
    )
