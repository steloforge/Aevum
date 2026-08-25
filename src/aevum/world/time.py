def advance_time(world, hours=1):
    world["hour"] += hours

    while world["hour"] >= 24:
        world["hour"] -= 24
        world["day"] += 1

    print(
        f"Aevum Time -> Day {world['day']}, "
        f"{world['hour']:02d}:00"
    )


def get_time_period(world):
    hour = world["hour"]

    if 5 <= hour < 9:
        return "early_morning"

    elif 9 <= hour < 12:
        return "morning"

    elif 12 <= hour < 17:
        return "afternoon"

    elif 17 <= hour < 21:
        return "evening"

    elif 21 <= hour < 24:
        return "night"

    else:
        return "late_night"
