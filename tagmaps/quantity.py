import numpy as np
from typing import Union

# from ...qurrium.type import Quantity

Quantity = dict[str, float]

def quantitiesMean(
    quantities: list[Quantity],
) -> Quantity:
    """Averaging a list of quantities.

    Args:
        quantities (list[Quantity]): List of quantities.

    Returns:
        Quantity: Mean of quantities.
    """
    return {} if len(quantities) == 0 else {k: np.mean([q[k] for q in quantities]) for k in quantities[0]}


def tagMapQuantityMean(
    tagMapQuantities: dict[str, list[Quantity]],
) -> dict[str, Quantity]:
    """Averaging the quantities in a :cls:`tagMap`.

    Args:
        tagMapQuantities (tagMap): tagMapQuantities.

    Returns:
        dict[str, Quantity]: Mean of quantities.
    """
    return {k: quantitiesMean(v) for k, v in tagMapQuantities.items()}


def Q(
    quantityComplex: Union[list[Quantity], dict[str, list[Quantity]]]
) -> Union[Quantity, dict[str, Quantity], any]:
    """Averaging a list of quantities or the quantities in a :cls:`tagMap`.

    Args:
        quantityComplex (Union[list[Quantity], dict[str, list[Quantity]]]): List of quantities or tagMapQuantities.

    Returns:
        Union[Quantity, dict[str, Quantity], any]: Mean of quantities.
    """
    if isinstance(quantityComplex, dict):
        if 'noTags' in quantityComplex:
            return tagMapQuantityMean(quantityComplex)
    elif isinstance(quantityComplex, list):
        if len(quantityComplex) > 0:
            if isinstance(quantityComplex[0], dict):
                return quantitiesMean(quantityComplex)
    else:
        return quantityComplex
    