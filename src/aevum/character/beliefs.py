"""
Belief systems for Aevum characters.

Beliefs represent a character's evolving interpretation of the world.
Experiences may support, contradict, or leave a belief unchanged.
"""


# ============================================================
# BELIEF CREATION
# ============================================================


def get_or_create_belief(
    character,
    belief_key,
    statement,
):
    if "beliefs" not in character:
        character["beliefs"] = {}

    if belief_key not in character["beliefs"]:
        character["beliefs"][belief_key] = {
            "statement": statement,
            "confidence": 50,
            "evidence_for": [],
            "evidence_against": [],
            "times_reconsidered": 0,
            "concepts": [],
        }

    return character["beliefs"][belief_key]


# ============================================================
# BELIEF CONCEPT GROUPS
# ============================================================


concept_groups = {
    "community_member": [
        "resident",
        "residents",
        "neighbor",
        "neighbors",
        "local residents",
        "citizen",
        "citizens",
    ],

    "assistance": [
        "help",
        "helped",
        "helping",
        "support",
        "supported",
        "aid",
        "assistance",
        "cooperation",
    ],

    "family": [
        "family",
        "father",
        "mother",
        "sister",
        "brother",
        "parent",
        "parents",
    ],

    "community": [
        "community",
        "district",
        "slum district",
        "neighborhood",
        "village",
    ],
}


# ============================================================
# BELIEF RELEVANCE
# ============================================================


def infer_belief_relevance(
    character,
    perception,
):
    relevant_beliefs = []

    event_text = " ".join(
        [
            perception["perceived_description"],
            perception["location"],
            " ".join(
                perception["participants"]
            ),
        ]
    ).lower()

    for belief_key, belief in (
        character["beliefs"].items()
    ):
        belief_concepts = belief.get(
            "concepts",
            [],
        )

        matched_groups = []

        for group_name, terms in (
            concept_groups.items()
        ):
            belief_match = any(
                term.lower()
                in belief_concepts
                for term in terms
            )

            event_match = any(
                term.lower()
                in event_text
                for term in terms
            )

            if (
                belief_match
                and event_match
            ):
                matched_groups.append(
                    group_name
                )

        score = len(
            matched_groups
        )

        if score > 0:
            relevant_beliefs.append(
                {
                    "belief_key":
                        belief_key,

                    "belief":
                        belief,

                    "match_score":
                        score,

                    "matched_groups":
                        matched_groups,
                }
            )

    relevant_beliefs.sort(
        key=lambda x: x[
            "match_score"
        ],
        reverse=True,
    )

    return relevant_beliefs


# ============================================================
# BELIEF EVIDENCE JUDGMENT
# ============================================================


def judge_belief_evidence(
    character,
    perception,
    belief_match,
):
    belief_key = (
        belief_match["belief_key"]
    )

    details = (
        perception["known_details"]
    )

    result = {
        "belief_key":
            belief_key,

        "direction":
            "neutral",

        "strength":
            0,

        "reason":
            (
                "The experience is relevant, "
                "but does not provide clear evidence."
            ),
    }

    # --------------------------------------------------------
    # COMMUNITY SUPPORT BELIEF
    # --------------------------------------------------------

    if belief_key == "community_support":

        help_given = details.get(
            "community_help_given"
        )

        help_refused = details.get(
            "community_help_refused"
        )

        if help_given:

            result["direction"] = (
                "supports"
            )

            result["strength"] = 70

            result["reason"] = (
                "Members of the community "
                "voluntarily helped someone "
                "who needed assistance."
            )

        elif help_refused:

            result["direction"] = (
                "contradicts"
            )

            result["strength"] = 70

            result["reason"] = (
                "Members of the community "
                "refused to help someone who "
                "clearly needed assistance."
            )

    return result


# ============================================================
# APPLY BELIEF JUDGMENT
# ============================================================


def apply_belief_judgment(
    character,
    event,
    perception,
    judgment,
):
    belief_key = judgment[
        "belief_key"
    ]

    if belief_key not in character[
        "beliefs"
    ]:
        print("Belief not found.")
        return

    belief = character[
        "beliefs"
    ][belief_key]

    direction = judgment[
        "direction"
    ]

    strength = judgment[
        "strength"
    ]

    if (
        direction == "neutral"
        or strength <= 0
    ):
        print(
            "No belief change for: "
            f"{belief['statement']}"
        )

        return

    confidence_change = (
        strength * 0.15
    )

    evidence_record = {
        "event_id":
            event["event_id"],

        "day":
            event["day"],

        "strength":
            strength,

        "reason":
            judgment["reason"],

        "experience":
            perception[
                "perceived_description"
            ],
    }

    if direction == "supports":

        belief["confidence"] += (
            confidence_change
        )

        belief["evidence_for"].append(
            evidence_record
        )

    elif direction == "contradicts":

        belief["confidence"] -= (
            confidence_change
        )

        belief[
            "evidence_against"
        ].append(
            evidence_record
        )

    belief["confidence"] = round(
        min(
            max(
                belief["confidence"],
                0,
            ),
            100,
        ),
        2,
    )

    belief[
        "times_reconsidered"
    ] += 1

    print(
        "\n--- BELIEF UPDATED ---"
    )

    print(
        f"Belief: "
        f"{belief['statement']}"
    )

    print(
        f"Direction: {direction}"
    )

    print(
        "Confidence change:",
        round(
            confidence_change,
            2,
        ),
    )

    print(
        "New confidence:",
        belief["confidence"],
    )

    return belief
