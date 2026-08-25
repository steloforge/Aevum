"""
Self-concept systems for Aevum characters.

Self-concept represents how a character gradually comes to see
themselves through repeated lived experiences and outcomes.
"""


def update_self_concept(
    character,
    perception,
    interpretation,
):
    details = perception[
        "known_details"
    ]

    if "self_concept" not in character:
        character["self_concept"] = {
            "protector": 0,
            "peacekeeper": 0,
            "family_guardian": 0,
            "rule_follower": 0,
            "fighter": 0,
        }

    # --------------------------------------------------------
    # Protected family
    # --------------------------------------------------------

    if details.get(
        "protected_family"
    ):
        character[
            "self_concept"
        ]["protector"] += 5

        character[
            "self_concept"
        ]["family_guardian"] += 7

    # --------------------------------------------------------
    # Protected someone else
    # --------------------------------------------------------

    if (
        details.get(
            "protected_other"
        )
        and details.get(
            "action_success"
        )
    ):
        character[
            "self_concept"
        ]["protector"] += 4

    # --------------------------------------------------------
    # Peaceful resolution
    # --------------------------------------------------------

    if details.get(
        "resolved_peacefully"
    ):
        character[
            "self_concept"
        ]["peacekeeper"] += 5

    # --------------------------------------------------------
    # Accepted law
    # --------------------------------------------------------

    if details.get(
        "accepted_law"
    ):
        character[
            "self_concept"
        ]["rule_follower"] += 3

    # --------------------------------------------------------
    # Family responsibility
    # --------------------------------------------------------

    if details.get(
        "fulfilled_responsibility"
    ):
        character[
            "self_concept"
        ]["family_guardian"] += 2

    # --------------------------------------------------------
    # Training identity
    # --------------------------------------------------------

    if details.get(
        "trained_skill"
    ):
        character[
            "self_concept"
        ]["fighter"] += 1

    # --------------------------------------------------------
    # Actual fighting behavior
    # --------------------------------------------------------

    action = details.get(
        "attempted_action",
        details.get(
            "performed_action",
            "",
        ),
    ).lower()

    if (
        "attack" in action
        or "fight" in action
        or "strike" in action
    ):
        character[
            "self_concept"
        ]["fighter"] += 2

    print(
        "Self-concept updated:"
    )

    print(
        character[
            "self_concept"
        ]
    )

    return character[
        "self_concept"
    ]
