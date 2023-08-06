from matplotlib.lines import Line2D as mpl_Line
import numpy as np

from pyLong.profiles.zprofile import zProfile

class Rickenmann(zProfile):
    def __init__(self):
        zProfile.__init__(self)

        self._name = "new rickenmann"

        self._results = {'zprofile': zProfile(),
                         'reverse': True,
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'volume': 0.,
                         'step': 0.,
                         'envelope': False,
                         'success': False}
        
    """
    Methods:
    - area
    - clear
    - copy_style
    - export
    - export_style
    - import_style
    - interpolate
    - intersect
    - length
    - listing
    - plot
    - run
    - update
    """
    
    def add_point(self, point):
        return False

    def area(self, kind="below"):
        """
        calculate the area below or above the rickenmann curve

        arguments:
        - kind: "below" | "above" - str

        returns:
        - area: area (m2) - float
        or
        - None - NoneType

        examples:
        >>> area = rickenmann.area()
        >>> area = rickenmann.area(kind="above")
        
        """
        if self._results["success"]:
            return zProfile.area(self, kind)
        else:
            return None

    def clear(self):
        """
        clear line

        returns:
        - None - NoneType

        examples:
        >>> rickenmann.clear()
        """
        zProfile.clear(self)

    def copy_style(self, corominas):
        """
        copy the style of a rickenmann calculation

        arguments:
        - rickenmann: rickenmann calculation whose style is to be copied - Rickenmann

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_rickenmann.copy_style(rickenmann)
        
        """
        zProfile.copy_style(self, corominas)

    def duplicate(self):
        return None
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3, reverse=False, header=["X","Z"]):
        """
        export rickenmann curve points

        arguments:
        - filename: file path - str
        - delimiter: columns delimiter "\\t" | " " | ";" | "," - str
        - separator: decimal separator "." | ";" - str
        - decimals: number of decimals to export - int
        - reverse: if True, export from end to start - bool
        - header: header, empty list for no header - list of str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> rickenmann.export("rickenmann.txt")
        >>> rickenmann.export("rickenmann.txt", delimiter=";", separator=".", decimals=2, header=[])
        
        """
        zProfile.export(self,
                        filename,
                        delimiter=delimiter,
                        separator=separator,
                        decimals=decimals,
                        reverse=reverse,
                        header=header)
    
    def export_style(self, filename):
        """
        export rickenmann curve style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> rickenmann.export_style("style.json")
        
        """
        return zProfile.export_style(self, filename)

    def from_dbf(self, filename, x_field="dist", z_field="Z"):
        return False

    def from_shp(self, filename):
        return False

    def from_txt(self, filename, x_field="X", z_field="Z", delimiter="\t", decimal="."):
        return False

    def import_style(self, filename):
        """
        import rickenmann curve style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> rickenmann.import_style("style.json")
        
        """
        return zProfile.import_style(self, filename)
        
    def interpolate(self, x):
        """
        interpolate the rickenmann curve

        arguments:
        - x: distance (m) - int | float

        returns:
        - z: interpolated altitude (m) - float
        or
        - None - NoneType

        examples:
        >>> z = rickenmann.interpolate(x=150.)
        """
        if self._results["success"]:
            return zProfile.interpolate(self, x)
        else:
            return None

    def intersect(self, corominas):
        """
        calculate the intersections with another rickenmann curve

        arguments:
        - rickenmann: rickenmann calculation - Rickenmann

        returns:
        - intersections: intersections - list
        or
        - None - NoneType

        examples:
        >>> intersections = rickenmann.intersect(new_rickenmann)
        
        """
        if self._results["success"]:
            return zProfile.intersect(corominas)
        else:
            return None

    def length(self, dim="2D"):
        """
        calculate the rickenmann curve length

        arguments:
        - dim: "2D" for plan length or "3D" for actual length - str
        
        returns:
        - plan length (m) - float
        or
        - actual length (m) - float
        or
        - None - NoneType

        examples:
        >>> length_2d = rickenmann.length()
        >>> length_3d = rickenmann.length(dim="3D")
        
        """
        if self._results["success"]:
            return zProfile.length(dim)
        else:
            return None
        
    def listing(self, decimals=3):
        """
        print the list of the rickenmann curve points

        arguments:
        - decimals: number of decimals to print - int

        returns:
        - None - NoneType

        examples:
        >>> rickenmann.listing()
        >>> rickenmann.listing(decimals=2)
        
        """
        if self._results["success"]:
            return zProfile.listing(self, decimals=decimals)
        else:
            return None
        
    def new_point(self, i, method, **kwargs):
        return None

    def plot(self, ax):
        """
        plot the rickenmann curve on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> rickenmann.plot(ax)
        >>> plt.show()
        """
        if self._results["success"]:
            zProfile.plot(self, ax)
        else:
            return None
        
    def remove_point(self, i):
        return False

    def resample(self, d):
        return None

    def reset(self):
        """
        clear results

        returns:
        - None - NoneType

        examples:
        >>> rickenmann.reset()
        
        """
        self._results = {'zprofile': zProfile(),
                         'reverse': False,
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'volume': 0.,
                         'step': 0.,
                         'envelope': False,
                         'success': False}

    def reverse(self, zprofile):
        return None

    def run(self, zprofile, reverse=True, x_start=0., volume=1000., envelope=False, step=1.):
        """
        run calculation

        arguments:
        - zprofile: profile - zProfile
        - reverse: reverse the profile - bool
        - x_start: start distance (m) - int | float
        - volume: volume (m3) - int | float
        - envelope: change to envelope equation - bool
        - step: altimetric calculation step (m) - int | float

        returns:
        - True if succes - bool
        - False else - bool

        examples:
        >>> rickenmann.run(zprofile, reserve=True, x_start=1500., volume=10000., envelope=True, step=1.)
        
        """
        if not (isinstance(zprofile, zProfile) and 
                isinstance(reverse, bool) and 
                isinstance(x_start, (int, float)) and
                isinstance(volume, (int, float)) and
                isinstance(step, (int, float)) and
                isinstance(envelope, bool)):
            self.reset()
            return False
        
        z_start = zprofile.interpolate(x_start)

        if not isinstance(z_start, (int, float)):
            self.reset()
            return False
        
        if not (0 < volume and 0 < step):
            self.reset()
            return False
        
        altitudes = np.arange(z_start, min(zprofile.z), -step)
        altitudes = list(altitudes)
        altitudes.append(min(zprofile.z))

        if not 1 < len(altitudes):
            self.reset()
            return False

        if reverse:
            new_zprofile = zprofile.reverse(zprofile)
            x_mean = (min(zprofile.x) + max(zprofile.x)) / 2
            x_start = 2 * x_mean - x_start
        else:
            new_zprofile = zprofile.duplicate()

        rickenmann = zProfile()

        if envelope:
            xz = [(x_start + 5.0 * volume**0.16 * (z_start - z)**0.83, z) for z in altitudes]
        else:
            xz = [(x_start + 1.9 * volume**0.16 * (z_start - z)**0.83, z) for z in altitudes]

        rickenmann.xz = xz

        if x_start not in rickenmann.x:
            self.reset()
            return False
        
        intersections = rickenmann.intersect(new_zprofile)

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
                x_end = rickenmann.x[-1]
                z_end = rickenmann.z[-1]

        else:
            self.reset()
            return False
        
        rickenmann = rickenmann.truncate(distances=(x_start, x_end))

        if not isinstance(rickenmann, zProfile):
            self.reset()
            return False

        if reverse:
            x_start = 2 * x_mean - x_start
            x_end = 2 * x_mean - x_end
            x = rickenmann.reverse(zprofile).x
            z = rickenmann.reverse(zprofile).z
        else:
            x = rickenmann.x
            z = rickenmann.z

        xz = [(x, z) for x, z in zip(x, z)]

        self._xz = xz

        self._results = {'zprofile': zprofile,
                         'reverse': reverse,
                         'x_start': x_start,
                         'z_start': z_start,
                         'x_end': x_end,
                         'z_end': z_end,
                         'volume': volume,
                         'step': step,
                         'envelope': envelope,
                         'success': True}
        
        return True

    def scale(self, Lx=1., Lz=1.):
        return None

    def simplify(self, **kwargs):
        return None

    def solve(self, z, x0):
        return None

    def translate(self, dx=0., dz=0.):
        return None

    def truncate(self, **kwargs):
        return None
    
    def update(self):
        """
        update line properties

        returns:
        - None - NoneType

        examples:
        >>> rickenmann.update()
        
        """  
        if self._results["success"]:
            zProfile.update(self)

    def __add__(self, corominas):
        return None

    def __sub__(self, corominas):
        return None
        
    @property
    def results(self):
        if self._results['success']:
            return self._results
        else:
            return {'success': False}
        
    @property
    def xz(self):
        if self._results["success"]:
            return list(self._xz)
        else:
            return None
        
    @xz.setter
    def xz(self, xz):
        pass
