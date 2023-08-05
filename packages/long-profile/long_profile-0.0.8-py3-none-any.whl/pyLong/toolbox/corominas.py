from matplotlib.lines import Line2D as mpl_Line
import numpy as np

from pyLong.profiles.zprofile import zProfile

class Corominas(zProfile):
    def __init__(self):
        zProfile.__init__(self)

        self._name = "new corominas"

        self._results = {'zprofile': zProfile(),
                         'reverse': True,
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'volume': 0.,
                         'step': 0.,
                         'model': "Debris flows - All",
                         'success': False}
        
    """
    Methods:
    - area
    - clear
    - copy_style
    - duplicate
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
        calculate the area below or above the corominas curve

        arguments:
        - kind: "below" | "above" - str

        returns:
        - area: area (m2) - float
        or
        - None - NoneType

        examples:
        >>> area = corominas.area()
        >>> area = corominas.area(kind="above")
        
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
        >>> corominas.clear()
        """
        zProfile.clear(self)

    def copy_style(self, corominas):
        """
        copy the style of a corominas calculation

        arguments:
        - corominas: corominas calculation whose style is to be copied - Corominas

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_corominas.copy_style(corominas)
        
        """
        zProfile.copy_style(self, corominas)

    def duplicate(self):
        """
        duplicate the corominas calculation

        returns:
        - new_corominas: duplicated corominas calculation - Corominas

        examples:
        >>> new_corominas = corominas.duplicate()

        """
        new_corominas = Corominas()
        new_corominas.copy_style(self)

        new_corominas.name = f"{self._name} duplicated"
        new_corominas.label = self._label

        new_corominas.xz = self._xz

        new_corominas._results = self._results

        return new_corominas
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3, reverse=False, header=["X","Z"]):
        """
        export corominas curve points

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
        >>> corominas.export("corominas.txt")
        >>> corominas.export("corominas.txt", delimiter=";", separator=".", decimals=2, header=[])
        
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
        export corominas curve style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> corominas.export_style("style.json")
        
        """
        return zProfile.export_style(self,
                                     filename)

    def from_dbf(self, filename, x_field="dist", z_field="Z"):
        return False

    def from_shp(self, filename):
        return False

    def from_txt(self, filename, x_field="X", z_field="Z", delimiter="\t", decimal="."):
        return False

    def import_style(self, filename):
        """
        import corominas curve style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> corominas.import_style("style.json")
        
        """
        return zProfile.import_style(self,
                                     filename)
        
    def interpolate(self, x):
        """
        interpolate the corominas curve

        arguments:
        - x: distance (m) - int | float

        returns:
        - z: interpolated altitude (m) - float
        or
        - None - NoneType

        examples:
        >>> z = corominas.interpolate(x=150.)
        """
        if self._results["success"]:
            return zProfile.interpolate(self, x)
        else:
            return None

    def intersect(self, corominas):
        """
        calculate the intersections with another corominas curve

        arguments:
        - corominas: corominas calculation - Corominas

        returns:
        - intersections: intersections - list
        or
        - None - NoneType

        examples:
        >>> intersections = corominas.intersect(new_corominas)
        
        """
        if self._results["success"]:
            return zProfile.intersect(corominas)
        else:
            return None

    def length(self, dim="2D"):
        """
        calculate the corominas curve length

        arguments:
        - dim: "2D" for plan length or "3D" for actual length - str
        
        returns:
        - plan length (m) - float
        or
        - actual length (m) - float
        or
        - None - NoneType

        examples:
        >>> length_2d = corominas.length()
        >>> length_3d = corominas.length(dim="3D")
        
        """
        if self._results["success"]:
            return zProfile.length(dim)
        else:
            return None
        
    def listing(self, decimals=3):
        """
        print the list of the corominas curve points

        arguments:
        - decimals: number of decimals to print - int

        returns:
        - None - NoneType

        examples:
        >>> corominas.listing()
        >>> corominas.listing(decimals=2)
        
        """
        if self._results["success"]:
            return zProfile.listing(self, decimals=decimals)
        else:
            return None
        
    def new_point(self, i, method, **kwargs):
        return None

    def plot(self, ax):
        """
        plot the corominas curve on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> corominas.plot(ax)
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
        >>> corominas.reset()
        
        """
        self._results = {'zprofile': zProfile(),
                         'reverse': False,
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'volume': 0.,
                         'step': 0.,
                         'model': "Debris flows - All",
                         'success': False}

    def reverse(self, zprofile):
        return None

    def run(self, zprofile, reverse=True, x_start=0., volume=1000., step=1., model="Debris flows - All"):
        """
        run calculation

        arguments:
        - zprofile: profile - zProfile
        - reverse: reverse the profile - bool
        - x_start: start distance (m) - int | float
        - volume: volume (m3) - int | float
        - step: altimetric calculation step (m) - int | float
        - model: model to be used - str
            - "Debris flows - All" or
            - "Debris flows - Obstructed" or
            - "Debris flows - Channelized" or
            - "Debris flows - Unobstructed" or
            - "Mud flows - All" or
            - "Mud flows - Unobstructed"

        returns:
        - True if succes - bool
        - False else - bool

        examples:
        >>> corominas.run(zprofile, reserve=True, x_start=1500., volume=10000., step=1., model="Debris flows - All")
        
        """
        if not (isinstance(zprofile, zProfile) and 
                isinstance(reverse, bool) and 
                isinstance(x_start, (int, float)) and
                isinstance(volume, (int, float)) and
                isinstance(step, (int, float)) and
                isinstance(model, str)):
            self.reset()
            return False
        
        if model not in ["Debris flows - All",
                         "Debris flows - Obstructed",
                         "Debris flows - Channelized",
                         "Debris flows - Unobstructed",
                         "Mud flows - All",
                         "Mud flows - Unobstructed"]:
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

        corominas = zProfile()
        
        if model == "Debris flows - All":
            xz = [(x_start + 10**0.012 * volume**0.105 * (z_start - z), z) for z in altitudes]
        elif model == "Debris flows - Obstructed":
            xz = [(x_start + 10**0.049 * volume**0.108 * (z_start - z), z) for z in altitudes]
        elif model == "Debris flows - Channelized":
            xz = [(x_start + 10**0.077 * volume**0.109 * (z_start - z), z) for z in altitudes]
        elif model == "Debris flows - Unobstructed":
            xz = [(x_start + 10**0.031 * volume**0.102 * (z_start - z), z) for z in altitudes]
        elif model == "Mud flows - All":
            xz = [(x_start + 10**0.214 * volume**0.070 * (z_start - z), z) for z in altitudes]
        else:
            xz = [(x_start + 10**0.220 * volume**0.138 * (z_start - z), z) for z in altitudes]
        
        corominas.xz = xz

        if x_start not in corominas.x:
            self.reset()
            return False
        
        intersections = corominas.intersect(new_zprofile)

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
                x_end = corominas.x[-1]
                z_end = corominas.z[-1]

        else:
            self.reset()
            return False
        
        corominas = corominas.truncate(distances=(x_start, x_end))

        if not isinstance(corominas, zProfile):
            self.reset()
            return False

        if reverse:
            x_start = 2 * x_mean - x_start
            x_end = 2 * x_mean - x_end
            x = corominas.reverse(zprofile).x
            z = corominas.reverse(zprofile).z
        else:
            x = corominas.x
            z = corominas.z

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
                         'model': "Debris flows - All",
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
        >>> corominas.update()
        
        """  
        if self._results["success"]:
            zProfile.update(self)

    def __add__(self, corominas):
        return None

    def __sub__(self, corominas):
        return None

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_line"] = mpl_Line([], [])

        return attributes
        
    @property
    def results(self):
        if self._results['success']:
            return self._results
        else:
            return {'success': False}
        
    @property
    def xz(self):
        if self._results["success"]:
            return self._xz
        else:
            return None
        
    @xz.setter
    def xz(self, xz):
        pass
