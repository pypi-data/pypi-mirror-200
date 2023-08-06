"""
Test DFO algorithm and functions
"""

import pytest

from discretefirstorder._dfo_optim import (
    _threshold,
    _solve_dfo,
    _calculate_learning_rate,
)


def test_threshold():
    """Test _threshold"""
    import numpy as np

    arr = np.array([-10, 5, 1, 3, -4, 8, 2])
    out = np.array([-10, 5, 0, 0, 0, 8, 0])
    assert np.array_equal(_threshold(arr, 3), out)


def test_threshold_warning():
    """Test threshold warning"""
    import numpy as np

    with pytest.warns(UserWarning):
        arr = np.array([1, 2, 3, 4, 5])
        k = 6
        _ = _threshold(arr, k)


def test_calculate_learning_rate():
    """Test _calculate_learning_rate"""
    import numpy as np

    X = np.diag([1, 2, 4])
    assert _calculate_learning_rate(X) == 0.0625


def test_not_implemented_learning_rate():
    """Test not implemented learning rate in _solve_dfo"""
    import numpy as np

    with pytest.raises(NotImplementedError):
        params = dict(
            coef=np.array([1, 1]),
            X=np.array([[1, 2], [-1, 0], [1, -1], [8, 3]]),
            y=np.array([1, 1]),
            learning_rate="myrate",  # not implemented,
            k=1,
            loss_type="mse",
            polish=True,
            max_iter=10,
            tol=1e-3,
        )
        _solve_dfo(**params)


def test_invalid_type_learning_rate():
    """Test invalid type learning rate in _solve_dfo"""
    import numpy as np

    with pytest.raises(TypeError):
        params = dict(
            coef=np.array([1, 1]),
            X=np.array([[1, 2], [-1, 0], [1, -1], [8, 3]]),
            y=np.array([1, 1]),
            learning_rate=True,  # invalid type
            k=1,
            loss_type="mse",
            polish=True,
            max_iter=10,
            tol=1e-3,
        )
        _solve_dfo(**params)
