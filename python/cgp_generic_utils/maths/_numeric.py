"""
library of numeric functions
"""

# imports python
import decimal


def clamp(value, minimumValue, maximumValue):
    """clamp the value between the minimum and the maximum value

    :param value: the value to clamp
    :type value: int or float

    :param minimumValue: the minimum value of the clamp
    :type minimumValue: int or float

    :param maximumValue: the maximum value of the clamp
    :type maximumValue: int or float

    :return: the clamped value
    :rtype: int or float
    """

    # errors
    if not minimumValue < maximumValue:
        raise RuntimeError('minimumValue is not strictly inferior to maximumValue')

    # execute
    return max(minimumValue, min(maximumValue, value))


def roundValue(value, decimalCount):
    """round the value to the count of decimals

    :param value: the value to round
    :type value: float

    :param decimalCount: the count of decimal to round for
    :type decimalCount: int

    :return: the rounded value
    :rtype: float
    """

    # return
    return decimal.Decimal(str(round(value, decimalCount)))
