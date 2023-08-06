# -*- coding: utf-8 -*-
''' CoDa related extensions to pandas dataframes
'''

__author__ = "Christian Brinch"
__copyright__ = "Copyright 2019"
__credits__ = ["Christian Brinch"]
__license__ = "AFL 3.0"
__version__ = "1.0"
__maintainer__ = "Christian Brinch"
__email__ = "cbri@food.dtu.dk"

import pandas as pd
import numpy as np
import scipy.stats as ss
import scipy.special as sp
from pycodamath import extra


def _clr_internal(obj):
    return (np.log(obj.T) - np.mean(np.log(obj.T), axis=0)).T


def _alr_internal(obj):
    return pd.DataFrame(np.log(obj.T/obj.T.loc[obj.columns[-1]])).T.iloc[:, :-1]


def _ilr_internal(obj, psi):
    return pd.DataFrame(np.dot(_clr_internal(obj), psi.T), index=obj.index)


def _ilr_inv_internal(obj, psi):
    return pd.DataFrame(np.exp(np.matmul(obj.values, psi)))


def init():
    ''' Initialize CoDa extension '''
    @ pd.api.extensions.register_dataframe_accessor("coda")
    class _:
        ''' A CoDa extension to pandas objects containing counts '''

        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def _check_for_zeros(self):
            if not self._obj.values.all():
                print("Dataframe contains zeros. Using Bayesian inference to replace zeros.")
                return True
            return False

        def clr(self):
            ''' Wrapper for CLR '''
            if self._check_for_zeros():
                return _clr_internal(self.aitchison_mean())

            return _clr_internal(self._obj)

        def clr_std(self, n_samples=5000):
            ''' Wrapper for CLR bayesian error estimate'''
            logratio = pd.DataFrame(index=self._obj.columns)
            for column in self._obj.T:
                p_matrix = ss.dirichlet.rvs(self._obj.T[column]+0.5, n_samples)
                c_matrix = _clr_internal(p_matrix)
                logratio[column] = [np.std(i) for i in zip(*c_matrix)]
            return logratio.T

        def alr(self, part=None):
            ''' Wrapper for ALR '''
            if part:
                parts = self._obj.T.index.tolist()
                parts.remove(part)
                self._obj = self._obj.T.reindex(parts+[part]).T

            print("Using "+self._obj.columns[-1] + " as denominator.")
            if self._check_for_zeros():
                return _alr_internal(self.aitchison_mean())

            return _alr_internal(self._obj)

        def alr_std(self, part=None, n_samples=5000):
            ''' Wrapper for ALR error estimate'''
            if part:
                parts = self._obj.index.tolist()
                parts.remove(part)
                self._obj.reindex(parts+[part])

            logratio = pd.DataFrame(index=self._obj.columns)
            for column in self._obj.T:
                p_matrix = ss.dirichlet.rvs(self._obj.T[column]+0.5, n_samples)
                c_matrix = [np.log(i/i[-1]) for i in p_matrix]
                logratio[column] = [np.std(i) for i in zip(*c_matrix)]
            return logratio.T.iloc[:, :-1]

        def ilr(self, psi=None):
            ''' Wrapper for ILR '''
            if psi is None:
                psi = extra.sbp_basis(self._obj)
            else:
                extra.check_basis(psi)

            if self._check_for_zeros():
                return _ilr_internal(self.aitchison_mean(), psi)

            return _ilr_internal(self._obj, psi)

        def ilr_inv(self, psi=None):
            ''' Wrapper for inverse ILR transformation '''
            if psi is None:
                psi = extra.sbp_basis(self._obj)
            else:
                extra.check_basis(psi)

            return _ilr_inv_internal(self._obj, psi)

        def zero_replacement(self, n_samples=5000):
            ''' Replace zero values using Dirichlet-multinomial Bayesian inherence '''
            counts = pd.DataFrame(index=self._obj.columns)
            for column in self._obj.T:
                p_matrix = ss.dirichlet.rvs(self._obj.T[column]+0.5, n_samples)
                counts[column] = [np.mean(i) for i in zip(*p_matrix)]
            return counts.T

        def aitchison_mean(self):
            ''' Return the Aitchison mean point estimate '''
            return np.exp(sp.digamma(self._obj+1.0)).coda.closure(1.0)

        def closure(self, cls_const):
            ''' Apply Closure to composition '''
            return cls_const*self._obj.divide(self._obj.sum(axis=1), axis=0)

        def varmatrix(self, nmp=False):
            '''
                Calculate the total variation of a composition
                TODO: for large datasets, this function blows up the memory.
                This could be overcome by using a clever running variance
                algorithm, alas I am lazy, so we estimate the variance by only
                using a maximum of 500 entries. This can still be a problem if
                dim[0] is large, so something needs to be done here. -- C.B.
            '''
            if self._check_for_zeros():
                comp = self.aitchison_mean()
            else:
                comp = self._obj

            # Quick fix: Estimate variance from at most 500 entries.
            reduc = np.array(comp)[:min(500, np.shape(comp)[0]), :]

            # New vectorized version. Faster than ketchup!
            vrmtrx = np.var(np.log(reduc[:, :, None]*1./reduc[:, None]), axis=0)
            if nmp:
                return vrmtrx
            return pd.DataFrame(vrmtrx, columns=self._obj.columns, index=self._obj.columns)

        def totvar(self):
            '''
                Calculate the total variance from the variance matrix
            '''
            var_matrix = self.varmatrix(True)
            return 1./(2*np.shape(var_matrix)[0]) * np.sum(var_matrix)

        def gmean(self):
            ''' Calculate the geometric mean '''
            if self._check_for_zeros():
                gmean = ss.mstats.gmean(self.aitchison_mean())
            else:
                gmean = ss.mstats.gmean(self._obj)
            return np.array([100 * i / np.sum(gmean) for i in gmean])

        def power(self, alpha):
            ''' Compositional scalar multiplication'''
            if self._check_for_zeros():
                return pow(self.aitchison_mean(), alpha)
            return pow(self._obj,alpha)

        def perturbation(self, comp):
            ''' Compositional addition with comp'''
            if self._check_for_zeros():
                return self.aitchison_mean()*np.array(comp)
            return self._obj*np.array(comp)

        def scale(self):
            ''' Scale composition with total variance '''
            return self.power(1./np.sqrt(self.totvar()))

        def center(self):
            ''' Center the composition '''
            return self.perturbation(1./self.gmean())
        