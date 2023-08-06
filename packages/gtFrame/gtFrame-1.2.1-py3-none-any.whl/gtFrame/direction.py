"""
This module implements the Direction2d and Direction3d classe, which serve
to represent direction-vectors (like velocity or acceleration). They hold
information on the frame of reference in which they are defined and can be
converted to different frames of reference by rotation. Unlike position vectors
these vectors remain unchanged by translation.

---------------
Module Contents
---------------
Classes:
    * Direction2d
    * Direction3d
"""

import copy
import numpy as np

from gtFrame import DEFAULT_RTOL
from gtFrame.basic import Frame2d, Frame3d


class Direction2d:
    """
    This class holds information about a direction expressed as a 2d-array
    of coordinates defined on a specific frame of reference.

    :param vector: the direction expressed as a vector in the given frame of
        reference
    :type vector: np.ndarray
    :param reference: the frame of reference on which the vector is defined
    :type reference: gtFrame.basic.Frame2d
    :param rtol: The relative tolerance to be used when comparing
        Direction2d objects. The default is set to the global variable
        DEFAULT_RTOL.
    :type rtol: float
    """
    def __init__(self, vector, reference, rtol=DEFAULT_RTOL):
        """
        Constructor method.
        """
        if vector.shape != (2,):
            raise ValueError("The direction vector has to be two dimensional.")
        self.vector = vector
        self.reference = reference
        self.rtol = rtol

    def __add__(self, other):
        """
        Adds the other Direction objects vector to self.vector and returns a
        new Direction2d object with the resulting vector.

        :param other: Direction2d object to add
        :type other: Direction2d
        :return: the resulting Direction2d object
        :rtype: Direction2d
        """
        if type(other).__name__ != "Direction2d":
            raise TypeError("Direction2d objects can only be summed with other"
                            "Direction2d objects")

        direction = copy.copy(self)
        direction.apply_direction(other)
        return direction

    def __eq__(self, other):
        """
        Compares two Direction2d objects and evaluates if they both point in
        the same direction. Returns True if both the directions match and
        False otherwise.

        :param other: the other Direction2d object
        :type other: gtFrame.direction.Direction2d
        :return: returns True if the directions match within tolerance and
            False if not
        :rtype: bool
        """
        if not isinstance(other, Direction2d):
            raise TypeError("Can only compare Direction2d to Direction2d"
                            "objects.")

        transformed = other.transform_to(self.reference)
        return np.allclose(self.vector, transformed, rtol=self.rtol)

    def __mul__(self, other):
        """
        Scales the direction vector by an amount given by 'other' and returns
        a new Direction2d object with the scaled vector.

        :param other: the scaling factor for the direction vector
        :type other: float
        :return: a new Direction2d object with the scaled vector
        :rtype: Direction2d
        """
        try:
            factor = float(other)
        except ValueError:
            raise ValueError("A Direction2d object can only be scaled "
                             "with a number.")
        except TypeError:
            raise TypeError("A Direction2d object can only be scaled "
                            "with a number.")

        return Direction2d(self.vector * factor, self.reference, self.rtol)

    def apply_direction(self, direction):
        """
        Adds the vector of 'direction' to the vector of self, after
        transforming it in to self.reference.

        :param direction: the Direction2d object to be applied to this one
        :type direction: Direction2d
        :return: None
        """
        rotated = direction.transform_to(self.reference)
        self.vector = self.vector + rotated

    def length(self):
        """
        Returns the length (i.e. euclidean norm) of the direction vector.

        :return: the euclidean norm of the direction vector
        :rtype: float
        """
        return np.linalg.norm(self.vector)

    def scale(self, factor):
        """
        Scales the length of the direction vector, by multiplying it with a
        factor.

        :param factor: the factor for scaling the vector
        :type factor: float
        :return: None
        """
        try:
            factor = float(factor)
        except ValueError:
            raise ValueError("A Direction2d object can only be scaled "
                             "with a number.")
        except TypeError:
            raise TypeError("A Direction2d object can only be scaled "
                            "with a number.")
        self.vector = self.vector * factor

    def transform_to(self, reference):
        """
        Transform the direction vector into another frame of reference.

        :param reference: the frame of reference to transform to
        :type reference: gtFrame.basic.Frame2d
        :return: the direction vector in the other frame of reference
        :rtype: np.ndarray
        """
        path = self.reference.find_transform_path(reference)
        return Frame2d.rotate_via_path(self.vector, path)


class Direction3d:
    """
    This class holds information about a direction expressed as a 3d-array
    of coordinates defined on a specific frame of reference.

    :param vector: the direction expressed as a vector in the given frame of
        reference
    :type vector: np.ndarray
    :param reference: the frame of reference on which the vector is defined
    :type reference: gtFrame.basic.Frame3d
    :param rtol: The relative tolerance to be used when comparing
        Direction3d objects. The default is set to the global variable
        DEFAULT_RTOL.
    :type rtol: float
    """
    def __init__(self, vector, reference, rtol=DEFAULT_RTOL):
        """
        Constructor method.
        """
        if vector.shape != (3,):
            raise ValueError("The direction vector has to be three "
                             "dimensional.")
        self.vector = vector
        self.reference = reference
        self.rtol = rtol

    def __add__(self, other):
        """
        Adds the other Direction objects vector to self.vector and returns a
        new Direction2d object with the resulting vector.

        :param other: Direction3d object to add
        :type other: Direction3d
        :return: the resulting Direction3d object
        :rtype: Direction3d
        """
        if type(other).__name__ != "Direction3d":
            raise TypeError("Direction3d objects can only be summed with other"
                            "Direction3d objects")

        direction = copy.copy(self)
        direction.apply_direction(other)
        return direction

    def __eq__(self, other):
        """
        Compares two Direction3d objects and evaluates if they both point in
        the same direction. Returns True if both the directions match and
        False otherwise.

        :param other: the other Direction3d object
        :type other: gtFrame.direction.Direction3d
        :return: returns True if the directions match within tolerance and
            False if not
        :rtype: bool
        """
        if not isinstance(other, Direction3d):
            raise TypeError("Can only compare Direction3d to Direction3d"
                            "objects.")

        transformed = other.transform_to(self.reference)
        return np.allclose(self.vector, transformed, rtol=self.rtol)

    def __mul__(self, other):
        """
        Scales the direction vector by an amount given by 'other' and returns
        a new Direction3d object with the scaled vector.

        :param other: the scaling factor for the direction vector
        :type other: float
        :return: a new Direction2d object with the scaled vector
        :rtype: Direction3d
        """
        try:
            factor = float(other)
        except ValueError:
            raise ValueError("A Direction3d object can only be scaled "
                             "with a number.")
        except TypeError:
            raise TypeError("A Direction3d object can only be scaled "
                            "with a number.")

        return Direction3d(self.vector * factor, self.reference, self.rtol)

    def apply_direction(self, direction):
        """
        Adds the vector of 'direction' to the vector of self, after
        transforming it in to self.reference.

        :param direction: the Direction3d object to be applied to this one
        :type direction: Direction3d
        :return: None
        """
        rotated = direction.transform_to(self.reference)
        self.vector = self.vector + rotated

    def length(self):
        """
        Returns the length (i.e. euclidean norm) of the direction vector.

        :return: the euclidean norm of the direction vector
        :rtype: float
        """
        return np.linalg.norm(self.vector)

    def scale(self, factor):
        """
        Scales the length of the direction vector, by multiplying it with a
        factor.

        :param factor: the factor for scaling the vector
        :type factor: float
        :return: None
        """
        try:
            factor = float(factor)
        except ValueError:
            raise ValueError("A Direction3d object can only be scaled "
                             "with a number.")
        except TypeError:
            raise TypeError("A Direction3d object can only be scaled "
                            "with a number.")
        self.vector = self.vector * factor

    def transform_to(self, reference):
        """
        Transform the direction vector into another frame of reference.

        :param reference: the frame of reference to transform to
        :type reference: gtFrame.basic.Frame3d
        :return: the direction vector in the other frame of reference
        :rtype: np.ndarray
        """
        path = self.reference.find_transform_path(reference)
        return Frame3d.rotate_via_path(self.vector, path)
