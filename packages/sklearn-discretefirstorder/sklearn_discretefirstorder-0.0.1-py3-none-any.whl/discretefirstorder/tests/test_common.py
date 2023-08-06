"""
Test common
"""

import pytest
from sklearn.utils.estimator_checks import check_estimator

from discretefirstorder import DFORegressor


@pytest.mark.parametrize("estimator", [DFORegressor()])
def test_all_estimators(estimator):
    """Standard scikit-learn estimator checks"""
    return check_estimator(estimator)
