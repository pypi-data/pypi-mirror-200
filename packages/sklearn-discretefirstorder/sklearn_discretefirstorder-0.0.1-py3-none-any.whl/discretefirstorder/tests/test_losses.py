"""
Test losses
"""

from discretefirstorder._losses import MSELoss


def test_mse_loss():
    """Test MSELoss"""
    import numpy as np

    y = np.array([2, 0, -1, 10])
    X = np.array([[1, 2], [-1, 0], [1, -1], [8, 3]])
    coef = np.array([1, 1])

    loss = MSELoss()
    loss_value = 2.0
    gradient_value = np.array([11, 4])

    assert loss.loss(coef, X, y) == loss_value
    assert np.array_equal(loss.gradient(coef, X, y), gradient_value)
