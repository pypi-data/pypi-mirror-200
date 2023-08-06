''' Class and methods for making compositional biplots based on PCA '''

import numpy as np
import matplotlib.pyplot as plt
import webcolors as wc
from matplotlib.colors import ListedColormap
from matplotlib import cm
import matplotlib.patches as mpatches
import pandas as pd
import scipy.stats as st
from pycodamath import extra


class GeomObj():
    ''' A generic container of geometric objects '''

    def __init__(self, **kwargs):
        vars(self).update(kwargs)
        self.area = self.polyarea()

    def polyarea(self):
        ''' Calculate the area of a polygon given two lists of vertices '''
        x, y = self.vertices
        return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))


def scree_plot(axis, eig_val):
    ''' Make scree plot from eigen values'''
    axis.set_xlabel('Component')
    axis.set_ylabel('Explained varaince')
    axis.set_xlim(0, min(len(eig_val)+1, 20))
    axis.bar(np.arange(len(eig_val))+1, (eig_val/np.sum(eig_val))**2)
    csum = np.cumsum(eig_val**2/np.sum(eig_val**2))
    for i in range(min(5, len(eig_val))):
        axis.annotate(str(np.round(csum[i]*100))+'%',
                      (i+1.2, (eig_val[i]/np.sum(eig_val))**2))


def _get_palette(group):
    cspace = cm.jet(np.linspace(0, 1, len(set(group))))
    palette = {}
    for idx, item in enumerate(set(group)):
        palette[item] = cspace[idx]
    return palette


def _svd(clr):
    ''' Internal SVD function '''
    scores, eig_val, loadings = np.linalg.svd(clr)
    scores = pd.DataFrame(scores.T[0:2, :], columns=clr.index, index=['pc1', 'pc2'])
    loadings = pd.DataFrame(np.inner(eig_val*np.identity(len(eig_val)),
                                     loadings.T[0:len(eig_val), 0:len(eig_val)])[0:2],
                            columns=clr.columns[0:len(eig_val)], index=['pc1', 'pc2'])
    return scores, eig_val, loadings


class Biplot():
    ''' A class to create and a PCA biplot '''

    def __init__(self, data, axis=None, default=True):
        if axis is None:
            _, self.axis = plt.subplots(figsize=(7.8, 7.8))
        else:
            self.axis = axis
        self.axis.set(adjustable='box', aspect='equal')
        self.scores, eig_val, self.loadings = _svd(data.coda.center().coda.scale().coda.clr())
        scales = [np.max(np.abs(self.loadings.values)),
                  [np.max(np.abs(self.scores.loc[idx].values)) for idx in ['pc1', 'pc2']]]


        self.axis.set_xlabel(f'P.C. 1 ({np.round(eig_val[0]**2 / np.sum(eig_val**2)*100):.1f}% explained variation)')                             
        self.axis.set_ylabel(f'P.C. 2 ({np.round(eig_val[1]**2 / np.sum(eig_val**2)*100):.1f}% explained variation)')
        self.axis.set_xlim(-scales[0]*1.1, scales[0]*1.1)
        self.axis.set_ylim(-scales[0]*1.1, scales[0]*1.1)
        self.axis.plot([self.axis.get_xlim()[0], self.axis.get_xlim()[1]],
                       [0.0, 0.0], '--', color='black', alpha=0.4)
        self.axis.plot([0.0, 0.0], [self.axis.get_ylim()[0], self.axis.get_ylim()[1]],
                       '--', color='black', alpha=0.4)

        self.scores = (scales[0]*(self.scores.T/scales[1])).T

        self.patches = []
        self.geomobj = {}
        plt.tight_layout()

        if default:
            self.plotloadings()
            self.plotscores()

    def plotloadings(self, cutoff=0, scale=None, labels=None):
        ''' Plot loadings '''
        if scale is None:
            scale = np.max(np.abs(self.loadings.values))

        for column in self.loadings:
            if np.sqrt(pow(self.loadings.loc['pc1', column], 2) +
                       pow(self.loadings.loc['pc2', column], 2)) > cutoff:
                self.axis.arrow(0, 0,
                                self.loadings.loc['pc1', column],
                                self.loadings.loc['pc2', column],
                                facecolor='black',
                                alpha=0.5,
                                linewidth=0.,
                                width=scale*0.01,
                                zorder=2000)
        self.plotloadinglabels(labels, cutoff)

    def plotloadinglabels(self, labels=None, cutoff=0):
        ''' Add labels to the loadings '''
        if labels is None:
            labels = self.loadings.columns

        for column in labels:
            if np.sqrt(pow(self.loadings.loc['pc1', column], 2) +
                       pow(self.loadings.loc['pc2', column], 2)) > cutoff:
                yoff = 0.  
                if self.loadings.loc['pc1', column] > 0.9*self.axis.get_xlim()[1]:
                    xoff = -1.2
                else:
                    xoff = 0
                self.axis.annotate(column, (self.loadings.loc['pc1', column]+xoff,
                                            self.loadings.loc['pc2', column]+yoff),
                                   ha='left',
                                   va='bottom',
                                   alpha=1.0,
                                   zorder=2001
                                   )

    def plotscores(self, group=None, palette=None, legend=True, labels=None):
        ''' Plot scores as points '''
        if labels is None:
            labels = self.scores.columns

        if palette is None:
            if group is not None:
                palette = _get_palette(group)
            else:
                palette = 'steelblue'

        if group is None:
            self.axis.plot(*self.scores[labels].values, 'o', alpha=0.5,
                           color=palette, zorder=7, markeredgewidth=0)
        else:
            for item in set(group):
                idx = group.loc[group == item].index
                self.axis.plot(*self.scores[idx].values, 'o', alpha=0.5, zorder=7,
                               label=item, color=palette[item], markeredgewidth=0)
                if legend:
                    self.patches.append(mpatches.Patch(color=palette[item], label=item))

    def plotscorelabels(self, labels=None):
        ''' Add labels to the scores '''
        if labels is None:
            labels = self.scores.columns

        for label in labels:
            self.axis.annotate(label, (self.scores.loc['pc1', label],
                                       self.scores.loc['pc2', label]),
                               ha='left',
                               va='bottom',
                               alpha=0.8,
                               zorder=201,
                               size=8
                               )

    def plotellipses(self, group, palette=None, legend=False):
        ''' Plot confidence ellipses '''
        if palette is None:
            palette = _get_palette(group)

        for item in set(group):
            idx = group.loc[group == item].index
            if len(idx) > 3:
                ellipse = extra.get_covariance_ellipse(pd.DataFrame(self.scores[idx].values.T),
                                                       conf=90)
                extra.plot_covariance_ellipse(self.axis, ellipse, color=palette[item])
                if legend:
                    self.patches.append(mpatches.Patch(color=palette[item], label=item))

    def plotcentroids(self, group, palette=None, legend=False):
        ''' Plot score group centroids '''
        if palette is None:
            palette = _get_palette(group)

        for item in set(group):
            idx = group.loc[group == item].index
            length = len(self.scores[idx].T)
            sum_x = np.sum(self.scores.loc['pc1', idx])
            sum_y = np.sum(self.scores.loc['pc2', idx])
            self.axis.plot([sum_x/length], [sum_y/length], 'x', alpha=0.7,
                           label=item, color=palette[item], markersize=24)
            if legend:
                self.patches.append(mpatches.Patch(color=palette[item], label=item))

    def plothulls(self, group, palette=None, legend=True):
        ''' Plot score group hulls '''
        if palette is None:
            palette = _get_palette(group)

        self.geomobj = {}
        for item in set(group):
            idx = group.loc[group == item].index
            if len(idx) > 3:
                # My secret hull construction algorithm
                idxmin = self.scores.loc['pc1', idx].idxmin()
                j = self.scores[idx].columns.get_loc(idxmin)
                hull = [list(self.scores[idxmin])]
                while (j != self.scores[idx].columns.get_loc(idxmin) or len(hull) == 1):
                    k = (j + 1) % len(idx)
                    for i in range(len(idx)):
                        if (self.scores[idx].iloc[1, k]-self.scores[idx].iloc[1, j]) * \
                           (self.scores[idx].iloc[0, i]-self.scores[idx].iloc[0, k]) - \
                           (self.scores[idx].iloc[0, k]-self.scores[idx].iloc[0, j]) * \
                           (self.scores[idx].iloc[1, i]-self.scores[idx].iloc[1, k]) < 0:
                            k = i
                    j = k
                    hull.append(list(self.scores[self.scores[idx].columns[k]]))
                self.geomobj[item] = GeomObj(vertices=tuple(map(list, zip(*hull))))

        for idx, item in enumerate(sorted(self.geomobj,
                                          key=lambda x: self.geomobj[x].area, reverse=True)):
            self.axis.fill(*self.geomobj[item].vertices,
                           color=palette[item], alpha=0.7, zorder=10+(2*idx))
            self.axis.fill(*self.geomobj[item].vertices, facecolor='none',
                           edgecolor='black', alpha=0.9, linewidth=2.2, zorder=11+(2*idx))

            if legend:
                self.patches.append(mpatches.Patch(color=palette[item], label=item))

    def plotcontours(self, group, palette=None, legend=True,
                     plot_outliers=True, percent_outliers=0.1, linewidth=2.2):
        ''' Plot scores as contours '''
        if palette is None and group is not None:
            palette = _get_palette(group)
        if percent_outliers > 1 or percent_outliers < 0:
            raise Exception('Percent_outliers has to be between 0 and 1')

        # Build color maps
        cmap = {}
        for item in set(group):
            colorvalues = np.ones((4, 4))
            if '#' in str(palette[item]):
                color = wc.hex_to_rgb(palette[item])
            elif palette[item][-1] != 1:
                color = wc.name_to_rgb(palette[item])
            else:
                color = palette[item]

            for i in range(3):
                colorvalues[:, i] = np.linspace(1, color[i]/256., 5)[1:]
            colorvalues[:, 3] = np.linspace(.95, .25, 4)
            cmap[item] = ListedColormap(colorvalues)

        self.geomobj = {}
        for item in set(group):
            minlevel = 0.2
            diff = 100
            k = 0
            while abs(diff) > 0 and k < 25:
                levels = np.arange(5)*(1.-minlevel)/4.+minlevel
                idx = group.loc[group == item].index
                xgrid, ygrid = np.mgrid[self.axis.get_xlim()[0]: self.axis.get_xlim()[1]: 300j,
                                        self.axis.get_ylim()[0]: self.axis.get_ylim()[1]: 300j]
                positions = np.vstack([xgrid.ravel(), ygrid.ravel()])
                values = np.vstack([self.scores.loc['pc1', idx], self.scores.loc['pc2', idx]])
                kernel = st.gaussian_kde(values)
                density = np.reshape(kernel(positions).T, xgrid.shape)
                vals = np.max(density)*levels
                self.axis.contour(xgrid, ygrid, density, vals)
                vertices = self.axis.collections[-4].get_paths()[0].vertices.T
                contained = [False for _ in range(len(idx))]
                for j in range(len(self.axis.collections[-5].get_paths())):
                    contained = np.logical_or(contained,
                                              self.axis.collections[-5].get_paths()[j].contains_points(
                                                  [[self.scores.loc['pc1', i],
                                                    self.scores.loc['pc2', i]] for i in idx]))
                _ = [self.axis.collections[-1].remove() for _ in np.arange(5)]
                outside = [a for a, b in zip(list(idx), contained) if not b]

                diff = round(percent_outliers*len(idx))-len(outside)
                minlevel = minlevel+diff/1000.
                k += 1

            self.geomobj[item] = GeomObj(vertices=vertices, grid=(
                xgrid, ygrid), density=density, values=vals, outside=outside)

        for idx, item in enumerate(sorted(self.geomobj,
                                          key=lambda x: self.geomobj[x].area, reverse=True)):
            self.axis.contourf(*self.geomobj[item].grid, self.geomobj[item].density,
                               self.geomobj[item].values, antialiased=True,
                               cmap=cmap[item], alpha=0.9, zorder=10+(2*idx))
            self.axis.contour(*self.geomobj[item].grid, self.geomobj[item].density,
                              self.geomobj[item].values, antialiased=True,
                              colors='black', alpha=0.9, linewidths=linewidth, zorder=11+(2*idx))
            self.axis.collections[-1].remove()

            if plot_outliers:
                self.plotscores(None, palette[item], False, self.geomobj[item].outside)

            if legend:
                self.patches.append(mpatches.Patch(color=palette[item], label=item))

    def labeloutliers(self, group, conf=3.):
        ''' Print labels on scores that are more than conf away from centroid '''
        for item in set(group):
            idx = group.loc[group == item].index
            length = len(self.scores[idx].T)
            sum_x = np.sum(self.scores.loc['pc1', idx])
            sum_y = np.sum(self.scores.loc['pc2', idx])

            pdist = {i: np.sqrt(pow(self.scores.loc['pc1', i]-sum_x/length, 2) +
                                pow(self.scores.loc['pc2', i]-sum_y/length, 2)) for i in idx}
            std = np.std(pdist.values())

            outliers = [i for i in pdist.keys() if pdist[i] > conf*std]
            self.plotscorelabels(outliers)

    def displaylegend(self, loc=2):
        ''' Display the item legend at location loc '''
        patches = sorted(self.patches, key=lambda x: x._label)
        self.axis.legend(handles=patches, fontsize=9, frameon=False, loc=loc)

    def removepatches(self):
        ''' remove arrows and polygons from plot '''
        for _ in range(len(self.axis.patches)):
            self.axis.patches[-1].remove()

    def removelabels(self):
        ''' remove labels from plot '''
        for _ in range(len(self.axis.texts)):
            self.axis.texts[-1].remove()

    def removescores(self):
        ''' remove points from plot '''
        for _ in range(len(self.axis.lines)):
            self.axis.lines[-1].remove()

    def removecontours(self):
        ''' remove points from plot '''
        for _ in range(len(self.axis.collections)):
            self.axis.collections[-1].remove()
