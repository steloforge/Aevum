"""
Authoritative Axiom action resolution.

A character chooses an intention.

Axiom checks world law and then determines the canonical outcome
from the action type, character capability, and world context.
"""

from aevum.axiom.actions import (
    validate_action,
)


def resolve_action_outcome(
    world,
    character,
    chosen_action,
    event,
):
    action_name = (
        chosen_action["action"]
    )

    action_type = (
        chosen_action.get(
            "action_type"
        )
    )

    target = (
        chosen_action.get(
            "target"
        )
    )

    location = event[
        "location"
    ]

    print(
        "\n--- ACTION RESOLUTION ---"
    )

    print(
        f"Character: "
        f"{character['name']}"
    )

    print(
        f"Action: {action_name}"
    )

    print(
        f"Action Type: "
        f"{action_type}"
    )

    print(
        f"Target: {target}"
    )

    print(
        f"Location: {location}"
    )

    # ========================================================
    # 1. WORLD LAW CHECK
    # ========================================================

    validation = validate_action(
        world=world,
        character=character,
        action=chosen_action,
        location=location,
    )

    if not validation[
        "allowed"
    ]:
        return {
            "status":
                "blocked",

            "action":
                action_name,

            "action_type":
                action_type,

            "target":
                target,

            "reason":
                validation[
                    "reason"
                ],
        }

    # ========================================================
    # 2. HELP PERSON
    # ========================================================

    if action_type == "help_person":

        capability_score = (
            character[
                "traits"
            ]["compassion"] * 0.35

            + character[
                "traits"
            ]["courage"] * 0.25

            + character[
                "traits"
            ]["self_control"] * 0.20

            + character[
                "skills"
            ]["discipline"] * 0.20
        )

        difficulty = 55

        if (
            capability_score
            >= difficulty + 20
        ):
            status = "success"

            reason = (
                f"{character['name']} successfully "
                f"helps {target} and gets them "
                "to safety."
            )

        elif (
            capability_score
            >= difficulty
        ):
            status = (
                "partial_success"
            )

            reason = (
                f"{character['name']} is able "
                f"to help {target}, but additional "
                "assistance is still needed."
            )

        else:
            status = "failure"

            reason = (
                f"{character['name']} tries "
                f"to help {target}, but is unable "
                "to provide enough assistance alone."
            )

        return {
            "status":
                status,

            "action":
                action_name,

            "action_type":
                action_type,

            "target":
                target,

            "reason":
                reason,

            "capability_score":
                round(
                    capability_score,
                    2,
                ),

            "difficulty":
                difficulty,
        }

    # ========================================================
    # 3. REQUEST HELP
    # ========================================================

    if action_type == "request_help":

        capability_score = (
            character[
                "traits"
            ]["courage"] * 0.35

            + character[
                "traits"
            ]["compassion"] * 0.25

            + character[
                "traits"
            ]["self_control"] * 0.20
        )

        difficulty = 50

        if (
            capability_score
            >= difficulty + 15
        ):
            status = "success"

            reason = (
                f"{character['name']} successfully "
                "persuades nearby people to assist "
                f"{target}."
            )

        elif (
            capability_score
            >= difficulty
        ):
            status = (
                "partial_success"
            )

            reason = (
                f"{character['name']} calls for help. "
                "Some people respond, but others "
                "continue to hesitate."
            )

        else:
            status = "failure"

            reason = (
                f"{character['name']} calls for help, "
                "but the nearby residents "
                "do not respond."
            )

        return {
            "status":
                status,

            "action":
                action_name,

            "action_type":
                action_type,

            "target":
                target,

            "reason":
                reason,

            "capability_score":
                round(
                    capability_score,
                    2,
                ),

            "difficulty":
                difficulty,
        }

    # ========================================================
    # 4. CONFRONT PERSON
    # ========================================================

    if (
        action_type
        == "confront_person"
    ):
        capability_score = (
            character[
                "traits"
            ]["courage"] * 0.30

            + character[
                "traits"
            ]["self_control"] * 0.30

            + character[
                "traits"
            ]["aggression"] * 0.20

            + character[
                "values"
            ]["personal_honor"] * 0.20
        )

        difficulty = 55

        if (
            capability_score
            >= difficulty + 15
        ):
            status = "success"

            reason = (
                f"{character['name']} firmly "
                f"confronts {target} and makes "
                "his position clear without "
                "losing control."
            )

        elif (
            capability_score
            >= difficulty
        ):
            status = (
                "partial_success"
            )

            reason = (
                f"{character['name']} confronts "
                f"{target}, but the exchange "
                "becomes tense."
            )

        else:
            status = "failure"

            reason = (
                f"{character['name']} confronts "
                f"{target}, but the confrontation "
                "does not go as intended."
            )

        return {
            "status":
                status,

            "action":
                action_name,

            "action_type":
                action_type,

            "target":
                target,

            "reason":
                reason,

            "capability_score":
                round(
                    capability_score,
                    2,
                ),

            "difficulty":
                difficulty,
        }

    # ========================================================
    # 5. IGNORE EVENT
    # ========================================================

    if action_type == "ignore_event":

        reason = (
            f"{character['name']} chooses "
            "not to intervene and continues on."
        )

        return {
            "status":
                "success",

            "action":
                action_name,

            "action_type":
                action_type,

            "target":
                target,

            "reason":
                reason,
        }

    # ========================================================
    # 6. UNKNOWN ACTION TYPE
    # ========================================================

    return {
        "status":
            "unresolved",

        "action":
            action_name,

        "action_type":
            action_type,

        "target":
            target,

        "reason":
            (
                "No resolution rule exists "
                "for this action type."
            ),
    }
