"""Simple function plotting using offline Plotly."""

import plotly.graph_objs as go
import plotly
import numpy as np
import types


def mesh_function_2D(fn, x_min, x_max, bins, **kwargs):
    """Take in a function and calculate a mesh of points."""
    x_mesh = np.arange(x_min, x_max, (x_max-x_min)/float(bins))
    y_mesh = [fn(x, **kwargs) for x in x_mesh]
    y_mesh = np.asarray(y_mesh)
    name = "{}".format(fn.__name__)
    kw_names = ""
    for kw in kwargs:
        kw_names += ", {}={}".format(kw, kwargs[kw])
    return [x_mesh, y_mesh, name, kw_names]


def mesh_function_3D(fn, x_min=1, x_max=10,
                     y_min=1, y_max=10, bins=20, **kwargs):
    """Take a function and create a matrix of points for plotting."""
    x_mesh = np.arange(x_min, x_max, (x_max-x_min)/float(bins))
    y_mesh = np.arange(y_min, y_max, (y_max-y_min)/float(bins))
    x_mesh, y_mesh = np.meshgrid(x_mesh, y_mesh)

    z_mesh = [[fn(x, y, **kwargs) for x, y in zip(x_row, y_row)]
              for x_row, y_row in zip(x_mesh, y_mesh)]

    return z_mesh


def fig2d(lines, title='Function'):
    """Plot lines from numpy arrays."""
    i = 0
    traces = []

    for ln in lines:
        i += 1
        xx, yy, name, kw_names, yaxis = ln

        name_list = []
        for n in range(len(lines)):
            name_list.append(lines[n][2])

        if name_list.count(name) > 1:
            name += kw_names

        color_fn = i*(255/(max(len(lines)-1, 1)))

        tr = go.Scatter(
                        x=xx,
                        y=yy,
                        mode='lines',
                        marker=go.Marker(color='hsv(%d, 100, 85)' % color_fn),
                        name='%s' % name,
                        yaxis='%s' % yaxis
                        )
        traces.append(tr)

    layout = go.Layout(
                    title=title,
                    xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)',
                                   gridcolor='rgb(255,255,255)'),
                    yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)',
                                   gridcolor='rgb(255,255,255)'),
                    yaxis2=go.YAxis(zerolinecolor='rgb(255,255,255)',
                                    gridcolor='rgb(255,255,255)',
                                    overlaying='y',
                                    side='right')
                    )

    data = traces
    fig = go.Figure(data=data, layout=layout)

    return fig


def splot(fn_list, x_min=1, x_max=10,
          y_min=1, y_max=10, bins=300, inline=True, **kwargs):
    """Grab a function(s), mesh it, the graph it."""
    title = "Comparison: "

    if isinstance(fn_list, types.FunctionType):
        title = fn_list.__name__
        fn_list = [fn_list]

    data_list = []
    for fn_group in fn_list:
        if isinstance(fn_group, types.FunctionType):
            fn_group = [fn_group]
        fn = fn_group[0]
        try:
            fn_kwargs = fn_group[1]
        except:
            fn_kwargs = {}

        try:
            yaxis = fn_kwargs.pop('yaxis')
            if (yaxis == 'right') or (yaxis == 'y2'):
                yaxis = 'y2'
            elif (yaxis == 'left') or (yaxis == 'y'):
                yaxis = 'y'
            else:
                raise ValueError('Invalid yaxis choice. Try "right" or "left"')
        except:
            yaxis = 'y'

        data = mesh_function_2D(fn, x_min, x_max, bins, **fn_kwargs)
        data.append(yaxis)
        data_list.append(data)

    fig = fig2d(data_list, title=title)
    if inline:
        plotly.offline.iplot(fig)
    else:
        plotly.offline.plot(fig)
    # return data_list


def splot3d(fn_list, x_min=1, x_max=10, y_min=1, y_max=10, bins=20, **kwargs):
    """take in a function of two variables and graph it."""
    if isinstance(fn_list, types.FunctionType):
        fn_list = [fn_list]

    data = []
    for fn in fn_list:
        zmatrix = mesh_function_3D(fn, x_min, x_max,
                                   y_min, y_max, bins, **kwargs)
        data.append(dict(z=zmatrix, type='surface'))

    plotly.offline.iplot(data)


def kw(**kwargs):
    return kwargs
