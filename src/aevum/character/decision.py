"""
Autonomous character decision-making.

This module evaluates subjective character pressures and produces
intentions.

It does not determine whether an intention actually succeeds.
Authoritative action validation and resolution belong to Axiom.
"""

from aevum.world.time import (
    get_time_period,
)


# ============================================================
# NEED URGENCY
# ============================================================


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


# ============================================================
# NEED PRESSURE
# ============================================================


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


# ============================================================
# SLEEP PRESSURE
# ============================================================


def calculate_sleep_pressure(
    character,
    action,
):
    """
    Calculate the special fatigue pressure for full sleep.

    Ordinary tiredness does not immediately create a strong
    desire for a full sleep cycle. Only fatigue above 20
    contributes to sleep pressure.
    """

    if action.get(
        "action_type"
    ) != "sleep":
        return {
            "score": 0,
            "reasons": [],
        }

    fatigue = character.get(
        "needs",
        {},
    ).get(
        "fatigue",
        0,
    )

    fatigue_urgency = (
        calculate_need_urgency(
            "fatigue",
            fatigue,
        )
    )

    effective_fatigue = max(
        fatigue - 20,
        0,
    )

    sleep_need_score = (
        effective_fatigue
        * 0.70
        * fatigue_urgency
    )

    return {
        "score":
            round(
                sleep_need_score,
                2,
            ),

        "reasons": [
            (
                "Sleep fatigue pressure: "
                f"+{round(sleep_need_score, 2)} "
                f"(urgency x{fatigue_urgency})"
            )
        ],
    }


# ============================================================
# RECENT ACTION HISTORY
# ============================================================


def record_recent_action(
    character,
    world,
    action_type,
    duration_hours,
):
    """
    Record a completed autonomous action so recent
    repetition can influence future decisions.

    Only a small rolling history is retained.
    """

    if "recent_actions" not in character:
        character["recent_actions"] = []

    character["recent_actions"].append({
        "action_type":
            action_type,

        "day":
            world["day"],

        "hour":
            world["hour"],

        "duration_hours":
            duration_hours,
    })

    # Keep only reasonably recent history.
    character["recent_actions"] = [
        action
        for action
        in character["recent_actions"]
        if (
            world["day"]
            - action["day"]
        ) <= 2
    ]


# ============================================================
# PREFERENCE / REPETITION EFFECT
# ============================================================


def calculate_repetition_effect(
    character,
    world,
    action_type,
):
    """
    Calculate the combined effect of personal activity
    preference and recent repetition.

    Characters are more inclined toward activities they
    enjoy, but repeatedly performing the same activity
    creates satiation.

    Enjoyed activities resist repetition fatigue better
    than disliked activities.
    """

    recent_actions = character.get(
        "recent_actions",
        [],
    )

    preference = character.get(
        "activity_preferences",
        {},
    ).get(
        action_type,
        50,
    )

    repetition_pressure = 0

    # ========================================================
    # RECENT REPETITION
    # ========================================================

    for past_action in recent_actions:

        if (
            past_action["action_type"]
            != action_type
        ):
            continue

        hours_ago = (
            (
                world["day"]
                - past_action["day"]
            )
            * 24
            + (
                world["hour"]
                - past_action["hour"]
            )
        )

        if hours_ago <= 4:
            recency_weight = 1.0

        elif hours_ago <= 8:
            recency_weight = 0.6

        elif hours_ago <= 16:
            recency_weight = 0.3

        else:
            recency_weight = 0.1

        repetition_pressure += (
            past_action.get(
                "duration_hours",
                1,
            )
            * recency_weight
        )

    # ========================================================
    # PERSONAL PREFERENCE
    # ========================================================

    # 50 is neutral.
    #
    # Above 50:
    # "I enjoy doing this."
    #
    # Below 50:
    # "I don't particularly want to do this."

    preference_bonus = (
        preference - 50
    ) * 0.10

    # ========================================================
    # SATIATION
    # ========================================================

    base_repetition_penalty = (
        repetition_pressure * 2
    )

    # Enjoyment makes a character more resistant to
    # becoming tired of repeating an activity.

    enjoyment_resistance = (
        preference / 100
    ) * 0.75

    repetition_penalty = (
        base_repetition_penalty
        * (
            1
            - enjoyment_resistance
        )
    )

    net_effect = (
        preference_bonus
        - repetition_penalty
    )

    return {
        "preference":
            preference,

        "preference_bonus":
            round(
                preference_bonus,
                2,
            ),

        "repetition_pressure":
            round(
                repetition_pressure,
                2,
            ),

        "repetition_penalty":
            round(
                repetition_penalty,
                2,
            ),

        "net_effect":
            round(
                net_effect,
                2,
            ),
    }


# ============================================================
# TIME-OF-DAY EFFECT
# ============================================================


def calculate_time_of_day_effect(
    world,
    action_type,
):
    """
    Calculate how appropriate an action is for the current
    time of day.

    This represents contextual preference, not world-law
    availability. An action may be undesirable at a certain
    time without being impossible.
    """

    period = get_time_period(
        world
    )

    effect = 0
    reason = None

    # ========================================================
    # EATING
    # ========================================================

    if action_type == "eat":

        if period in [
            "early_morning",
            "afternoon",
            "evening",
        ]:
            effect += 2
            reason = (
                "Natural meal time"
            )

    # ========================================================
    # FAMILY SHOP WORK
    # ========================================================

    elif (
        action_type
        == "family_duty"
    ):

        if period in [
            "morning",
            "afternoon",
        ]:
            effect += 3
            reason = (
                "Normal shop hours"
            )

        elif period == "evening":
            effect -= 2
            reason = (
                "Shop day is winding down"
            )

        elif period in [
            "night",
            "late_night",
        ]:
            effect -= 8
            reason = (
                "Shop is likely closed"
            )

    # ========================================================
    # SECRET TRAINING
    # ========================================================

    elif action_type == "train":

        if period == "evening":
            effect += 2
            reason = (
                "More privacy for secret training"
            )

        elif period == "night":
            effect += 3
            reason = (
                "Night provides privacy"
            )

        elif period == "late_night":
            effect -= 3
            reason = (
                "Too late for effective training"
            )

    # ========================================================
    # FAMILY TIME
    # ========================================================

    elif (
        action_type
        == "social_family"
    ):

        if period == "evening":
            effect += 5
            reason = (
                "Family is likely together"
            )

        elif period == "night":
            effect += 2
            reason = (
                "Quiet family time"
            )

        elif period == "late_night":
            effect -= 4
            reason = (
                "Family is likely sleeping"
            )

    # ========================================================
    # REST
    # ========================================================

    elif action_type == "rest":

        if period == "evening":
            effect += 2
            reason = (
                "The day is winding down"
            )

        elif period == "night":
            effect += 6
            reason = (
                "Natural time to rest"
            )

        elif period == "late_night":
            effect += 12
            reason = (
                "Very strong sleep-time pressure"
            )

    # ========================================================
    # SLEEP
    # ========================================================

    elif action_type == "sleep":

        if period == "early_morning":
            effect -= 8
            reason = (
                "Normally too early in the day to sleep"
            )

        elif period == "morning":
            effect -= 12
            reason = (
                "The character would normally be awake"
            )

        elif period == "afternoon":
            effect -= 10
            reason = (
                "Too early for normal sleep"
            )

        elif period == "evening":
            effect -= 6
            reason = (
                "Still somewhat early for a full night's sleep"
            )

        elif period == "night":
            effect += 10
            reason = (
                "Natural sleeping hours"
            )

        elif period == "late_night":
            effect += 20
            reason = (
                "The body strongly expects sleep"
            )

    return {
        "period":
            period,

        "effect":
            effect,

        "reason":
            reason,
    }


# ============================================================
# SELF-DIRECTED ACTION SCORING
# ============================================================


def score_self_directed_action(
    character,
    world,
    action,
):
    """
    Score a self-directed action from the character's
    current subjective motivations.

    Current scoring layers:

    - need pressure
    - special sleep pressure
    - activity preference
    - recent repetition
    - time-of-day context

    Values, goals, traits, and risk will be layered in
    separately.
    """

    score = 0
    reasons = []

    # ========================================================
    # 1. NEED PRESSURE
    # ========================================================

    need_effect = (
        calculate_need_pressure(
            character,
            action,
        )
    )

    score += need_effect[
        "score"
    ]

    reasons.extend(
        need_effect[
            "reasons"
        ]
    )

    # ========================================================
    # 2. SLEEP FATIGUE PRESSURE
    # ========================================================

    sleep_effect = (
        calculate_sleep_pressure(
            character,
            action,
        )
    )

    score += sleep_effect[
        "score"
    ]

    reasons.extend(
        sleep_effect[
            "reasons"
        ]
    )

    # ========================================================
    # 3. PERSONAL PREFERENCE / REPETITION
    # ========================================================

    preference_effect = (
        calculate_repetition_effect(
            character,
            world,
            action[
                "action_type"
            ],
        )
    )

    score += preference_effect[
        "net_effect"
    ]

    preference_bonus = (
        preference_effect[
            "preference_bonus"
        ]
    )

    if preference_bonus >= 0:
        reasons.append(
            "Activity preference: "
            f"+{preference_bonus}"
        )

    else:
        reasons.append(
            "Activity preference: "
            f"{preference_bonus}"
        )

    if (
        preference_effect[
            "repetition_penalty"
        ]
        > 0
    ):
        reasons.append(
            "Recent repetition: "
            f"-{preference_effect['repetition_penalty']}"
        )

    # ========================================================
    # 4. TIME OF DAY
    # ========================================================

    time_effect = (
        calculate_time_of_day_effect(
            world,
            action[
                "action_type"
            ],
        )
    )

    score += time_effect[
        "effect"
    ]

    if (
        time_effect["effect"]
        != 0
    ):
        sign = (
            "+"
            if (
                time_effect["effect"]
                > 0
            )
            else ""
        )

        reasons.append(
            f"Time of day "
            f"({time_effect['period']}): "
            f"{sign}{time_effect['effect']} "
            f"- {time_effect['reason']}"
        )

    return {
        "action":
            action["name"],

        "action_type":
            action[
                "action_type"
            ],

        "score":
            round(
                score,
                2,
            ),

        "reasons":
            reasons,
    }
