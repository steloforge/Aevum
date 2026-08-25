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
# Calculate Value Reference
# ============================================================

def calculate_value_relevance(
    character,
    action_type,
):
    """
    Calculate how relevant a character's values are
    to the current action.

    Values should reinforce an existing reason to act,
    rather than always applying at full strength.
    """

    if action_type != "family_duty":
        return 1.0

    needs = character.get(
        "needs",
        {},
    )

    family_pressure = needs.get(
        "family_responsibility",
        0,
    )

    relevance = (
        0.25
        + (family_pressure / 100) * 0.75
    )

    return round(
        relevance,
        3,
    )

# ============================================================
# Calculate Value Effect
# ============================================================

def calculate_value_effect(
    character,
    action,
):
    """
    Calculate the value-based contribution to an
    autonomous action's score.
    """

    values = character.get(
        "values",
        {},
    )

    tags = action.get(
        "tags",
        [],
    )

    value_relevance = (
        calculate_value_relevance(
            character,
            action["action_type"],
        )
    )

    family_bonus = 0
    community_bonus = 0
    honor_bonus = 0

    if "family" in tags:
        family_bonus = (
            values.get(
                "family",
                0,
            )
            * 0.08
            * value_relevance
        )

    if "community" in tags:
        community_bonus = (
            values.get(
                "community",
                0,
            )
            * 0.05
            * value_relevance
        )

    if "honor" in tags:
        honor_bonus = (
            values.get(
                "personal_honor",
                0,
            )
            * 0.05
            * value_relevance
        )

    total_effect = (
        family_bonus
        + community_bonus
        + honor_bonus
    )

    return {
        "value_relevance":
            round(
                value_relevance,
                3,
            ),

        "family_bonus":
            round(
                family_bonus,
                2,
            ),

        "community_bonus":
            round(
                community_bonus,
                2,
            ),

        "honor_bonus":
            round(
                honor_bonus,
                2,
            ),

        "total_effect":
            round(
                total_effect,
                2,
            ),
    }


# ============================================================
# GOAL RELEVANCE
# ============================================================


def calculate_goal_relevance(
    character,
    action_type,
):
    """
    Calculate how relevant long-term goal motivation is
    to the current action.

    Training motivation scales with the character's current
    training drive rather than always applying ambition and
    discipline at full strength.
    """

    if action_type != "train":
        return 1.0

    needs = character.get(
        "needs",
        {},
    )

    training_drive = needs.get(
        "training_drive",
        0,
    )

    relevance = (
        0.25
        + (training_drive / 100) * 0.75
    )

    return round(
        relevance,
        3,
    )


# ============================================================
# GOAL EFFECT
# ============================================================


def calculate_goal_effect(
    character,
    action,
):
    """
    Calculate the long-term goal contribution to an
    autonomous action's score.
    """

    action_type = action.get(
        "action_type"
    )

    goal_relevance = (
        calculate_goal_relevance(
            character,
            action_type,
        )
    )

    ambition_bonus = 0
    discipline_bonus = 0

    if action_type == "train":

        ambition = character.get(
            "traits",
            {},
        ).get(
            "ambition",
            0,
        )

        discipline = character.get(
            "skills",
            {},
        ).get(
            "discipline",
            0,
        )

        ambition_bonus = (
            ambition
            * 0.08
            * goal_relevance
        )

        discipline_bonus = (
            discipline
            * 0.05
            * goal_relevance
        )

    total_effect = (
        ambition_bonus
        + discipline_bonus
    )

    return {
        "goal_relevance":
            round(
                goal_relevance,
                3,
            ),

        "ambition_bonus":
            round(
                ambition_bonus,
                2,
            ),

        "discipline_bonus":
            round(
                discipline_bonus,
                2,
            ),

        "total_effect":
            round(
                total_effect,
                2,
            ),
    }


# ============================================================
# RISK HESITATION
# ============================================================


def calculate_risk_effect(
    character,
    action,
):
    """
    Calculate hesitation toward risky autonomous actions.

    Characters with stronger rule obedience are more
    reluctant to choose actions explicitly tagged as risky.
    """

    tags = action.get(
        "tags",
        [],
    )

    if "risk" not in tags:
        return {
            "risk_penalty": 0,
            "total_effect": 0,
        }

    rule_obedience = character.get(
        "traits",
        {},
    ).get(
        "rule_obedience",
        0,
    )

    risk_penalty = (
        rule_obedience
        * 0.03
    )

    return {
        "risk_penalty":
            round(
                risk_penalty,
                2,
            ),

        "total_effect":
            round(
                -risk_penalty,
                2,
            ),
    }


# ============================================================
# Generate self directed actions
# ============================================================

def generate_self_directed_actions(
    character,
):
    """
    Generate the character's baseline self-directed
    action candidates.

    This function defines possible intentions.
    Availability is checked separately.
    """

    actions = [
        {
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

        {
            "name":
                "Rest for a while",

            "action_type":
                "rest",

            "tags": [
                "self_care",
            ],

            "satisfies": {
                "fatigue": 18,
            },
        },

        {
            "name":
                "Go to sleep",

            "action_type":
                "sleep",

            "tags": [
                "self_care",
                "sleep",
            ],

            "satisfies": {},
        },

        {
            "name":
                "Help at the family shop",

            "action_type":
                "family_duty",

            "tags": [
                "family",
                "community",
                "honor",
            ],

            "satisfies": {
                "family_responsibility": 35,
                "social": 10,
            },
        },

        {
            "name":
                "Practice knight techniques in secret",

            "action_type":
                "train",

            "tags": [
                "ambition",
                "discipline",
                "risk",
            ],

            "satisfies": {
                "training_drive": 40,
            },
        },

        {
            "name":
                "Spend time with family",

            "action_type":
                "social_family",

            "tags": [
                "family",
                "social",
            ],

            "satisfies": {
                "social": 30,
                "family_responsibility": 15,
            },
        },
    ]

    return actions

# ============================================================
# SELF-DIRECTED ACTION AVAILABILITY
# ============================================================


def is_self_directed_action_available(
    character,
    world,
    action,
):
    """
    Determine whether a self-directed action is currently
    available to the character.

    This is separate from action scoring:
    an action may be desirable but still unavailable.
    """

    action_type = action[
        "action_type"
    ]

    hour = world[
        "hour"
    ]

    # ========================================================
    # FAMILY SHOP
    # ========================================================

    if action_type == "family_duty":

        if not (
            8 <= hour < 18
        ):
            return {
                "available": False,
                "reason":
                    "Family shop is closed",
            }

    # ========================================================
    # FAMILY SOCIAL TIME
    # ========================================================

    if (
        action_type
        == "social_family"
    ):

        if (
            0 <= hour < 6
        ):
            return {
                "available": False,
                "reason":
                    "Family is likely sleeping",
            }

    return {
        "available": True,
        "reason": None,
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

    # ========================================================
    # 5. VALUES
    # ========================================================

    value_effect = (
        calculate_value_effect(
            character,
            action,
        )
    )

    score += value_effect[
        "total_effect"
    ]

    if (
        value_effect[
            "value_relevance"
        ]
        != 1.0
    ):
        reasons.append(
            "Current value relevance: "
            f"x{value_effect['value_relevance']}"
        )

    if (
        value_effect[
            "family_bonus"
        ]
        > 0
    ):
        reasons.append(
            "Family value: "
            f"+{value_effect['family_bonus']}"
        )

    if (
        value_effect[
            "community_bonus"
        ]
        > 0
    ):
        reasons.append(
            "Community value: "
            f"+{value_effect['community_bonus']}"
        )

    if (
        value_effect[
            "honor_bonus"
        ]
        > 0
    ):
        reasons.append(
            "Honor value: "
            f"+{value_effect['honor_bonus']}"
        )

    # ========================================================
    # 6. GOAL RELEVANCE / AMBITION / DISCIPLINE
    # ========================================================

    goal_effect = (
        calculate_goal_effect(
            character,
            action,
        )
    )

    score += goal_effect[
        "total_effect"
    ]

    if (
        action[
            "action_type"
        ]
        == "train"
    ):
        reasons.append(
            "Current goal relevance: "
            f"x{goal_effect['goal_relevance']}"
        )

    if (
        goal_effect[
            "ambition_bonus"
        ]
        > 0
    ):
        reasons.append(
            "Ambition: "
            f"+{goal_effect['ambition_bonus']}"
        )

    if (
        goal_effect[
            "discipline_bonus"
        ]
        > 0
    ):
        reasons.append(
            "Discipline: "
            f"+{goal_effect['discipline_bonus']}"
        )


    # ========================================================
    # 7. RISK / RULE HESITATION
    # ========================================================

    risk_effect = (
        calculate_risk_effect(
            character,
            action,
        )
    )

    score += risk_effect[
        "total_effect"
    ]

    if (
        risk_effect[
            "risk_penalty"
        ]
        > 0
    ):
        reasons.append(
            "Rule-risk hesitation: "
            f"-{risk_effect['risk_penalty']}"
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

        "action_data":
            action,
    }


# ============================================================
# CHOOSE SELF-DIRECTED ACTION
# ============================================================


def choose_self_directed_action(
    character,
    world,
):
    """
    Choose the highest-scoring currently available
    self-directed action.

    Returns both the chosen action and diagnostic
    information about unavailable candidates.
    """

    actions = (
        generate_self_directed_actions(
            character,
        )
    )

    scored = []
    unavailable = []

    for action in actions:

        availability = (
            is_self_directed_action_available(
                character,
                world,
                action,
            )
        )

        if not availability[
            "available"
        ]:
            unavailable.append({
                "action":
                    action["name"],

                "action_type":
                    action[
                        "action_type"
                    ],

                "reason":
                    availability[
                        "reason"
                    ],
            })

            continue

        result = (
            score_self_directed_action(
                character,
                world,
                action,
            )
        )

        scored.append(
            result
        )

    if not scored:
        return {
            "chosen_action": None,
            "scored_actions": [],
            "unavailable_actions":
                unavailable,
        }

    scored.sort(
        key=lambda result:
            result["score"],
        reverse=True,
    )

    return {
        "chosen_action":
            scored[0],

        "scored_actions":
            scored,

        "unavailable_actions":
            unavailable,
    }
