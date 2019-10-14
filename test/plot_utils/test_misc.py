import unittest
import copy
import random

from plotink import plot_utils

from plotink.plot_utils_import import from_dependency_import

cspsubdiv = from_dependency_import('ink_extensions.cspsubdiv')

# python -m unittest discover in top-level package dir

class PlotUtilsTestCase(unittest.TestCase):

    def test_subdivideCubicPath_no_divisions(self):
        """ when applied to a straight line, there will be no subdivisions as the "curve"
        can be represented easily as only one/two segments """
        orig_beziers = [[(0,0), (0.5, 0.5), (1, 1)],
                        [(1.25, 1.25), (1.75, 1.75), (2, 2)]]
        processed_beziers = copy.deepcopy(orig_beziers)
        
        plot_utils.subdivideCubicPath(processed_beziers, 0)

        self.assertEqual(orig_beziers, processed_beziers)

    def test_subdivideCubicPath_divisions(self):
        orig_beziers = [[(1, 1), (2, 2), (0, 0)],
                        [(2, 2), (1, 1), (0, 0)]]
        processed_beziers = copy.deepcopy(orig_beziers)

        plot_utils.subdivideCubicPath(processed_beziers, .2)

        self.assertGreater(len(processed_beziers), len(orig_beziers))
        # but some things should not be modified
        self.assertEqual(orig_beziers[1][1:], processed_beziers[len(processed_beziers) - 1][1:])

    def test_max_dist_from_n_points_1(self):
        """ behavior for one point """
        input = [(0,0), (5,5), (10,0)]

        self.assertEqual(5, plot_utils.max_dist_from_n_points(input))

    def test_max_dist_from_n_points_2(self):
        """ check that the results are the same as the original maxdist """
        inputs = [self.get_random_points(4, i + .01) for i in range(5)]  # check a few possibilities

        for input in inputs:
            self.assertEqual(cspsubdiv.maxdist(input), plot_utils.max_dist_from_n_points(input))

    def test_max_dist_from_n_points_3(self):
        """ behavior for three points """
        input = [(0,0), (0, 3), (-4, 0), (4, -7), (10,0)]

        self.assertEqual(7, plot_utils.max_dist_from_n_points(input))

    @staticmethod
    def get_random_points(num, seed=0):
        """ generate random (but deterministic) points where coords are between 0 and 1 """
        random.seed(seed)

        return [(random.random(), random.random()) for _ in range(num)]
