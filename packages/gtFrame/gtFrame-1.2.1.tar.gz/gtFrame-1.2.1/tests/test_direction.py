"""
Tests for the :mod:`direction` module.
"""
import copy
import math
import random

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as Rotation3d

from gtFrame import DEFAULT_RTOL
from gtFrame.basic import Frame2d, Frame3d, origin2d, origin3d
from gtFrame.direction import Direction2d, Direction3d
from gtFrame.rotation import Rotation2d

# TOLERANCES
RTOL = 1e-12

# Defines how many iterations tests should run which run multiple times.
# ITERS
ITERS = 10


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


class TestDirection2d:
    """
    Holds tests for the Direction2d class.
    """
    def test_constructor_assign(self):
        """
        Tests whether the constructor assigns the correct fields.
        """
        vector = np.random.random(2)
        frame = random_frame2d()

        direction = Direction2d(vector, frame)

        assert np.allclose(direction.vector, vector, rtol=RTOL)
        assert direction.reference == frame

    def test_constructor_exception(self):
        """
        Tests whether the constructor throws an exception if an array with the
        wrong dimension is passed.
        """
        vector = np.random.random(random.randint(3, 100))
        frame = random_frame2d()

        with pytest.raises(ValueError):
            direction = Direction2d(vector, frame)      # noqa: F841

    def test_constructor_tolerances(self):
        """
        Test the assignment of rtol in the constructor.
        """
        vector = np.random.random(2)
        frame = random_frame2d()
        rtol = random.random()

        direction_a = Direction2d(vector, frame)
        direction_b = Direction2d(vector, frame, rtol=rtol)

        assert direction_a.rtol == DEFAULT_RTOL
        assert direction_b.rtol == rtol

    def test_add(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.__add__` method.
        """
        frame = Frame2d(np.random.random(2), Rotation2d(random.random()))
        direction_a = Direction2d(np.random.random(2), frame)
        direction_b = Direction2d(np.random.random(2), frame)

        result = direction_a + direction_b
        direction_a.apply_direction(direction_b)

        assert np.allclose(result.vector, direction_a.vector, rtol=RTOL)
        assert direction_a.reference == result.reference
        assert direction_a.rtol == result.rtol

    def test_add_type(self):
        """
        Tests whether the :meth:`gtFrame.direction.Direction2d._add__` method
        checks for class/variable type.
        """
        direction = Direction2d(np.random.random(2), origin2d)

        with pytest.raises(TypeError):
            direction + 1
        with pytest.raises(TypeError):
            direction + "1"
        with pytest.raises(TypeError):
            frame = Frame2d(np.random.random(2), Rotation2d(random.random()))
            direction + frame

    def test_eq_edgecases(self):
        """
        Tests the .__eq__ method with some edge cases.
        """
        # Testcase 1 - 0-Vector as direction
        vector = np.zeros(2)
        frame_a = random_frame2d()
        frame_b = random_frame2d()
        direction_a = Direction2d(vector, frame_a)
        direction_b = Direction2d(vector, frame_b)

        assert direction_a == direction_b

        # Testcase 2 - aligned frames of reference
        vector = np.random.random(2)
        position = np.random.random(2)
        rotation = Rotation2d(random.random() * 2 * math.pi)
        frame_a = Frame2d(position, rotation, parent_frame=origin2d)
        frame_b = Frame2d(position, rotation, parent_frame=origin2d)
        direction_a = Direction2d(vector, frame_a)
        direction_b = Direction2d(vector, frame_b)

        assert direction_a == direction_b

    def test_eq_random(self):
        """
        Tests the .__eq__ method with random values.
        """
        vector = np.random.random(2)
        last_frame = origin2d
        direction_a = Direction2d(vector, last_frame)

        for i in range(random.randint(1, 100)):
            frame = random_frame2d(last_frame)
            last_frame = frame

            # rotate vector
            path = direction_a.reference.find_transform_path(frame)
            rotated = Frame2d.rotate_via_path(vector, path)

            direction_b = Direction2d(rotated, frame)

            assert direction_a == direction_b

    def test_mul(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.__mul__` method.
        """
        vector = np.random.random(2)
        frame = random_frame2d()
        r_tol = random.random()
        direction = Direction2d(vector, frame, r_tol)

        factor = random.random() * 10
        scaled = direction * factor

        assert np.allclose(scaled.vector, direction.vector * factor, rtol=RTOL)
        assert scaled.reference == direction.reference
        assert scaled.rtol == direction.rtol

    def test_mul_int(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.__mul__` method with
        integers as factors.
        """
        vector = np.random.random(2)
        frame = random_frame2d()
        r_tol = random.random()
        direction = Direction2d(vector, frame, r_tol)

        for factor in range(ITERS):
            scaled = direction * factor

            assert np.allclose(scaled.vector, direction.vector * factor,
                               rtol=RTOL)
            assert scaled.reference == direction.reference
            assert scaled.rtol == direction.rtol

    def test_mul_invalid(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.__mul__` method with
        invalid values as factors.
        """
        inv_1 = [0.2, 2]
        inv_2 = "hello"

        vector = np.random.random(2)
        frame = random_frame2d()
        r_tol = random.random()
        direction = Direction2d(vector, frame, r_tol)

        with pytest.raises(TypeError):
            direction * inv_1

        with pytest.raises(ValueError):
            direction * inv_2

    def test_apply_direction_static(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.apply_direction` method
        with static pre-defined test cases.
        """
        # testcase 1
        direction_1 = Direction2d(np.array([1, 1], dtype=np.float64), origin2d)
        frame = Frame2d(np.zeros(2), Rotation2d(- math.pi / 2),
                        parent_frame=origin2d)
        direction_2 = Direction2d(np.array([1, 0], dtype=np.float64), frame)
        expected = np.array([1, 0], dtype=np.float64)

        direction_1.apply_direction(direction_2)
        assert np.allclose(direction_1.vector, expected, rtol=RTOL)

        # testcase 2
        direction_1 = Direction2d(np.array([0, 1], dtype=np.float64), origin2d)
        frame = Frame2d(np.zeros(2), Rotation2d(math.pi / 2))
        direction_2 = Direction2d(np.array([1, 0], dtype=np.float64), frame)
        expected = np.array([0, 2], dtype=np.float64)

        direction_1.apply_direction(direction_2)
        assert np.allclose(direction_1.vector, expected, rtol=RTOL)

    def test_apply_direction_random(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.apply_direction` method
        with randomly generated values.
        """
        for _ in range(ITERS):
            direction_1 = Direction2d(np.random.random(2), origin2d)
            rotation = Rotation2d(random.random() * 2 * math.pi)
            frame = Frame2d(np.random.random(2), rotation)
            direction_2 = Direction2d(np.random.random(2), frame)

            expected = direction_1.vector + rotation.apply(direction_2.vector)
            direction_1.apply_direction(direction_2)
            assert np.allclose(direction_1.vector, expected, rtol=RTOL)

    def test_length(self):
        """
        Tests the .length method.
        """
        vector = np.random.random(2)
        frame = random_frame2d()
        direction = Direction2d(vector, frame)

        expected = np.linalg.norm(vector)

        assert direction.length() == expected

    def test_scale(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.scale` method.
        """
        vector = np.random.random(2)
        frame = random_frame2d()
        r_tol = random.random()
        direction = Direction2d(vector, frame, r_tol)

        factor = random.random() * 10
        direction.scale(factor)

        assert np.allclose(direction.vector, vector * factor, rtol=RTOL)

    def test_scale_int(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.scale` method with
        integers as factors.
        """
        vector = np.random.random(2)
        frame = random_frame2d()
        r_tol = random.random()
        direction = Direction2d(vector, frame, r_tol)

        for factor in range(ITERS):
            scaled = copy.copy(direction)
            scaled.scale(factor)

            assert np.allclose(scaled.vector, direction.vector * factor,
                               rtol=RTOL)

    def test_scale_invalid(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.scale` method with
        invalid values as factors.
        """
        inv_1 = [0.2, 2]
        inv_2 = "hello"

        vector = np.random.random(2)
        frame = random_frame2d()
        r_tol = random.random()
        direction = Direction2d(vector, frame, r_tol)

        with pytest.raises(TypeError):
            direction.scale(inv_1)

        with pytest.raises(ValueError):
            direction.scale(inv_2)

    def test_transform_to_random(self):
        """
        Tests whether the .transform_to method with random values.
        """
        vector = np.random.random(2)
        latest_frame = origin2d
        direction = Direction2d(vector, origin2d)
        rotated = vector

        for i in range(random.randint(1, 100)):
            frame = random_frame2d(latest_frame)
            latest_frame = frame
            rotated = frame.rotation.apply_inverse(rotated)

        assert np.allclose(direction.transform_to(latest_frame), rotated,
                           rtol=RTOL)

    def test_transform_to_compare(self):
        """
        Tests the .transform_to method by comparing it against .transform_to
        from Frame2d. If all the frames are pivoting around the same point
        (chosen to be [0, 0]) then the result from a transformation with
        translation and a pure rotation should match.
        """
        position = np.zeros(2)

        system = [origin2d]
        # create a system of frames
        for i in range(random.randint(1, 100)):
            rotation = Rotation2d(random.random() * 2 * math.pi)
            frame = Frame2d(position, rotation,
                            parent_frame=random.choice(system))
            system.append(frame)

        # run comparison tests
        for i in range(ITERS):
            vector = np.random.random(2)
            frame_a = random.choice(system)
            frame_b = random.choice(system)
            direction = Direction2d(vector, frame_a)

            assert np.allclose(direction.transform_to(frame_b),
                               frame_a.transform_to(frame_b, vector),
                               rtol=RTOL)


class TestDirection3d:
    """
    Holds tests for the Direction3d class.
    """
    def test_constructor_assign(self):
        """
        Tests whether the constructor assigns the correct fields.
        """
        vector = np.random.random(3)
        frame = random_frame3d()

        direction = Direction3d(vector, frame)

        assert np.allclose(direction.vector, vector, rtol=RTOL)
        assert direction.reference == frame

    def test_constructor_exception(self):
        """
        Tests whether the constructor throws an exception if an array with the
        wrong dimension is passed.
        """
        vector = np.random.random(random.randint(4, 100))
        frame = random_frame3d()

        with pytest.raises(ValueError):
            direction = Direction3d(vector, frame)      # noqa: F841

    def test_constructor_tolerances(self):
        """
        Test the assignment of rtol in the constructor.
        """
        vector = np.random.random(3)
        frame = random_frame3d()
        rtol = random.random()

        direction_a = Direction3d(vector, frame)
        direction_b = Direction3d(vector, frame, rtol=rtol)

        assert direction_a.rtol == DEFAULT_RTOL
        assert direction_b.rtol == rtol

    def test_transform_to_random(self):
        """
        Tests whether the .transform_to method with random values.
        """
        vector = np.random.random(3)
        latest_frame = origin3d
        direction = Direction3d(vector, origin3d)
        rotated = vector

        for i in range(random.randint(1, 100)):
            frame = random_frame3d(latest_frame)
            latest_frame = frame
            rotated = frame.rotation.inv().apply(rotated)

        assert np.allclose(direction.transform_to(latest_frame), rotated,
                           rtol=RTOL)

    def test_add(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.__add__` method.
        """
        frame = Frame3d(np.random.random(3),
                        Rotation3d.from_rotvec(np.random.random(3)))
        direction_a = Direction3d(np.random.random(3), frame)
        direction_b = Direction3d(np.random.random(3), frame)

        result = direction_a + direction_b
        direction_a.apply_direction(direction_b)

        assert np.allclose(result.vector, direction_a.vector, rtol=RTOL)
        assert direction_a.reference == result.reference
        assert direction_a.rtol == result.rtol

    def test_add_type(self):
        """
        Tests whether the :meth:`gtFrame.direction.Direction3d._add__` method
        checks for class/variable type.
        """
        direction = Direction3d(np.random.random(3), origin3d)

        with pytest.raises(TypeError):
            direction + 1
        with pytest.raises(TypeError):
            direction + "1"
        with pytest.raises(TypeError):
            frame = Frame3d(np.random.random(3),
                            Rotation3d.from_rotvec(np.random.random(3)))
            direction + frame

    def test_eq_edgecases(self):
        """
        Tests the .__eq__ method with some edge cases.
        """
        # Testcase 1 - 0-Vector as direction
        vector = np.zeros(3)
        frame_a = random_frame3d()
        frame_b = random_frame3d()
        direction_a = Direction3d(vector, frame_a)
        direction_b = Direction3d(vector, frame_b)

        assert direction_a == direction_b

        # Testcase 2 - aligned frames of reference
        vector = np.random.random(3)
        position = np.random.random(3)
        rotation = Rotation3d.from_rotvec(np.random.random(3))
        frame_a = Frame3d(position, rotation, parent_frame=origin3d)
        frame_b = Frame3d(position, rotation, parent_frame=origin3d)
        direction_a = Direction3d(vector, frame_a)
        direction_b = Direction3d(vector, frame_b)

        assert direction_a == direction_b

    def test_eq_random(self):
        """
        Tests the .__eq__ method with random values.
        """
        vector = np.random.random(3)
        last_frame = origin3d
        direction_a = Direction3d(vector, last_frame)

        for i in range(random.randint(1, 100)):
            frame = random_frame3d(last_frame)
            last_frame = frame

            # rotate vector
            path = direction_a.reference.find_transform_path(frame)
            rotated = Frame3d.rotate_via_path(vector, path)

            direction_b = Direction3d(rotated, frame)

            assert direction_a == direction_b

    def test_mul(self):
        """
        Tests the :meth:`gtFrame.direction.Direction3d.__mul__` method.
        """
        vector = np.random.random(3)
        frame = random_frame3d()
        r_tol = random.random()
        direction = Direction3d(vector, frame, r_tol)

        factor = random.random() * 10
        scaled = direction * factor

        assert np.allclose(scaled.vector, direction.vector * factor, rtol=RTOL)
        assert scaled.reference == direction.reference
        assert scaled.rtol == direction.rtol

    def test_mul_int(self):
        """
        Tests the :meth:`gtFrame.direction.Direction3d.__mul__` method with
        integers as factors.
        """
        vector = np.random.random(3)
        frame = random_frame3d()
        r_tol = random.random()
        direction = Direction3d(vector, frame, r_tol)

        for factor in range(ITERS):
            scaled = direction * factor

            assert np.allclose(scaled.vector, direction.vector * factor,
                               rtol=RTOL)
            assert scaled.reference == direction.reference
            assert scaled.rtol == direction.rtol

    def test_mul_invalid(self):
        """
        Tests the :meth:`gtFrame.direction.Direction3d.__mul__` method with
        invalid values as factors.
        """
        inv_1 = [0.2, 2]
        inv_2 = "hello"

        vector = np.random.random(3)
        frame = random_frame3d()
        r_tol = random.random()
        direction = Direction3d(vector, frame, r_tol)

        with pytest.raises(TypeError):
            direction * inv_1

        with pytest.raises(ValueError):
            direction * inv_2

    def test_apply_direction_static(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.apply_direction` method
        with static pre-defined test cases.
        """
        # testcase 1
        direction_1 = Direction3d(np.array([1, 1, 0], dtype=np.float64),
                                  origin3d)
        frame = Frame3d(np.zeros(3),
                        Rotation3d.from_rotvec([0, 0, - math.pi / 2]),
                        parent_frame=origin3d)
        direction_2 = Direction3d(np.array([1, 0, 0], dtype=np.float64), frame)
        expected = np.array([1, 0, 0], dtype=np.float64)

        direction_1.apply_direction(direction_2)
        assert np.allclose(direction_1.vector, expected, rtol=RTOL)

        # testcase 2
        direction_1 = Direction3d(np.array([0, 1, 0], dtype=np.float64),
                                  origin3d)
        frame = Frame3d(np.zeros(3),
                        Rotation3d.from_rotvec([0, 0, math.pi / 2]))
        direction_2 = Direction3d(np.array([1, 0, 0], dtype=np.float64), frame)
        expected = np.array([0, 2, 0], dtype=np.float64)

        direction_1.apply_direction(direction_2)
        assert np.allclose(direction_1.vector, expected, rtol=RTOL)

    def test_apply_direction_random(self):
        """
        Tests the :meth:`gtFrame.direction.Direction2d.apply_direction` method
        with randomly generated values.
        """
        for _ in range(ITERS):
            direction_1 = Direction3d(np.random.random(3), origin3d)
            rotation = Rotation3d.from_rotvec(np.random.random(3))
            frame = Frame3d(np.random.random(3), rotation)
            direction_2 = Direction3d(np.random.random(3), frame)

            expected = direction_1.vector + rotation.apply(direction_2.vector)
            direction_1.apply_direction(direction_2)
            assert np.allclose(direction_1.vector, expected, rtol=RTOL)

    def test_length(self):
        """
        Tests the .length method.
        """
        vector = np.random.random(3)
        frame = random_frame3d()
        direction = Direction3d(vector, frame)

        expected = np.linalg.norm(vector)

        assert direction.length() == expected

    def test_scale(self):
        """
        Tests the :meth:`gtFrame.direction.Direction3d.scale` method.
        """
        vector = np.random.random(3)
        frame = random_frame3d()
        r_tol = random.random()
        direction = Direction3d(vector, frame, r_tol)

        factor = random.random() * 10
        direction.scale(factor)

        assert np.allclose(direction.vector, vector * factor, rtol=RTOL)

    def test_scale_int(self):
        """
        Tests the :meth:`gtFrame.direction.Direction3d.scale` method with
        integers as factors.
        """
        vector = np.random.random(3)
        frame = random_frame3d()
        r_tol = random.random()
        direction = Direction3d(vector, frame, r_tol)

        for factor in range(ITERS):
            scaled = copy.copy(direction)
            scaled.scale(factor)

            assert np.allclose(scaled.vector, direction.vector * factor,
                               rtol=RTOL)

    def test_scale_invalid(self):
        """
        Tests the :meth:`gtFrame.direction.Direction3d.scale` method with
        invalid values as factors.
        """
        inv_1 = [0.2, 2]
        inv_2 = "hello"

        vector = np.random.random(3)
        frame = random_frame3d()
        r_tol = random.random()
        direction = Direction3d(vector, frame, r_tol)

        with pytest.raises(TypeError):
            direction.scale(inv_1)

        with pytest.raises(ValueError):
            direction.scale(inv_2)

    def test_transform_to_compare(self):
        """
        Tests the .transform_to method by comparing it against .transform_to
        from Frame3d. If all the frames are pivoting around the same point
        (chosen to be [0, 0, 0]) then the result from a transformation with
        translation and a pure rotation should match.
        """
        position = np.zeros(3)

        system = [origin3d]
        # create a system of frames
        for i in range(random.randint(1, 100)):
            rotation = Rotation3d.from_rotvec(np.random.random(3))
            frame = Frame3d(position, rotation,
                            parent_frame=random.choice(system))
            system.append(frame)

        # run comparison tests
        for i in range(ITERS):
            vector = np.random.random(3)
            frame_a = random.choice(system)
            frame_b = random.choice(system)
            direction = Direction3d(vector, frame_a)

            assert np.allclose(direction.transform_to(frame_b),
                               frame_a.transform_to(frame_b, vector),
                               rtol=RTOL)
