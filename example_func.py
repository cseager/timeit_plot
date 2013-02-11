
# Example functions to test timeit_compare()
import itertools

# TODO: test slice instead of zip for n > len/2 to reduce the number of tees instantiated
def use_iterators(iterable, n=2):
    """for n=2, i -> (s0,s1), (s1,s2), (s2,s3), ...

    for n=3, i -> (s0,s1,s2), (s1,s2,s3), (s2,s3,s4), ..."""
    if len(iterable) <= n:
        return iterable
    mytee = itertools.tee(iterable, n)
    for i, t in enumerate(mytee):
        for j in range(i):
            next(t, None)
    return zip(*mytee)
    
    
def use_indexing(iterable, n=2):
    """for n=2, i -> (s0,s1), (s1,s2), (s2,s3), ...

    for n=3, i -> (s0,s1,s2), (s1,s2,s3), (s2,s3,s4), ..."""
    if n < 2 or len(iterable) <= n:
        return iterable
    ngrams = []
    for i in enumerate(iterable[:-(n-1)]):
        ngrams.append( tuple([iterable[i[0] + j] for j in range(n)]) )
    return ngrams
