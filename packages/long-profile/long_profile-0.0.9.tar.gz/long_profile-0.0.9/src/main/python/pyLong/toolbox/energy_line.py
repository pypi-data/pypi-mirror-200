from math import radians, tan

from matplotlib.axes import Subplot
import numpy as np

from pyLong.annotations.line import Line
from pyLong.profiles.zprofile import zProfile


class EnergyLine(Line):
    def __init__(self):
        Line.__init__(self)
        self._name = "new energy line"

        self._results = {'zprofile': zProfile(),
                         'reverse': False,
                         'method': "",
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'angle': 0.,
                         'success': False}
        
    """
    Methods:
    - clear
    - copy_style
    - export_style
    - import_style
    - plot
    - reset
    - run
    - update
    """

    def clear(self):
        """
        clear energy line

        returns:
        - None - NoneType
        
        """
        Line.clear(self)

    def copy_style(self, energy_line):
        """
        copy the style of an energy line

        arguments:
        - energy_line: energy line whose style is to be copied - EnergyLine

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_energy_line.copy_style(energy_line)
        
        """
        if isinstance(energy_line, EnergyLine):
            Line.copy_style(self, energy_line)
            return True
        else:
            return False

    def duplicate(self):
        return None
    
    def export_style(self, filename):
        """
        export energy line style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> energy_line.export_style("style.json")
        
        """
        Line.export_style(self, filename)

    def import_style(self, filename):
        """
        import energy line style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> energy_line.import_style("style.json")

        """
        Line.import_style(self, filename)

    def plot(self, ax):
        """
        plot energy line on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> energy_line.plot(ax)
        >>> plt.show()
        """
        if self._results['success']:
            Line.plot(self, ax)
        
    def reset(self):
        """
        clear results

        returns:
        - None - NoneType

        examples:
        >>> energy_line.reset()
        
        """
        self._results = {'zprofile': zProfile(),
                         'reverse': False,
                         'method': "",
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'angle': 0.,
                         'success': False}
        
    def reverse(self, *args):
        pass
        
    def run(self, zprofile, reverse=False, **kwargs):
        """
        run calculation

        arguments:
        - zprofile: profile - zProfile
        - reverse: reverse the profile - bool
        - method: method "x_start + x_end" | "x_start + angle" | "x_end + angle" - str
        - x_start: start distance (m) - int | float
        - x_end: end distance (m) - int | float
        - angle: angle (deg) - int | float

        returns:
        - True if succes - bool
        - False else - bool

        examples:
        >>> energy_line.run(zprofile, method="start + end", x_start=0., x_end=1000.)
        >>> energy_line.run(zprofile, reverse=False, method="start + angle", x_start=0., angle=35.)
        >>> energy_line.run(zprofile, reverse=False, method="end + angle", x_end=1000., angle=35.)
        
        """
        if not (isinstance(zprofile, zProfile) and isinstance(reverse, bool)):
            self.reset()
            return False

        if "method" not in kwargs.keys():
            self.reset()
            return False
        else:
            method = kwargs["method"]

        if method not in ["x_start + x_end", "x_start + angle", "x_end + angle"]:
            self.reset()
            return False
        
        if method == "x_start + x_end":
            if not ("x_start" in kwargs.keys() and "x_end" in kwargs.keys()):
                self.reset()
                return False
            else:
                x_start = kwargs["x_start"]
                x_end = kwargs["x_end"]

            if not (isinstance(x_start, (int, float)) and isinstance(x_end, (int, float))):
                self.reset()
                return False
            elif x_start == x_end:
                self.reset()
                return False
            else:
                z_start = zprofile.interpolate(x_start)
                z_end = zprofile.interpolate(x_end)
            
            if not (isinstance(z_start, (int, float)) and isinstance(z_end, (int, float))):
                self.reset()
                return False
            else:
                self._results = {'zprofile': zprofile,
                                 'reverse': reverse,
                                 'method': method,
                                 'x_start': x_start,
                                 'z_start': z_start,
                                 'x_end': x_end,
                                 'z_end': z_end,
                                 'angle': float(np.degrees(np.arctan2(abs(z_end - z_start),
                                                                      abs(x_end - x_start)))),
                                 'success': True}
                return True
                
        elif method == "x_start + angle":
            if not ("x_start" in kwargs.keys() and "angle" in kwargs.keys()):
                self.reset()
                return False
            else:
                x_start = kwargs["x_start"]
                angle = kwargs["angle"]

            if not (isinstance(x_start, (int, float)) and isinstance(angle, (int, float))):
                self.reset()
                return False
            elif not -90 < angle < 90:
                self.reset()
                return False
            else:
                angle = abs(angle)
                z_start = zprofile.interpolate(x_start)

            if not isinstance(z_start, (int, float)):
                self.reset()
                return False

            if reverse:
                new_zprofile = zprofile.reverse(zprofile)
                x_mean = (min(zprofile.x) + max(zprofile.x)) / 2
                x_start = 2 * x_mean - x_start
            else:
                new_zprofile = zprofile.duplicate()

            x_end = new_zprofile.x[-1]
            z_end = - tan(radians(angle)) * (x_end - x_start) + z_start

            xz = [(x_start, z_start),
                  (x_end, z_end)]
            
            energy_profile = zProfile()
            energy_profile.xz = xz

            intersections = new_zprofile.intersect(energy_profile)

            if isinstance(intersections, list):
                if len(intersections) > 0:
                    if x_start in [x for x, z in intersections]:
                        i = [x for x, z in intersections].index(x_start)
                        intersections.pop(i)

                if len(intersections) > 0:
                    if abs(x_start - intersections[0][0]) < 1e-3:
                        intersections.pop(0)

                if len(intersections) > 0:
                    x_end, z_end = intersections[0]
                    z_end = new_zprofile.interpolate(x_end)
            else:
                self.reset()
                return False

            if reverse:
                x_start = 2 * x_mean - x_start
                x_end = 2 * x_mean - x_end

            self._results = {'zprofile': zprofile,
                             'reverse': reverse,
                             'method': method,
                             'x_start': x_start,
                             'z_start': z_start,
                             'x_end': x_end,
                             'z_end': z_end,
                             'angle': angle,
                             'success': True}
            return True

        else:
            if not ("x_end" in kwargs.keys() and "angle" in kwargs.keys()):
                self.reset()
                return False
            else:
                x_end = kwargs["x_end"]
                angle = kwargs["angle"]

            if not (isinstance(x_end, (int, float)) and isinstance(angle, (int, float))):
                self.reset()
                return False
            elif not -90 < angle < 90:
                self.reset()
                return False
            else:
                angle = abs(angle)
                z_end = zprofile.interpolate(x_end)

            if not isinstance(z_end, (int, float)):
                self.reset()
                return False

            if reverse:
                new_zprofile = zprofile.reverse(zprofile)
                x_mean = (min(zprofile.x) + max(zprofile.x)) / 2
                x_end = 2 * x_mean - x_end
            else:
                new_zprofile = zprofile.duplicate()

            x_start = new_zprofile.x[0]
            z_start = - tan(radians(angle)) * (x_start - x_end) + z_end

            xz = [(x_start, z_start),
                  (x_end, z_end)]
            
            energy_profile = zProfile()
            energy_profile.xz = xz

            intersections = new_zprofile.intersect(energy_profile)

            if isinstance(intersections, list):
                if len(intersections) > 0:
                    if x_end in [x for x, z in intersections]:
                        i = [x for x, z in intersections].index(x_end)
                        intersections.pop(i)

                if len(intersections) > 0:
                    if abs(x_end - intersections[0][0]) < 1e-3:
                         intersections.pop(0)

                if len(intersections) > 0:
                    x_start, z_start = intersections[0]
                    z_start = new_zprofile.interpolate(x_start)

            if reverse:
                x_start = 2 * x_mean - x_start
                x_end = 2 * x_mean - x_end

            self._results = {'zprofile': zprofile,
                             'reverse': reverse,
                             'method': method,
                             'x_start': x_start,
                             'z_start': z_start,
                             'x_end': x_end,
                             'z_end': z_end,
                             'angle': angle,
                             'success': True}
            return True

    def update(self):
        """
        update energy line properties

        returns:
        - None - NoneType

        examples:
        >>> energy_line.update()
        
        """  
        if self._results["success"]:
            self._xy = [(self._results["x_start"], self._results["z_start"]),
                        (self._results["x_end"], self._results["z_end"])]
        
            Line.update(self)

    @property
    def results(self):
        if self._results['success']:
            return self._results
        else:
            return {'success': False}
        
    @property
    def xy(self):
        if self._results["success"]:
            return list(self._xy)
        
    @xy.setter
    def xy(self, xy):
        pass
