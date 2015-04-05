"""
Vector, Quaternion and rotation matrices used
in the sdf-builder. This is powered by a fork
of pyeuclid found at https://github.com/ezag/pyeuclid
"""
from .euclid import Vector3, Quaternion
from .euclid import Matrix4 as RotationMatrix

# Epsilon value used for zero comparisons
EPSILON = 1e-5
OPPOSITE = -1
PARALLEL = 1
NOT_PARALLEL = 0


def vector_parallellism(a: Vector3, b: Vector3):
    """
    Check whether the given vectors parallel, opposite
    or not parallel.
    Returns one of the OPPOSITE / PARALLEL / NOT_PARALLEL
    "constants"
    :param a:
    :param b:
    :return:
    """
    dot = a.normalized().dot(b.normalized())
    if dot <= (-1 + EPSILON):
        return OPPOSITE
    elif dot >= (1 - EPSILON):
        return PARALLEL
    else:
        return NOT_PARALLEL


def vectors_parallel(a: Vector3, b: Vector3):
    """
    Shortcut method to vector_parallellism(a, b) == PARALLEL
    :param a:
    :param b:
    :return:
    """
    return vector_parallellism(a, b) == PARALLEL


def vectors_orthogonal(a: Vector3, b: Vector3):
    """
    Returns true if the two given vectors are orthogonal (i.e.
    their dot product is below a EPSILON)
    :param a:
    :param b:
    :return:
    """
    return abs(a.normalized().dot(b.normalized())) <= EPSILON