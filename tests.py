from nose.tools import raises
import numpy as np

from Elements import KinematicObject


def test_KinematicObject_init():
	obj1 = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [1.0, 1.0])
	obj2 = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0], [0.0], [1.0])
	obj3 = KinematicObject(np.array([0.0, 0.0]), [0.0, 0.0], 1, [0.0], np.array([0.0]), [1.0])
	assert True


@raises(ValueError)
def test_KinematicObject_Invalid_posvel_Sizes():
	obj1 = KinematicObject([0.0, 0.0], [0.0], 1, [0.0, 0.0], [0.0, 0.0], [1.0, 1.0])
	obj2 = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0], [0.0, 0.0], [1.0])
	obj3 = KinematicObject(np.array([0.0, 0.0]), [0.0, 0.0], 1, [0.0], np.array([0.0]), [1.0])


@raises(ValueError)
def test_KinematicObject_Invalid_rotvel_Sizes():
	obj2 = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0], [0.0, 0.0], [1.0])
	obj3 = KinematicObject(np.array([0.0, 0.0]), [0.0, 0.0], 1, [0.0], np.array([0.0]), [1.0])


@raises(ValueError)
def test_KinematicObject_Invalid_rotmom_Sizes():
	obj2 = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0], [0.0], [1.0, 0.0])


def test_KinematicObject_point_dist():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [1.0, 1.0])
	assert obj.dist([0.0, 1.0]) == 1.0


def test_KinematicObject_KinematicObject_dist():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [1.0, 1.0])
	obj2 = KinematicObject([0.0, 1.0], [10.0, 0.0], 1, [0.0], [0.0], [1.0])
	assert obj.dist(obj2) == 1.0


@raises(ValueError)
def test_KinematicObject_invalid_point_dist():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [1.0, 1.0])
	assert obj.dist([0.0, 1.0, 0.0]) == 1.0


def test_KinematicObject_pos_step():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [1.0, 1.0])
	print obj.step([0.0, 1.0], [0.0, 0.0], 1)
	for i, j in zip(obj.step([0.0, 0.0], [1.0, 0.0], 1), (np.array([0., 2.]), np.array([0., 1.]),
												np.array([1., 0.]), np.array([1., 0.]))):
		print "Comparing {} and {}".format(i, j)
		assert (i == j).all()

def test_KinematicObject_rot_step():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [0.5, 1.0])
	print obj.step([0.0, 1.0], [1.0, 1.0], 1)
	for i, j in zip(obj.step([0.0, 0.0], [0.0, 0.0], 1), (np.array([0., 2.]), np.array([0., 1.]),
												np.array([4., 2.]), np.array([2., 1.]))):
		print "Comparing {} and {}".format(i, j)
		assert (i == j).all()


@raises(ValueError)
def test_KinematicObject_pos_exept_delt():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [0.5, 1.0])
	print obj.step([0.0, 1.0], [1.0, 1.0], 1)
	for i, j in zip(obj.step([0.0, 0.0], [0.0, 0.0], 0), (np.array([0., 2.]), np.array([0., 1.]),
												np.array([4., 2.]), np.array([2., 1.]))):
		print "Comparing {} and {}".format(i, j)
		assert (i == j).all()


@raises(ValueError)
def test_KinematicObject_pos_exept_force():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [0.5, 1.0])
	print obj.step([0.0, 1.0], [1.0, 1.0], 1)
	for i, j in zip(obj.step([0.0], [0.0, 0.0], 1), (np.array([0., 2.]), np.array([0., 1.]),
												np.array([4., 2.]), np.array([2., 1.]))):
		print "Comparing {} and {}".format(i, j)
		assert (i == j).all()

@raises(ValueError)
def test_KinematicObject_pos_exept_mom():
	obj = KinematicObject([0.0, 0.0], [0.0, 0.0], 1, [0.0, 0.0], [0.0, 0.0], [0.5, 1.0])
	print obj.step([0.0, 1.0], [1.0, 1.0], 1)
	for i, j in zip(obj.step([0.0, 0.0], [0.0], 1), (np.array([0., 2.]), np.array([0., 1.]),
												np.array([4., 2.]), np.array([2., 1.]))):
		print "Comparing {} and {}".format(i, j)
		assert (i == j).all()


