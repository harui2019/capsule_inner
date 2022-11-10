import numpy as np
from typing import Union

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
    
    combined = {}
    if len(quantities) > 0:
        for k in quantities[0]:
            if 'SD' in k:
                tmp = [v[k]**2 for v in quantities]
                sample_num = len(tmp)
                combined[k] = np.sqrt(sum([v**2 for v in tmp]) / sample_num)
            else:
                combined[k] = np.mean([v[k] for v in quantities])
        
    return combined


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
        return tagMapQuantityMean(quantityComplex)
    elif isinstance(quantityComplex, list):
        if len(quantityComplex) > 0:
            if all(isinstance(v, dict) for v in quantityComplex):
                return quantitiesMean(quantityComplex)
            else:
                return quantityComplex
        else:
            return quantityComplex
    else:
        return quantityComplex
    