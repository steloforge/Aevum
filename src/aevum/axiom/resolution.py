"""
Authoritative Axiom action resolution.

A character chooses an intention.

Axiom checks world law and then determines the canonical outcome
from the action type, character capability, and world context.
"""

from aevum.axiom.actions import (
    validate_action,
)

from aevum.axiom.events import (
    create_world_event,
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

def create_outcome_event(
    world,
    character,
    original_event,
    chosen_action,
    outcome,
):
    """
    Convert an authoritative action resolution into a new
    canonical Axiom world event.

    The outcome event describes what actually happened,
    not what the character believes happened.
    """

    action_name = chosen_action[
        "action"
    ]

    action_type = chosen_action.get(
        "action_type"
    )

    target = chosen_action.get(
        "target"
    )

    status = outcome[
        "status"
    ]

    details = {
        "source_event_id":
            original_event[
                "event_id"
            ],

        "performed_action":
            action_name,

        "action_type":
            action_type,

        "target":
            target,

        "action_success":
            status == "success",

        "partial_success":
            status
            == "partial_success",

        "action_failed":
            status == "failure",

        "action_blocked":
            status == "blocked",
    }

    # ========================================================
    # HELP PERSON
    # ========================================================

    if action_type == "help_person":

        if status == "success":

            description = (
                f"{character['name']} successfully "
                f"helped {target} and got them "
                "to safety."
            )

            details.update(
                {
                    "helped_person":
                        True,

                    "protected_other":
                        True,

                    "resolved_peacefully":
                        True,
                }
            )

        elif (
            status
            == "partial_success"
        ):

            description = (
                f"{character['name']} helped "
                f"{target}, but additional "
                "assistance was still needed."
            )

            details.update(
                {
                    "helped_person":
                        True,

                    "protected_other":
                        False,
                }
            )

        elif status == "failure":

            description = (
                f"{character['name']} tried "
                f"to help {target}, but was "
                "unable to provide enough "
                "assistance."
            )

            details.update(
                {
                    "helped_person":
                        False,

                    "attempted_to_help":
                        True,
                }
            )

        elif status == "blocked":

            description = (
                f"{character['name']} attempted "
                f"to help {target}, but the "
                "action was prevented."
            )

            details.update(
                {
                    "helped_person":
                        False,

                    "blocked_reason":
                        outcome["reason"],
                }
            )

        else:

            description = (
                f"{character['name']} attempted "
                f"to help {target}, but the "
                "result could not be resolved."
            )

    # ========================================================
    # REQUEST HELP
    # ========================================================

    elif action_type == "request_help":

        if status == "success":

            description = (
                f"{character['name']} called "
                "for assistance, and nearby "
                f"people joined in to help "
                f"{target}."
            )

            details.update(
                {
                    "community_help_given":
                        True,

                    "helped_person":
                        True,

                    "resolved_peacefully":
                        True,
                }
            )

        elif (
            status
            == "partial_success"
        ):

            description = (
                f"{character['name']} called "
                "for assistance. Some people "
                f"helped {target}, while "
                "others hesitated."
            )

            details.update(
                {
                    "community_help_given":
                        True,

                    "helped_person":
                        True,
                }
            )

        else:

            description = (
                f"{character['name']} called "
                f"for help for {target}, "
                "but nobody responded."
            )

            details.update(
                {
                    "community_help_refused":
                        True,

                    "helped_person":
                        False,
                }
            )

    # ========================================================
    # CONFRONT PERSON
    # ========================================================

    elif (
        action_type
        == "confront_person"
    ):

        description = outcome[
            "reason"
        ]

        details.update(
            {
                "public_conflict":
                    True,

                "resolved_peacefully":
                    status == "success",
            }
        )

    # ========================================================
    # IGNORE EVENT
    # ========================================================

    elif action_type == "ignore_event":

        description = (
            f"{character['name']} chose "
            "not to intervene and "
            "continued on."
        )

        details.update(
            {
                "ignored_event":
                    True,
            }
        )

    # ========================================================
    # UNKNOWN ACTION
    # ========================================================

    else:

        description = outcome[
            "reason"
        ]

    participants = [
        character["name"]
    ]

    if target:
        participants.append(
            target
        )

    return create_world_event(
        world=world,
        event_type="action_outcome",
        description=description,
        location=original_event[
            "location"
        ],
        participants=participants,
        details=details,
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
