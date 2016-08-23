splot
=====

Simplified plotly wrapper for python.

Dependencies
============
* <a "href=https://plot.ly/python/offline/">plotly offline for python</a>  
* numpy

Usage
=====
```
def bounce(x, a=5):
    return abs(10*m.sin(a*x)/(m.e**(x/2)))

splot(bounce)
```

`splot` can also take a list of functions, and can take keyword arguments (as a dict, or using the kw function) for each function:
```
splot([bounce, [bounce, {'a':5}], [bounce, kw(n=4)]]
```

Optional keywords can be used to refine the graph:  
`x_min`, `x_max` set the bounds on the graph. (Default: 1, 10)  
`bins` sets the number of points to plot. (Default: 300)  
`inline` sets whether the graph is placed inline or in a new tab. (Default: True)  


`splot3d` similarly allows graphing of functions of two variables.
```
def thing3d(x, y):
    return abs(0.1*m.sin(x**2+y**2))

r=m.pi*2/4
splot3d(thing3d, x_min=-r, x_max=r, y_min=-r, y_max=r, bins=300)
```
