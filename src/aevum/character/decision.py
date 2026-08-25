"""
Autonomous character decision-making.

This module evaluates subjective character pressures and produces
intentions.

It does not determine whether an intention actually succeeds.
Authoritative action validation and resolution belong to Axiom.
"""


def calculate_need_urgency(
    need_name,
    pressure,
):
    """
    Return the urgency multiplier for a character need.

    Physical needs become increasingly urgent as pressure rises.
    Non-physical needs currently use a neutral multiplier.
    """

    if need_name in [
        "hunger",
        "fatigue",
    ]:

        if pressure < 30:
            return 1.0

        if pressure < 50:
            return 1.25

        if pressure < 70:
            return 1.75

        if pressure < 85:
            return 2.5

        return 4.0

    return 1.0


def calculate_need_pressure(
    character,
    action,
):
    """
    Calculate how strongly the character's current needs motivate
    a particular action.

    Returns both the numerical contribution and explainability
    reasons used by the decision system.
    """

    needs = character[
        "needs"
    ]

    satisfies = action.get(
        "satisfies",
        {},
    )

    score = 0
    reasons = []

    for (
        need_name,
        satisfaction_amount,
    ) in satisfies.items():

        current_pressure = needs.get(
            need_name,
            0,
        )

        urgency_multiplier = (
            calculate_need_urgency(
                need_name,
                current_pressure,
            )
        )

        need_score = (
            current_pressure
            * satisfaction_amount
            / 100
            * urgency_multiplier
        )

        score += need_score

        reasons.append(
            f"{need_name} pressure: "
            f"+{round(need_score, 2)} "
            f"(urgency x{urgency_multiplier})"
        )

    return {
        "score":
            round(
                score,
                2,
            ),

        "reasons":
            reasons,
    }
