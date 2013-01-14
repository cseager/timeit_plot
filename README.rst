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
tests them a certain number of times, and reports back the execution time. ::

    >>> # From http://docs.python.org/2/library/timeit.html
    >>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
    0.8187260627746582
    >>> timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
    0.7288308143615723
    >>> timeit.timeit('"-".join(map(str, range(100)))', number=10000)
    0.5858950614929199

``timeit_compare()`` uses string substitution while iterating over
ranges of values to record how fast the function(s) perform with
the specified conditions. ::

    >>> functions = ['"-".join(str(n) for n in range({0}))', 
            '"-".join([str(n) for n in range({0})])', 
            '"-".join(map(str, range({0})))']
    >>> data = timeit_compare(functions, [[10,101,10]], number=10000)
    testing "-".join(str(n) for n in range({0}))...
    testing "-".join([str(n) for n in range({0})])...
    testing "-".join(map(str, range({0})))...
    >>> timeit_plot2D(data, 'list length', 'list comprehension vs map')
    >>> plt.show()

.. image: https://github.com/cseager/timeit_plot/blob/master/images/joined%20lists.png
    :alt: plot of 3 expression performances

2. Further examples
-------------------

The example functions included, ``use_iterators()`` and ``use_indexing()``, 
compare methods of grouping lists. ::

    >>> functions = ("use_iterators(range({0}),{1})", "use_indexing(range({0}),{1})")
    >>> variable_ranges = [[20,21],[3,21]]
    >>> data = timeit_compare(functions, variable_ranges, setups='main')
    testing use_iterators(range({0}),{1})...
    testing use_indexing(range({0}),{1})...

This outputs a defaultdict with function strings as keys, 
values are a list of timeit test results. The values are recorded 
as lists of ``[test_conditions, result]``, with conditions listed
in the order the user entered them in ``variable_ranges``. 
For example, the first entry from ``data`` would be: 
``{'use_iterators(range({0}),{1})': [[20, 3, 0.6359], ...]``

In this example, the first variable is held constant, because 
range(*[20,21]) = [20]. The second variable is chosen for the following
plot by using the keyword arg ``series=1``. ::

    >>> timeit_plot2D(data, 'ngram length', 'list length 20', series=1, style='scatter')
    >>> plt.show()


.. image:: https://github.com/cseager/timeit_plot/blob/master/images/ngram%20length%20on%2020%20items%20v%20time.png
    :alt: example scatter plot

There are also plotting functions to examine how two parameters 
can affect the performance of a single function. The following large 
test can be sped up by either decreasing the number of cycles done 
by timeit, or by providing a step size in the range variable to 
reduce the overall number of data points gathered. ::

    >>> # WARNING: the following set of timed tests may take a while!
    >>> data2 = timeit_compare(functions, [[4,20], [2,18]], setups='main')
    testing use_iterators(range({0}),{1})...
    testing use_indexing(range({0}),{1})...
    >>> # Reduce the ranges and cycles to speed it up. 
    >>> data3 = timeit_compare(functions, [[4,50,4],[2,50,3]], number=1000, setups='main')
    testing use_iterators(range({0}),{1})...
    testing use_indexing(range({0}),{1})...

Data with two variables can be plotted either in a 3D mesh plot: ::

    >>> timeit_plot3D(data3, 'list size', 'ngram length')


.. image:: https://github.com/cseager/timeit_plot/blob/master/images/3D%20indexing.png
    :alt: example 3D plot

Or it can be shown with a heatmap plot: ::

    >>> timeit_heatmap(data3, 'list size', 'ngram length')


.. image:: https://github.com/cseager/timeit_plot/blob/master/images/heatmap%20indexing.png
    :alt: example heatmap plot
        
Or a bubble plot: ::

    >>> timeit_plot2D(data3, 'list size', 'bubble size = time', series=[0,1],
                style='bubble', bubble_size=5000, ylabel='ngram length')


.. image:: https://github.com/cseager/timeit_plot/blob/master/images/bubble%20plot.png
    :alt: example bubble plot

The ``bubble_size`` parameter is a multipler. The value needed 
to get the desired bubble size will depend on the number of 
cycles used to generate the data (fewer cycles will result in 
faster tests and thus smaller z values). 
