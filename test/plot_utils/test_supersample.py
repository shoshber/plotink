import unittest
import copy

from plotink import plot_utils

from . import get_random_points

# python -m unittest discover in top-level package dir

class SuperSampleTestCase(unittest.TestCase):
    def test_supersample_few_vertices(self):
        """ supersample returns the list of vertices unchanged if the list is too small (<= 2) """
        verticeses = [ get_random_points(i, i) for i in range(3) ] # inputs of size 1, 2, 3

        for orig_vertices in verticeses:
            processed_vertices = copy.deepcopy(orig_vertices)
            plot_utils.supersample(processed_vertices, 0)
            self.assertEqual(orig_vertices, processed_vertices)

    def test_supersample_no_deletions(self):
        orig_vertices = get_random_points(12, 1)
        tolerance = -1 # an impossibly low tolerance

        processed_vertices = copy.deepcopy(orig_vertices)
        plot_utils.supersample(processed_vertices, tolerance)
        self.assertEqual(orig_vertices, processed_vertices)

    def test_supersample_delete_one(self):
        tolerance = 1
        verticeses = [[(0, 0), (0, tolerance - .1), (2, 0)],
                      [(0, 0), (1, tolerance - .2), (2, 0), (3, tolerance + 20000), (4, 0)]]

        for orig_vertices in verticeses:
            processed_vertices = copy.deepcopy(orig_vertices)
            plot_utils.supersample(processed_vertices, tolerance)

            self.assertEqual(len(orig_vertices) - 1, len(processed_vertices), # removed one exactly
                             "Incorrect result: {}".format(processed_vertices))
            # other vertices stayed the same
            self.assertEqual(orig_vertices[0], processed_vertices[0])
            for i in range(2, len(orig_vertices)):
                self.assertEqual(orig_vertices[i], processed_vertices[i - 1])

    def test_supersample_delete_groups(self):
        tolerance = .05
        vertices = [(0, 10), (tolerance - .02, 9), (0, 8), # del 1
                         (1, 8), (2, 8 + tolerance / 2), (3, 8 + tolerance / 3), (4, 8), # del 3
                         (4, 7), (5, 7), (5, 6), # no deletions
                         (0, 0), (1, tolerance - .01), (2, 0)] # del 1 again

        expected_result = [(0, 10), (0, 8),
                           (4, 8),
                           (4, 7), (5, 7), (5, 6),
                           (0, 0), (2, 0)]

        plot_utils.supersample(vertices, tolerance)

        self.assertEqual(expected_result, vertices)


    def test_supersample_delete_all(self):
        verticeses = [get_random_points(i + 3, i + 1) for i in range(5)]
        tolerance = 100 # guaranteed to be higher than any of the distances

        for orig_vertices in verticeses:
            processed_vertices = copy.deepcopy(orig_vertices)
            plot_utils.supersample(processed_vertices, tolerance)

            self.assertEqual(2, len(processed_vertices), # deleted all but start and end
                             "Error for test case {}. Should be length 2, instead got {}"
                             .format(orig_vertices, processed_vertices))
            # start and end are the same
            self.assertEqual(orig_vertices[0], processed_vertices[0])
            self.assertEqual(orig_vertices[len(orig_vertices) - 1], processed_vertices[1])
