"""
Axiom action generation and world-law validation.

Characters may form intentions, but Axiom determines whether
those intentions are permitted by authoritative world rules.
"""


def generate_possible_actions(
    character,
    event,
):
    event_type = event["event_type"]

    details = event.get(
        "details",
        {},
    )

    actions = []

    target = details.get(
        "target",
        "person in need",
    )

    if event_type == "community_neglect":
        actions = [
            {
                "name":
                    f"Help {target}",

                "action":
                    f"Help {target}",

                "action_type":
                    "help_person",

                "tags": [
                    "community",
                    "peaceful",
                    "compassion",
                    "honor",
                    "help",
                ],

                "target":
                    target,
            },

            {
                "name":
                    (
                        "Call out to others to help "
                        f"{target}"
                    ),

                "action":
                    (
                        "Call out to others to help "
                        f"{target}"
                    ),

                "action_type":
                    "request_help",

                "tags": [
                    "community",
                    "peaceful",
                    "leadership",
                    "help",
                ],

                "target":
                    target,
            },

            {
                "name":
                    (
                        "Confront the residents "
                        "who refused to help"
                    ),

                "action":
                    (
                        "Confront the residents "
                        "who refused to help"
                    ),

                "action_type":
                    "confront_person",

                "tags": [
                    "community",
                    "aggressive",
                    "honor",
                ],

                "target":
                    "Local Residents",
            },

            {
                "name":
                    (
                        "Ignore the situation "
                        "and continue walking"
                    ),

                "action":
                    (
                        "Ignore the situation "
                        "and continue walking"
                    ),

                "action_type":
                    "ignore_event",

                "tags": [
                    "self_interest",
                    "avoid_public_conflict",
                ],

                "target":
                    None,
            },
        ]

    return actions


def validate_action(
    world,
    character,
    action,
    location,
):
    result = {
        "allowed": True,
        "reason": None,
    }

    laws = world.get(
        "laws",
        {},
    )

    safe_zones = laws.get(
        "safe_zones",
        [],
    )

    action_name = (
        action["action"].lower()
    )

    in_safe_zone = (
        location in safe_zones
    )

    if (
        in_safe_zone
        and laws.get(
            "no_attacking_in_safe_zones",
            False,
        )
        and "attack" in action_name
    ):
        result["allowed"] = False

        result["reason"] = (
            "Attacking is prohibited within "
            "a protected safe zone."
        )

        return result

    if (
        in_safe_zone
        and laws.get(
            "no_killing_in_safe_zones",
            False,
        )
        and "kill" in action_name
    ):
        result["allowed"] = False

        result["reason"] = (
            "Killing is impossible within "
            "a protected safe zone."
        )

        return result

    return result


def attempt_action(
    world,
    character,
    action,
    location,
):
    """
    Ask Axiom whether a character's intention is permitted.

    This checks world law only. It does not yet resolve
    capability or outcome difficulty.
    """

    print(
        "\n--- ACTION ATTEMPT ---"
    )

    print(
        f"Character: "
        f"{character['name']}"
    )

    print(
        f"Intention: "
        f"{action['action']}"
    )

    print(
        f"Location: {location}"
    )

    validation = validate_action(
        world=world,
        character=character,
        action=action,
        location=location,
    )

    print(
        "\n--- WORLD CHECK ---"
    )

    if validation["allowed"]:
        print(
            "Action permitted by Axiom."
        )

        result = {
            "success":
                True,

            "action":
                action["action"],

            "reason":
                "Action permitted.",
        }

    else:
        print(
            "Action denied by "
            "Axiom's world rules."
        )

        print(
            "Reason: "
            f"{validation['reason']}"
        )

        result = {
            "success":
                False,

            "action":
                action["action"],

            "reason":
                validation["reason"],
        }

    return result
