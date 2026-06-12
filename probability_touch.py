import math

def probability_of_touch(
    spot,
    strike,
    iv,
    dte=1
):

    sigma = (
        spot *
        iv *
        math.sqrt(dte / 365)
    )

    if sigma == 0:
        return 0

    z = abs(
        strike - spot
    ) / sigma

    probability = (
        2 * (
            1 - (
                0.5 * (
                    1 +
                    math.erf(
                        z /
                        math.sqrt(2)
                    )
                )
            )
        )
    )

    return round(
        probability * 100,
        2
    )