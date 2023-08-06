"""
Tests for the :mod:`gtFrame.rotation` module
"""
import math
import random

import numpy as np

from gtFrame.rotation import Rotation2d

# TOLERANCES
RTOL = 1e-12


class TestRotation2d:
    """
    Tests for the :class:`gtFrame.rotation.Rotation2d`
    """
    def test_constructor(self):
        """
        Test the constructor.

        :return: None
        """
        angle = random.random() * (2 * math.pi)
        rot = Rotation2d(angle)

        expected_matrix = np.array([
            [math.cos(angle), - math.sin(angle)],
            [math.sin(angle), math.cos(angle)]], dtype=np.float64)

        assert rot._angle == angle
        assert np.allclose(rot._matrix, expected_matrix, rtol=RTOL)

    def test_apply_static(self):
        """
        Test the .apply method.

        :return: None
        """
        angle_0 = math.pi / 2
        rot_0 = Rotation2d(angle_0)
        vector_0 = np.array([3, 2])
        expected_0 = np.array([-2, 3])

        angle_1 = math.pi
        rot_1 = Rotation2d(angle_1)
        vector_1 = np.array([1, 0])
        expected_1 = np.array([-1, 0])

        angle_2 = math.pi / 4
        rot_2 = Rotation2d(angle_2)
        vector_2 = np.array([5, 0])
        expected_2 = np.array([(math.sqrt(2) / 2) * 5, (math.sqrt(2) / 2) * 5])

        assert np.allclose(rot_0.apply(vector_0), expected_0, rtol=RTOL)
        assert np.allclose(rot_1.apply(vector_1), expected_1, rtol=RTOL)
        assert np.allclose(rot_2.apply(vector_2), expected_2, rtol=RTOL)

    def test_apply_random(self):
        """
        Test .apply method with random values.

        :return: None
        """
        angles = [random.random() for i in range(20)]

        for angle in angles:
            vector = np.random.random(2)
            vector_copy = vector.copy()
            rot = Rotation2d(angle)

            expected = rot.as_matrix() @ vector

            assert np.allclose(rot.apply(vector), expected, rtol=RTOL)
            # Check that vector hasn't changed.
            assert np.all(vector == vector_copy)

    def test_apply_inverse_random(self):
        """
        Test the .apply_inverse method with random values.

        :return: None
        """
        vector = np.random.rand(2)
        angle = random.random() * (2 * math.pi)
        rot = Rotation2d(angle)

        rotated_vector = rot.apply(vector)

        assert np.allclose(rot.apply_inverse(rotated_vector), vector,
                           rtol=RTOL)

    def test_as_degree_static(self):
        """
        Test .as_degree method with static values.

        :return: None
        """
        angles = np.array([i for i in range(-20, 20)])
        degrees = np.degrees(angles)

        checks = []

        for index in range(len(angles)):
            rot = Rotation2d(angles[index])
            checks.append(math.isclose(rot.as_degrees(), degrees[index],
                                       rel_tol=RTOL))

        assert all(checks)

    def test_as_degree_random(self):
        """
        Test .as_degree method with random values.

        :return: None
        """
        angles = np.array([random.random() for _ in range(0, 20)])
        degrees = np.degrees(angles)

        checks = []

        for index in range(len(angles)):
            rot = Rotation2d(angles[index])
            checks.append(math.isclose(rot.as_degrees(), degrees[index],
                                       rel_tol=RTOL))

        assert all(checks)

    def test_as_inverse_static(self):
        """
        Test the .as_inverse method with static values.

        :return: None
        """
        angle = math.pi / 4
        expected_inverse = np.array([[0.70710678,  0.70710678],
                                    [-0.70710678,  0.70710678]],
                                    dtype=np.float64)
        rot = Rotation2d(angle)

        assert np.allclose(rot.as_inverse(), expected_inverse, rtol=RTOL)

    def test_as_inverse_random(self):
        """
        Test the .as_inverse method with random values.

        :return: None
        """
        angle = random.random() * (2 * math.pi)
        rot = Rotation2d(angle)
        matrix = np.array([[math.cos(angle), - math.sin(angle)],
                           [math.sin(angle), math.cos(angle)]],
                          dtype=np.float64)
        expected_inverse = np.linalg.inv(matrix)

        assert np.allclose(rot.as_inverse(), expected_inverse, rtol=RTOL)

    def test_as_matrix_static(self):
        """
        Test .as_matrix method with static values.

        :return: None
        """
        angle_0 = 0
        matrix_0 = np.array([[1, 0],
                            [0, 1]])
        rot_0 = Rotation2d(angle_0)

        angle_1 = math.pi / 2
        matrix_1 = np.array([[0, -1],
                            [1, 0]])
        rot_1 = Rotation2d(angle_1)

        angle_2 = math.pi
        matrix_2 = np.array([[-1, 0],
                             [0, -1]])
        rot_2 = Rotation2d(angle_2)

        assert np.allclose(rot_0.as_matrix(), matrix_0, rtol=RTOL)
        assert np.allclose(rot_1.as_matrix(), matrix_1, rtol=RTOL)
        assert np.allclose(rot_2.as_matrix(), matrix_2, rtol=RTOL)

    def test_as_matrix_random(self):
        """
        Test .as_matrix method with random angles.

        :return: None
        """
        angles = [random.random() for _ in range(20)]

        for angle in angles:
            rot = Rotation2d(angle)
            expected_matrix = np.array([[math.cos(angle), - math.sin(angle)],
                                        [math.sin(angle), math.cos(angle)]])
            assert np.allclose(rot.as_matrix(), expected_matrix, rtol=RTOL)

    def test_as_rad_static(self):
        """
        Test .as_rad method with static values.

        :return: None
        """
        angles = [i for i in range(-20, 20)]

        checks = []

        for angle in angles:
            rot = Rotation2d(angle)
            checks.append(rot.as_rad() == angle)

        assert all(checks)

    def test_is_close(self):
        """
        Test the .is_close method of the :class:`gtFrame.rotation.Rotation2d`.

        :return: None
        """
        tested_rtol = 1e-12

        angle_0 = random.random()
        angles_0 = [angle_0, angle_0]
        rot_0_a = Rotation2d(angles_0[0])
        rot_0_b = Rotation2d(angles_0[1])

        angle_1 = random.random()
        angles_1 = [angle_1, (tested_rtol * 1.1) * angle_1]
        rot_1_a = Rotation2d(angles_1[0])
        rot_1_b = Rotation2d(angles_1[1])

        assert rot_0_a.is_close(rot_0_b, rtol=tested_rtol)
        assert not rot_1_a.is_close(rot_1_b, rtol=tested_rtol)

    def test_update(self):
        """
        Test the update method with random values.

        :return: None
        """
        initial_angle = random.random()
        angles = [random.random() for _ in range(20)]

        rot = Rotation2d(initial_angle)

        for angle in angles:
            rot.update(angle)
            expected_matrix = np.array([[math.cos(angle), - math.sin(angle)],
                                        [math.sin(angle), math.cos(angle)]])
            assert math.isclose(rot.as_rad(), angle, rel_tol=RTOL)
            assert np.allclose(rot.as_matrix(), expected_matrix, rtol=RTOL)
