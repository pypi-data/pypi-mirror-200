import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import statsmodels.api as sm
import numpy as np

import hyclib as lib

def subplots(rows, cols, plot_size=(6.4,4.8), keep_shape=False, **kwargs):
    fig, axes = plt.subplots(rows, cols, figsize=(plot_size[0]*cols, plot_size[1]*rows), **kwargs)
    if keep_shape:
        axes = np.array(axes)
        axes = axes.reshape((rows, cols))
    return fig, axes

def scaterr(x, y, yerr, ax=None, cap=False, **kwargs):
    if 'marker' not in kwargs:
        kwargs['marker'] = '.'
    if 'ls' not in kwargs and 'linestyle' not in kwargs:
        kwargs['ls'] = 'none'
    if 'capsize' not in kwargs and cap:
        kwargs['capsize'] = 2.0
    
    if ax is None:
        ax = plt.gca()
    
    return ax.errorbar(x.tolist(), y.tolist(), yerr=yerr.tolist(), **kwargs)

def hide_unused_axes(axes):
    for ax in axes.flat:
        if not ax.has_data():
            ax.set_axis_off()

def plot_ci(fit_res, alpha=0.05, xlim=None, plot_kwargs=None, fill_kwargs=None, ax=None):
    if ax is None:
        ax = plt.gca()
        
    if plot_kwargs is None:
        plot_kwargs = {}
    
    if fill_kwargs is None:
        fill_kwargs = {}
        
    default_plot_kwargs = {
        'color': 'C0',
    }
    default_plot_kwargs.update(plot_kwargs)
    plot_kwargs = default_plot_kwargs
    
    default_fill_kwargs = {
        'alpha': 0.15,
        'facecolor': 'C0',
        'edgecolor': 'none',
    }
    default_fill_kwargs.update(fill_kwargs)
    fill_kwargs = default_fill_kwargs
    
    if xlim is None:
        xlim = ax.get_xlim()
    x = np.linspace(*xlim)
    pred_res = fit_res.get_prediction(sm.add_constant(x))
    summary_frame = pred_res.summary_frame(alpha=alpha)
    
    artists = {}
    artists['line'] = ax.plot(x, summary_frame['mean'], **plot_kwargs)
    artists['fill'] = ax.fill_between(x, summary_frame['mean_ci_lower'], summary_frame['mean_ci_upper'], **fill_kwargs)
    
    return artists
    
def regplot(x, y, yerr=None, scatter_kwargs=None, ci_kwargs=None, text_kwargs=None, ax=None):
    if ax is None:
        ax = plt.gca()
        
    if scatter_kwargs is None:
        scatter_kwargs = {}
        
    if ci_kwargs is None:
        ci_kwargs = {}
    
    if text_kwargs is None:
        text_kwargs = {}
        
    default_scatter_kwargs = {
        'marker': 'o',
        'ls': 'none',
    }
    default_scatter_kwargs.update(scatter_kwargs)
    scatter_kwargs = default_scatter_kwargs
    
    default_text_kwargs = {
        'loc': 'upper right',
    }
    default_text_kwargs.update(text_kwargs)
    text_kwargs = default_text_kwargs
    
    if yerr is None:
        model = sm.OLS(y,sm.add_constant(x))
    else:
        model = sm.WLS(y,sm.add_constant(x),weights=1/yerr**2)
        
    fit_res = model.fit()
    
    artists = {}
    artists['scatter'] = ax.errorbar(x, y, yerr=yerr, **scatter_kwargs)
    artists['ci'] = plot_ci(fit_res, ax=ax, **ci_kwargs)
    artists['text'] = ax.add_artist(AnchoredText(
        '\n'.join([
            f'm={fit_res.params[1]:.1e}$\pm${fit_res.bse[1]:.1e}',
            f'b={fit_res.params[0]:.1e}$\pm${fit_res.bse[0]:.1e}',
            f'r={fit_res.rsquared**0.5:.2f}, p={fit_res.pvalues[1]:.1e}',
        ]),
        **text_kwargs
    ))
    
    return artists

def _lineplot(data, x, y, yerr=None, weighted=False, label=None, errstyle='fill', ax=None, **kwargs):
    default_kwargs = {
        'errorbar_kwargs': {'label': label},
        'plot_kwargs': {'label': label},
        'fill_kwargs': {'alpha': 0.25},
    }
    kwargs = {k: v | (kwargs[k] if k in kwargs else v) for k, v in default_kwargs.items()}
    
    if ax is None:
        ax = plt.gca()
    
    x_, y_, yerr_ = [], [], []
    for xi, group in data.groupby(x):
        x_.append(xi)
        yi = group[y]
        if yerr is None:
            yi, yerri = lib.np.nanmean(yi), lib.np.nansem(yi)
        else:
            yerri = group[yerr]
            if weighted:
                yi, yerri = lib.np.nanweightedmeanerr(yi, yerri)
            else:
                yi, yerri = lib.np.nanmeanerr(yi, yerri)
        y_.append(yi)
        yerr_.append(yerri)
    x_, y_, yerr_ = np.array(x_), np.array(y_), np.array(yerr_)

    if errstyle == 'bar':
        l = ax.errorbar(x_, y_, yerr=yerr_, **kwargs['errorbar_kwargs'])
    elif errstyle == 'fill':
        l1 = ax.plot(x_, y_, **kwargs['plot_kwargs'])
        l2 = ax.fill_between(x_, y_-yerr_, y_+yerr_, **kwargs['fill_kwargs'])
        l = (l1, l2)
    else:
        raise ValueError(f"errstyle must be 'fill' or 'bar', but {errstyle=} given.")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    
    return l

def lineplot(data, x, y, yerr=None, hue=None, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()
        
    if hue is not None:
        groupby = data.groupby(hue)
        ls = {}
        for i, (label, group) in enumerate(groupby):
            l = _lineplot(group, x, y, yerr=yerr, label=label, color=mpl.cm.get_cmap('Blues')((i+1)/len(groupby)), ax=ax, **kwargs)
            ls[label] = l
        ax.legend(title=hue)
        return ls
    else:
        return _lineplot(data, x, y, yerr=yerr, ax=ax, **kwargs)
    
def extract_data(obj):
    if isinstance(obj, mpl.lines.Line2D):
        x, y = obj.get_data()
        x, y = x.astype(float), y.astype(float)
        
        data = {'x': x, 'y': y}
    
    elif isinstance(obj, mpl.container.ErrorbarContainer):
        l, _, lc = obj
        x, y = l.get_data()
        x, y = x.astype(float), y.astype(float)
        
        if len(lc) != 1:
            raise NotImplementedError()
        lc = lc[0]
        yerr = np.zeros((len(x), 2))
        for i, l in enumerate(lc.get_segments()):
            yerr[i,:] = l[:,1]
            
        if np.allclose(0.5*(yerr[:,0] + yerr[:,1]), y):
            yerr = yerr[:,1] - y
            
        data = {'x': x, 'y': y, 'yerr': yerr}
    
    else:
        raise NotImplementedError(f'Object with dtype {obj.dtype} not implemented')
        
    return data

def vec(vec, origin=None, ax=None, pad=0.05, **kwargs):
    assert len(vec) == 2
    
    default_kwargs = {
        'angles': 'xy',
        'scale_units': 'xy',
        'scale': 1
    }
    default_kwargs.update(kwargs)
    
    if ax is None:
        ax = plt.gca()
        
    if origin is None:
        origin = [0,0]
        
    arrow = ax.quiver(*origin, *vec, **default_kwargs)
    
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    
    xmin = min(origin[0], origin[0]+vec[0])
    xmax = max(origin[0], origin[0]+vec[0])
    xrange = xmax - xmin
    xmin = min(xlim[0], xmin-pad*xrange)
    xmax = max(xlim[1], xmax+pad*xrange)
    
    ymin = min(origin[1], origin[1]+vec[1])
    ymax = max(origin[1], origin[1]+vec[1])
    yrange = ymax - ymin
    ymin = min(ylim[0], ymin-pad*yrange)
    ymax = max(ylim[1], ymax+pad*yrange)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    return arrow

def set_aspect(option, ax=None):
    if ax is None:
        ax = plt.gca()
    
    if option == 'equal_square':
        ax.set_aspect('equal')
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        xrange = xlim[1] - xlim[0]
        yrange = ylim[1] - ylim[0]
        
        if xrange < yrange:
            ratio = yrange / xrange
            xcenter = 0.5*(xlim[0] + xlim[1])
            xlim = ((xlim[0]-xcenter)*ratio+xcenter, (xlim[1]-xcenter)*ratio+xcenter)
        else:
            ratio = xrange / yrange
            ycenter = 0.5*(ylim[0] + ylim[1])
            ylim = ((ylim[0]-ycenter)*ratio+ycenter, (ylim[1]-ycenter)*ratio+ycenter)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
    else:
        ax.set_aspect(option)