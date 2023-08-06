"""
Discrete First-Order Method for Classification and Regression
"""

from abc import ABCMeta, abstractmethod

import numpy as np
from scipy.linalg import lstsq
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model._base import _preprocess_data
from sklearn.utils.validation import (
    check_array,
    check_is_fitted,
    check_random_state,
    check_X_y,
)

from ._dfo_optim import LOSSES, _solve_dfo, _threshold


# TODO consider inheriting from LinearModel
class BaseDFO(BaseEstimator, metaclass=ABCMeta):
    """Base class for Discrete First Order classification and regression."""

    def __init__(
        self,
        loss,
        learning_rate="auto",
        k=1,
        polish=True,
        n_runs=50,
        max_iter=100,
        tol=1e-3,
        fit_intercept=False,
        normalize=False,
        random_state=None,
    ):
        super(BaseDFO, self).__init__()
        self.loss = loss
        self.learning_rate = learning_rate
        self.k = k
        self.polish = polish
        self.n_runs = n_runs
        self.max_iter = max_iter
        self.tol = tol
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.random_state = random_state

        # check loss
        if loss not in LOSSES.keys():
            raise NotImplementedError(f"Loss '{loss}' not implemented!")

        # check learning rate
        if isinstance(learning_rate, str):
            if learning_rate != "auto":
                raise ValueError(
                    "If learning rate is a string it must be set to 'auto'."
                )

    @abstractmethod
    def fit(self, X, y):
        """Fit model."""


class DFORegressor(RegressorMixin, BaseDFO):
    """Discrete first-order regressor.

    Parameters
    ----------
    loss : str
        type of loss to be minimized. One of 'mse' or 'mae'.

    learning_rate : str or float
        learning rate to be used.

    k : int
        number of non-zero features to keep.

    polish : bool
        whether to polish coefficients by running least
        squares on the active set.

    n_runs : int
        number of runs of the discrete first order optimization procedure.

    max_iter : int
        maximum number of steps to take during one run
        of the discrete first order optimization algorithm.

    tol : float
        tolerance below which the optimization algorithm stops.

    fit_intercept : bool
        whether to fit an intercept term

    normalize : bool
        whether to normalize the input data.

    Attributes
    ----------
    coef_ : ndarray, shape (n_features,)
        coefficient vector.

    intercept_ : float
        intercept.

    Examples
    --------
    >>> from discretefirstorder import DFORegressor
    >>> import numpy as np
    >>> X = np.arange(100).reshape(100, 1)
    >>> y = np.random.normal(size=(100, ))
    >>> estimator = DFORegressor()
    >>> estimator.fit(X, y)
    DFORegressor()
    """

    def __init__(
        self,
        loss="mse",
        learning_rate="auto",
        k=1,
        polish=True,
        n_runs=50,
        max_iter=100,
        tol=1e-3,
        fit_intercept=True,
        normalize=True,
        random_state=None,
    ):
        super(DFORegressor, self).__init__(
            loss=loss,
            learning_rate=learning_rate,
            k=k,
            polish=polish,
            n_runs=n_runs,
            max_iter=max_iter,
            tol=tol,
            fit_intercept=fit_intercept,
            normalize=normalize,
            random_state=random_state,
        )

    def _set_intercept(self, X_offset, y_offset, X_scale):
        """Set intercept (adapted from sklearn LinearModel)

        Parameters
        ----------
        X_offset : ndarray of shape (n_features,)
            average (offset) value of each feature

        y_offset : float
            average (offset) target value

        X_scale : ndarray of shape (n_features,)
            scale of each feature
        """
        if self.fit_intercept:
            self.coef_ = np.divide(self.coef_, X_scale)
            self.intercept_ = y_offset - np.dot(X_offset, self.coef_.T)
        else:
            self.intercept_ = 0.0

    # noinspection PyAttributeOutsideInit
    def fit(self, X, y, coef_init=None):
        """Implementation of the fit method for the discrete first-order regressor.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            the training input samples.
        y : array-like of shape (n_samples,)
            the target values.
        coef_init : (optional) array-like of shape (n_features,)
            initial value of regression coefficients

        Returns
        -------
        self : object
            Returns self.
        """
        # check that X and y have correct shape
        X, y = check_X_y(X, y)
        n_samples, n_features = X.shape

        # other checks
        if self.k > X.shape[1]:
            raise ValueError(
                f"Parameter k with value {self.k} is greater than input number of features."
            )

        self.random_state_ = check_random_state(self.random_state)

        # preprocess data (center and scale)
        # this is like in other linear models
        # by default we expect fit_intercept = False and normalize = False
        # therefore no preprocessing
        X, y, X_offset, y_offset, X_scale = _preprocess_data(
            X, y, self.fit_intercept, self.normalize
        )

        # init coefficients
        if coef_init is None:
            # regardless of X.shape[1] we rely on scipy's routine
            # for undetermined cases, it will use the pseudo inverse of X.T X
            coef_init, _, _, _ = lstsq(X, y)
            coef_init = _threshold(coef_init, self.k)

        # optimize
        objective = float("inf")
        coef = coef_init
        coef_init_temp = coef_init
        n_iter = None

        for _ in range(self.n_runs):
            coef_temp, objective_temp, n_iter_temp = _solve_dfo(
                coef=coef_init_temp,
                X=X,
                y=y,
                learning_rate=self.learning_rate,
                k=self.k,
                loss_type=self.loss,
                polish=self.polish,
                max_iter=self.max_iter,
                tol=self.tol,
            )
            if objective_temp < objective:
                coef = coef_temp
                objective = objective_temp
                n_iter = n_iter_temp

            coef_init_temp = coef_init + (
                2
                * self.random_state_.rand(n_features)
                * np.max(np.abs(coef_init))
            )

        # coefficients for scaled features
        self.coef_ = coef
        # TODO consider using LinearModel's _set_intercept
        # rescale coefficients and set intercept
        self._set_intercept(X_offset, y_offset, X_scale)

        self.n_iter_ = n_iter

        # add fitted flag
        self.is_fitted_ = True

        return self

    def predict(self, X):
        """Implementation of a prediction for the discrete first-order regressor.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The output corresponding to each input sample
        """
        # check is fit had been called
        check_is_fitted(self, ["coef_", "intercept_"])

        # input validation
        X = check_array(X)

        return X @ self.coef_ + self.intercept_
