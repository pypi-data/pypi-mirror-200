import numpy as np
import math
from scipy import stats

def teg_nchoosek(x, y):
    try:
        return math.gamma(x + 1) / (math.gamma(y + 1) * math.gamma(x - y + 1))
    except:
        return 0

def teg_incomplete_beta_comb_series(x, a, b):
    # From https://dlmf.nist.gov/8.17
    N = 200
    Ix = (1-x)**b * np.sum(np.array([teg_nchoosek(b + (a+j) - 1, (a+j)) * x**(a+j) for j in range(0, N)]))
    return Ix

def teg_incomplete_beta(x, a, b):
    Ix = teg_incomplete_beta_comb_series(x, a, b)
    return Ix

def teg_cdf_f(F, df_model, df_error):
    x = df_model * F / (df_model * F + df_error)
    if F < 1:
        Ix = teg_incomplete_beta(x, df_model/2, df_error/2)
    else:
        Ix = 1 - teg_incomplete_beta(1 - x, df_error / 2, df_model / 2)
    return Ix

def get_F_p(F, df_model, df_error):
    p = 1 - teg_cdf_f(F, df_model, df_error)
    # p = 1 - stats.f.cdf(F, df_model, df_error)
    return p

def sim_data(nObs, nPred, fix_coeffs={}, fix_intercept=0):
    # Example: coeffs = {0: 1, 3: 2}
    X = np.array(np.random.rand(nObs * nPred))
    X = X.reshape((nObs, nPred))
    y = np.array(np.random.rand(nObs))
    if len(fix_coeffs) > 0:
        effects = X[:,list(fix_coeffs.keys())] @ np.array([a[1] for a in fix_coeffs.items()])
        y = y + effects
    y = y + fix_intercept
    return X, y

def get_coeffs(X, y):
    XX = X.transpose() @ X
    coeffs = np.linalg.inv(XX) @ X.transpose() @ y
    return coeffs

def get_AIC(E, k, N):
    logL = -N * np.log(np.sqrt(E)) - (N/2)*np.log(2*np.pi) - (1/(2*E)) * E*N
    AIC = -2 * logL + 2 * (k + 1)
    return AIC

def F_test_and_AIC(X, y, coeffs, Constraints):
    if len(Constraints) == 0:
        # Set all predictor coefficients to 0
        Constraints = {}
        Constraints['coefficients'] = np.identity(X.shape[1])
        Constraints['coefficients'] = Constraints['coefficients'][:-1,:]
        Constraints['constants'] = np.array([0 for r in range(Constraints['coefficients'].shape[0])])
    CM = Constraints['coefficients']
    Cv = Constraints['constants']
    XX = X.transpose() @ X
    coeffs_constr = coeffs - np.linalg.inv(XX) @ CM.transpose() @ np.linalg.inv(CM @ np.linalg.inv(XX) @ CM.transpose()) @ (CM @ coeffs - Cv)
    SSH = (coeffs - coeffs_constr).transpose() @ XX @ (coeffs - coeffs_constr)
    y_pred = X @ coeffs
    SSE = np.sum((y_pred - y) ** 2)
    nConstr = len(Cv)
    df_model = nConstr
    df_error = len(y) - len(coeffs)
    F = (SSH/df_model) / (SSE/df_error)
    p = get_F_p(F, df_model, df_error)
    # AIC
    AIC_free = get_AIC(SSE, len(coeffs), len(y))
    AIC_constrained = get_AIC(SSH, len(coeffs) - nConstr, len(y))
    return p, F, df_model, df_error, AIC_free, AIC_constrained

def run_tests(X, y, coeffs, Constraints, O):
    # Test of the whole model, versus or given constraints.
    p, F, df_model, df_error, AIC_free, AIC_constrained = F_test_and_AIC(X, y, coeffs, Constraints)
    O['p'] = p
    O['F'] = F
    O['df_model'] = df_model
    O['df_error'] = df_error
    O['AIC_free'] = AIC_free
    O['AIC_constrained'] = AIC_constrained
    # Tests per predictor
    O['coeffs_p'] = []
    O['coeffs_F'] = []
    O['coeffs_df_model'] = []
    O['coeffs_df_error']= []
    for pred in range(0, len(coeffs)):
        Temp_Constraints = {}
        Temp_Constraints['coefficients'] = np.array([0 for a in range(len(coeffs))]).reshape(1,len(coeffs))
        Temp_Constraints['coefficients'][0][pred] = 1
        Temp_Constraints['constants'] = np.array([0])
        p, F, df_model, df_error, AIC_free, AIC_constrained = F_test_and_AIC(X, y, coeffs, Temp_Constraints)
        O['coeffs_p'].append(p)
        O['coeffs_F'].append(F)
        O['coeffs_df_model'].append(df_model)
        O['coeffs_df_error'].append(df_error)
    return O

def print_report(O):
    print("Test of the model:\n\tF({:.3g},{:.3g}) = {:.3g}, p = {:.3g}".format(O['df_model'], O['df_error'], O['F'], O['p']))
    print("\tAIC constrained - free = {:.3g} (negative supports constraints).".format(O['AIC_constrained'] - O['AIC_free']))
    print("Tests per coefficient.")
    for pred in range(len(O['coeffs'])):
        p = O['coeffs_p'][pred]
        F = O['coeffs_F'][pred]
        df_model = O['coeffs_df_model'][pred]
        df_error = O['coeffs_df_error'][pred]
        if pred == len(O['coeffs']) - 1:
            print("\tIntercept: b = {:.3g}, F({:.3g},{:.3g}) = {:.3g}, p = {:.3g}".format(O['coeffs'][pred], df_model, df_error, F, p))
        else:
            print("\tPredictor {:d}: b = {:.3g}, F({:.3g},{:.3g}) = {:.3g}, p = {:.3g}".format(pred, O['coeffs'][pred], df_model, df_error, F, p))

def run_regression(X, y, Constraints={}, report=True, explicit_intercept=False):
    # By default, do not add the intercept in the input.
    # Constraints['coefficients'] is a matrix of row-wise coefficients defining contrast scores.
    # Constraints['constants'] is a vector of constants for the contrasts.
    O = {}
    # Add intercept to X
    if not explicit_intercept:
        intercept_v = np.array([1 for x in range(X.shape[0])]).reshape(X.shape[0], 1)
        X = np.hstack([X, intercept_v])
        if not len(Constraints) == 0:
            CM = Constraints['coefficients']
            constraint_column = np.array([0 for x in range(CM.shape[0])]).reshape(CM.shape[0], 1)
            Constraints['coefficients'] = np.hstack([Constraints['coefficients'], constraint_column])
    # Get coefficients
    coeffs = get_coeffs(X, y)
    O['coeffs'] = coeffs
    # Statistical tests
    O = run_tests(X, y, coeffs, Constraints, O)
    # Print out report
    if report:
        print_report(O)
    return O
