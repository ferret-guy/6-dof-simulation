import numpy as np

""""All coordinates and points are in ECEF unless otherwise noted"""


class KinematicObject(object):
	def __init__(self, pos, vel, mass, rot, rot_rate, mom):
		"""An object that has basic position and rotation components (with rates)

		:param pos:
			An array of position axes and initial positions (in meters)
		:type pos:
			numpy.ndarray or list
		:param vel:
			An array of velocity axes and initial values (in meters/sec)
		:type vel:
			numpy.ndarray or list
		:param mass:
			The mass of the object (in kg)
		:type mass:
			float
		:param rot:
			An array of rotation axes and initial values (in rad)
		:type rot:
			numpy.ndarray or list
		:param rot_rate:
			An array of rotation rates and initial values (in rad/s)
		:type rot_rate:
			numpy.ndarray or list
		:param mom:
			An array of rotation moments (in kg m^2)
		:type mom:
			numpy.ndarray or list
		"""

		self.pos = np.array(pos)
		self.vel = np.array(vel)
		self.mass = mass

		self.rot = np.array(rot)
		self.rot_rate = np.array(rot_rate)
		self.mom = np.array(mom)

		if self.pos.shape != self.vel.shape:
			raise ValueError("Position and Velocity must have the same dimensions! ({} vs {})".format(self.pos.shape,
																									self.vel.shape))
		if self.rot.shape != self.rot_rate.shape:
			raise ValueError("Rotation and Rotation rate must have the same dimensions! ({} vs {})".format(self.rot.shape,
																										self.rot_rate.shape))
		if self.rot.shape != self.mom.shape:
			raise ValueError("Rotation and Moments must have the same dimensions! ({} vs {})".format(self.rot.shape,
																									self.mom.shape))

	def step(self, forces, moments, deltat):
		"""Takes the inputted force and moment arrays and updates the current objects positions

		:param forces:
			An array of forces on the object (in Newtons)
		:type forces:
			numpy.ndarray or list
		:param moments:
			An array of moments on the object (in N m)
		:type moments:
			numpy.ndarray or list
		:param deltat:
			The timestamp to compute
		:type deltat:
			float
		:return:
			The updated pos, vel, rot, rot_rate
		:rtype:
			Tuple(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
		"""

		forces = np.array(forces)
		moments = np.array(moments)

		if forces.shape != self.pos.shape:
			raise ValueError("Forces must have the same shape as pos ({})".format(self.pos.shape))
		if moments.shape != self.rot.shape:
			raise ValueError("Moments must have the same shape as rot ({})".format(self.rot.shape))
		if deltat <= 0:
			raise ValueError("DeltaT must be positive!")

		self.vel = self.vel * deltat + np.divide(forces, self.mass) * deltat
		self.pos += np.dot(self.vel, deltat)

		self.rot_rate = self.rot_rate * deltat + np.divide(moments, self.mom) * deltat
		self.rot += np.dot(self.rot_rate, deltat)

		return self.pos, self.vel, self.rot, self.rot_rate

	def dist(self, point):
		"""Returns the distance between this object and another point or object

		:param point:
			The point to measure the distance from
		:type point:
			numpy.ndarray or list
		:return:
			The distance between the current object and the point
		:rtype:
			float
		"""
		if isinstance(point, KinematicObject):
			point = point.pos
		point = np.array(point)
		if point.shape != self.pos.shape:
			raise ValueError("Point must have the same shape as pos ({})".format(self.pos.shape))
		return np.linalg.norm(self.pos - point)


class Vehicle(KinematicObject):
	def __int__(self, pos, vel, mass, rot, rot_rate, mom, thrust):
		"""A flying Vehicle that has basic position and rotation components (with rates) and axial thrust with moments

				:param pos:
					An array of position axes and initial positions (in meters)
				:type pos:
					numpy.ndarray or list
				:param vel:
					An array of velocity axes and initial values (in meters/sec)
				:type vel:
					numpy.ndarray or list
				:param mass:
					The mass of the object (in kg)
				:type mass:
					float
				:param rot:
					An array of rotation axes and initial values (in rad)
				:type rot:
					numpy.ndarray or list
				:param rot_rate:
					An array of rotation rates and initial values (in rad/s)
				:type rot_rate:
					numpy.ndarray or list
				:param mom:
					An array of rotation moments (in kg m^2)
				:type mom:
					numpy.ndarray or list
				:param thrust:
					The thrust of the onboard engine (in N)
				:type thrust:
					float
				"""
		super(Vehicle, self).__init__(pos, vel, mass, rot, rot_rate, mom)

		self.forces = np.zeros(self.pos.shape)
		self.thrust = thrust

	def thrust_force(self, thrust=None):
		if thrust is None:
			thrust = self.thrust
		"""Adds a force of thrust to the current vehicle"""
		self.forces += np.zeros(self.pos.shape)
