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

from aevum.world.time import (
    advance_time,
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

# ============================================================
# AWAKE NEED DRIFT
# ============================================================


def apply_awake_need_drift(
    character,
    hours_passed,
):
    """
    Apply normal need changes while a character is awake.

    This represents the passage-of-time cost that occurs
    alongside ordinary waking actions.
    """

    needs = character[
        "needs"
    ]

    needs["hunger"] = (
        needs.get(
            "hunger",
            0,
        )
        + 2.0 * hours_passed
    )

    needs["fatigue"] = (
        needs.get(
            "fatigue",
            0,
        )
        + 1.5 * hours_passed
    )

    needs["social"] = (
        needs.get(
            "social",
            0,
        )
        + 0.3 * hours_passed
    )

    needs["family_responsibility"] = (
        needs.get(
            "family_responsibility",
            0,
        )
        + 0.4 * hours_passed
    )

    needs["training_drive"] = (
        needs.get(
            "training_drive",
            0,
        )
        + 0.5 * hours_passed
    )

    for need_name in needs:

        needs[need_name] = round(
            min(
                max(
                    needs[need_name],
                    0,
                ),
                100,
            ),
            2,
        )

    return needs


def resolve_waking_self_directed_action(
    world,
    character,
    action_name,
    action_type,
    action_data,
    duration_hours,
):
    """
    Resolve the shared mechanics of a normal waking
    self-directed action.
    """

    satisfies = action_data.get(
        "satisfies",
        {},
    )

    for need_name, reduction in satisfies.items():

        if need_name not in character["needs"]:
            continue

        character["needs"][need_name] = round(
            max(
                character["needs"][need_name]
                - reduction,
                0,
            ),
            2,
        )

    advance_time(
        world,
        duration_hours,
    )

    apply_awake_need_drift(
        character,
        duration_hours,
    )

    return {
        "status":
            "success",

        "action":
            action_name,

        "action_type":
            action_type,

        "action_data":
            action_data,

        "duration_hours":
            duration_hours,

        "reason":
            (
                f"{character['name']} "
                f"completed {action_name}."
            ),

        "updated_needs":
            character["needs"].copy(),
    }

def resolve_self_directed_action(
    world,
    character,
    chosen_action,
):
    """
    Resolve a self-directed character intention through
    authoritative Axiom world rules.

    Self-directed actions originate from the character's
    internal state rather than from a triggering world event.

    This function determines what actually occurs.
    """

    action_name = chosen_action[
        "action"
    ]

    action_type = chosen_action[
        "action_type"
    ]

    action_data = chosen_action.get(
        "action_data",
        {},
    )

    print(
        "\n--- SELF-DIRECTED ACTION RESOLUTION ---"
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

    # ========================================================
    # 1. EAT
    # ========================================================

    if action_type == "eat":

        return resolve_waking_self_directed_action(
            world=world,
            character=character,
            action_name=action_name,
            action_type=action_type,
            action_data=action_data,
            duration_hours=1,
        )

        # ----------------------------------------------------
        # SATISFY HUNGER
        # ----------------------------------------------------

        current_hunger = (
            character[
                "needs"
            ].get(
                "hunger",
                0,
            )
        )

        character[
            "needs"
        ][
            "hunger"
        ] = round(
            max(
                current_hunger
                - hunger_reduction,
                0,
            ),
            2,
        )

        # ----------------------------------------------------
        # TIME PASSES
        # ----------------------------------------------------

        advance_time(
            world,
            duration_hours,
        )

        # ----------------------------------------------------
        # NORMAL WAKING NEED DRIFT
        # ----------------------------------------------------

        apply_awake_need_drift(
            character,
            duration_hours,
        )

        return {
            "status":
                "success",

            "action":
                action_name,

            "action_type":
                action_type,

            "action_data":
                action_data,

            "duration_hours":
                duration_hours,

            "reason":
                (
                    f"{character['name']} "
                    "ate a meal."
                ),

            "updated_needs":
                character[
                    "needs"
                ].copy(),
        }

    # ========================================================
    # 2. REST
    # ========================================================

    if action_type == "rest":

        return resolve_waking_self_directed_action(
            world=world,
            character=character,
            action_name=action_name,
            action_type=action_type,
            action_data=action_data,
            duration_hours=2,
        )

        # ----------------------------------------------------
        # SATISFY FATIGUE
        # ----------------------------------------------------

        current_fatigue = (
            character[
                "needs"
            ].get(
                "fatigue",
                0,
            )
        )

        character[
            "needs"
        ][
            "fatigue"
        ] = round(
            max(
                current_fatigue
                - fatigue_reduction,
                0,
            ),
            2,
        )

        # ----------------------------------------------------
        # TIME PASSES
        # ----------------------------------------------------

        advance_time(
            world,
            duration_hours,
        )

        # ----------------------------------------------------
        # NORMAL WAKING NEED DRIFT
        # ----------------------------------------------------

        apply_awake_need_drift(
            character,
            duration_hours,
        )

        return {
            "status":
                "success",

            "action":
                action_name,

            "action_type":
                action_type,

            "action_data":
                action_data,

            "duration_hours":
                duration_hours,

            "reason":
                (
                    f"{character['name']} "
                    "rested for a while."
                ),

            "updated_needs":
                character[
                    "needs"
                ].copy(),
        }

    
    # ========================================================
    # 3. FAMILY DUTY
    # ========================================================

    if action_type == "family_duty":

        return resolve_waking_self_directed_action(
            world=world,
            character=character,
            action_name=action_name,
            action_type=action_type,
            action_data=action_data,
            duration_hours=3,
        )

    # ========================================================
    # 4. TRAIN
    # ========================================================

    if action_type == "train":

        return resolve_waking_self_directed_action(
            world=world,
            character=character,
            action_name=action_name,
            action_type=action_type,
            action_data=action_data,
            duration_hours=2,
        )
    
    # ========================================================
    # 5. UNKNOWN SELF-DIRECTED ACTION
    # ========================================================

    return {
        "status":
            "unresolved",

        "action":
            action_name,

        "action_type":
            action_type,

        "action_data":
            action_data,

        "reason":
            (
                "No self-directed Axiom resolution "
                "rule exists for this action type."
            ),
    }



# ============================================================
# CREATE SELF-DIRECTED OUTCOME EVENT
# ============================================================


def create_self_directed_outcome_event(
    world,
    character,
    self_outcome,
):
    """
    Convert an authoritative self-directed action resolution
    into a canonical Axiom world event.

    The resolution determines what actually happened.
    This function records that outcome in canonical event form.
    """

    action_name = self_outcome[
        "action"
    ]

    action_type = self_outcome[
        "action_type"
    ]

    status = self_outcome[
        "status"
    ]

    duration_hours = self_outcome.get(
        "duration_hours",
        0,
    )

    details = {
        "performed_action":
            action_name,

        "action_type":
            action_type,

        "action_success":
            status == "success",

        "duration_hours":
            duration_hours,
    }

    # ========================================================
    # EATING
    # ========================================================

    if action_type == "eat":

        description = (
            f"{character['name']} "
            "took time to eat a meal."
        )

        details.update({
            "self_care":
                True,

            "satisfied_hunger":
                True,
        })

        participants = [
            character[
                "name"
            ],
        ]

        location = (
            "Family Shop"
        )

    # ========================================================
    # RESTING
    # ========================================================

    elif action_type == "rest":

        description = (
            f"{character['name']} "
            "took time to rest and recover."
        )

        details.update({
            "self_care":
                True,

            "recovered_fatigue":
                True,
        })

        participants = [
            character[
                "name"
            ],
        ]

        location = (
            "Family Living Quarters"
        )
    
    # ========================================================
    # FAMILY DUTY
    # ========================================================

    elif action_type == "family_duty":

        description = (
            f"{character['name']} spent {duration_hours} hours "
            "helping operate the family shop."
        )

        details.update({
            "helped_family":
                True,

            "supported_community":
                True,

            "fulfilled_responsibility":
                True,
        })

        participants = [
            character["name"],
            "Ryuk's Mother",
            "Ryuk's Father",
        ]

        location = "Family Shop"
    
    # ========================================================
    # TRAINING
    # ========================================================

    elif action_type == "train":

        description = (
            f"{character['name']} spent "
            f"{duration_hours} hours secretly "
            "practicing knight martial techniques."
        )

        details.update({
            "trained_skill":
                True,

            "secret_training":
                True,

            "pursued_goal":
                "Become a knight",
        })

        participants = [
            character["name"],
        ]

        location = (
            "Private Training Area"
        )
    
    
    # ========================================================
    # FALLBACK
    # ========================================================

    else:

        description = (
            self_outcome.get(
                "reason",
                (
                    f"{character['name']} "
                    f"attempted {action_name}."
                ),
            )
        )

        participants = [
            character[
                "name"
            ],
        ]

        location = "Unknown"

    return create_world_event(
        world=world,
        event_type=(
            "self_directed_outcome"
        ),
        description=description,
        location=location,
        participants=participants,
        details=details,
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

   
