"""
Event interpretation systems for Aevum characters.

Interpretation converts perceived world facts into subjective meaning,
emotional reactions, emotional causes, and perceived importance.
"""


def interpret_event(
    character,
    perception,
):
    details = perception[
        "known_details"
    ]

    emotions = {
        "fear": 0,
        "anger": 0,
        "guilt": 0,
        "sadness": 0,
        "happiness": 0,
        "stress": 0,
    }

    emotion_causes = {}

    interpretation_parts = []

    importance = 30

    traits = character["traits"]
    values = character["values"]

    # ========================================================
    # BLOCKED ACTION
    # ========================================================

    if details.get(
        "action_allowed"
    ) is False:

        attempted_action = details.get(
            "attempted_action",
            "",
        ).lower()

        emotions["anger"] += 15

        if traits[
            "rule_obedience"
        ] >= 60:

            interpretation_parts.append(
                "The law stopped me before "
                "I went too far."
            )

            emotions["guilt"] += 15

            emotion_causes["guilt"] = (
                character["name"]
            )

        else:

            interpretation_parts.append(
                "The law prevented me from "
                "doing what I intended."
            )

            emotions["anger"] += 10

        if (
            "attack" in attempted_action
            or "kill" in attempted_action
        ):
            if values["peace"] >= 70:

                emotions["guilt"] += 15
                emotions["stress"] += 10

                emotion_causes[
                    "guilt"
                ] = character["name"]

                emotion_causes[
                    "stress"
                ] = "Blocked Action"

                interpretation_parts.append(
                    "I let my anger push me toward "
                    "unnecessary violence."
                )

        importance += 20

    # ========================================================
    # FAMILY PROTECTION
    # ========================================================

    if details.get(
        "protected_family"
    ):

        emotions[
            "happiness"
        ] += 20

        emotion_causes[
            "happiness"
        ] = "Protected Family"

        interpretation_parts.append(
            "I protected my family "
            "when they needed me."
        )

        importance += (
            values["family"] * 0.2
        )

    # ========================================================
    # PEACEFUL RESOLUTION
    # ========================================================

    if details.get(
        "resolved_peacefully"
    ):

        emotions[
            "happiness"
        ] += 15

        interpretation_parts.append(
            "I handled the situation without "
            "unnecessary violence."
        )

        if values["peace"] >= 70:
            emotions[
                "happiness"
            ] += 10

        importance += 10

    # ========================================================
    # PUBLIC CONFLICT
    # ========================================================

    if details.get(
        "public_conflict"
    ):

        emotions["stress"] += 15

        emotion_causes[
            "stress"
        ] = details.get(
            "target",
            "Public Conflict",
        )

        if traits["patience"] >= 60:
            interpretation_parts.append(
                "I disliked causing a scene "
                "in public."
            )

    # ========================================================
    # COMMUNITY SUPPORT
    # ========================================================

    if details.get(
        "community_help_given"
    ):

        emotions[
            "happiness"
        ] += 15

        emotion_causes[
            "happiness"
        ] = "Community Support"

        interpretation_parts.append(
            "Seeing people help someone in need "
            "reminds me that there is still good "
            "in this community."
        )

        importance += 10

    # ========================================================
    # COMMUNITY NEGLECT
    # ========================================================

    if details.get(
        "community_help_refused"
    ):

        emotions[
            "sadness"
        ] += 15

        emotions[
            "anger"
        ] += 10

        emotions[
            "stress"
        ] += 5

        emotion_causes[
            "sadness"
        ] = "Community Neglect"

        emotion_causes[
            "anger"
        ] = "Local Residents"

        interpretation_parts.append(
            "Seeing people ignore someone who "
            "needed help disappointed me."
        )

        importance += 15

    # ========================================================
    # OLD MANUAL BELIEF EVIDENCE
    # ========================================================

    belief_evidence = details.get(
        "belief_evidence",
        [],
    )

    for evidence in belief_evidence:

        statement = evidence[
            "statement"
        ]

        direction = evidence[
            "direction"
        ]

        strength = evidence[
            "strength"
        ]

        if direction == "supports":

            interpretation_parts.append(
                "This experience makes me believe "
                f"more strongly that "
                f"{statement.lower()}"
            )

            emotions[
                "happiness"
            ] += (
                strength * 0.15
            )

            importance += (
                strength * 0.10
            )

        elif direction == "contradicts":

            interpretation_parts.append(
                "This experience makes me question "
                f"whether {statement.lower()}"
            )

            emotions[
                "sadness"
            ] += (
                strength * 0.10
            )

            emotions[
                "stress"
            ] += (
                strength * 0.08
            )

            importance += (
                strength * 0.12
            )

    # ========================================================
    # TARGET RELATIONSHIP
    # ========================================================

    target = details.get(
        "target"
    )

    if (
        target
        and target
        in character[
            "relationships"
        ]
    ):

        relationship = character[
            "relationships"
        ][target]

        if relationship[
            "trust"
        ] < 40:

            emotions[
                "anger"
            ] += 10

            emotion_causes[
                "anger"
            ] = target

        if relationship[
            "fear"
        ] > 40:

            emotions[
                "fear"
            ] += 15

            emotion_causes[
                "fear"
            ] = target

    # ========================================================
    # SUCCESSFUL HELPING ACTION
    # ========================================================

    if (
        details.get(
            "action_success"
        )
        and details.get(
            "helped_person"
        )
    ):

        emotions[
            "happiness"
        ] += 25

        emotion_causes[
            "happiness"
        ] = details.get(
            "target",
            "Successful Help",
        )

        interpretation_parts.append(
            "Someone needed help, and I was able to help them."
        )

        importance += 20

        if details.get(
            "protected_other"
        ):

            interpretation_parts.append(
                "I was able to protect someone who needed me."
            )

            importance += 10

    # ========================================================
    # SELF-DIRECTED FAMILY DUTY
    # ========================================================

    if details.get(
        "fulfilled_responsibility"
    ):

        emotions[
            "happiness"
        ] += 15

        emotion_causes[
            "happiness"
        ] = (
            "Completed Responsibility"
        )

        interpretation_parts.append(
            "I did my part for my family and community."
        )

        importance += 15

    # ========================================================
    # TRAINING / AMBITION
    # ========================================================

    if details.get(
        "trained_skill"
    ):

        emotions[
            "happiness"
        ] += 10

        interpretation_parts.append(
            "I spent time improving myself and moving closer "
            "to becoming a knight."
        )

        importance += 15

    # ========================================================
    # SELF CARE
    # ========================================================

    if details.get(
        "self_care"
    ):

        interpretation_parts.append(
            "I took care of myself so I can keep going."
        )

        importance += 5

    # ========================================================
    # FAMILY CONNECTION
    # ========================================================

    if details.get(
        "spent_time_with_family"
    ):

        emotions[
            "happiness"
        ] += 20

        emotion_causes[
            "happiness"
        ] = "Family"

        interpretation_parts.append(
            "Spending time with my family reminded me "
            "why they matter so much to me."
        )

        importance += 15

    # ========================================================
    # FINAL INTERPRETATION
    # ========================================================

    if not interpretation_parts:

        interpretation_parts.append(
            "Something happened, but I am still "
            "deciding what it means to me."
        )

    interpretation_text = " ".join(
        interpretation_parts
    )

    for emotion in emotions:

        emotions[
            emotion
        ] = round(
            min(
                max(
                    emotions[
                        emotion
                    ],
                    0,
                ),
                100,
            ),
            2,
        )

    importance = min(
        round(
            importance,
            2,
        ),
        100,
    )

    return {
        "event_id":
            perception[
                "event_id"
            ],

        "interpretation":
            interpretation_text,

        "emotions":
            emotions,

        "emotion_causes":
            emotion_causes,

        "importance":
            importance,

        "confidence":
            95,
    }
