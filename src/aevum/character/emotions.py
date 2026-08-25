"""
Emotional state systems for Aevum characters.

Characters maintain a persistent emotional state that responds to
experiences, personality-based regulation, opposing emotions, and
recovery over time.
"""


# ============================================================
# EMOTIONAL RESPONSE
# ============================================================


def process_emotional_response(
    character,
    emotions,
    response_strength=1.0,
    use_regulation=True,
    suppress_opposing_emotions=True,
):
    """
    Apply an emotional response to a character's live emotional state.

    response_strength controls how much of the supplied emotional
    response reaches the character.

    When regulation is enabled, self-control reduces emotional
    spillover.

    Negative emotional activation can also temporarily suppress
    happiness and increase stress.
    """

    # --------------------------------------------------------
    # Ensure live emotional state exists
    # --------------------------------------------------------

    if "current_emotions" not in character:
        character["current_emotions"] = {
            "fear": 0,
            "anger": 0,
            "guilt": 0,
            "sadness": 0,
            "stress": 0,
            "happiness": 50,
        }

    current = character["current_emotions"]

    # --------------------------------------------------------
    # Emotional regulation
    # --------------------------------------------------------

    if use_regulation:
        self_control = character.get(
            "traits",
            {},
        ).get(
            "self_control",
            50,
        )

        regulation_factor = (
            1.0
            - (self_control / 100) * 0.40
        )

    else:
        regulation_factor = 1.0

    # --------------------------------------------------------
    # Apply supplied emotions
    # --------------------------------------------------------

    applied_emotions = {}

    negative_emotions = {
        "fear",
        "anger",
        "guilt",
        "sadness",
        "stress",
    }

    negative_activation = 0

    for emotion, intensity in emotions.items():

        if emotion not in current:
            current[emotion] = 0

        effect = (
            intensity
            * response_strength
            * regulation_factor
        )

        # Positive emotion accumulates more gently.
        if emotion == "happiness":
            effect *= 0.5

        current[emotion] += effect

        current[emotion] = round(
            min(
                max(
                    current[emotion],
                    0,
                ),
                100,
            ),
            2,
        )

        applied_emotions[emotion] = round(
            effect,
            2,
        )

        if emotion in negative_emotions:
            negative_activation += effect

    # --------------------------------------------------------
    # Emotional interaction
    # --------------------------------------------------------

    happiness_reduction = 0

    if (
        suppress_opposing_emotions
        and negative_activation > 0
    ):
        happiness_reduction = (
            negative_activation * 0.30
        )

        happiness_reduction = min(
            happiness_reduction,
            35,
        )

        current["happiness"] -= (
            happiness_reduction
        )

        current["happiness"] = round(
            min(
                max(
                    current["happiness"],
                    0,
                ),
                100,
            ),
            2,
        )

    # Negative activation also creates stress.
    stress_increase = (
        negative_activation * 0.10
    )

    current["stress"] += (
        stress_increase
    )

    current["stress"] = round(
        min(
            max(
                current["stress"],
                0,
            ),
            100,
        ),
        2,
    )

    # --------------------------------------------------------
    # Return response information
    # --------------------------------------------------------

    return {
        "applied_emotions":
            applied_emotions,

        "regulation_factor":
            round(
                regulation_factor,
                3,
            ),

        "negative_activation":
            round(
                negative_activation,
                2,
            ),

        "happiness_reduction":
            round(
                happiness_reduction,
                2,
            ),

        "stress_increase":
            round(
                stress_increase,
                2,
            ),

        "current_emotions":
            current.copy(),
    }


# ============================================================
# EMOTION RESET
# ============================================================


def reset_emotions(character):
    character["current_emotions"] = {
        "fear": 0,
        "anger": 0,
        "guilt": 0,
        "sadness": 0,
        "stress": 0,
        "happiness": 50,
    }

    print(
        f"{character['name']}'s current emotions "
        f"have been reset."
    )


# ============================================================
# INTERPRETED EMOTIONS
# ============================================================


def apply_interpreted_emotions(
    character,
    interpretation,
    intensity_multiplier=1.0,
):
    print(
        "\n--- EMOTIONAL STATE UPDATE ---"
    )

    response = process_emotional_response(
        character=character,
        emotions=interpretation["emotions"],
        response_strength=intensity_multiplier,
        use_regulation=True,
        suppress_opposing_emotions=True,
    )

    for emotion, value in (
        response["current_emotions"].items()
    ):
        print(
            f"{emotion}: {value}"
        )

    return response


# ============================================================
# EMOTIONAL RECOVERY
# ============================================================


def drift_emotions_over_time(
    character,
    hours_passed,
    sleeping=False,
):
    """
    Move emotional state gradually toward baseline.

    Awake characters recover gradually.

    Sleeping characters recover more strongly.
    """

    if "current_emotions" not in character:
        return

    emotions = character["current_emotions"]

    if sleeping:
        hourly_rate = 0.18
    else:
        hourly_rate = 0.08

    # Convert the hourly recovery rate into a safe
    # multi-hour exponential recovery rate.
    recovery_strength = (
        1
        - ((1 - hourly_rate) ** hours_passed)
    )

    for emotion, current_value in emotions.items():

        if emotion == "happiness":
            baseline = 50
        else:
            baseline = 0

        difference = (
            baseline
            - current_value
        )

        emotions[emotion] += (
            difference
            * recovery_strength
        )

        emotions[emotion] = round(
            min(
                max(
                    emotions[emotion],
                    0,
                ),
                100,
            ),
            2,
        )

    return emotions
