from matplotlib.lines import Line2D as mpl_Line
import numpy as np
from scipy import interpolate

from pyLong.profiles.zprofile import zProfile

class FlowR(zProfile):
    def __init__(self):
        zProfile.__init__(self)

        self._name = "new flow-r"

        self._results = {'zprofile': zProfile(),
                         'reverse': True,
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'angle': 11.,
                         'initial_speed': 5.,
                         'maximum_speed': 10.,
                         'step': 1.,
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
        calculate the area below or above the flow-r curve

        arguments:
        - kind: "below" | "above" - str

        returns:
        - area: area (m2) - float
        or
        - None - NoneType

        examples:
        >>> area = flow_r.area()
        >>> area = flow_r.area(kind="above")
        
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
        >>> flow_r.clear()
        """
        zProfile.clear(self)

    def copy_style(self, corominas):
        """
        copy the style of a flow-r calculation

        arguments:
        - flow_r: flow-r calculation whose style is to be copied - FlowR

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_flow_r.copy_style(flow_r)
        
        """
        zProfile.copy_style(self, corominas)

    def duplicate(self):
        """
        duplicate the flow-r calculation

        returns:
        - new_flow_r: duplicated flow-r calculation - FlowR

        examples:
        >>> new_flow_r = flow_r.duplicate()

        """
        new_flow_r = FlowR()
        new_flow_r.copy_style(self)

        new_flow_r.name = f"{self._name} duplicated"
        new_flow_r.label = self._label

        new_flow_r.xz = self._xz

        new_flow_r._results = self._results

        return new_flow_r
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3, reverse=False, header=["X","Z"]):
        """
        export flow-r curve points

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
        >>> flow_r.export("flow_r.txt")
        >>> flow_r.export("flow_r.txt", delimiter=";", separator=".", decimals=2, header=[])
        
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
        export flow-r curve style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> flow_r.export_style("style.json")
        
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
        import flow-r curve style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> flow_r.import_style("style.json")
        
        """
        return zProfile.import_style(self,
                                     filename)
        
    def interpolate(self, x):
        """
        interpolate the flow-r curve

        arguments:
        - x: distance (m) - int | float

        returns:
        - z: interpolated altitude (m) - float
        or
        - None - NoneType

        examples:
        >>> z = flow_r.interpolate(x=150.)
        """
        if self._results["success"]:
            return zProfile.interpolate(self, x)
        else:
            return None

    def intersect(self, flow_r):
        """
        calculate the intersections with another flow-r curve

        arguments:
        - flow_r: flow-r calculation - FlowR

        returns:
        - intersections: intersections - list
        or
        - None - NoneType

        examples:
        >>> intersections = flow_r.intersect(new_flow_r)
        
        """
        if self._results["success"]:
            return zProfile.intersect(flow_r)
        else:
            return None

    def length(self, dim="2D"):
        """
        calculate the flow-r curve length

        arguments:
        - dim: "2D" for plan length or "3D" for actual length - str
        
        returns:
        - plan length (m) - float
        or
        - actual length (m) - float
        or
        - None - NoneType

        examples:
        >>> length_2d = flow_r.length()
        >>> length_3d = flow_r.length(dim="3D")
        
        """
        if self._results["success"]:
            return zProfile.length(dim)
        else:
            return None
        
    def listing(self, decimals=3):
        """
        print the list of the flow-r curve points

        arguments:
        - decimals: number of decimals to print - int

        returns:
        - None - NoneType

        examples:
        >>> flow_r.listing()
        >>> flow_r.listing(decimals=2)
        
        """
        if self._results["success"]:
            return zProfile.listing(self, decimals=decimals)
        else:
            return None
        
    def new_point(self, i, method, **kwargs):
        return None

    def plot(self, ax):
        """
        plot the flow-r curve on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> flow_r.plot(ax)
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
        >>> flow_r.reset()
        
        """
        self._results = {'zprofile': zProfile(),
                         'reverse': True,
                         'x_start': 0.,
                         'z_start': 0.,
                         'x_end': 0.,
                         'z_end': 0.,
                         'angle': 11.,
                         'initial_speed': 5.,
                         'maximum_speed': 10.,
                         'step': 1.,
                         'success': False}

    def reverse(self, zprofile):
        return None

    def run(self, zprofile, reverse=True, x_start=0., angle=11., initial_speed=5., maximum_speed=10., step=1.):
        """
        run calculation

        arguments:
        - zprofile: profile - zProfile
        - reverse: reverse the profile - bool
        - x_start: start distance (m) - int | float
        - angle: energy angle (deg) - int | float
        - initial_speed: initial speed (m/s) - int | float
        - maximum_speed: maximum speed (m/s) - int | float
        - step: altimetric calculation step (m) - int | float

        returns:
        - True if succes - bool
        - False else - bool

        examples:
        >>> flow_r.run(zprofile, reserve=True, x_start=1500., angle=11., initial_speed=5., maximum_speed=10., step=1.)
        
        """
        if not (isinstance(zprofile, zProfile) and 
                isinstance(reverse, bool) and 
                isinstance(x_start, (int, float)) and
                isinstance(angle, (int, float)) and
                isinstance(initial_speed, (int, float)) and
                isinstance(maximum_speed, (int, float)) and
                isinstance(step, (int, float))):
            self.reset()
            return False
        
        z_start = zprofile.interpolate(x_start)

        if not isinstance(z_start, (int, float)):
            self.reset()
            return False
        
        if not (0 < angle < 90 and 0 < initial_speed < maximum_speed and 0 < step):
            self.reset()
            return False

        if reverse:
            new_zprofile = zprofile.reverse(zprofile)
            x_mean = (min(zprofile.x) + max(zprofile.x)) / 2
            x_start = 2 * x_mean - x_start
        else:
            new_zprofile = zprofile.duplicate()

        distances = np.arange(x_start, max(zprofile.x), step)
        distances = list(distances)
        distances.append(max(zprofile.x))

        if not 1 < len(distances):
            self.reset()
            return False
        
        f = interpolate.interp1d(np.array(new_zprofile.x), np.array(new_zprofile.z))
        altitudes = list(f(np.array(distances)))

        n = len(distances)
        speed_debris_flow = list(-1 * np.ones(n))
        energy_debris_flow = list(np.zeros(n))
        
        speed_debris_flow[0] = initial_speed

        g = 9.81

        energy_debris_flow[0] = z_start + initial_speed**2 / (2 * g)

        flow_r = zProfile()

        for i in range(1, n):
            expr = speed_debris_flow[i-1]**2 + 2 * g *(altitudes[i-1] - altitudes[i]) - 2 * g * (distances[i] - distances[i-1]) * np.tan(np.radians(angle))
            if expr > 0:
                speed_debris_flow[i] = min(np.sqrt(expr), maximum_speed)
            else:
                speed_debris_flow[i] = 0
                k = i
                energy_debris_flow[i] = altitudes[i]
                break
            energy_debris_flow[i] = altitudes[i] + speed_debris_flow[i]**2 / (2 * g)
        
        try:
            k = np.argwhere(np.array(speed_debris_flow) == 0.)[0][0]
        except:
            self.reset()
            return False
        
        x_end = distances[k]
        z_end = altitudes[k]

        xz = [(x, z) for x, z in zip(distances[:k+1], altitudes[:k+1])]
        flow_r.xz = xz

        if reverse:
            x_start = 2 * x_mean - x_start
            x_end = 2 * x_mean - x_end
            x = flow_r.reverse(zprofile).x
            z = flow_r.reverse(zprofile).z
        else:
            x = flow_r.x
            z = flow_r.z

        xz = [(float(x), float(z)) for x, z in zip(x, z)]      
        
        self._xz = xz

        self._results = {'zprofile': zprofile,
                         'reverse': reverse,
                         'x_start': x_start,
                         'z_start': z_start,
                         'x_end': x_end,
                         'z_end': z_end,
                         'angle': angle,
                         'initial_speed': initial_speed,
                         'maximum_speed': maximum_speed,
                         'step': step,
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
        >>> flow_r.update()
        
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
