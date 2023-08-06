import math
import random

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as Rotation3d

from gtFrame import DEFAULT_RTOL
from gtFrame.basic import Frame2d, Frame3d, origin2d, origin3d
from gtFrame.direction import Direction2d, Direction3d
from gtFrame.position import Position2d, Position3d
from gtFrame.rotation import Rotation2d

# TOLERANCES
RTOL = 1e-12

# Defines how many iterations tests should run which run multiple times.
# ITERS
ITERS = 10


def random_direction2d(vector=None, reference=None, rtol=DEFAULT_RTOL):
    """
    Generates a random Direction2d object with random values, but rtol will
    be set to DEFAULT_RTOL

    :param vector: override direction vector
    :type vector: np.ndarray
    :param reference: override reference
    :type reference: gtFrame.basic.Frame2d
    :param rtol: override rtol; default is DEFAULT_RTOL, set this to None if
        rtol should also be random
    :type rtol: float
    :return: a random Direction2d object
    :rtype: gtFrame.direction.Direction2d
    """
    if vector is None:
        vector = np.random.random(2)
    if reference is None:
        reference = random_frame2d()
    if rtol is None:
        rtol = random.random()
    return Direction2d(vector, reference, rtol)


def random_direction3d(vector=None, reference=None, rtol=DEFAULT_RTOL):
    """
    Generates a random Direction3d object with random values, but rtol will
    be set to DEFAULT_RTOL

    :param vector: override direction vector
    :type vector: np.ndarray
    :param reference: override reference
    :type reference: gtFrame.basic.Frame3d
    :param rtol: override rtol; default is DEFAULT_RTOL, set this to None if
        rtol should also be random
    :type rtol: float
    :return: a random Direction3d object
    :rtype: gtFrame.direction.Direction3d
    """
    if vector is None:
        vector = np.random.random(3)
    if reference is None:
        reference = random_frame3d()
    if rtol is None:
        rtol = random.random()
    return Direction3d(vector, reference, rtol)


def random_frame2d(parent=origin2d):
    """
    Generates a random Frame2d frame of reference with random values.

    :param parent: the desired parent frame (default is origin2d)
    :type parent: gtFrame.basic.Frame2d
    :return: a randomly generated Frame2d object
    :rtype: gtFrame.basic.Frame2d
    """
    rotation = Rotation2d(random.random() * 2 * math.pi)
    position = np.random.random(2)
    return Frame2d(position, rotation, parent_frame=parent)


def random_frame3d(parent=origin3d):
    """
    Generates a random Frame3d frame of reference with random values.

    :param parent: the desired parent frame (default is origin2d)
    :type parent: gtFrame.basic.Frame3d
    :return: a randomly generated Frame3d object
    :rtype: gtFrame.basic.Frame3d
    """
    rotation = Rotation3d.from_rotvec(np.random.random(3))
    position = np.random.random(3)
    return Frame3d(position, rotation, parent_frame=parent)


def random_position2d(coordinates=None, reference=None):
    """
    Generates a random Position2d object with random values.

    :param coordinates: override random coordinates assigned to object
    :type coordinates: np.ndarray
    :param reference: override random reference assigned to object
    :type reference: gtFrame.basic.Frame2d
    """
    if coordinates is None:
        coordinates = np.random.random(2)
    if reference is None:
        reference = random_frame2d()

    return Position2d(coordinates, reference)


def random_position3d(coordinates=None, reference=None):
    """
    Generates a random Position3d object with random values.

    :param coordinates: override random coordinates assigned to object
    :type coordinates: np.ndarray
    :param reference: override random reference assigned to object
    :type reference: gtFrame.basic.Frame3d
    """
    if coordinates is None:
        coordinates = np.random.random(3)
    if reference is None:
        reference = random_frame3d()

    return Position3d(coordinates, reference)


class TestPosition2d:
    """
    Holds tests for Position2d.
    """
    def test_constructor_assign(self):
        """
        Tests whether the constructor correctly assigns the attributes.

        :return: None
        """
        coordinates = np.random.random(2)
        frame = random_frame2d()

        position = Position2d(coordinates, frame)

        assert np.allclose(position.coordinates, coordinates, rtol=RTOL)
        assert position.reference == frame

    def test_constructor_exception(self):
        """
        Tests whether the constructor raises an error if the wrong dimension
        vector is passed.

        :return: None
        """
        coordinates = np.random.random(random.randint(3, 100))
        frame = random_frame2d()

        with pytest.raises(ValueError):
            position = Position2d(coordinates, frame)       # noqa: F841

    def test_constructor_tolerances(self):
        """
        Test the assignment of the rtol attribute on init.
        """
        coordinates = np.random.random(2)
        frame = random_frame2d()
        rtol = random.random()

        position_a = Position2d(coordinates, frame)
        position_b = Position2d(coordinates, frame, rtol=rtol)

        assert position_a.rtol == DEFAULT_RTOL
        assert position_b.rtol == rtol

    def test_eq(self):
        """
        Tests the == operator (i.e. the __eq__ method).

        :return: None
        """
        coordinates = np.random.random(2)
        frame_a = random_frame2d()
        frame_b = random_frame2d()

        position_a = Position2d(coordinates, frame_a)
        position_b = Position2d(frame_b.transform_from(frame_a, coordinates),
                                frame_b)

        assert position_a == position_b

    def test_add_direction_static(self):
        """
        Tests the .add_direction method with static testcases. This test
        assumes that the comparison between Position2d objects is valid.
        """
        # Testcase 1 - 0-Direction
        position = Position2d(np.random.random(2), origin2d)
        direction = Direction2d(np.zeros(2), origin2d)

        result = position.add_direction(direction)
        expected = Position2d(position.coordinates, origin2d)

        assert result == expected

        # Testcase 2
        position = Position2d(np.array([0, 1]), origin2d)
        frame = Frame2d(np.zeros(2), Rotation2d(math.pi / 2), origin2d)
        direction = Direction2d(np.array([0, 1]), frame)

        result = position.add_direction(direction)
        expected = Position2d(np.array([-1, 1]), origin2d)

        assert result == expected

    def test_add_direction_inheritance(self):
        """
        Tests whether the returned objects from .add_direction method inherit
        the reference and rtol from the calling object.
        """
        frame = random_frame2d()
        position = Position2d(np.random.random(2), frame, rtol=random.random())
        direction = random_direction2d()

        result = position.add_direction(direction)

        assert result.reference == position.reference
        assert result.rtol == position.rtol

    def test_add_direction_random(self):
        """
        Tests the .add_direction method with random values.
        """
        for i in range(ITERS):
            position = random_position2d()
            direction = random_direction2d()

            result = position.add_direction(direction)

            transformed = direction.transform_to(position.reference)
            expected_coordinates = position.coordinates + transformed
            expected = Position2d(expected_coordinates, position.reference)

            assert result == expected

    def test_add_direction_reversible(self):
        """
        Tests whether adding the direction gained from .get_direction method
        results in the other position coordinates. This test relies on the
        validity of .get_direction.
        """
        for i in range(ITERS):
            position_a = random_position2d()
            position_b = random_position2d()

            direction = position_a.get_direction(position_b)

            assert position_a.add_direction(direction) == position_b

    def test_apply_direction(self):
        """
        Tests the .apply_direction method by comparing it to results from
        the .add_direction method. This test therefore relies on the validity
        of the .add_direction method.
        """
        for i in range(ITERS):
            position = random_position2d()
            direction = random_direction2d()

            expected = position.add_direction(direction)
            position.apply_direction(direction)

            assert position == expected

    def test_get_direction_static(self):
        """
        Tests the .get_direction method with static pre-defined testcases.
        """
        # Testcase 1
        position_a = Position2d(np.array([1, 1]), origin2d)
        frame_b = Frame2d(np.array([1, 0]), Rotation2d(0), origin2d)
        position_b = Position2d(np.array([1, 1]), frame_b)

        direction = position_a.get_direction(position_b)
        expected = Direction2d(np.array([1, 0]), origin2d)

        assert np.allclose(direction.vector, expected.vector, rtol=RTOL)
        assert direction.reference == expected.reference

        # Testcase 2
        position_a = Position2d(np.array([0, 1]), origin2d)
        frame_b = Frame2d(np.array([0, 0]), Rotation2d(math.pi / 2))
        position_b = Position2d(np.array([1, 0]), frame_b)

        direction = position_a.get_direction(position_b)
        expected = Direction2d(np.array([0, 0]), origin2d)

        assert np.allclose(direction.vector, expected.vector, rtol=RTOL)
        assert direction.reference == expected.reference

    def test_get_direction_random(self):
        """
        Tests the .get_direction method with random values. The test assumes
        that adding the direction to position_a should result in position_b.
        Furthermore, this test assumes that the comparison between two
        Position2d objects is valid.
        """
        for i in range(ITERS):
            position_a = random_position2d()
            position_b = random_position2d()

            direction = position_a.get_direction(position_b)

            control_coordinates = position_a.coordinates + direction.vector
            control = Position2d(control_coordinates, position_a.reference)

            assert position_b == control

    def test_get_distance_compare(self):
        """
        Tests the .get_distance method by comparing to Direction2d object
        return from .get_direction. This test relies on the validity of the
        .get_direction and Distance2d.length() method.
        """
        for i in range(ITERS):
            position_a = random_position2d()
            position_b = random_position2d()

            expected = position_a.get_direction(position_b).length()

            assert position_a.get_distance(position_b) == expected

    def test_get_distance_symmetry(self):
        """
        Tests the .get_distance method by checking whether selection invariance
        of two points is given. This means that
        position_a.get_distance(position_b) is the same as
        position_b.get_distance(position_a).
        """
        for i in range(ITERS):
            position_a = random_position2d()
            position_b = random_position2d()

            assert math.isclose(position_a.get_distance(position_b),
                                position_b.get_distance(position_a),
                                rel_tol=RTOL)

    def test_transform_to(self):
        """
        Test the transform_to method.

        :return: None
        """
        coordinates = np.random.random(2)
        frame = random_frame2d()
        foreign_frame = random_frame2d()
        position = Position2d(coordinates, frame)

        transformed = position.transform_to(foreign_frame)
        expected = foreign_frame.transform_from(frame, coordinates)

        assert np.allclose(transformed, expected, rtol=RTOL)


class TestPosition3d:
    """
    Holds tests for Position3d.
    """
    def test_constructor_assign(self):
        """
        Tests whether the constructor correctly assigns the attributes.

        :return: None
        """
        coordinates = np.random.random(3)
        frame = random_frame3d()

        position = Position3d(coordinates, frame)

        assert np.allclose(position.coordinates, coordinates, rtol=RTOL)
        assert position.reference == frame

    def test_constructor_exception(self):
        """
        Tests whether the constructor raises an error if the wrong dimension
        vector is passed.

        :return: None
        """
        coordinates = np.random.random(random.randint(4, 100))
        frame = random_frame3d()

        with pytest.raises(ValueError):
            position = Position3d(coordinates, frame)       # noqa:F841

    def test_constructor_tolerances(self):
        """
        Test the assignment of the rtol attribute on init.
        """
        coordinates = np.random.random(3)
        frame = random_frame3d()
        rtol = random.random()

        position_a = Position3d(coordinates, frame)
        position_b = Position3d(coordinates, frame, rtol=rtol)

        assert position_a.rtol == DEFAULT_RTOL
        assert position_b.rtol == rtol

    def test_eq(self):
        """
        Tests the == operator (i.e. the __eq__ method).

        :return: None
        """
        coordinates = np.random.random(3)
        frame_a = random_frame3d()
        frame_b = random_frame3d()

        position_a = Position3d(coordinates, frame_a)
        position_b = Position3d(frame_b.transform_from(frame_a, coordinates),
                                frame_b)

        assert position_a == position_b

    def test_add_direction_static(self):
        """
        Tests the .add_direction method with static testcases. This test
        assumes that the comparison between Position3d objects is valid.
        """
        # Testcase 1 - 0-Direction
        position = Position3d(np.random.random(3), origin3d)
        direction = Direction3d(np.zeros(3), origin3d)

        result = position.add_direction(direction)
        expected = Position3d(position.coordinates, origin3d)

        assert result == expected

        # Testcase 2
        position = Position3d(np.array([0, 1, 0]), origin3d)
        frame = Frame3d(np.zeros(3),
                        Rotation3d.from_rotvec(np.array([0, 0, math.pi / 2])),
                        origin3d)
        direction = Direction3d(np.array([0, 1, 0]), frame)

        result = position.add_direction(direction)
        expected = Position3d(np.array([-1, 1, 0]), origin3d)

        assert result == expected

    def test_add_direction_inheritance(self):
        """
        Tests whether the returned objects from .add_direction method inherit
        the reference and rtol from the calling object.
        """
        frame = random_frame3d()
        position = Position3d(np.random.random(3), frame, rtol=random.random())
        direction = random_direction3d()

        result = position.add_direction(direction)

        assert result.reference == position.reference
        assert result.rtol == position.rtol

    def test_add_direction_random(self):
        """
        Tests the .add_direction method with random values.
        """
        for i in range(ITERS):
            position = random_position3d()
            direction = random_direction3d()

            result = position.add_direction(direction)

            transformed = direction.transform_to(position.reference)
            expected_coordinates = position.coordinates + transformed
            expected = Position3d(expected_coordinates, position.reference)

            assert result == expected

    def test_add_direction_reversible(self):
        """
        Tests whether adding the direction gained from .get_direction method
        results in the other position coordinates. This test relies on the
        validity of .get_direction.
        """
        for i in range(ITERS):
            position_a = random_position3d()
            position_b = random_position3d()

            direction = position_a.get_direction(position_b)

            assert position_a.add_direction(direction) == position_b

    def test_apply_direction(self):
        """
        Tests the .apply_direction method by comparing it to results from
        the .add_direction method. This test therefore relies on the validity
        of the .add_direction method.
        """
        for i in range(ITERS):
            position = random_position3d()
            direction = random_direction3d()

            expected = position.add_direction(direction)
            position.apply_direction(direction)

            assert position == expected

    def test_get_direction_static(self):
        """
        Tests the .get_direction method with static pre-defined testcases.
        """
        # Testcase 1
        position_a = Position3d(np.array([1, 1, 0]), origin3d)
        frame_b = Frame3d(np.array([1, 0, 0]),
                          Rotation3d.from_rotvec(np.array([0, 0, 0])),
                          origin3d)
        position_b = Position3d(np.array([1, 1, 0]), frame_b)

        direction = position_a.get_direction(position_b)
        expected = Direction3d(np.array([1, 0, 0]), origin3d)

        assert np.allclose(direction.vector, expected.vector, rtol=RTOL)
        assert direction.reference == expected.reference

        # Testcase 2
        position_a = Position3d(np.array([0, 1, 0]), origin3d)
        frame_b = Frame3d(np.array([0, 0, 0]),
                          Rotation3d.from_rotvec(
                              np.array([0, 0, math.pi / 2])), origin3d)
        position_b = Position3d(np.array([1, 0, 0]), frame_b)

        direction = position_a.get_direction(position_b)
        expected = Direction3d(np.array([0, 0, 0]), origin3d)

        assert np.allclose(direction.vector, expected.vector, rtol=RTOL)
        assert direction.reference == expected.reference

    def test_get_direction_random(self):
        """
        Tests the .get_direction method with random values. The test assumes
        that adding the direction to position_a should result in position_b.
        Furthermore, this test assumes that the comparison between two
        Position3d objects is valid.
        """
        for i in range(ITERS):
            position_a = random_position3d()
            position_b = random_position3d()

            direction = position_a.get_direction(position_b)

            control_coordinates = position_a.coordinates + direction.vector
            control = Position3d(control_coordinates, position_a.reference)

            assert position_b == control

    def test_get_distance_compare(self):
        """
        Tests the .get_distance method by comparing to Direction3d object
        return from .get_direction. This test relies on the validity of the
        .get_direction and Distance2d.length() method.
        """
        for i in range(ITERS):
            position_a = random_position3d()
            position_b = random_position3d()

            expected = position_a.get_direction(position_b).length()

            assert position_a.get_distance(position_b) == expected

    def test_get_distance_symmetry(self):
        """
        Tests the .get_distance method by checking whether selection invariance
        of two points is given. This means that
        position_a.get_distance(position_b) is the same as
        position_b.get_distance(position_a).
        """
        for i in range(ITERS):
            position_a = random_position3d()
            position_b = random_position3d()

            assert math.isclose(position_a.get_distance(position_b),
                                position_b.get_distance(position_a),
                                rel_tol=RTOL)

    def test_transform_to(self):
        """
        Test the transform_to method.

        :return: None
        """
        coordinates = np.random.random(3)
        frame = random_frame3d()
        foreign_frame = random_frame3d()
        position = Position3d(coordinates, frame)

        transformed = position.transform_to(foreign_frame)
        expected = foreign_frame.transform_from(frame, coordinates)

        assert np.allclose(transformed, expected, rtol=RTOL)
