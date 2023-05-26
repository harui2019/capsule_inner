import numpy as np
from typing import Union

def quantitiesMean(
    quantities: list[dict[str, float]],
) -> dict[str, float]:
    """Averaging a list of quantities.

    Args:
        quantities (list[dict[str, float]]): List of quantities.

    Returns:
        dict[str, float]: Mean of quantities.
    """
    
    combined = {}
    if len(quantities) > 0:
        for k in quantities[0]:
            if 'SD' in k:
                tmp = [v[k]**2 for v in quantities]
                sample_num = len(tmp)
                # combined[k] = np.sqrt(sum([v**2 for v in tmp]) / sample_num)
            elif 'CellList' in k:
                tmp = []
                for v in quantities:
                    tmp += v[k]
                combined[k.replace('CellList', 'SD')] = np.std(tmp)
            else:
                combined[k] = np.mean([v[k] for v in quantities])
        
    return combined


def tagListQuantityMean(
    tagListQuantities: dict[str, list[ dict[str, float]]],
) -> dict[str, dict[str, float]]:
    """Averaging the quantities in a :cls:`tagList`.

    Args:
        tagListQuantities (tagList): tagListQuantities.

    Returns:
        dict[str, dict[str, float]]: Mean of quantities.
    """
    return {k: quantitiesMean(v) for k, v in tagListQuantities.items()}


def Q(
    quantityComplex: Union[list[dict[str, float]], dict[str, list[dict[str, float]]]]
) -> Union[dict[str, float], dict[str, dict[str, float]], any]:
    """Averaging a list of quantities or the quantities in a :cls:`tagList`.

    Args:
        quantityComplex (Union[list[dict[str, float]], dict[str, list[dict[str, float]]]]): List of quantities or tagListQuantities.

    Returns:
        Union[dict[str, float], dict[str, dict[str, float]], any]: Mean of quantities.
    """
    if isinstance(quantityComplex, dict):
        return tagListQuantityMean(quantityComplex)
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
    