"""Smooth trajectory generation

Create a trajectory using polynomial smoothing. There are three polynomial
smoothing methods implemented: linear (1st order), cubic (3rd order), and
quintic (5th order).

Functions
---------
linear_polynomial()
cubic_polynomial()
quintic_polynomial()
time_scaling()
straight_trajectory()

"""

import numpy as np
import numpy.linalg as la
from numpy.polynomial.polynomial import polyval
import scipy.linalg as sla


def linear_polynomial(t_initial: float, t_final: float) -> np.ndarray:
    """Linear polynomial smoothing

    Fit a linear polynomial between the initial and final time values
    a0 + a1 * t

    Parameters
    ----------
    t_initial (float): Initial time value
    t_final (float): Final time value

    Returns
    -------
    (np.ndarray): The coefficients of the polynomial in increasing order
                  [a0, a1]

    """

    coef_matrix = np.array([[1.0, t_initial], [1.0, t_final]])

    val = np.array([0.0, 1.0])

    return la.inv(coef_matrix) @ val


def cubic_polynomial(t_initial: float, t_final: float) -> np.ndarray:
    """Cubic polynomial smoothing

    Fit a cubic polynomial between the initial and final time values
    a0 + a1 * t + a2 * t**2 + a3 * t**3

    Parameters
    ----------
    t_initial (float): Initial time value
    t_final (float): Final time value

    Returns
    -------
    (np.ndarray): The coefficients of the polynomial in increasing order
                  [a0, a1, a2, a3]

    """

    coef_matrix = np.array(
        [
            [1.0, t_initial, t_initial**2, t_initial**3],
            [0.0, 1.0, 2.0 * t_initial, 3.0 * t_initial**2],
            [1.0, t_final, t_final**2, t_final**3],
            [0.0, 1.0, 2.0 * t_final, 3.0 * t_final**2],
        ]
    )

    val = np.array([0.0, 0.0, 1.0, 0.0])

    return la.inv(coef_matrix) @ val


def quintic_polynomial(t_initial: float, t_final: float) -> np.ndarray:
    """Quintic polynomial smoothing

    Fit a quintic polynomial between the initial and final time values
    a0 + a1 * t + a2 * t**2 + a3 * t**3 + a4 * t**4 + a5 * t**5

    Parameters
    ----------
    t_initial (float): Initial time value
    t_final (float): Final time value

    Returns
    -------
    (np.ndarray): The coefficients of the polynomial in increasing order
                  [a0, a1, a2, a3, a4, a5]

    """

    coef_matrix = np.array(
        [
            [
                1.0,
                t_initial,
                t_initial**2,
                t_initial**3,
                t_initial**4,
                t_initial**5,
            ],
            [
                0.0,
                1.0,
                2.0 * t_initial,
                3.0 * t_initial**2,
                4 * t_initial**3,
                5 * t_initial**4,
            ],
            [
                0.0,
                0.0,
                2.0,
                6.0 * t_initial,
                12.0 * t_initial**2,
                20.0 * t_initial**3,
            ],
            [1.0, t_final, t_final**2, t_final**3, t_final**4, t_final**5],
            [
                0.0,
                1.0,
                2.0 * t_final,
                3.0 * t_final**2,
                4.0 * t_final**3,
                5.0 * t_final**4,
            ],
            [0.0, 0.0, 2.0, 6.0 * t_final, 12.0 * t_final**2, 20.0 * t_final**3],
        ]
    )

    val = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0])

    return la.inv(coef_matrix) @ val


def time_scaling(poly_coefs: np.array, time: float) -> float:
    """Time scaling for the trajectory

    Map a given time value in [t_initial, t_final] to [0, 1] interval

    Parameters
    ----------
    poly_coefs (np.array): Coefficients of the smooting polynomial
    t (float): Time value to be evaluated

    Returns
    -------
    float: Time value mapped to [0, 1] interval

    """

    return polyval(time, poly_coefs)


def straight_trajectory(
    time: float, poly_coefs: np.array, initial_conf: np.array, final_conf: np.array
) -> np.array:
    """Straight trajectory in SE(3)

    Create a straight line trajectory in SE(3)

    Parameters
    ----------
    time (float): Time value
    poly_coefs (np.ndarray): Coefficients of the time scaling polynomial
    initial_conf (np.ndarray): Initial configuration in SE(3)
    final_conf (np.ndarray): Final configuration in SE(3)

    Returns
    -------
    (np.ndarray): Configuration represented in SE(3) at time t

    """

    # Map the given time to [0, 1] interval
    scaled_time = time_scaling(poly_coefs, time)

    return initial_conf @ sla.expm(
        sla.logm(la.inv(initial_conf) @ final_conf) * scaled_time
    )
