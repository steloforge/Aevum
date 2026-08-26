from aevum.character.beliefs import (
    get_or_create_belief,
)

from aevum.character.processing import (
    apply_sleep_cognitive_effects,
    consolidate_recent_memories_during_sleep,
    process_outcome_for_character,
    recover_emotions_during_sleep,
)

from aevum.axiom.resolution import (
    create_self_directed_outcome_event,
    resolve_self_directed_action,
)

def make_character():
    character = {
        "name": "Test Character",

        "needs": {
            "hunger": 60,
            "fatigue": 20,
            "social": 10,
            "family_responsibility": 15,
            "training_drive": 25,
        },
        
        "traits": {
            "self_control": 50,
            "rule_obedience": 70,
            "patience": 70,
        },

        "values": {
            "peace": 80,
            "family": 80,
        },

        "memory": [],

        "relationships": {},

        "current_emotions": {
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
            "stress": 0,
            "happiness": 50,
        },

        "self_concept": {
            "protector": 0,
            "peacekeeper": 0,
            "family_guardian": 0,
            "rule_follower": 0,
            "fighter": 0,
        },

        "beliefs": {},
    }

    belief = get_or_create_belief(
        character,
        "community_support",
        (
            "People in my community "
            "look out for one another."
        ),
    )

    belief["concepts"] = [
        "residents",
        "help",
        "community",
    ]

    return character


def test_world_event_flows_through_character_cognition():
    character = make_character()

    world = {
        "day": 12,
        "hour": 10,
    }

    event = {
        "event_id": "event_1",

        "day": 12,

        "event_type":
            "action_outcome",

        "description":
            (
                "Several residents helped "
                "an injured neighbor."
            ),

        "location":
            "Community Market",

        "participants": [
            "Test Character",
            "Resident",
            "Neighbor",
        ],

        "details": {
            "community_help_given":
                True,

            "resolved_peacefully":
                True,
        },
    }

    result = (
        process_outcome_for_character(
            character=character,
            world=world,
            outcome_event=event,
            autosave_after=False,
        )
    )

    # --------------------------------------------------------
    # PERCEPTION
    # --------------------------------------------------------

    assert (
        result[
            "perception"
        ]["event_id"]
        == "event_1"
    )

    # --------------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------------

    assert (
        result[
            "interpretation"
        ]["emotions"]["happiness"]
        > 0
    )

    # --------------------------------------------------------
    # LIVE EMOTIONAL STATE
    # --------------------------------------------------------

    assert (
        character[
            "current_emotions"
        ]["happiness"]
        > 50
    )

    # --------------------------------------------------------
    # MEMORY
    # --------------------------------------------------------

    assert len(
        character["memory"]
    ) == 1

    memory = character[
        "memory"
    ][0]

    assert (
        memory["description"]
        == event["description"]
    )

    assert (
        memory["clarity"]
        == 95
    )

    assert (
        "community market"
        in memory[
            "associations"
        ]
    )

    assert (
        "community help given"
        in memory[
            "associations"
        ]
    )

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    assert (
        "Resident"
        in character[
            "relationships"
        ]
    )

    assert (
        "Neighbor"
        in character[
            "relationships"
        ]
    )

    assert (
        character[
            "relationships"
        ][
            "Resident"
        ][
            "familiarity"
        ]
        == 5
    )

    assert (
        character[
            "relationships"
        ][
            "Neighbor"
        ][
            "familiarity"
        ]
        == 5
    )

    assert (
        "Community Support"
        not in character[
            "relationships"
        ]
    )

    assert set(
        result[
            "relationship_updates"
        ]
    ) == {
        "Resident",
        "Neighbor",
    }
    
    # --------------------------------------------------------
    # IDENTITY
    # --------------------------------------------------------

    assert (
        character[
            "self_concept"
        ]["peacekeeper"]
        == 5
    )

    # --------------------------------------------------------
    # BELIEF
    # --------------------------------------------------------

    belief = character[
        "beliefs"
    ]["community_support"]

    assert (
        belief["confidence"]
        == 60.5
    )

    assert len(
        belief["evidence_for"]
    ) == 1

    assert (
        belief[
            "times_reconsidered"
        ]
        == 1
    )

def test_autonomous_eating_becomes_lived_memory():
    character = make_character()

    world = {
        "day": 12,
        "hour": 10,
        "next_event_id": 1,
    }

    chosen_action = {
        "action":
            "Eat a meal",

        "action_type":
            "eat",

        "action_data": {
            "name":
                "Eat a meal",

            "action_type":
                "eat",

            "tags": [
                "self_care",
            ],

            "satisfies": {
                "hunger": 45,
            },
        },
    }

    # ========================================================
    # 1. CHARACTER INTENTION -> AXIOM RESOLUTION
    # ========================================================

    outcome = (
        resolve_self_directed_action(
            world,
            character,
            chosen_action,
        )
    )

    assert (
        outcome["status"]
        == "success"
    )

    # Hunger:
    #
    # 60
    # -45 from eating
    # +2 from one hour passing
    # = 17

    assert (
        character[
            "needs"
        ][
            "hunger"
        ]
        == 17.0
    )

    assert (
        world["hour"]
        == 11
    )

    # ========================================================
    # 2. AXIOM RESOLUTION -> CANONICAL EVENT
    # ========================================================

    event = (
        create_self_directed_outcome_event(
            world,
            character,
            outcome,
        )
    )

    assert (
        event["event_type"]
        == "self_directed_outcome"
    )

    assert (
        event["details"][
            "action_success"
        ]
        is True
    )

    assert (
        event["details"][
            "self_care"
        ]
        is True
    )

    # ========================================================
    # 3. CANONICAL EVENT -> CHARACTER COGNITION
    # ========================================================

    result = (
        process_outcome_for_character(
            character=character,
            world=world,
            outcome_event=event,
            autosave_after=False,
        )
    )

    # --------------------------------------------------------
    # PERCEPTION
    # --------------------------------------------------------

    assert (
        result[
            "perception"
        ][
            "event_id"
        ]
        == event[
            "event_id"
        ]
    )

    # --------------------------------------------------------
    # MEMORY
    # --------------------------------------------------------

    assert len(
        character["memory"]
    ) == 1

    memory = (
        result["memory"]
    )

    assert (
        memory["description"]
        == (
            "Test Character "
            "took time to eat a meal."
        )
    )

    assert (
        memory["location"]
        == "Family Shop"
    )

    assert (
        memory["clarity"]
        == 95
    )

    # --------------------------------------------------------
    # SELF-ACTION SHOULD NOT CREATE A RELATIONSHIP WITH SELF
    # --------------------------------------------------------

    assert (
        character[
            "relationships"
        ]
        == {}
    )

    assert (
        result[
            "relationship_updates"
        ]
        == []
    )

# ============================================================
# SLEEP COGNITION
# ============================================================


def test_sleep_recovers_persistent_emotions_toward_baseline():
    character = {
        "current_emotions": {
            "fear": 80,
            "anger": 60,
            "guilt": 40,
            "sadness": 50,
            "stress": 70,
            "happiness": 10,
        },
    }

    recover_emotions_during_sleep(
        character,
        hours_slept=8,
    )

    # Negative emotions should move toward zero.

    assert (
        character[
            "current_emotions"
        ][
            "fear"
        ]
        < 80
    )

    assert (
        character[
            "current_emotions"
        ][
            "anger"
        ]
        < 60
    )

    assert (
        character[
            "current_emotions"
        ][
            "stress"
        ]
        < 70
    )

    # Happiness should recover toward its
    # baseline of 50.

    assert (
        character[
            "current_emotions"
        ][
            "happiness"
        ]
        > 10
    )

    assert (
        character[
            "current_emotions"
        ][
            "happiness"
        ]
        < 50
    )


def test_sleep_consolidates_recent_important_memory():
    character = {
        "memory": [
            {
                "id":
                    1,

                "created_day":
                    1,

                "clarity":
                    80,

                "importance":
                    50,

                "emotions": {
                    "fear": 20,
                    "anger": 10,
                },
            },
        ],
    }

    world = {
        "day": 2,
        "hour": 6,
    }

    memories_processed = (
        consolidate_recent_memories_during_sleep(
            character,
            world,
        )
    )

    memory = character[
        "memory"
    ][0]

    # Importance:
    # 50 * .03 = 1.5
    #
    # Emotional intensity:
    # 30 * .01 = .3
    #
    # Total consolidation:
    # +1.8
    #
    # 80 + 1.8 = 81.8

    assert (
        memory["clarity"]
        == 81.8
    )

    assert (
        memories_processed
        == 1
    )


def test_sleep_cognitive_effects_require_canonical_sleep_event():
    character = {
        "current_emotions": {
            "fear": 80,
            "happiness": 10,
        },

        "memory": [
            {
                "id":
                    1,

                "created_day":
                    1,

                "clarity":
                    80,

                "importance":
                    50,

                "emotions": {
                    "fear": 20,
                },
            },
        ],
    }

    world = {
        "day": 2,
        "hour": 6,
    }

    sleep_event = {
        "event_id":
            "event_1",

        "event_type":
            "self_directed_outcome",

        "details": {
            "action_type":
                "sleep",

            "action_success":
                True,

            "duration_hours":
                8,

            "self_care":
                True,

            "slept":
                True,

            "recovered_energy":
                True,
        },
    }

    result = (
        apply_sleep_cognitive_effects(
            character,
            world,
            sleep_event,
        )
    )

    assert (
        result[
            "hours_slept"
        ]
        == 8
    )

    assert (
        result[
            "memories_processed"
        ]
        == 1
    )

    assert (
        character[
            "current_emotions"
        ][
            "fear"
        ]
        < 80
    )

    assert (
        character[
            "current_emotions"
        ][
            "happiness"
        ]
        > 10
    )

    assert (
        character[
            "memory"
        ][0][
            "clarity"
        ]
        > 80
    )
