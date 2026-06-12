import math

def estimate_pop(
    spot,
    breakeven,
    expected_move
):

    if expected_move <= 0:
        return 50

    z = (
        breakeven - spot
    ) / expected_move

    pop = (
        0.5 *
        (
            1 +
            math.erf(
                z /
                math.sqrt(2)
            )
        )
    ) * 100

    return round(pop, 1)