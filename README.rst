timeit_plot
=====

A Python utility to plot timeit output in matplotlib. 

Written by Clair Seager (github.com/cseager)

0. Dependencies
---------------

numpy, matplotlib

1. Documentation and usage
--------------------------

This module contains utility functions to plot the results of several
timeit tests using matplotlib. Be aware that it will run many
timeit tests at one time, and timeit can take a while to finish 
if the default number of cycles is used. 

The timeit module's Python interface takes functions expressed as strings, 
tests them a certain number of times, and reports back the execution time. 
From `Python documentation: <http://docs.python.org/2/library/timeit.html>`_::

    >>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
    0.8187260627746582
    >>> timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
    0.7288308143615723
    >>> timeit.timeit('"-".join(map(str, range(100)))', number=10000)
    0.5858950614929199

``timeit_compare()`` uses string substitution while iterating over
ranges of values to record how fast the function(s) perform with
the specified conditions. ::

    >>> import timeit_plot as tp
    >>> from matplotlib import pyplot as plt
    >>> functions = ['"-".join(str(n) for n in range({0}))', 
                     '"-".join([str(n) for n in range({0})])', 
                     '"-".join(map(str, range({0})))']
    >>> data = tp.timeit_compare(functions, range(10,101,10), number=10000)
    testing "-".join(str(n) for n in range({0}))...
    testing "-".join([str(n) for n in range({0})])...
    testing "-".join(map(str, range({0})))...
    >>> tp.timeit_plot2D(data, 'list length', 'list comprehension vs map')
    >>> plt.show()

.. image:: https://raw.github.com/cseager/timeit_plot/master/images/joined%20lists.png
    :alt: plot of 3 expression running times


2. Further examples
-------------------

``timeit_compare()`` can take any number of functions and variables, built-in 
or user created. This can be helpful in determining or comparing algorithms' 
Big O or time complexity. For example, compare a recursive Fibonacci function 
to a memoized version: ::

    >>> from example_func import *
    >>> functions = ["memoize_fib({0})", "recursive_fib({0})"]
    >>> test_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> data = tp.timeit_compare(functions, test_values, setups="main")
    >>> tp.timeit_plot2D(data, 'n', 'comparison of Fibonacci algorithms')
    >>> plt.show()

.. image:: https://raw.github.com/cseager/timeit_plot/master/images/fibonacci_comparison.png
    :alt: plot of two Fibonacci methods' running time


The functions do not need to be set up to take single values, but it is helpful 
to set them up in a way that grows the inputs during the testing. The example 
functions included, ``use_iterators()`` and ``use_indexing()``, 
compare methods of grouping lists into n-grams. This is conceptually similar to the ``pairwise`` 
recipe given in the `documentation, <http://www.python.org/doc//current/library/itertools.html#recipes>`_ but is more general for n >= 2. 

In this case, the two parameters that affect performance are: 

1. The length of the object to be split into n-grams
2. The size of the n-gram 

These can both be parametrized in ``timeit_compare``, which will test all combinations
of the variable ranges given: ::  

    >>> functions = ("use_iterators(range({0}),{1})", "use_indexing(range({0}),{1})")
    >>> variable_ranges = [range(21),range(3,21)]
    >>> data = tp.timeit_compare(functions, variable_ranges, setups='main', number=1000)
    testing use_iterators(range({0}),{1})...
    testing use_indexing(range({0}),{1})...

This outputs a defaultdict with function strings as keys, 
values are a list of timeit test results. The values are recorded 
as lists of ``[test_conditions, result]``, with conditions listed
in the order the user entered them in ``variable_ranges``. 
For example, the first entry from ``data`` would be: 
``{'use_iterators(range({0}),{1})': [[0, 3, 0.0059], ...]``

For the following plot, a filter is applied to show only the results for 
inputs of length 20. The second variable is chosen as the independent 
variable in the plot by using the keyword arg ``series=1``: ::

    >>> d2 = {}
    >>> for k, v in data.iteritems(): 
    ...     d2[k] = [p for p in v if p[0]==20]
    >>> tp.timeit_plot2D(d2, 'ngram length', 'list length 20', series=1, style='scatter', size=100)
    >>> plt.show()

.. image:: https://raw.github.com/cseager/timeit_plot/master/images/ngram%20length%20on%2020%20items%20v%20time.png
    :alt: example scatter plot

There are also plotting functions to examine how two parameters 
can affect the performance of a single function. The following large 
test can be sped up by either decreasing the number of cycles done 
by timeit, or by providing a step size in the range variable to 
reduce the overall number of data points gathered. ::

    >>> # WARNING: the following set of timed tests may take a while!
    >>> data2 = tp.timeit_compare(functions, [range(4,20), range(2,18)], setups='main')
    testing use_iterators(range({0}),{1})...
    testing use_indexing(range({0}),{1})...
    >>> # Reduce the ranges and cycles to speed it up. 
    >>> data3 = tp.timeit_compare(functions, [range(4,50,4),range(2,50,3)], number=1000, setups='main')
    testing use_iterators(range({0}),{1})...
    testing use_indexing(range({0}),{1})...

Data with two variables can be plotted either in a 3D mesh plot: ::

    >>> tp.timeit_plot3D(data3, 'list size', 'ngram length')

.. image:: https://raw.github.com/cseager/timeit_plot/master/images/3D%20indexing.png
    :alt: example 3D plot

Or it can be shown with a heatmap plot: ::

    >>> tp.timeit_heatmap(data3, 'list size', 'ngram length')

.. image:: https://raw.github.com/cseager/timeit_plot/master/images/heatmap%20indexing.png
    :alt: example heatmap plot
        
Or a bubble plot: ::

    >>> tp.timeit_plot2D(data3, 'list size', 'bubble size = time', series=[0,1],
                style='bubble', size=5000, ylabel='ngram length')

.. image:: https://raw.github.com/cseager/timeit_plot/master/images/bubble%20plot.png
    :alt: example bubble plot

The ``bubble_size`` parameter is a multipler. The value needed 
to get the desired bubble size will depend on the number of 
cycles used to generate the data (fewer cycles will result in 
faster tests and thus smaller z values). 
