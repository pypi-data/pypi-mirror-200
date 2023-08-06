#!/usr/bin/env python
"""
Defines the Model class

Copyright (C) CSIRO 2017
"""
import numpy as np
pi = np.pi


class Model(object):

    angularScales = {'radian': 1.0, 'degree': np.degrees(1.0)}

    def __init__(self, params):
        self.params = params
        self.angUnit = 'radian'
        self.angScale = Model.angularScales[self.angUnit]

        self.base = 0.0
        self.amplitude = 0.0
        self.centre = np.array([0.0, 0.0])
        self.axes = np.array([0.0, 0.0])
        self.angle = 0.0
        self.major_angle = 0.0
        self.semimajor = 0.0
        self.semiminor = 0.0

    def set_ang_unit(self, unit):
        if unit in Model.angularScales:
            self.angUnit = unit
            self.angScale = Model.angularScales[unit]

    def get_params(self):
        return self.params

    def get_centre(self):
        return self.centre * self.angScale

    def get_axes(self):
        return np.array([self.semimajor, self.semiminor]) * self.angScale

    def get_major_angle(self):
        return self.major_angle * self.angScale

    def get_position_angle(self):
        """  Return the angle of the ellipse in the astronomical
        convention measured from North in ccw direction.
        """
        return ((self.major_angle+pi/2.) % pi) * self.angScale

    def get_eccentricity(self):
        return self.eccentricity

    def get_amplitude(self):
        return self.amplitude

    def get_base(self):
        return self.base

    def get_residual_rms(self):
        return 0.0

    def is_good_fit(self):
        return True

    def evaluate(self, arg):
        return 0.0, 0.0

    def get_locus50(self, arg):
        return 0.0
