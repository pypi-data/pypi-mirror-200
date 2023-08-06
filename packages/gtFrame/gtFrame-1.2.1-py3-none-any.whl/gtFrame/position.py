"""
This module implements the position class, which acts as a wrapper containing
information about a position vector (either 2d or 3d numpy array) and the
frame of reference on which the vector coordinates are defined.

---------------
Module Contents
---------------
Classes:
    * Position2d
    * Position3d

"""
import numpy as np

from gtFrame import DEFAULT_RTOL
from gtFrame.direction import Direction2d, Direction3d


class Position2d:
    """
    This class holds the coordinates of a 2d vector in a numpy array and the
    frame of reference in which they have been defined.

    :param coordinates: the coordinates of the 2d-vector representing a point
        in space
    :type coordinates: np.ndarray
    :param reference: the reference in which the coordinates are defined
    :type reference: gtFrame.basic.Frame2d
    :param rtol: The relative tolerance to be used when comparing
        Position2d objects. The default is set to the global variable
        DEFAULT_RTOL.
    :type rtol: float
    """
    def __init__(self, coordinates, reference, rtol=DEFAULT_RTOL):
        """
        Constructor method.
        """
        if coordinates.shape != (2,):
            raise ValueError("The coordinates have to be two-dimensional.")

        self.coordinates = coordinates
        self.reference = reference
        self.rtol = rtol

    def __eq__(self, position):
        """
        Checks if two position objects point to the same point in space.

        :param position: a position object to check against self
        :type position: gtFrame.position.Position2d
        :return: True if the two positions point to the same point in space;
            False otherwise
        :rtype: bool
        """
        other = position.transform_to(self.reference)
        return np.allclose(self.coordinates, other, rtol=self.rtol)

    def add_direction(self, direction):
        """
        Returns the point that results in adding a direction vector to this
        point.

        :param direction: a direction vector to be added to the point
        :type direction: gtFrame.direction.Direction2d
        :return: The resulting point from the addition with a direction vector.
            The returned Position2d object will inherit the reference and rtol
            of this (self) object.
        :rtype: Position2d
        """
        rotated = direction.transform_to(self.reference)
        return Position2d(self.coordinates + rotated, self.reference,
                          rtol=self.rtol)

    def apply_direction(self, direction):
        """
        Adds a given direction vector to this Position2d object. This results
        in the same point as would be returned by the .add_direction method.
        The difference is that .apply_direction applies the changes to the
        coordinates from this object, while .add_direction creates a new
        :class:`gtFrame.direction.Position2d` object with the modified
        coordinates.

        :param direction: a direction vector to be added to the point
        :type direction: gtFrame.direction.Direction2d
        :return: None
        """
        rotated = direction.transform_to(self.reference)
        self.coordinates = self.coordinates + rotated

    def get_direction(self, other):
        """
        Returns the direction from one position to another as a
        :class:`gtFrame.direction.Direction2d` object. The
        :class:`gtFrame.direction.Direction2d` object will be defined on the
        reference of this object (i.e. self.reference)

        :param other: the other position to point to
        :type other: gtFrame.position.Position2d
        :return: the direction from this position to 'other' as a
            :class:`gtFrame.direction.Direction2d` object
        :rtype: gtFrame.direction.Direction2d
        """
        transformed = other.transform_to(self.reference)
        direction_vector = transformed - self.coordinates
        return Direction2d(direction_vector, self.reference, rtol=self.rtol)

    def get_distance(self, other):
        """
        Returns the distance from one position to another.

        :param other: the other position
        :type other: gtFrame.position.Position2d
        :return: distance to 'other' position
        :rtype: float
        """
        transformed = other.transform_to(self.reference)
        return np.linalg.norm(self.coordinates - transformed)

    def transform_to(self, reference):
        """
        Transform the coordinates of the vector into a desired reference.

        :param reference: the desired reference for the coordinates to be
            transformed into
        :type reference: gtFrame.basic.Frame2d
        :return: the transformed coordinates
        :rtype: np.ndarray
        """
        return self.reference.transform_to(reference, self.coordinates)


class Position3d:
    """
    This class holds the coordinates of a 3d vector in a numpy array and the
    frame of reference in which they have been defined.

    :param coordinates: the coordinates of the 3d-vector representing a point
        in space
    :type coordinates: np.ndarray
    :param reference: the reference in which the coordinates are defined
    :type reference: gtFrame.basic.Frame3d
    :param rtol: The relative tolerance to be used when comparing
        Position3d objects. The default is set to the global variable
        DEFAULT_RTOL.
    :type rtol: float
    """
    def __init__(self, coordinates, reference, rtol=DEFAULT_RTOL):
        """
        Constructor method.
        """
        if coordinates.shape != (3,):
            raise ValueError("The coordinates have to be two-dimensional.")

        self.coordinates = coordinates
        self.reference = reference
        self.rtol = rtol

    def __eq__(self, position):
        """
        Checks if two position objects point to the same point in space.

        :param position: a position object to check against self
        :type position: gtFrame.position.Position3d
        :return: True if the two positions point to the same point in space;
            False otherwise
        :rtype: bool
        """
        other = position.transform_to(self.reference)
        return np.allclose(self.coordinates, other, rtol=self.rtol)

    def add_direction(self, direction):
        """
        Returns the point that results in adding a direction vector to this
        point.

        :param direction: a direction vector to be added to the point
        :type direction: gtFrame.direction.Direction3d
        :return: The resulting point from the addition with a direction vector.
            The returned Position2d object will inherit the reference and rtol
            of this (self) object.
        :rtype: Position3d
        """
        rotated = direction.transform_to(self.reference)
        return Position3d(self.coordinates + rotated, self.reference,
                          rtol=self.rtol)

    def apply_direction(self, direction):
        """
        Adds a given direction vector to this Position3d object. This results
        in the same point as would be returned by the .add_direction method.
        The difference is that .apply_direction applies the changes to the
        coordinates from this object, while .add_direction creates a new
        :class:`gtFrame.direction.Position3d` object with the modified
        coordinates.

        :param direction: a direction vector to be added to the point
        :type direction: gtFrame.direction.Direction3d
        :return: None
        """
        rotated = direction.transform_to(self.reference)
        self.coordinates = self.coordinates + rotated

    def get_direction(self, other):
        """
        Returns the direction from one position to another as a
        :class:`gtFrame.direction.Direction3d` object. The
        :class:`gtFrame.direction.Direction3d` object will be defined on the
        reference of this object (i.e. self.reference)

        :param other: the other position to point to
        :type other: gtFrame.position.Position3d
        :return: the direction from this position to 'other' as a
            :class:`gtFrame.direction.Direction3d` object
        :rtype: gtFrame.direction.Direction3d
        """
        transformed = other.transform_to(self.reference)
        direction_vector = transformed - self.coordinates
        return Direction3d(direction_vector, self.reference, rtol=self.rtol)

    def get_distance(self, other):
        """
        Returns the distance from one position to another.

        :param other: the other position
        :type other: gtFrame.position.Position3d
        :return: distance to 'other' position
        :rtype: float
        """
        transformed = other.transform_to(self.reference)
        return np.linalg.norm(self.coordinates - transformed)

    def transform_to(self, reference):
        """
        Transform the coordinates of the vector into a desired reference.

        :param reference: the desired reference for the coordinates to be
            transformed into
        :type reference: gtFrame.basic.Frame3d
        :return: the transformed coordinates
        :rtype: np.ndarray
        """
        return self.reference.transform_to(reference, self.coordinates)
