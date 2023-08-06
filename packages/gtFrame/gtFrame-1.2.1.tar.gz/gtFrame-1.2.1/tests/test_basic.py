"""
Tests for the :mod:`gtFrame.basic` module.
"""
import math
import random

import numpy as np
import pytest
from scipy.spatial.transform import Rotation as Rotation3d

import gtFrame.basic
from gtFrame.basic import Frame2d
from gtFrame.basic import Frame3d
from gtFrame.basic import origin2d
from gtFrame.basic import origin3d
from gtFrame.basic import RootFrame2d
from gtFrame.basic import RootFrame3d
from gtFrame.rotation import Rotation2d

# TOLERANCES
RTOL = 1e-12


def generate_frame2d(parent=origin2d):
    """
    Generate a random :class:`gtFrame.basic.Frame2d`.

    :param parent: The parent of the generated :class:`gtFrame.basic.Frame2d`
        object. The default is origin2d.
    :type parent: gtFrame.basic.Frame2d
    :return: randomly generated Frame2d
    :rtype: gtFrame.basic.Frame2d
    """
    position = np.random.random(2)
    angle = random.random() * (2 * math.pi)
    rotation = Rotation2d(angle)
    return Frame2d(position, rotation, parent_frame=parent)


def generate_frame3d(parent=origin3d):
    """
    Generate a random :class:`gtFrame.basic.Frame3d`.

    :param parent: The parent of the generated :class:`gtFrame.basic.Frame3d`
        object. The default is origin3d.
    :type parent: gtFrame.basic.Frame3d
    :return: randomly generated Frame3d
    :rtype: gtFrame.basic.Frame3d
    """
    position = np.random.random(3)
    rotation = Rotation3d.from_rotvec(np.random.random(3))
    return Frame3d(position, rotation, parent_frame=parent)


@pytest.fixture
def random_frame2d():
    """
    Generate a random :class:`gtFrame.basic.Frame2d`.

    :return: randomly generated Frame2d
    :rtype: gtFrame.basic.Frame2d
    """
    position = np.random.random(2)
    angle = random.random() * (2 * math.pi)
    rotation = Rotation2d(angle)
    return Frame2d(position, rotation)


@pytest.fixture
def frame2d_system():
    """
    Generate a system of frames (Frame2d).

    origin
    ├── Frame 1
    │   └── Frame 2
    │       ├── Frame 3
    │       │   └── Frame 6
    │       └── Frame 7
    └── Frame 4
        └── Frame 5

    :return: generated system of frames as a list
    :rtype: list
    """
    system = list()
    desired_parents = ["O", 0, 1, "O", 3, 2, 1]

    for parent_idx in desired_parents:
        position = np.random.random(2)
        angle = random.random() * (2 * math.pi)
        rotation = Rotation2d(angle)

        if parent_idx == "O":
            frame = Frame2d(position, rotation)
        else:
            frame = Frame2d(position, rotation,
                            parent_frame=system[parent_idx])
        system.append(frame)

    return system


@pytest.fixture()
def random_frame3d():
    """
    Generate a random :class:`Frame3d` object.

    :return: the random Frame3d
    :rtype: Frame3d
    """
    position = np.random.random(3)
    rotation = Rotation3d.from_rotvec(np.random.random(3))
    frame = Frame3d(position, rotation)
    return frame


@pytest.fixture
def frame3d_system():
    """
    Generate a system of frames (Frame3d).

    origin
    ├── Frame 1
    │   └── Frame 2
    │       ├── Frame 3
    │       │   └── Frame 6
    │       └── Frame 7
    └── Frame 4
        └── Frame 5

    :return: the generated system of frames as a list
    :rtype: list
    """
    system = list()
    desired_parents = ["O", 0, 1, "O", 3, 2, 1]

    for parent_idx in desired_parents:
        position = np.random.random(3)
        rotation = Rotation3d.from_rotvec(np.random.random(3))

        if parent_idx == "O":
            frame = Frame3d(position, rotation)
        else:
            frame = Frame3d(position, rotation,
                            parent_frame=system[parent_idx])
        system.append(frame)

    return system


class TestModule:
    """
    Test for module attributes and functions.
    """
    def test_origin2d(self):
        """
        Test for existence and correctness of the origin2d variable.

        :return: None
        """
        assert np.allclose(gtFrame.basic.origin2d.position,
                           np.array([0, 0]), rtol=RTOL)
        assert gtFrame.basic.origin2d.rotation.as_rad() == 0

    def test_origin3d(self):
        """
        Test for existence and correctness of origin3d variable.

        :return: None
        """
        assert np.allclose(origin3d.position,
                           np.array([0, 0, 0], dtype=np.float64), rtol=RTOL)
        assert np.allclose(origin3d.rotation.as_matrix(), np.identity(3),
                           rtol=RTOL)


class TestRootFrame2d:
    """
    Tests for :class:`RootFrame2d`.
    """
    def test_constructor(self):
        """
        Test the constructor.

        :return: None
        """
        root_frame = RootFrame2d()

        assert np.allclose(root_frame.position, np.array([0, 0]), rtol=RTOL)
        assert root_frame.rotation.as_rad() == 0

    def test_find_transform_path(self, frame2d_system):
        """
        Test the find_transform_path method of RootFrame2d with static
        system-structure but random positions and rotations.

        :return: None
        """
        frame1 = frame2d_system[0]
        frame2 = frame2d_system[1]
        frame3 = frame2d_system[2]
        frame4 = frame2d_system[3]
        frame5 = frame2d_system[4]
        frame6 = frame2d_system[5]
        frame7 = frame2d_system[6]

        expected1 = [(frame1, "from")]
        expected2 = [(frame1, "from"), (frame2, "from")]
        expected3 = [(frame1, "from"), (frame2, "from"), (frame3, "from")]
        expected4 = [(frame4, "from")]
        expected5 = [(frame4, "from"), (frame5, "from")]
        expected6 = [(frame1, "from"), (frame2, "from"), (frame3, "from"),
                     (frame6, "from")]
        expected7 = [(frame1, "from"), (frame2, "from"), (frame7, "from")]

        assert expected1 == origin2d.find_transform_path(frame1)
        assert expected2 == origin2d.find_transform_path(frame2)
        assert expected3 == origin2d.find_transform_path(frame3)
        assert expected4 == origin2d.find_transform_path(frame4)
        assert expected5 == origin2d.find_transform_path(frame5)
        assert expected6 == origin2d.find_transform_path(frame6)
        assert expected7 == origin2d.find_transform_path(frame7)

    def test_transform_from(self, frame2d_system):
        """
        Test the .transform_from method with random vectors and random paths.
        :return: None
        """
        vectors = [np.random.random(2) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = frame2d_system[random.randint(0, 6)]
            destination = origin2d

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame2d.transform_via_path(vector, path)

            assert np.allclose(destination.transform_from(source, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_to(self, frame2d_system):
        """
        Test the .transform_to method with random vectors and random paths.
        :return: None
        """
        vectors = [np.random.random(2) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = origin2d
            destination = frame2d_system[random.randint(0, 6)]

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame2d.transform_via_path(vector, path)

            assert np.allclose(source.transform_to(destination, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_reversible(self, frame2d_system):
        """
        Test wether the .transform_to and transform_from methods are
        reversible.
        :return: None
        """
        vectors = [np.random.random(2) for _ in range(10)]

        for vector in vectors:
            source = origin2d
            destination = frame2d_system[random.randint(0, 6)]

            interim = source.transform_to(destination, vector)
            result = source.transform_from(destination, interim)

            assert np.allclose(result, vector, rtol=RTOL)


class TestFrame2d:
    """
    Test for :class:`gtFrame.basic.Frame2d`
    """
    def test_constructor_default_parent(self):
        """
        Test the constructor with default parent.

        :return: None
        """
        position = np.random.random(2)
        position_copy = position.copy()
        rot = Rotation2d(random.random())

        frame = Frame2d(position, rot)

        assert np.allclose(frame.position, position, rtol=RTOL)
        assert frame.rotation == rot
        assert frame._parent == origin2d

        # Check if np arrays were copied
        position = position + np.array([1, 1], dtype=np.float64)
        assert np.allclose(frame.position, position_copy, rtol=RTOL)
        assert not np.allclose(frame.position, position, rtol=RTOL)

    def test_constructor_random_parent(self, random_frame2d):
        """
        Test the parent assignment in the constructor. (complimentary to
        :func:`test_constructor_default_parent`)

        :return: None
        """
        position = np.random.random(2)
        rot = Rotation2d(random.random())

        frame = Frame2d(position, rot, parent_frame=random_frame2d)

        assert frame._parent == random_frame2d

    def test_constructor_shape_check(self):
        """
        Test the position array shape check in the constructor.

        :return: None
        """
        position = np.array([1, 2, 3], dtype=np.float64)
        rot = Rotation2d(random.random())

        with pytest.raises(ValueError):
            frame = Frame2d(position, rot)      # noqa: F841

    def test_find_transform_path(self):
        """
        Test the .find_transform_path method with static values.

        :return: None
        """
        position = np.array([0, 0], dtype=np.float64)
        rot = Rotation2d(0)

        frame1 = Frame2d(position, rot)
        frame2 = Frame2d(position, rot, parent_frame=frame1)
        frame3 = Frame2d(position, rot, parent_frame=frame2)
        frame4 = Frame2d(position, rot)
        frame5 = Frame2d(position, rot, parent_frame=frame4)
        frame6 = Frame2d(position, rot, parent_frame=frame3)
        frame7 = Frame2d(position, rot, parent_frame=frame2)

        path0 = frame3.find_transform_path(frame1)
        path1 = frame6.find_transform_path(frame5)
        path2 = frame7.find_transform_path(frame6)
        path3 = frame5.find_transform_path(frame1)
        path4 = frame2.find_transform_path(frame6)
        path5 = frame7.find_transform_path(origin2d)

        # LEGACY
        # expected0 = [(frame3, "to"), (frame2, "to")]
        # expected1 = [(frame6, "to"), (frame3, "to"), (frame2, "to"),
        #              (frame1, "to"), (frame4, "from"), (frame5, "from")]
        # expected2 = [(frame7, "to"), (frame2, "to"), (frame1, "to"),
        #              (frame1, "from"), (frame2, "from"), (frame3, "from"),
        #              (frame6, "from")]
        # expected3 = [(frame5, "to"), (frame4, "to"), (frame1, "from")]
        # expected4 = [(frame3, "from"), (frame6, "from")]
        # expected5 = [(frame7, "to"), (frame2, "to"), (frame1, "to")]

        expected0 = [(frame3, "to"), (frame2, "to")]
        expected1 = [(frame6, "to"), (frame3, "to"), (frame2, "to"),
                     (frame1, "to"), (frame4, "from"), (frame5, "from")]
        expected2 = [(frame7, "to"), (frame3, "from"), (frame6, "from")]
        expected3 = [(frame5, "to"), (frame4, "to"), (frame1, "from")]
        expected4 = [(frame3, "from"), (frame6, "from")]
        expected5 = [(frame7, "to"), (frame2, "to"), (frame1, "to")]

        assert path0 == expected0
        assert path1 == expected1
        assert path2 == expected2
        assert path3 == expected3
        assert path4 == expected4
        assert path5 == expected5

    def test_parent(self, random_frame2d):
        """
        Test the .parent method.

        :return: None
        """
        position = np.random.random(2)
        rot = Rotation2d(random.random())

        frame = Frame2d(position, rot, parent_frame=random_frame2d)

        assert frame.parent() == random_frame2d

    def test_rotate_via_path_static(self):
        """
        Test the .rotate_via_path method with static values.

        :return: None
        """
        # Testcase 1
        # Rotating a vector by 90 degrees
        vector = np.array([1, 0])
        rotation = Rotation2d(math.pi / 2)
        frame = Frame2d(np.random.random(2), rotation)
        path = origin2d.find_transform_path(frame)
        expected = np.array([0, -1])
        result = Frame2d.rotate_via_path(vector, path)

        assert np.allclose(result, expected, rtol=RTOL)

        # Testcase 2
        # Rotating a vector by 90 degrees twice
        vector = np.array([0, 1])
        rotation1 = Rotation2d(math.pi / 2)
        rotation2 = Rotation2d(- math.pi / 2)
        frame1 = Frame2d(np.random.random(2), rotation1)
        frame2 = Frame2d(np.random.random(2), rotation2)
        path = frame1.find_transform_path(frame2)
        expected = np.array([0, -1])
        result = Frame2d.rotate_via_path(vector, path)

        assert np.allclose(result, expected, rtol=RTOL)

        # Testcase 3
        # Rotating a vector by 45 degrees
        vector = np.array([1, 0])
        rotation = Rotation2d(math.pi / 4)
        frame = Frame2d(np.random.random(2), rotation)
        path = frame.find_transform_path(origin2d)
        expected = np.array([1 / math.sqrt(2), 1 / math.sqrt(2)])
        result = Frame2d.rotate_via_path(vector, path)

        assert np.allclose(result, expected, rtol=RTOL)

    def test_rotate_via_path_random(self):
        """
        Test the .rotate_via_path method with a chain of random Frames.

        :return: None
        """
        vector = np.random.random(2)
        rotated = vector
        last_frame = origin2d

        for i in range(random.randint(1, 100)):
            frame = generate_frame2d(last_frame)
            last_frame = frame
            rotated = frame.rotation.apply_inverse(rotated)

        path = origin2d.find_transform_path(last_frame)
        result = Frame2d.rotate_via_path(vector, path)

        assert np.allclose(result, rotated, rtol=RTOL)

    def test_rotate_via_path_system(self, frame2d_system):
        """
        Test the .rotate_via_path method with a Frame2d system.

        :return: None
        """
        # Frame assignments
        frame1 = frame2d_system[0]
        frame2 = frame2d_system[1]
        frame3 = frame2d_system[2]
        frame4 = frame2d_system[3]
        frame5 = frame2d_system[4]
        frame6 = frame2d_system[5]
        frame7 = frame2d_system[6]

        # Testcase 0 frame7 -> frame3
        vector0 = np.random.random(2)
        path0 = [(frame7, "to"), (frame2, "to"), (frame1, "to"),
                 (frame1, "from"), (frame2, "from"), (frame3, "from")]
        intermediate0 = frame7.rotation.apply(vector0)
        expected0 = frame3.rotation.apply_inverse(intermediate0)

        # Testcase 1 frame6 -> frame1
        vector1 = np.random.random(2)
        path1 = [(frame6, "to"), (frame3, "to"), (frame2, "to")]
        intermediate1 = frame6.rotation.apply(vector1)
        intermediate1 = frame3.rotation.apply(intermediate1)
        expected1 = frame2.rotation.apply(intermediate1)

        # Testcase 2 frame5 -> frame2
        vector2 = np.random.random(2)
        path2 = [(frame5, "to"), (frame4, "to"), (frame1, "from"),
                 (frame2, "from")]
        intermediate2 = frame5.rotation.apply(vector2)
        intermediate2 = frame4.rotation.apply(intermediate2)
        intermediate2 = frame1.rotation.apply_inverse(intermediate2)
        expected2 = frame2.rotation.apply_inverse(intermediate2)

        assert np.allclose(Frame2d.rotate_via_path(vector0, path0),
                           expected0, rtol=RTOL)
        assert np.allclose(Frame2d.rotate_via_path(vector1, path1),
                           expected1, rtol=RTOL)
        assert np.allclose(Frame2d.rotate_via_path(vector2, path2),
                           expected2, rtol=RTOL)

    def test_transform_from_parent_static(self):
        """
        Test the .transform_from_parent method with static values

        :return: None
        """
        position = np.array([5, 1], dtype=np.float64)
        angle = math.pi / 4
        rotation = Rotation2d(angle)
        frame = Frame2d(position, rotation)

        vector = np.array([1, 2], dtype=np.float64)
        expected_vector = np.array([-2.12132034, 3.53553391],
                                   dtype=np.float64)

        assert np.allclose(frame.transform_from_parent(vector),
                           expected_vector, rtol=RTOL)

        # Check that vector remains unchanged
        assert np.allclose(vector, np.array([1, 2], dtype=np.float64),
                           rtol=RTOL)

    def test_transform_from_parent_random(self):
        """
        Test the .transform_from_parent method with random values.

        :return: None
        """
        position = np.random.random(2)
        angle = random.random() * (2 * math.pi)
        rotation = Rotation2d(angle)
        frame = Frame2d(position, rotation)

        vector = np.random.random(2)
        vector_copy = vector.copy()

        translated_vector = vector - position
        expected_vector = rotation.apply_inverse(translated_vector)

        assert np.allclose(frame.transform_from_parent(vector),
                           expected_vector, rtol=RTOL)

        # Check that vector remains unchanged
        assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_to_parent_static(self):
        """
        Test the .transform_to_parent method with static values.

        :return: None
        """
        position = np.array([3, 1], dtype=np.float64)
        angle = - math.pi / 4
        rotation = Rotation2d(angle)
        frame = Frame2d(position, rotation)

        vector = np.array([1, 2], dtype=np.float64)
        expected_vector = np.array([5.12132034, 1.70710678], dtype=np.float64)

        assert np.allclose(frame.transform_to_parent(vector),
                           expected_vector, rtol=RTOL)

        # Check that vector remains unchanged
        assert np.allclose(vector, np.array([1, 2], dtype=np.float64),
                           rtol=RTOL)

    def test_transform_to_parent_random(self):
        """
        Test the .transform_to_parent method with random values.

        :return: None
        """
        position = np.random.random(2)
        angle = random.random() * (2 * math.pi)
        rotation = Rotation2d(angle)
        frame = Frame2d(position, rotation)

        vector = np.random.random(2)
        vector_copy = vector.copy()

        rotated_vector = rotation.apply(vector)
        expected_vector = rotated_vector + position

        assert np.allclose(frame.transform_to_parent(vector),
                           expected_vector, rtol=RTOL)

        # Check that vector remains unchanged
        assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_parent_reversible(self):
        """
        Test wether the .transform_from_parent and .transform_to_parent
        methods are reversible.

        :return: None
        """
        for _ in range(10):
            position = np.random.random(2)
            angle = random.random() * (2 * math.pi)
            rotation = Rotation2d(angle)
            frame = Frame2d(position, rotation)

            vector = np.random.random(2)

            intermediate_vector = frame.transform_from_parent(vector)

            assert np.allclose(frame.transform_to_parent(intermediate_vector),
                               vector, rtol=RTOL)

    def test_transform_from(self, frame2d_system):
        """
        Test the .transform_from method with random vectors and random paths.

        :return: None
        """
        vectors = [np.random.random(2) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = frame2d_system[random.randint(0, 6)]
            destination = frame2d_system[random.randint(0, 6)]

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame2d.transform_via_path(vector, path)

            assert np.allclose(destination.transform_from(source, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_to(self, frame2d_system):
        """
        Test the .transform_to method with random vectors and random paths.

        :return: None
        """
        vectors = [np.random.random(2) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = frame2d_system[random.randint(0, 6)]
            destination = frame2d_system[random.randint(0, 6)]

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame2d.transform_via_path(vector, path)

            assert np.allclose(source.transform_to(destination, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_reversible(self, frame2d_system):
        """
        Test wether the .transform_to and transform_from methods are
        reversible.

        :return: None
        """
        vectors = [np.random.random(2) for _ in range(10)]

        for vector in vectors:
            source = frame2d_system[random.randint(0, 6)]
            destination = frame2d_system[random.randint(0, 6)]

            interim = source.transform_to(destination, vector)
            result = source.transform_from(destination, interim)

            assert np.allclose(result, vector, rtol=RTOL)

    def test_transform_via_path(self, frame2d_system):
        """
        Test the .transform_via_path static method with a static path but with
        random orientations and vectors.

        :return: None
        """
        # Frame assignments
        frame1 = frame2d_system[0]
        frame2 = frame2d_system[1]
        frame3 = frame2d_system[2]
        frame4 = frame2d_system[3]
        frame5 = frame2d_system[4]
        frame6 = frame2d_system[5]
        frame7 = frame2d_system[6]

        # Testcase 0 frame7 -> frame3
        vector0 = np.random.random(2)
        path0 = [(frame7, "to"), (frame2, "to"), (frame1, "to"),
                 (frame1, "from"), (frame2, "from"), (frame3, "from")]
        intermediate0 = frame7.transform_to_parent(vector0)
        expected0 = frame3.transform_from_parent(intermediate0)

        # Testcase 1 frame6 -> frame1
        vector1 = np.random.random(2)
        path1 = [(frame6, "to"), (frame3, "to"), (frame2, "to")]
        intermediate1 = frame6.transform_to_parent(vector1)
        intermediate1 = frame3.transform_to_parent(intermediate1)
        expected1 = frame2.transform_to_parent(intermediate1)

        # Testcase 2 frame5 -> frame2
        vector2 = np.random.random(2)
        path2 = [(frame5, "to"), (frame4, "to"), (frame1, "from"),
                 (frame2, "from")]
        intermediate2 = frame5.transform_to_parent(vector2)
        intermediate2 = frame4.transform_to_parent(intermediate2)
        intermediate2 = frame1.transform_from_parent(intermediate2)
        expected2 = frame2.transform_from_parent(intermediate2)

        assert np.allclose(Frame2d.transform_via_path(vector0, path0),
                           expected0, rtol=RTOL)
        assert np.allclose(Frame2d.transform_via_path(vector1, path1),
                           expected1, rtol=RTOL)
        assert np.allclose(Frame2d.transform_via_path(vector2, path2),
                           expected2, rtol=RTOL)


class TestRootFrame3d:
    """
    Tests for the :class:`RootFrame3d` class.
    """
    def test_constructor(self):
        """
        Test the constructor of :class:`RootFrame3d`.

        :return: None
        """
        frame = RootFrame3d()

        assert np.allclose(frame.position,
                           np.array([0, 0, 0], dtype=np.float64), rtol=RTOL)
        assert np.allclose(frame.rotation.as_matrix(), np.identity(3),
                           rtol=RTOL)

    def test_find_transform_path(self, frame3d_system):
        """
        Test the find_transform_path method of RootFrame3d with static
        system-structure but random positions and rotations.

        :return: None
        """
        frame1 = frame3d_system[0]
        frame2 = frame3d_system[1]
        frame3 = frame3d_system[2]
        frame4 = frame3d_system[3]
        frame5 = frame3d_system[4]
        frame6 = frame3d_system[5]
        frame7 = frame3d_system[6]

        expected1 = [(frame1, "from")]
        expected2 = [(frame1, "from"), (frame2, "from")]
        expected3 = [(frame1, "from"), (frame2, "from"), (frame3, "from")]
        expected4 = [(frame4, "from")]
        expected5 = [(frame4, "from"), (frame5, "from")]
        expected6 = [(frame1, "from"), (frame2, "from"), (frame3, "from"),
                     (frame6, "from")]
        expected7 = [(frame1, "from"), (frame2, "from"), (frame7, "from")]

        assert expected1 == origin3d.find_transform_path(frame1)
        assert expected2 == origin3d.find_transform_path(frame2)
        assert expected3 == origin3d.find_transform_path(frame3)
        assert expected4 == origin3d.find_transform_path(frame4)
        assert expected5 == origin3d.find_transform_path(frame5)
        assert expected6 == origin3d.find_transform_path(frame6)
        assert expected7 == origin3d.find_transform_path(frame7)

    def test_transform_from(self, frame3d_system):
        """
        Test the .transform_from method with random vectors and random paths.
        :return: None
        """
        vectors = [np.random.random(3) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = frame3d_system[random.randint(0, 6)]
            destination = origin3d

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame3d.transform_via_path(vector, path)

            assert np.allclose(destination.transform_from(source, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_to(self, frame3d_system):
        """
        Test the .transform_to method with random vectors and random paths.
        :return: None
        """
        vectors = [np.random.random(3) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = origin3d
            destination = frame3d_system[random.randint(0, 6)]

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame3d.transform_via_path(vector, path)

            assert np.allclose(source.transform_to(destination, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_reversible(self, frame3d_system):
        """
        Test wether the .transform_to and transform_from methods are
        reversible.
        :return: None
        """
        vectors = [np.random.random(3) for _ in range(10)]

        for vector in vectors:
            source = origin3d
            destination = frame3d_system[random.randint(0, 6)]

            interim = source.transform_to(destination, vector)
            result = source.transform_from(destination, interim)

            assert np.allclose(result, vector, rtol=RTOL)


class TestFrame3d:
    """
    Tests for the :class:`Frame3d` class.
    """
    def test_constructor_default_parent(self):
        """
        Test the constructor method with the default frame

        :return: None
        """
        position = np.random.random(3)
        position_copy = position.copy()
        rotation = Rotation3d.from_rotvec(np.random.random(3))
        frame = Frame3d(position, rotation)

        assert np.allclose(frame.position, position, rtol=RTOL)
        assert frame.rotation == rotation
        assert frame._parent == origin3d

        # Check that position is copied
        frame.position[0] = 1
        assert np.allclose(position, position_copy, rtol=RTOL)

    def test_constructor_random_parent(self, random_frame3d):
        """
        Test the constructor method with random parent frames.

        :return: None
        """
        # Repeat test multiple times.
        for _ in range(10):
            position = np.random.random(3)
            position_copy = position.copy()
            rotation = Rotation3d.from_rotvec(np.random.random(3))
            frame = Frame3d(position, rotation, parent_frame=random_frame3d)

            assert np.allclose(frame.position, position, rtol=RTOL)
            assert frame.rotation == rotation
            assert frame._parent == random_frame3d

            # check that position is copied
            frame.position[0] = 1
            assert np.allclose(position, position_copy, rtol=RTOL)

    def test_constructor_shape_check(self):
        """
        Test if the constructor checks for the shape of the position array.

        :return: None
        """
        position = np.random.random(2)
        rotation = Rotation3d.from_rotvec(np.random.random(3))

        with pytest.raises(ValueError):
            frame = Frame3d(position, rotation)             # noqa: F841

    def test_find_transform_path(self):
        """
        Test the .find_transform_path method with static values.
        (This test is the same the test for Frame2d.find_transform_path)

        :return: None
        """
        position = np.array([0, 0, 0], dtype=np.float64)
        rot = Rotation3d.from_rotvec(np.random.random(3))

        frame1 = Frame3d(position, rot)
        frame2 = Frame3d(position, rot, parent_frame=frame1)
        frame3 = Frame3d(position, rot, parent_frame=frame2)
        frame4 = Frame3d(position, rot)
        frame5 = Frame3d(position, rot, parent_frame=frame4)
        frame6 = Frame3d(position, rot, parent_frame=frame3)
        frame7 = Frame3d(position, rot, parent_frame=frame2)

        path0 = frame3.find_transform_path(frame1)
        path1 = frame6.find_transform_path(frame5)
        path2 = frame7.find_transform_path(frame6)
        path3 = frame5.find_transform_path(frame1)
        path4 = frame2.find_transform_path(frame6)
        path5 = frame7.find_transform_path(origin3d)

        # LEGACY
        # expected0 = [(frame3, "to"), (frame2, "to")]
        # expected1 = [(frame6, "to"), (frame3, "to"), (frame2, "to"),
        #              (frame1, "to"), (frame4, "from"), (frame5, "from")]
        # expected2 = [(frame7, "to"), (frame2, "to"), (frame1, "to"),
        #              (frame1, "from"), (frame2, "from"), (frame3, "from"),
        #              (frame6, "from")]
        # expected3 = [(frame5, "to"), (frame4, "to"), (frame1, "from")]
        # expected4 = [(frame3, "from"), (frame6, "from")]
        # expected5 = [(frame7, "to"), (frame2, "to"), (frame1, "to")]

        expected0 = [(frame3, "to"), (frame2, "to")]
        expected1 = [(frame6, "to"), (frame3, "to"), (frame2, "to"),
                     (frame1, "to"), (frame4, "from"), (frame5, "from")]
        expected2 = [(frame7, "to"), (frame3, "from"), (frame6, "from")]
        expected3 = [(frame5, "to"), (frame4, "to"), (frame1, "from")]
        expected4 = [(frame3, "from"), (frame6, "from")]
        expected5 = [(frame7, "to"), (frame2, "to"), (frame1, "to")]

        assert path0 == expected0
        assert path1 == expected1
        assert path2 == expected2
        assert path3 == expected3
        assert path4 == expected4
        assert path5 == expected5

    def test_parent(self, random_frame3d):
        """
        Test the .parent method.

        :return: None
        """
        position = np.random.random(3)
        rotation = Rotation3d.from_rotvec(np.random.random(3))
        frame = Frame3d(position, rotation, parent_frame=random_frame3d)

        assert frame.parent() == random_frame3d

    def test_rotate_via_path_static(self):
        """
        Test the .rotate_via_path method with static values.

        :return: None
        """
        # Testcase 1
        # Rotating a vector by 90 degrees
        vector = np.array([1, 0, 0])
        rotation = Rotation3d.from_rotvec(np.array([0, 0, math.pi / 2]))
        frame = Frame3d(np.random.random(3), rotation)
        path = origin3d.find_transform_path(frame)
        expected = np.array([0, -1, 0])
        result = Frame3d.rotate_via_path(vector, path)

        assert np.allclose(result, expected, rtol=RTOL)

        # Testcase 2
        # Rotating a vector by 90 degrees twice
        vector = np.array([0, 1, 0])
        rotation1 = Rotation3d.from_rotvec(np.array([0, 0, math.pi / 2]))
        rotation2 = Rotation3d.from_rotvec(np.array([0, 0, - math.pi / 2]))
        frame1 = Frame3d(np.random.random(3), rotation1)
        frame2 = Frame3d(np.random.random(3), rotation2)
        path = frame1.find_transform_path(frame2)
        expected = np.array([0, -1, 0])
        result = Frame3d.rotate_via_path(vector, path)

        assert np.allclose(result, expected, rtol=RTOL)

        # Testcase 3
        # Rotating a vector by 45 degrees
        vector = np.array([1, 0, 0])
        rotation = Rotation3d.from_rotvec(np.array([0, 0, math.pi / 4]))
        frame = Frame3d(np.random.random(3), rotation)
        path = frame.find_transform_path(origin3d)
        expected = np.array([1 / math.sqrt(2), 1 / math.sqrt(2), 0])
        result = Frame3d.rotate_via_path(vector, path)

        assert np.allclose(result, expected, rtol=RTOL)

    def test_rotate_via_path_random(self):
        """
        Test the .rotate_via_path method with a chain of random Frames.

        :return: None
        """
        vector = np.random.random(3)
        rotated = vector
        last_frame = origin3d

        for i in range(random.randint(1, 100)):
            frame = generate_frame3d(last_frame)
            last_frame = frame
            rotated = frame.rotation.inv().apply(rotated)

        path = origin3d.find_transform_path(last_frame)
        result = Frame3d.rotate_via_path(vector, path)

        assert np.allclose(result, rotated, rtol=RTOL)

    def test_rotate_via_path_system(self, frame3d_system):
        """
        Test the .transform_via_path static method with a static path but with
        random orientations and vectors.
        (This test is the same as the test for Frame2d.transform_via_path)

        :return: None
        """
        # Frame assignments
        frame1 = frame3d_system[0]
        frame2 = frame3d_system[1]
        frame3 = frame3d_system[2]
        frame4 = frame3d_system[3]
        frame5 = frame3d_system[4]
        frame6 = frame3d_system[5]
        frame7 = frame3d_system[6]

        # Testcase 0 frame7 -> frame3
        vector0 = np.random.random(3)
        path0 = [(frame7, "to"), (frame2, "to"), (frame1, "to"),
                 (frame1, "from"), (frame2, "from"), (frame3, "from")]
        intermediate0 = frame7.rotation.apply(vector0)
        expected0 = frame3.rotation.inv().apply(intermediate0)

        # Testcase 1 frame6 -> frame1
        vector1 = np.random.random(3)
        path1 = [(frame6, "to"), (frame3, "to"), (frame2, "to")]
        intermediate1 = frame6.rotation.apply(vector1)
        intermediate1 = frame3.rotation.apply(intermediate1)
        expected1 = frame2.rotation.apply(intermediate1)

        # Testcase 2 frame5 -> frame2
        vector2 = np.random.random(3)
        path2 = [(frame5, "to"), (frame4, "to"), (frame1, "from"),
                 (frame2, "from")]
        intermediate2 = frame5.rotation.apply(vector2)
        intermediate2 = frame4.rotation.apply(intermediate2)
        intermediate2 = frame1.rotation.inv().apply(intermediate2)
        expected2 = frame2.rotation.inv().apply(intermediate2)

        assert np.allclose(Frame3d.rotate_via_path(vector0, path0),
                           expected0, rtol=RTOL)
        assert np.allclose(Frame3d.rotate_via_path(vector1, path1),
                           expected1, rtol=RTOL)
        assert np.allclose(Frame3d.rotate_via_path(vector2, path2),
                           expected2, rtol=RTOL)

    def test_transform_from_parent_static(self):
        """
        Test the .transform_from_parent method.

        :return: None
        """
        position = np.array([0, 2, 0], dtype=np.float64)
        rotation = Rotation3d.from_rotvec(np.array([- math.pi / 2, 0, 0]))
        frame = Frame3d(position, rotation)

        vectors = list()
        vectors_copy = list()
        expected = list()

        vectors.append(np.array([1, 0, 0], dtype=np.float64))          # e1
        vectors_copy.append(np.array([1, 0, 0], dtype=np.float64))
        expected.append(np.array([1, 0, -2], dtype=np.float64))

        vectors.append(np.array([0, 1, 0], dtype=np.float64))          # e2
        vectors_copy.append(np.array([0, 1, 0], dtype=np.float64))
        expected.append(np.array([0, 0, -1], dtype=np.float64))

        vectors.append(np.array([0, 0, 1], dtype=np.float64))          # e3
        vectors_copy.append(np.array([0, 0, 1], dtype=np.float64))
        expected.append(np.array([0, -1, -2], dtype=np.float64))

        for i in range(len(vectors)):
            assert np.allclose(frame.transform_from_parent(vectors[i]),
                               expected[i], rtol=RTOL)

            # Check that vector remains unchanged.
            assert np.allclose(vectors[i], vectors_copy[i], rtol=RTOL)

    def test_transform_from_parent_random(self):
        """
        Test the .transform_from_parent method with dynamic values.

        :return: None
        """
        position = np.random.random(3)
        rotation = Rotation3d.from_rotvec(np.random.random(3))
        inverse_rotation = rotation.inv()
        frame = Frame3d(position, rotation)

        for _ in range(10):
            vector = np.random.random(3)
            vector_copy = vector.copy()

            expected = inverse_rotation.apply(vector - position)

            assert np.allclose(frame.transform_from_parent(vector), expected,
                               rtol=RTOL)

            # Check that vector remains unchanged.
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_to_parent_static(self):
        """
        Test the .transform_to_parent with static values

        :return: None
        """
        position = np.array([0, 2, 0], dtype=np.float64)
        rotation = Rotation3d.from_rotvec(np.array([- math.pi / 2, 0, 0]))
        frame = Frame3d(position, rotation)

        vectors = list()
        vectors_copy = list()
        expected = list()

        vectors.append(np.array([1, 0, -2], dtype=np.float64))
        vectors_copy.append(np.array([1, 0, -2], dtype=np.float64))
        expected.append(np.array([1, 0, 0], dtype=np.float64))      # e1

        vectors.append(np.array([0, 0, -1], dtype=np.float64))
        vectors_copy.append(np.array([0, 0, -1], dtype=np.float64))
        expected.append(np.array([0, 1, 0], dtype=np.float64))      # e2

        vectors.append(np.array([0, -1, -2], dtype=np.float64))
        vectors_copy.append(np.array([0, -1, -2], dtype=np.float64))
        expected.append(np.array([0, 0, 1], dtype=np.float64))      # e3

        for i in range(len(vectors)):
            assert np.allclose(frame.transform_to_parent(vectors[i]),
                               expected[i], rtol=RTOL)

            # Check that vector remains unchanged.
            assert np.allclose(vectors[i], vectors_copy[i], rtol=RTOL)

    def test_transform_to_parent_random(self):
        """
        Test the .transform_to_parent method with random values.

        :return: None
        """
        position = np.random.random(3)
        rotation = Rotation3d.from_rotvec(np.random.random(3))
        frame = Frame3d(position, rotation)

        for _ in range(10):
            vector = np.random.random(3)
            vector_copy = vector.copy()

            expected = rotation.apply(vector) + position

            assert np.allclose(frame.transform_to_parent(vector),
                               expected, rtol=RTOL)

            # Check that vector remains unchanged.
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_parent_reversible(self):
        """
        Check whether the methods .transform_from_parent and
        .transform_to_parent are reversible.

        :return: None
        """
        position = np.random.random(3)
        rotation = Rotation3d.from_rotvec(np.random.random(3))
        frame = Frame3d(position, rotation)

        for _ in range(10):
            vector = np.random.random(3)

            interim_from = frame.transform_from_parent(vector)
            interim_to = frame.transform_to_parent(vector)

            assert np.allclose(frame.transform_to_parent(interim_from), vector,
                               rtol=RTOL)
            assert np.allclose(frame.transform_from_parent(interim_to), vector,
                               rtol=RTOL)

    def test_transform_from(self, frame3d_system):
        """
        Test the .transform_from method with random vectors and random paths.

        :return: None
        """
        vectors = [np.random.random(3) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = frame3d_system[random.randint(0, 6)]
            destination = frame3d_system[random.randint(0, 6)]

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame3d.transform_via_path(vector, path)

            assert np.allclose(destination.transform_from(source, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_to(self, frame3d_system):
        """
        Test the .transform_to method with random vectors and random paths.

        :return: None
        """
        vectors = [np.random.random(3) for _ in range(10)]

        for vector in vectors:
            vector_copy = vector.copy()
            source = frame3d_system[random.randint(0, 6)]
            destination = frame3d_system[random.randint(0, 6)]

            # calculate expected
            path = source.find_transform_path(destination)
            expected = Frame3d.transform_via_path(vector, path)

            assert np.allclose(source.transform_to(destination, vector),
                               expected, rtol=RTOL)

            # Check that vector didn't change
            assert np.allclose(vector, vector_copy, rtol=RTOL)

    def test_transform_reversible(self, frame3d_system):
        """
        Test wether the .transform_to and transform_from methods are
        reversible.

        :return: None
        """
        vectors = [np.random.random(3) for _ in range(10)]

        for vector in vectors:
            source = frame3d_system[random.randint(0, 6)]
            destination = frame3d_system[random.randint(0, 6)]

            interim = source.transform_to(destination, vector)
            result = source.transform_from(destination, interim)

            assert np.allclose(result, vector, rtol=RTOL)

    def test_transform_via_path(self, frame3d_system):
        """
        Test the .transform_via_path static method with a static path but with
        random orientations and vectors.
        (This test is the same as the test for Frame2d.transform_via_path)

        :return: None
        """
        # Frame assignments
        frame1 = frame3d_system[0]
        frame2 = frame3d_system[1]
        frame3 = frame3d_system[2]
        frame4 = frame3d_system[3]
        frame5 = frame3d_system[4]
        frame6 = frame3d_system[5]
        frame7 = frame3d_system[6]

        # Testcase 0 frame7 -> frame3
        vector0 = np.random.random(3)
        path0 = [(frame7, "to"), (frame2, "to"), (frame1, "to"),
                 (frame1, "from"), (frame2, "from"), (frame3, "from")]
        intermediate0 = frame7.transform_to_parent(vector0)
        expected0 = frame3.transform_from_parent(intermediate0)

        # Testcase 1 frame6 -> frame1
        vector1 = np.random.random(3)
        path1 = [(frame6, "to"), (frame3, "to"), (frame2, "to")]
        intermediate1 = frame6.transform_to_parent(vector1)
        intermediate1 = frame3.transform_to_parent(intermediate1)
        expected1 = frame2.transform_to_parent(intermediate1)

        # Testcase 2 frame5 -> frame2
        vector2 = np.random.random(3)
        path2 = [(frame5, "to"), (frame4, "to"), (frame1, "from"),
                 (frame2, "from")]
        intermediate2 = frame5.transform_to_parent(vector2)
        intermediate2 = frame4.transform_to_parent(intermediate2)
        intermediate2 = frame1.transform_from_parent(intermediate2)
        expected2 = frame2.transform_from_parent(intermediate2)

        assert np.allclose(Frame3d.transform_via_path(vector0, path0),
                           expected0, rtol=RTOL)
        assert np.allclose(Frame3d.transform_via_path(vector1, path1),
                           expected1, rtol=RTOL)
        assert np.allclose(Frame3d.transform_via_path(vector2, path2),
                           expected2, rtol=RTOL)
