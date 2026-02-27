"""
This file contains all functions used in the fitting algorithm dofitPython
The algorithm fits a multi-modal lognormal distribution to a particle number size distribution
The algorithm is adapted form the MATLAB code written by Tareq Hussein in September 2006
https://www.borenv.net/BER/archive/pdfs/ber10/ber10-337.pdf

This code is the version 2.0 of the Python implementation of the algorithm.
New features:
- multiprocessing for parallel processing of data
- improved performance and stability
- reduced memory usage

Written by ThÃ©odore Khadir, May 2024
Contact info: theodore.khadir@aces.su.se
"""

import numpy as np
from scipy import interpolate
import warnings
warnings.filterwarnings("ignore")

def main_fit(Dp, distrib, tol_1n=0.010, tol_2n=0.005, finescanning='yes', N_coarse=10, N_fine=8):
    """
    Run the fitting algorithm to fit a multi-modal lognormal distribution to the data.

    Parameters:
    Dp (array): Particle diameters.
    distrib (array): Distribution values corresponding to the particle diameters.
    tol_1n (float): Tolerance for reducing 2 modes to 1 mode.
    tol_2n (float): Tolerance for reducing 3 modes to 2 modes.
    finescanning (str): Whether to perform fine scanning ('yes' or 'no').
    N_coarse (int): Number of steps in the coarse scan.
    N_fine (int): Number of steps in the fine scan.

    Returns:
    list: Fitted model parameters.
    """
    model_param = fit_3_modes(Dp, distrib, finescanning, N_coarse=N_coarse, N_fine=N_fine)
    model_param = eliminate_null_modes(model_param)
    model_param = reduce_modes(Dp, model_param, tol_1n, tol_2n, distrib)
    return model_param

def fit_3_modes(Dp, distrib, finescanning, N_coarse=10, N_fine=8):
    """
    Fit the distribution using a 3-mode lognormal distribution.

    Parameters:
    Dp (array): Particle diameters.
    distrib (array): Distribution values.
    finescanning (str): Whether to perform fine scanning ('yes' or 'no').
    N_coarse (int): Number of steps in the coarse scan.
    N_fine (int): Number of steps in the fine scan.

    Returns:
    list: Fitted model parameters for 3 modes.
    """
    model_param = fit_modes(Dp, distrib, 3, finescanning, N_coarse=N_coarse, N_fine=N_fine)
    return model_param

def fit_modes(Dp, distrib, num_modes, finescanning, N_coarse=10, N_fine=8):
    """
    Fit the distribution using a specified number of modes.

    Parameters:
    Dp (array): Particle diameters.
    distrib (array): Distribution values.
    num_modes (int): Number of modes to fit.
    finescanning (str): Whether to perform fine scanning ('yes' or 'no').
    N_coarse (int): Number of steps in the coarse scan.
    N_fine (int): Number of steps in the fine scan.

    Returns:
    list: Fitted model parameters.
    """
    N = N_coarse
    sig = np.array([1.5] * num_modes)

    # Define the diameter ranges for each mode
    Dp_min = np.array([2, 35, 90][:num_modes]) * 1e-9
    Dp_max = np.array([20, 70, 200][:num_modes]) * 1e-9  # Adjust these ranges as necessary

    Dpg, sig, Ntot, limit, LIMIT, dlogDpg = scan_params(distrib, Dp, N, np.inf, np.inf, sig, Dp_min, Dp_max, num_modes)

    if finescanning == 'yes':
        N = N_fine
        for _ in range(2):
            Dp_min = 10 ** (np.log10(Dpg) - np.array([6, 3, 1][:num_modes]) * dlogDpg)
            Dp_max = 10 ** (np.log10(Dpg) + np.array([4, 4, 6][:num_modes]) * dlogDpg)
            Dpg, sig, Ntot, limit, LIMIT = fine_fit(distrib, Dp, N, limit, LIMIT, Dpg, sig, Ntot, Dp_min, Dp_max, num_modes)

    return [Dpg, sig, Ntot]

def scan_params(distrib, Dp, N, limit_, LIMIT_, sig_, Dp_min, Dp_max, num_modes):
    """
    Scan for the best parameters by exploring the parameter space.

    Parameters:
    distrib (array): Distribution values.
    Dp (array): Particle diameters.
    N (int): Number of steps for scanning.
    limit_ (float): Initial limit for variance.
    LIMIT_ (float): Upper limit for variance.
    sig_ (array): Initial guess for the sigma (spread) of the modes.
    Dp_min (array): Minimum diameter for each mode.
    Dp_max (array): Maximum diameter for each mode.
    num_modes (int): Number of modes to fit.

    Returns:
    list: Best-fit parameters and their variances.
    """
    dlogDpg = np.zeros(num_modes) * np.nan
    Dpg_list = [np.logspace(np.log10(Dp_max[i]), np.log10(Dp_min[i]), N) for i in range(num_modes)]
    for i in range(num_modes):
        dlogDpg[i] = np.log10(Dpg_list[i][1]) - np.log10(Dpg_list[i][0])

    limit = limit_
    LIMIT = LIMIT_
    A = np.zeros((num_modes, num_modes)) * np.nan
    F = np.zeros((num_modes, 1)) * np.nan

    # Initialize Dpg and Ntot with default values
    Dpg = np.zeros(num_modes) * np.nan
    Ntot = np.zeros((num_modes, 1)) * np.nan
    sig = sig_

    for indices in np.ndindex((N,) * num_modes):
        A_list = [lognorm_dist(Dpg_list[i][indices[i]], sig_[i], Dp) for i in range(num_modes)]
        for i in range(num_modes):
            A[i, i] = np.sum(A_list[i] ** 2)
            F[i, 0] = np.sum(distrib * A_list[i])
            for j in range(i):
                A[i, j] = A[j, i] = np.sum(A_list[i] * A_list[j])

        try:
            Ntot_ = np.linalg.inv(A).dot(F)
        except np.linalg.LinAlgError:
            # Regularization: Add a small value to the diagonal
            A += np.eye(num_modes) * 1e-10
            try:
                Ntot_ = np.linalg.inv(A).dot(F)
            except np.linalg.LinAlgError:
                # Use pseudo-inverse as a fallback
                Ntot_ = np.linalg.pinv(A).dot(F)

        if all(Ntot_ >= 0):
            variance = np.sqrt(np.sum(((np.sum([Ntot_[i] * A_list[i] for i in range(num_modes)], axis=0) - distrib) ** 2) / np.size(Dp)))
            if variance <= limit:
                limit = variance
                Dpg = [Dpg_list[i][indices[i]] for i in range(num_modes)]
                Ntot = Ntot_
                sig = sig_

    return [Dpg, sig, Ntot, limit, LIMIT, dlogDpg]

def fine_fit(distrib, Dp, N, limit, LIMIT, Dpg, sig, Ntot, Dp_min, Dp_max, num_modes):
    """
    Fine-tune the fitting parameters by narrowing down the parameter space.

    Parameters:
    distrib (array): Distribution values.
    Dp (array): Particle diameters.
    N (int): Number of steps for fine scanning.
    limit (float): Current best limit for variance.
    LIMIT (float): Upper limit for variance.
    Dpg (array): Current best guess for the mode diameters.
    sig (array): Current best guess for the mode sigmas.
    Ntot (array): Current best guess for the mode concentrations.
    Dp_min (array): Minimum diameter for each mode in fine scanning.
    Dp_max (array): Maximum diameter for each mode in fine scanning.
    num_modes (int): Number of modes to fit.

    Returns:
    list: Refined fit parameters and their variances.
    """
    Dpg_list = [np.logspace(np.log10(Dp_max[i]), np.log10(Dp_min[i]), N) for i in range(num_modes)]
    sig_min, sig_max, dsig = 1.1, 2.1, 0.05
    sig_list = [np.arange(sig_min, sig_max + dsig, dsig) for _ in range(num_modes)]

    Dpg, sig, Ntot, limit, LIMIT = iterate_params(Dpg, sig, Ntot, N, limit, LIMIT, Dp, distrib, Dpg_list, sig_list, num_modes, 'Dpg')
    Dpg, sig, Ntot, limit, LIMIT = iterate_params(Dpg, sig, Ntot, N, limit, LIMIT, Dp, distrib, Dpg_list, sig_list, num_modes, 'sig')

    return [Dpg, sig, Ntot, limit, LIMIT]

def iterate_params(Dpg, sig, Ntot, N, limit, LIMIT, Dp, distrib, Dpg_list, sig_list, num_modes, param_type):
    """
    Iterate over parameters to find the best fit by adjusting one parameter type at a time.

    Parameters:
    Dpg (array): Current best guess for the mode diameters.
    sig (array): Current best guess for the mode sigmas.
    Ntot (array): Current best guess for the mode concentrations.
    N (int): Number of steps for scanning.
    limit (float): Current best limit for variance.
    LIMIT (float): Upper limit for variance.
    Dp (array): Particle diameters.
    distrib (array): Distribution values.
    Dpg_list (list of arrays): List of possible diameters for each mode.
    sig_list (list of arrays): List of possible sigmas for each mode.
    num_modes (int): Number of modes to fit.
    param_type (str): Parameter type to iterate ('Dpg' or 'sig').

    Returns:
    list: Best-fit parameters and their variances after iteration.
    """
    A = np.zeros((num_modes, num_modes)) * np.nan
    F = np.zeros((num_modes, 1)) * np.nan

    for indices in np.ndindex((N,) * num_modes):
        if param_type == 'Dpg':
            A_list = [lognorm_dist(Dpg_list[i][indices[i]], sig[i], Dp) for i in range(num_modes)]
        else:
            A_list = [lognorm_dist(Dpg[i], sig_list[i][indices[i]], Dp) for i in range(num_modes)]

        for i in range(num_modes):
            A[i, i] = np.sum(A_list[i] ** 2)
            F[i, 0] = np.sum(distrib * A_list[i])
            for j in range(i):
                A[i, j] = A[j, i] = np.sum(A_list[i] * A_list[j])

        try:
            Ntot_ = np.linalg.inv(A).dot(F)
        except np.linalg.LinAlgError:
            # Regularization: Add a small value to the diagonal
            A += np.eye(num_modes) * 1e-10
            try:
                Ntot_ = np.linalg.inv(A).dot(F)
            except np.linalg.LinAlgError:
                # Use pseudo-inverse as a fallback
                Ntot_ = np.linalg.pinv(A).dot(F)

        if all(Ntot_ >= 0):
            variance = np.sqrt(np.sum(((np.sum([Ntot_[i] * A_list[i] for i in range(num_modes)], axis=0) - distrib) ** 2) / np.size(Dp)))
            if variance <= limit:
                limit = variance
                if param_type == 'Dpg':
                    Dpg = [Dpg_list[i][indices[i]] for i in range(num_modes)]
                else:
                    sig = [sig_list[i][indices[i]] for i in range(num_modes)]
                Ntot = Ntot_

    return [Dpg, sig, Ntot, limit, LIMIT]

def lognorm_dist(Dpg, sig, Dp):
    """
    Generate a lognormal distribution.

    Parameters:
    Dpg (float): Geometric mean diameter of the mode.
    sig (float): Geometric standard deviation of the mode.
    Dp (array): Particle diameters.

    Returns:
    array: Lognormal distribution values.
    """
    return 0.39894228 / np.log10(sig) * np.exp(-0.5 * (np.log10(Dp) - np.log10(Dpg)) ** 2 / (np.log10(sig) ** 2))

def eliminate_null_modes(model_param):
    """
    Eliminate modes with null or negative concentration.

    Parameters:
    model_param (list): Fitted model parameters.

    Returns:
    list: Model parameters with null or negative modes eliminated.
    """
    model_param[2] = np.where(model_param[2] <= 0, np.nan, model_param[2])
    return model_param

def reduce_modes(Dp, model_param, tol_1n, tol_2n, distrib):
    """
    Reduce the number of modes if some modes are overlapping.

    Parameters:
    Dp (array): Particle diameters.
    model_param (list): Fitted model parameters.
    tol_1n (float): Tolerance for reducing 2 modes to 1 mode.
    tol_2n (float): Tolerance for reducing 3 modes to 2 modes.
    distrib (array): Distribution values.

    Returns:
    list: Reduced model parameters.
    """
    model_param = reduce_3_to_2_modes(Dp, model_param, tol_2n, distrib)
    if model_param[2].size == 2:
        model_param = reduce_2_to_1_mode(Dp, model_param, tol_1n, distrib)
    return model_param

def reduce_3_to_2_modes(Dp, model_param, tol_2n, distrib):
    """
    Check and reduce 3 modes to 2 modes if overlapping.

    Parameters:
    Dp (array): Particle diameters.
    model_param (list): Fitted model parameters.
    tol_2n (float): Tolerance for reducing 3 modes to 2 modes.
    distrib (array): Distribution values.

    Returns:
    list: Model parameters after reducing to 2 modes, if applicable.
    """
    if check_overlap(model_param[0][0], model_param[1][0], model_param[2][0], model_param[0][1], model_param[1][1], model_param[2][1]) or \
       check_overlap(model_param[0][1], model_param[1][1], model_param[2][1], model_param[0][2], model_param[1][2], model_param[2][2]):
        model_param_2 = fit_modes(Dp, distrib, 2, 'no')

        # Check the length before accessing the elements
        if len(model_param_2) > 3 and model_param_2[3] <= model_param[3] * (1 + tol_2n):
            return model_param_2

    return model_param

def reduce_2_to_1_mode(Dp, model_param, tol_1n, distrib):
    """
    Check and reduce 2 modes to 1 mode if overlapping.

    Parameters:
    Dp (array): Particle diameters.
    model_param (list): Fitted model parameters.
    tol_1n (float): Tolerance for reducing 2 modes to 1 mode.
    distrib (array): Distribution values.

    Returns:
    list: Model parameters after reducing to 1 mode, if applicable.
    """
    if check_overlap(model_param[0][0], model_param[1][0], model_param[2][0], model_param[0][1], model_param[1][1]):
        model_param_1 = fit_modes(Dp, distrib, 1, 'no')
        if model_param_1[3] <= model_param[3] * (1 + tol_1n):
            return model_param_1
    return model_param

def check_overlap(Dpg1, sig1, N1, Dpg2, sig2, N2):
    """
    Check if two modes are overlapping based on their parameters.

    Parameters:
    Dpg1, Dpg2 (float): Geometric mean diameters of the modes.
    sig1, sig2 (float): Geometric standard deviations of the modes.
    N1, N2 (float): Concentrations of the modes.

    Returns:
    bool: True if modes are overlapping, False otherwise.
    """
    sig = [sig1, sig2] if sig1 > sig2 else [sig2, sig1]
    Dpg = [Dpg1, Dpg2] if sig1 > sig2 else [Dpg2, Dpg1]
    N = [N1, N2] if sig1 > sig2 else [N2, N1]

    N21_min = np.array([
        [np.nan, 1.00, 0.95, 0.90, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.52],
        [0.03620, np.nan, np.nan, np.nan, np.nan, 30, 10, 5, 3, 1, 0],
        [0.10862, np.nan, np.nan, 60, 40, 30, 10, 6, 3, 1, 0],
        [0.18103, np.nan, np.nan, 80, 35, 20, 10, 7, 3, 2, 0],
        [0.25345, np.nan, np.nan, 90, 30, 15, 9, 7, 4, 2, 0],
        [0.32586, np.nan, np.nan, 80, 25, 15, 7, 7, 4, 2, 0],
        [0.39828, 8, 10, 30, 20, 15, 7, 7, 3, 2, 0],
        [0.47069, 3, 5, 10, 10, 8, 5, 5, 3, 2, 0],
        [0.54310, 2, 3, 5, 8, 6, 5, 5, 2, 1, 0],
        [0.61552, 1, 2, 3, 5, 5, 5, 3, 2, 1, 0],
        [0.68793, 0, 1, 2, 3, 3, 3, 2, 1, 0, 0],
        [0.76034, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0],
        [0.83276, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0.90517, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.97759, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1.05000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    sig21 = sig[1] / sig[0]
    N21 = N[1] / N[0]
    logD21 = abs(np.log10(Dpg[1] / Dpg[0]))

    X, Y = N21_min[0, 1:], N21_min[1:, 0]
    V = N21_min[1:, 1:] / 100
    f = interpolate.interp2d(X, Y, V, kind='linear')
    constrain = f(sig21, logD21)

    if logD21 < N21_min[1, 0]:
        return True
    elif sig21 in N21_min[0, 1:] and logD21 in N21_min[1:, 0]:
        if not np.isnan(constrain).any() and N21 >= constrain:
            return False
        return True
    elif logD21 > N21_min[-1, 0]:
        return False
    return True

# Wrapper function for multiprocessing
def process_row(row):
    """
    Wrapper function for processing a row of data in multiprocessing.

    Parameters:
    row (list): A row of data containing Index, particle diameters, and distribution values.

    Returns:
    list: Index and the first three fitted model parameters.
    """
    Index, Dp, distrib = row
    return [Index] + main_fit(Dp, distrib, tol_1n=0.010, tol_2n=0.1, finescanning='yes', N_coarse=10, N_fine=8)[0:3]
