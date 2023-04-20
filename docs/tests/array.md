In this file I'll be placing doc tests for `odeanimate.array`.

The following code should be an example of a trivial array, of shape `(1, 1)`, with zero in it.

    >>> from odeanimate.array import Array
    >>> A = Array([0])
    >>> A[0, 0]
    0

Let's provide an example, let's say we want to express the matrix


Now that we know this is working, let's talk about the addition

    >>> A = Array([1, 2], [1, 2])
    >>> B = Array([1, 2], [-1, -2])
    >>> C = A + B
    >>> C[0, 1]
    0
    >>> C[0, 1] == A[0, 1] + B[0, 1]
    True
