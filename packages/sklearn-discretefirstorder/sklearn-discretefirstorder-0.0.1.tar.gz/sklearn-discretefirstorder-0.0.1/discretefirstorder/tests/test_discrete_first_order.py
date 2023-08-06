"""
Test estimators
"""

import pytest
from sklearn.datasets import load_iris, load_diabetes

from discretefirstorder import DFORegressor


@pytest.fixture
def iris_data():
    """Load Iris dataset for testing"""
    return load_iris(return_X_y=True)


@pytest.fixture
def diabetes_data():
    """Load diabetes dataset for testing"""
    return load_diabetes(return_X_y=True)


def test_dfo_regressor_default():
    """Test DFORegressor default params"""
    reg = DFORegressor()
    assert reg.loss == "mse"
    assert reg.learning_rate == "auto"
    assert reg.k == 1
    assert reg.polish is True
    assert reg.n_runs == 50
    assert reg.max_iter == 100
    assert reg.tol == 1e-3
    assert reg.fit_intercept is True
    assert reg.normalize is True


def test_dfo_regressor():
    """Test DFORegressor params"""
    reg = DFORegressor(
        learning_rate=0.001,
        k=5,
        polish=False,
        n_runs=25,
        max_iter=50,
        tol=1e-4,
        fit_intercept=False,
        normalize=False,
    )
    assert reg.loss == "mse"
    assert reg.learning_rate == 0.001
    assert reg.k == 5
    assert reg.polish is False
    assert reg.n_runs == 25
    assert reg.max_iter == 50
    assert reg.tol == 1e-4
    assert reg.fit_intercept is False
    assert reg.normalize is False


def test_dfo_regressor_fit(iris_data):
    """Test DFORegressor fit method"""
    reg = DFORegressor()
    reg.fit(*iris_data)
    assert hasattr(reg, "is_fitted_")


def test_invalid_loss():
    """Test invalid loss"""
    with pytest.raises(NotImplementedError):
        _ = DFORegressor(loss="myloss")


def test_invalid_value_learning_rate():
    """Test invalid string value for learning rate"""
    with pytest.raises(ValueError):
        _ = DFORegressor(learning_rate="myrate")


def test_invalid_k(iris_data):
    """Test invalid k given data"""
    with pytest.raises(ValueError):
        reg = DFORegressor(k=10)  # n_features = 4
        reg.fit(*iris_data)
