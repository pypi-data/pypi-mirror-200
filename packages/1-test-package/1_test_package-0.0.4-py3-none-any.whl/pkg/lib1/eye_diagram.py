import numpy as np
from ..lib2.math_x import *  # relative path
# .  means current folder, e.g. lib1
# .. means one folder above, e.g. pkg
# ..lib2.math_x -> pkg.lib2.math_x

class Eye_Diagram(object):
    def __init__(self, ui, spb, ipn, x_bin, y_bin):
        self.folder_path = ''

        self.UI = ui
        self.SPB = spb
        self.ipn = ipn  # interpolation, number of points inserted between every 2 adjacent samples.
        self.x_bin = x_bin
        self.y_bin = y_bin

        self.x_min = -self.UI/2  #
        self.x_max = self.UI/2
        self.y_min = None
        self.y_max = None

        self.number_of_symbols = 0  # total sampled symbols by clock ticks.

        self.eye_1D = np.empty([2, 1], dtype=object)  # let's store eye_1D in RAM at first, i.e. on the fly
        self.eye_2D = np.zeros([self.y_bin, self.x_bin])  # let's store eye_2D in RAM at first, i.e. on the fly.
        # both eyes are in 1 UI.

        self.eye_1D_2UI = None
        self.eye_2D_2UI = None


        self.create_eye_1D = False  # generate eye_1D or not.

    def add_test(self):
        return self.x_bin + self.y_bin


def lib1_double_add(a, b):
    c = add_x(a, b)
    return 2 * c

def new_add(a, b):
    return a + b + 100





