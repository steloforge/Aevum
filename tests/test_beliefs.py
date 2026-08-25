from aevum.character.beliefs import (
    apply_belief_judgment,
    get_or_create_belief,
    infer_belief_relevance,
    judge_belief_evidence,
)


def make_character():
    character = {
        "name": "Test Character",
        "beliefs": {},
    }

    belief = get_or_create_belief(
        character,
        "community_support",
        "People in my community look out for one another.",
    )

    belief["concepts"] = [
        "residents",
        "help",
        "community",
    ]

    return character


def make_perception(
    details=None,
):
    if details is None:
        details = {}

    return {
        "perceived_description":
            (
                "Several residents helped "
                "an injured neighbor."
            ),

        "location":
            "Community Market",

        "participants": [
            "Resident",
            "Neighbor",
        ],

        "known_details":
            details,
    }


def test_new_belief_starts_neutral():
    character = {
        "name": "Test Character",
    }

    belief = get_or_create_belief(
        character,
        "community_support",
        "People help one another.",
    )

    assert belief[
        "confidence"
    ] == 50

    assert belief[
        "evidence_for"
    ] == []

    assert belief[
        "evidence_against"
    ] == []

    assert belief[
        "times_reconsidered"
    ] == 0


def test_get_existing_belief_does_not_replace_it():
    character = {
        "name": "Test Character",
    }

    first = get_or_create_belief(
        character,
        "community_support",
        "Original statement.",
    )

    first["confidence"] = 75

    second = get_or_create_belief(
        character,
        "community_support",
        "Different statement.",
    )

    assert second is first
    assert second["confidence"] == 75
    assert (
        second["statement"]
        == "Original statement."
    )


def test_relevant_belief_is_detected():
    character = make_character()

    results = infer_belief_relevance(
        character,
        make_perception(),
    )

    assert len(results) == 1

    assert (
        results[0]["belief_key"]
        == "community_support"
    )

    assert (
        results[0]["match_score"]
        > 0
    )


def test_unrelated_event_does_not_match_belief():
    character = make_character()

    perception = {
        "perceived_description":
            "A storm formed over the mountains.",

        "location":
            "Mountain Pass",

        "participants": [],

        "known_details": {},
    }

    results = infer_belief_relevance(
        character,
        perception,
    )

    assert results == []


def test_help_given_supports_community_belief():
    character = make_character()

    perception = make_perception(
        {
            "community_help_given":
                True,
        }
    )

    match = infer_belief_relevance(
        character,
        perception,
    )[0]

    judgment = judge_belief_evidence(
        character,
        perception,
        match,
    )

    assert (
        judgment["direction"]
        == "supports"
    )

    assert (
        judgment["strength"]
        == 70
    )


def test_help_refused_contradicts_community_belief():
    character = make_character()

    perception = make_perception(
        {
            "community_help_refused":
                True,
        }
    )

    match = infer_belief_relevance(
        character,
        perception,
    )[0]

    judgment = judge_belief_evidence(
        character,
        perception,
        match,
    )

    assert (
        judgment["direction"]
        == "contradicts"
    )

    assert (
        judgment["strength"]
        == 70
    )


def test_supporting_evidence_increases_confidence():
    character = make_character()

    perception = make_perception(
        {
            "community_help_given":
                True,
        }
    )

    match = infer_belief_relevance(
        character,
        perception,
    )[0]

    judgment = judge_belief_evidence(
        character,
        perception,
        match,
    )

    event = {
        "event_id": "event_1",
        "day": 5,
    }

    belief = apply_belief_judgment(
        character,
        event,
        perception,
        judgment,
    )

    # Strength 70 * 0.15 = 10.5
    assert (
        belief["confidence"]
        == 60.5
    )

    assert len(
        belief["evidence_for"]
    ) == 1

    assert (
        belief["times_reconsidered"]
        == 1
    )


def test_contradicting_evidence_reduces_confidence():
    character = make_character()

    perception = make_perception(
        {
            "community_help_refused":
                True,
        }
    )

    match = infer_belief_relevance(
        character,
        perception,
    )[0]

    judgment = judge_belief_evidence(
        character,
        perception,
        match,
    )

    event = {
        "event_id": "event_2",
        "day": 5,
    }

    belief = apply_belief_judgment(
        character,
        event,
        perception,
        judgment,
    )

    assert (
        belief["confidence"]
        == 39.5
    )

    assert len(
        belief["evidence_against"]
    ) == 1

    assert (
        belief["times_reconsidered"]
        == 1
    )


def test_neutral_judgment_does_not_change_belief():
    character = make_character()

    belief = character[
        "beliefs"
    ]["community_support"]

    perception = make_perception()

    judgment = {
        "belief_key":
            "community_support",

        "direction":
            "neutral",

        "strength":
            0,

        "reason":
            "No clear evidence.",
    }

    event = {
        "event_id":
            "event_3",

        "day":
            5,
    }

    result = apply_belief_judgment(
        character,
        event,
        perception,
        judgment,
    )

    assert result is None
    assert belief["confidence"] == 50
    assert belief["times_reconsidered"] == 0
