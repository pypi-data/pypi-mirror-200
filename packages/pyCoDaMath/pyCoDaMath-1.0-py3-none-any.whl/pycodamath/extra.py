# -*- coding: utf-8 -*-
''' Auxilliary functions for pyCoDaMath
'''

__author__ = "Christian Brinch"
__copyright__ = "Copyright 2019"
__credits__ = ["Christian Brinch"]
__license__ = "AFL 3.0"
__version__ = "1.0"
__maintainer__ = "Christian Brinch"
__email__ = "cbri@food.dtu.dk"

import math
import numpy as np
from matplotlib.patches import Ellipse


def sbp_basis(obj):
    ''' Define basis to use in IRL transformation '''
    dim = np.shape(obj)[1]
    psi = np.zeros([dim-1, dim])
    for i in range(dim-1):
        for j in range(dim):
            if j+1 <= dim-i-1:
                psi[i, j] = np.sqrt(1./((dim-i-1)*(dim-i)))
            elif j+1 == dim-i:
                psi[i, j] = -np.sqrt((dim-i-1)/(dim-i))

    check_basis(psi)
    return psi


def norm(balances):
    ''' Normalize a matrix of balances '''
    psi = []
    for row in balances:
        minus = sum(1 for i in row if i < 0)
        plus = sum(1 for i in row if i > 0)
        psi.append([1/plus*np.sqrt(plus*minus/(plus+minus)) if i > 0 else -1/minus *
                    np.sqrt(plus*minus/(plus+minus)) if i < 0 else 0 for i in row])

    psi = np.array(psi)
    check_basis(psi)
    return psi


def check_basis(psi):
    ''' Check if basis is orthonormal '''
    ident = np.matmul(psi, psi.T)
    if np.trace(ident) != np.shape(ident)[0]:
        raise AttributeError("Error: Basis is not normalized.")
    if np.abs(np.sum(ident-np.diag(np.diagonal(ident)))) > 1e-6:
        raise AttributeError("Error: Basis is not orthogonal.")


def points_in_ellipse(ellipse, npoints):
    ''' Return n points along the edge of an ellipse '''
    return [(ellipse['shape'][0] * math.cos(x) * math.cos(-ellipse['angle'])
             - ellipse['shape'][1] * math.sin(x)*math.sin(-ellipse['angle']) + ellipse['center'][0],
             ellipse['shape'][0] * math.cos(x) * math.sin(-ellipse['angle'])
             + ellipse['shape'][1] * math.sin(x)*math.cos(-ellipse['angle']) + ellipse['center'][1])
            for x in np.linspace(0, 2*np.pi, npoints)]


def check_point_in_ellipse(scores, ellipse):
    ''' This function takes a point and checks if it is inside or outside an
        ellipse
    '''
    xcoord = scores[0] - ellipse['center'][0]
    ycoord = scores[1] - ellipse['center'][1]

    xct = xcoord * np.cos(-ellipse['angle']) - ycoord * np.sin(-ellipse['angle'])
    yct = xcoord * np.sin(-ellipse['angle']) + ycoord * np.cos(-ellipse['angle'])

    if (xct**2/(ellipse['shape'][0])**2) + (yct**2/(ellipse['shape'][1])**2) > 1.25:
        return True
    return False


def get_covariance_ellipse(data, conf=95):
    ''' Return a covariance ellipse object '''
    if len(data.columns) > 2:
        raise AttributeError(
            ("Error: get_covariance_ellipse expects only two columns. " +
             "Got {0:d}.").format(len(data.columns)))

    lambda_, angle = np.linalg.eig(np.cov(data.loc[:, 0], data.loc[:, 1]))
    lambda_ = np.sqrt(lambda_)

    if conf == 95:
        scale = 5.991  # 95% confidence interval
    elif conf == 90:
        scale = 4.605  # 90%
    elif conf == 99:
        scale = 9.210  # 99%
    else:
        raise AttributeError(
            "Error: get_covariance_ellipse parameter conf can only accept values {90, 95, 99}.")

    return {'shape': (lambda_[0]*np.sqrt(scale), lambda_[1]*np.sqrt(scale)),
            # 'angle': np.arccos(-angle[0, 0]),
            'angle': np.arctan(angle[1, 0]/angle[0, 0]),
            'center': (np.mean(data.loc[:, 0]), np.mean(data.loc[:, 1]))}


def plot_covariance_ellipse(axis, ellipse, color=0):
    ''' plot covariance ellipse '''
    if color is None:
        color = 'black'
    ell = Ellipse(xy=ellipse['center'],
                  width=2*ellipse['shape'][0],
                  height=2*ellipse['shape'][1],
                  angle=np.rad2deg(ellipse['angle']),
                  alpha=0.5,
                  edgecolor=color,
                  fill=False,
                  lw=1.5,
                  ls='-')
    axis.add_artist(ell)
    ell = Ellipse(xy=ellipse['center'],
                  width=2*ellipse['shape'][0],
                  height=2*ellipse['shape'][1],
                  angle=np.rad2deg(ellipse['angle']),
                  alpha=0.15,
                  edgecolor=None,
                  fill=True,
                  color=color)
    axis.add_artist(ell)
