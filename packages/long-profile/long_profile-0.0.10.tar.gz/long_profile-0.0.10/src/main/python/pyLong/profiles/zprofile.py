import json
from math import ceil, radians, pi, atan, tan, sqrt
import os

from matplotlib.axes import Subplot
from matplotlib.lines import Line2D as mpl_Line
import numpy as np
import pandas as pd
from rdp import rdp
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
import shapefile
from simpledbf import Dbf5
import visvalingamwyatt as vw

from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles, marker_styles
from pyLong.misc.intersect import intersection


class zProfile:
    def __init__(self):
        self._name = "new zprofile"

        self._label = ""

        self._xz = [(0., 0.), (1000., 1000.)]

        self._line = mpl_Line([], [])

        self._line_style = "solid"

        self._line_color = "Black"
        
        self._line_thickness = 1.

        self._marker_style = "none"
        
        self._marker_color = "Black"
        
        self._marker_size = 1.

        self._opacity = 1.
        
        self._order = 1

        self._visible = True

        self._active = True

    """
    Methods:
    - add_point
    - area
    - clear
    - copy_style
    - duplicate
    - export
    - export_style
    - from_dbf
    - from_shp
    - from_txt
    - import_style
    - interpolate
    - intersect
    - length
    - listing
    - new_point
    - plot
    - remove_point
    - resample
    - reverse
    - scale
    - simplify
    - solve
    - translate
    - truncate
    - update
    - __add__ --> merge
    - __sub__ --> subtract
    """
    
    def add_point(self, point):
        """
        add a point
        
        arguments:
        - point: (x, z) - tuple
            - x: distance (m) - int | float
            - z: altitude (m) - int | float

        returns:
        - True if success
        - False else

        examples:
        >>> zprofile.add_point((550., 1100.))

        """
        if not isinstance(point, tuple):
            return False
        elif not len(point) > 1:
            return False
        else:
            x, z = point[0], point[1]
            if not (isinstance(x, (int, float)) and isinstance(z, (int, float))):
                return False
            elif x in self.x:
                return False
            else:
                self._xz.append((x, z))
                self._xz.sort()
                return True

    def area(self, kind="below"):
        """
        calculate the area below or above the profile

        arguments:
        - kind: "below" | "above" - str

        returns:
        - area: area (m2) - float
        or
        - None - NoneType

        examples:
        >>> area = zprofile.area()
        >>> area = zprofile.area(kind="above")
        
        """
        if not isinstance(kind, str):
            return None
        elif kind not in ["above", "below"]:
            return None
        else:
            x = self.x
            z = [z - self.z_min for z in self.z]

            if kind == "below":
                return float(np.trapz(z, x))
            else:
                return (self.length() * (max(z) - min(z))) - float(np.trapz(z, x)) 
                        
    def clear(self):
        """
        clear line

        returns:
        - None - NoneType

        examples:
        >>> zprofile.clear()
        
        """
        self._line = mpl_Line([], [])
        
    def copy_style(self, zprofile):
        """
        copy the style of a profile

        arguments:
        - zprofile: profile whose style is to be copied - zProfile

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_zprofile.copy_style(zprofile)
        
        """
        if isinstance(zprofile, zProfile):
            self._line_style = zprofile.line_style
            self._line_color = zprofile.line_color
            self._line_thickness = zprofile.line_thickness
            self._marker_style = zprofile.marker_style
            self._marker_color = zprofile.marker_color
            self._marker_size = zprofile.marker_size
            self._opacity = zprofile.opacity
            self._order = zprofile.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the profile

        returns:
        - new_zprofile: duplicated profile - zProfile

        examples:
        >>> new_zprofile = zprofile.duplicate()

        """
        new_zprofile = zProfile()
        new_zprofile.copy_style(self)
        
        new_zprofile.name = f"{self._name} duplicated"
        new_zprofile.label = self._label
        
        new_zprofile.xz = list(self._xz)
        
        return new_zprofile
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3, reverse=False, header=["X","Z"]):
        """
        export profile points

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
        >>> zprofile.export("profile.txt")
        >>> zprofile.export("profile.txt", delimiter=";", separator=".", decimals=2, header=[])
        
        """
        if not isinstance(header, list):
            return False
        else:
            if len(header) == 0:
                header = False
            elif len(header) > 1:
                if not (isinstance(header[0], str) and isinstance(header[1], str)):
                    return False
                else:
                    header = [header[0], header[1]]
            else:
                return False

        if not (isinstance(filename, str) and isinstance(decimals, int)):
            return False
        elif delimiter not in ["\t", " ", ";", ","] or separator not in [".", ","]:
            return False
        elif delimiter == separator:
            return False
        elif not len(filename) > 0:
            return False
        else:
            xz = sorted(self._xz, reverse=reverse)
            x = [x for x, z in xz]
            z = [z for x, z in xz]

            x = np.array(x)
            z = np.array(z)
            
            xz = np.array([x, z]).T
            xz = pd.DataFrame(xz) 
            
            try:
                xz.to_csv(filename,
                          sep = delimiter,
                          float_format = f"%.{decimals}f",
                          decimal = separator,
                          index = False,
                          header = header)
                return True
            except:
                return False
    
    def export_style(self, filename):
        """
        export profile style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> zprofile.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'line_style': self._line_style,
                     'line_color': self._line_color,
                     'line_thickness': self._line_thickness,
                     'marker_style': self._marker_style,
                     'marker_color': self._marker_color,
                     'marker_size': self._marker_size,
                     'opacity': self._opacity,
                     'order': self._order}
            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False

    def from_dbf(self, filename, x_field="dist", z_field="Z"):
        """
        import points from a .dbf file

        arguments:
        - filename: .dbf file path - str
        - x_field: distance field name - str
        - z_field: altitude field name - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> zprofile.from_dbf("profile.dbf")
        >>> zprofile.from_dbf("profile.dbf", x_field="X", z_field="Z")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        elif not os.path.isfile(filename):
            return False
        elif not (isinstance(x_field, str) and isinstance(z_field, str)):
            return False
        else:
            try:
                dbf = Dbf5(filename)
            except:
                return False
        
        data = dbf.to_dataframe()
        data = data.dropna()

        if data.shape[0] < 2 or data.shape[1] < 2:
            return False
        elif not (x_field in list(data.columns) and z_field in list(data.columns)):
            return False
        elif not (data.loc[:, x_field].dtype in ['float64', 'int64'] and \
                  data.loc[:, z_field].dtype in ['float64', 'int64']):
            return False
        
        i = list(data.columns).index(x_field)
        x = list(data.values[:, i])
        
        i = list(data.columns).index(z_field)
        z = list(data.values[:, i])
        
        xz = [(x, z) for x, z in zip(x, z)]
        
        xz.sort()
        x = [x for x, z in xz]
        dx = np.array(x[1:]) - np.array(x[:-1])
        dx = list(dx)
        
        if 0 in dx:
            return False
        else:
            self._xz = xz
            return True  

    def from_shp(self, filename):
        """
        import points from a .shp file

        arguments:
        - filename: .shp file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> zprofile.from_shp("profile.shp")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        elif not os.path.isfile(filename):
            return False
        else:
            try:
                sf = shapefile.Reader(filename)
            except:
                return False
        
        shapes = sf.shapes()
        
        if len(shapes) < 1:
            return False
        else:
            shape = shapes[0]

        if shape.shapeType != 13:
            return False
        
        dist = [0]
        for i, (x, y) in enumerate(shape.points):
            if i != 0:
                d = ((x - shape.points[i-1][0])**2 + (y - shape.points[i-1][1])**2)**0.5
                dist.append(d + dist[i-1])
                
        xz = [(float(x), float(z)) for x, z in zip(dist, shape.z)]
        
        xz.sort()
        x = [x for x, z in xz]
        dx = np.array(x[1:]) - np.array(x[:-1])
        dx = list(dx)
        
        if 0 in dx:
            return False
        else:
            self._xz = xz
            return True  

    def from_txt(self, filename, x_field="X", z_field="Z", delimiter="\t", decimal="."):
        """
        import points from a .txt file

        arguments:
        - filename: .txt file path - str
        - x_field: distance field name - str
        - z_field: altitude field name - str
        - delimiter: column delimiter "\\t" | " " | ";" | "," - str
        - decimal: decimal separator "." |"," - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> zprofile.from_txt("profile.txt")
        >>> zprofile.from_txt("profile.txt", x_field="dist", z_field="altitude", delimiter=";", decimal=",")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        elif not os.path.isfile(filename):
            return False
        elif not (isinstance(x_field, str) and isinstance(z_field, str)):
            return False
        elif not (delimiter in [" ", "\t", ";", ","] and decimal in [".", ","] and delimiter != decimal):
            return False
        else:
            try:
                data = pd.read_csv(filename,
                                   delimiter=delimiter,
                                   decimal=decimal,
                                   skiprows=0,
                                   encoding="utf-8",
                                   index_col=False)
                
            except:
                return False
            
        data = data.dropna()
        
        if data.shape[0] < 2 or data.shape[1] < 2:
            return False
        elif not (x_field in list(data.columns) and z_field in list(data.columns)):
            return False
        elif not (data.loc[:, x_field].dtype in ['float64', 'int64'] and \
                  data.loc[:, z_field].dtype in ['float64', 'int64']):
            return False
        
        i = list(data.columns).index(x_field)
        x = list(data.values[:, i])
        
        i = list(data.columns).index(z_field)
        z = list(data.values[:, i])
        
        xz = [(float(x), float(z)) for x, z in zip(x, z)]
        
        xz.sort()
        x = [x for x, z in xz]
        dx = np.array(x[1:]) - np.array(x[:-1])
        dx = list(dx)
        
        if 0 in dx:
            return False
        else:
            self._xz = xz
            return True  
                    
    def import_style(self, filename):
        """
        import profile style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> zprofile.import_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        elif not os.path.isfile(filename):
            return False
        else:
            try:
                with open(filename, 'r') as file:
                    style = json.load(file)
            except:
                return False

            if isinstance(style, dict):
                if 'line_style' in style.keys():
                    self.line_style = style['line_style']
                if 'line_color' in style.keys():
                    self.line_color = style['line_color']
                if 'line_thickness' in style.keys():
                    self.line_thickness = style['line_thickness']
                if 'marker_style' in style.keys():
                    self.marker_style = style['marker_style']
                if 'marker_color' in style.keys():
                    self.marker_color = style['marker_color']
                if 'line_thickness' in style.keys():
                    self.marker_size = style['marker_size']
                if 'opacity' in style.keys():
                    self.opacity = style['opacity']
                if 'order' in style.keys():
                    self.order = style['order']
                return True
            else:
                return False

    def interpolate(self, x):
        """
        interpolate the profile

        arguments:
        - x: distance (m) - int | float

        returns:
        - z: interpolated altitude (m) - float
        or
        - None - NoneType

        examples:
        >>> z = zprofile.interpolate(x=150.)
        """
        if not isinstance(x, (int, float)):
            return None
        elif not min(self.x) <= x <= max(self.x):
            return None
        else:
            Xs = self.x
            Xs.append(x)
            Xs.sort()
            i = Xs.index(x)

            if x == Xs[0]:
                return float(self.z[0])
            elif x == Xs[-1]:
                return float(self.z[-1])
            else:
                f = interp1d(self.x[i-1:i+1], self.z[i-1:i+1], kind='linear')
                return float(f(x))

    def intersect(self, zprofile):
        """
        calculate the intersections with another profile

        arguments:
        - zprofile: profile - zProfile

        returns:
        - intersections: intersections - list
        or
        - None - NoneType

        examples:
        >>> intersections = zprofile.intersect(new_zprofile)
        
        """
        if not isinstance(zprofile, zProfile):
            return None
        else:
            try:
                xs, zs = intersection(self.x, self.z, zprofile.x, zprofile.z)
            except:
                return None
            
            xz = [(float(x), float(z)) for x, z in zip(xs, zs)]
            return xz
                
    def length(self, dim="2D"):
        """
        calculate the profile length

        arguments:
        - dim: "2D" for plan length or "3D" for actual length - str
        
        returns:
        - plan length (m) - float
        or
        - actual length (m) - float
        or
        - None - NoneType

        examples:
        >>> length_2d = zprofile.length()
        >>> length_3d = zprofile.length(dim="3D")
        
        """
        if not isinstance(dim, str):
            return None
        elif dim.upper() not in ['2D', '3D']:
            return None
        elif dim.upper() == '2D':
            return float(self._xz[-1][0] - self._xz[0][0])
        else:
            dist = 0
            for i in range(1, len(self._xz)):
                dist += ((self.x[i] - self.x[i-1])**2 + (self.z[i] - self.z[i-1])**2)**0.5
            return float(dist)
                
    def listing(self, decimals=3):
        """
        print the list of points

        arguments:
        - decimals: number of decimals to print - int

        returns:
        - None - NoneType

        examples:
        >>> zprofile.listing()
        >>> zprofile.listing(decimals=2)
        
        """
        if not isinstance(decimals, int):
            return None
        else:
            for i, (x, z) in enumerate(self._xz):
                print(f"point {i}: x = {round(float(x), decimals)} m ; z = {round(float(z), decimals)} m") 
            
    def new_point(self, i, method, **kwargs):
        """
        calculate a new point

        arguments:
        - i: index of the reference point from which the new one will be determined - int
        - method: "dX + dZ" | "slope + X" | "slope + dX" | "slope + Z" | "slope + dZ" - str
        - X: distance (m) - int | float
        - Z: altitude (m) - int | float
        - dX: signed distance variation (m) - int | float
        - dZ: signed altitude variation (m) - int | float
        - slope: signed slope in the counterclockwise direction - int | float
        - slope_unit: slope unit "radian" | "degree" | "percent" - str

        returns:
        - x, z: distance, altitude of the new point - int | float, int | float
        or
        - None, None - NoneType, NoneType

        examples:
        >>> x, z = zprofile.new_point(i=2, method="dX + dZ", dX=5, dZ=10)
        >>> x, z = zprofile.new_point(i=1, method="slope + X", X=150, slope=45, slope_unit="degree")
        >>> x, z = zprofile.new_point(i=1, method="slope + dZ", dZ=10, slope=100, slope_unit="percent")
        
        """
        if not (isinstance(i, int) and isinstance(method, str)):
            return None, None
        elif not 0 <= i < len(self._xz):
            return None, None
        elif method not in ["dX + dZ", "slope + X", "slope + dX", "slope + Z", "slope + dZ"]:
            return None, None
        
        if method == "dX + dZ":
            if not ("dX" in kwargs.keys() and "dZ" in kwargs.keys()):
                return None, None
            elif not (isinstance(kwargs["dX"], (int, float)) and isinstance(kwargs["dZ"], (int, float))):
                return None, None
            else:
                dX = kwargs["dX"]
                dZ = kwargs["dZ"]
                
                return self.x[i] + dX, self.z[i] + dZ
        
        elif method == "slope + X":
            if not ("slope" in kwargs.keys() and "X" in kwargs.keys() and "slope_unit" in kwargs.keys()):
                return None, None
            elif kwargs["slope_unit"] not in ["radian", "degree", "percent"]:
                return None, None
            elif not (isinstance(kwargs["slope"], (int, float)) and isinstance(kwargs["X"], (int, float))):
                return None, None
            else:
                slope = kwargs["slope"]
                X = kwargs["X"]
                slope_unit = kwargs["slope_unit"]
                
                if slope_unit == "radian":
                    if not -pi/2 < slope < pi/2:
                        return None, None
                    else:
                        angle = slope
                elif slope_unit == "degree":
                    if not -90 < slope < 90:
                        return None, None
                    else:
                        angle = radians(slope)
                else:
                    angle = atan(slope / 100)
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.z[i]
                
                return X, f(X)
        
        elif method == "slope + dX":
            if not ("slope" in kwargs.keys() and "dX" in kwargs.keys() and "slope_unit" in kwargs.keys()):
                return None, None
            elif kwargs["slope_unit"] not in ["radian", "degree", "percent"]:
                return None, None
            elif not (isinstance(kwargs["slope"], (int, float)) and isinstance(kwargs["dX"], (int, float))):
                return None, None
            else:
                slope = kwargs["slope"]
                dX = kwargs["dX"]
                slope_unit = kwargs["slope_unit"]
                
                if slope_unit == "radian":
                    if not -pi/2 < slope < pi/2:
                        return None, None
                    else:
                        angle = slope
                elif slope_unit == "degree":
                    if not -90 < slope < 90:
                        return None, None
                    else:
                        angle = radians(slope)
                else:
                    angle = atan(slope / 100)
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.z[i]
                
                return self.x[i] + dX, f(self.x[i] + dX)
        
        elif method == "slope + Z":
            if not ("slope" in kwargs.keys() and "Z" in kwargs.keys() and "slope_unit" in kwargs.keys()):
                return None, None
            elif kwargs["slope_unit"] not in ["radian", "degree", "percent"]:
                return None, None
            elif not (isinstance(kwargs["slope"], (int, float)) and isinstance(kwargs["Z"], (int, float))):
                return None, None
            else:
                slope = kwargs["slope"]
                Z = kwargs["Z"]
                slope_unit = kwargs["slope_unit"]
                
                if slope_unit == "radian":
                    if not -pi/2 < slope < pi/2:
                        return None, None
                    else:
                        angle = slope
                elif slope_unit == "degree":
                    if not -90 < slope < 90:
                        return None, None
                    else:
                        angle = radians(slope)
                else:
                    angle = atan(slope / 100)
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.z[i]
                
                return self.x[i] + (Z - self.z[i]) / tan(angle), Z
        
        elif method == "slope + dZ":
            if not ("slope" in kwargs.keys() and "dZ" in kwargs.keys() and "slope_unit" in kwargs.keys()):
                return None, None
            elif kwargs["slope_unit"] not in ["radian", "degree", "percent"]:
                return None, None
            elif not (isinstance(kwargs["slope"], (int, float)) and isinstance(kwargs["dZ"], (int, float))):
                return None, None
            else:
                slope = kwargs["slope"]
                dZ = kwargs["dZ"]
                slope_unit = kwargs["slope_unit"]
                
                if slope_unit == "radian":
                    if not -pi/2 < slope < pi/2:
                        return None, None
                    else:
                        angle = slope
                elif slope_unit == "degree":
                    if not -90 < slope < 90:
                        return None, None
                    else:
                        angle = radians(slope)
                else:
                    angle = atan(slope / 100)
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.z[i]
                
                return self.x[i] + dZ / tan(angle), self.z[i] + dZ
        
    def plot(self, ax):
        """
        plot profile on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> zprofile.plot(ax)
        >>> plt.show()
        """
        if isinstance(ax, Subplot):
            self.clear()
            self.update()

            ax.add_line(self._line)            
        
    def remove_point(self, i):
        """
        remove point i

        arguments:
        - i: index of point to remove - int

        returns:
        - True if success
        - False else

        examples:
        >>> zprofile.remove_point(1)

        """
        if len(self._xz) == 2:
            return False
        elif not isinstance(i, int):
            return False
        elif not 0 <= i < len(self._xz):
            return False
        else:
            self._xz.pop(i)
            return True
                
    def resample(self, d):
        """
        resample the profile

        arguments:
        - d: distance (m) - int | float

        returns:
        - new_zprofile: resampled profile - zProfile
        or
        - None - NoneType

        examples:
        >>> new_zprofile = zprofile.resample(d=10.)
        
        """
        if not isinstance(d, (int, float)):
            return None
        elif d <= 0:
            return None
        else:
            x = self.x
            z = self.z
            
            new_zprofile = self.duplicate()
            new_zprofile.name = f"{self._name} resampled"
            
            for i in range(1, len(x)):
                l = sqrt((x[i] - x[i-1])**2 + (z[i] - z[i-1])**2)
                if l / d > 1:
                    n = ceil(l / d)
                    
                    for value in np.linspace(x[i-1], x[i], n+1):
                        value = float(value)
                        new_zprofile.add_point((value, self.interpolate(value)))
                        
            return new_zprofile

    def reverse(self, zprofile):
        """
        reverse the profile according to a reference profile

        arguments:
        - zprofile: reference profile to perform the reversing - zProfile

        returns:
        - new_zprofile: reversed profile - zProfile
        or
        - None - NoneType

        examples:
        >>> new_zprofile = zprofile.reverse(zprofile)

        """
        if not isinstance(zprofile, zProfile):
            return None
        else:
            new_zprofile = self.duplicate()
            new_zprofile.name = f"{self._name} reversed"
            
            x_start = zprofile.x[0]
            x_end = zprofile.x[-1]

            xz = [(-x + x_end + x_start, z) for (x, z) in self._xz]

            xz.sort()
            new_zprofile.xz = xz
            
            return new_zprofile
        
    def scale(self, Lx=1., Lz=1.):
        """
        scale the profile along X- and/or Z-axis

        arguments:
        - Lx: scale factor - int | float
        - Lz: scale factor - int | float

        returns:
        - new_zprofile: scaled profile - zProfile
        or
        - None - NoneType

        examples:
        >>> new_zprofile = zprofile.scale(Lz=2.)
        >>> new_zprofile = zprofile.scale(Lx=0.995, Lz=1.005)
        
        """
        new_zprofile = self.duplicate()
        new_zprofile.name = f"{self._name} scaled"
        
        if not (isinstance(Lx, (int, float)) and isinstance(Lz, (int, float))):
            return None
        else:
            new_zprofile.xz = [(x * Lx, z * Lz) for x, z in new_zprofile.xz]
            
            return new_zprofile
    
    def simplify(self, **kwargs):
        """
        simplify the profile geometry

        arguments:
        - method: "vw" | "rdp" - str
        - if method="vw":
            - ratio: percentage of points to keep - int | float
            or
            - number: number of points to keep - int
            or
            - threshold: threshold area to be respected - int | float
        - if method="rdp":
            - epsilon: threshold value - int | float
            and
            - algo: "iter" | "rec" - str

        returns:
        - xz, stats - simplified points, statistics - list, dict
        or
        - None, None - NoneType, NoneType

        examples:
        >>> xz, stats = zprofile.simplify(method="vw", ratio=0.5)
        >>> xz, stats = zprofile.simplify(method="rdp", epsilon=1., algo="iter")

        references:
        - VisvalingamWyatt algorithm: https://pypi.org/project/visvalingamwyatt/
        - Ramer-Douglas-Peucker algorithm: https://rdp.readthedocs.io/en/latest/
        
        """
        def f(xz):
            zprofile = zProfile()
            zprofile.xz = xz
            
            dz = []
            for x, z in self._xz:
                dz.append(abs(z - zprofile.interpolate(x)))
                
            n_input = len(self._xz)
            L_input = self.length(dim="3D")
            n_output = len(xz)
            L_output = zprofile.length(dim="3D")
            n_removed = n_input - n_output
            dL = L_input - L_output
            
            dz = np.array(dz)
            if len(dz[dz != 0]) > 0:                
                max_error = np.max(dz[dz != 0.])
                min_error = np.min(dz[dz != 0.])
                mean_error = np.mean(dz[dz != 0.])
                std_error = np.std(dz[dz != 0.])
            else:                   
                max_error = 0.
                min_error = 0.
                mean_error = 0.
                std_error = 0.
                   
            return {"input vertices": n_input,
                    "input 3D length": L_input,
                    "output vertices": n_output,
                    "output 3D length": L_output,
                    "removed vertices": n_removed,
                    "3D length delta": dL,
                    "max |dz|": max_error,
                    "min |dz|": min_error,
                    "mean |dz|": mean_error,
                    "std |dz|": std_error}
        
        if "method" not in kwargs.keys():
            return None, None
        elif kwargs["method"] not in ["vw", "rdp"]:
            return None, None
    
        if kwargs["method"] == "vw":
            xz = np.array([np.array(self.x), np.array(self.z)]).T
            simplifier = vw.Simplifier(xz)
            
            if "ratio" in kwargs.keys():
                if not isinstance(kwargs["ratio"], (int, float)):
                    return None, None
                elif not 0. < kwargs["ratio"] <= 1.:
                    return None, None
                else:
                    xzs = simplifier.simplify(ratio=kwargs['ratio'])
                        
                    x = list(xzs[:,0])
                    z = list(xzs[:,1])
                    
                    xz = [(float(x), float(z)) for x, z in zip(x, z)]
                    
                    if len(xz) == 0:
                        xz = [self._xz[0], self._xz[-1]]
                    
                    if xz[0][0] != self.x[0]:
                        xz.insert(0, self.xz[0])
                    
                    if xz[-1][0] != self.x[-1]:
                        xz.append(self.xz[-1])
                    
                    return xz, f(xz)
                
            elif "number" in kwargs.keys():
                if not isinstance(kwargs["number"], int):
                    return None, None
                elif not  1 < kwargs["number"] <= len(self.x):
                    return None, None
                else:
                    xzs = simplifier.simplify(number=kwargs["number"]-1)
                        
                    x = list(xzs[:,0])
                    z = list(xzs[:,1])
                    
                    xz = [(float(x), float(z)) for x, z in zip(x, z)]
                    
                    if len(xz) == 0:
                        xz = [self._xz[0], self._xz[-1]]
                    
                    if xz[0][0] != self.x[0]:
                        xz.insert(0, self.xz[0])
                    
                    if xz[-1][0] != self.x[-1]:
                        xz.append(self.xz[-1])
                    
                    return xz, f(xz)
                
            elif "threshold" in kwargs.keys():
                if not isinstance(kwargs["threshold"], (int, float)):
                    return None, None
                elif not 0 <= kwargs["threshold"]:
                    return None, None
                else:
                    xzs = simplifier.simplify(threshold=kwargs["threshold"])
                        
                    x = list(xzs[:,0])
                    z = list(xzs[:,1])
                    
                    xz = [(float(x), float(z)) for x, z in zip(x, z)]
                    
                    if len(xz) == 0:
                        xz = [self._xz[0], self._xz[-1]]
                    
                    if xz[0][0] != self.x[0]:
                        xz.insert(0, self._xz[0])
                    
                    if xz[-1][0] != self.x[-1]:
                        xz.append(self._xz[-1])
                        
                    return xz, f(xz)
            else:
                return None, None
        
        else:
            if not ("epsilon" in kwargs.keys() and "algo" in kwargs.keys()):
                return None, None
            elif not isinstance(kwargs["epsilon"], (int, float)):
                return None, None
            elif not 0 <= kwargs["epsilon"]:
                return None, None
            elif kwargs["algo"] not in ["iter", "rec"]:
                return None, None
            
            if kwargs["algo"] == "iter":
                xzs = rdp(self.xz, epsilon=kwargs["epsilon"], algo="iter")
                
                xz = [(float(x), float(z)) for x, z in xzs]
                
                if len(xz) == 0:
                    xz = [self._xz[0], self._xz[-1]]
                
                if xz[0][0] != self.x[0]:
                    xz.insert(0, self.xz[0])

                if xz[-1][0] != self.x[-1]:
                    xz.append(self.xz[-1])

                return xz, f(xz)
                
            else:
                xzs = rdp(self.xz, epsilon=kwargs["epsilon"], algo="rec")
                
                xz = [(float(x), float(z)) for x, z in xzs]
                
                if len(xz) == 0:
                    xz = [self._xz[0], self._xz[-1]]
                
                if xz[0][0] != self.x[0]:
                    xz.insert(0, self.xz[0])

                if xz[-1][0] != self.x[-1]:
                    xz.append(self.xz[-1])

                return xz, f(xz)
        
    def solve(self, z, x0):
        """
        try to find the distance x associated to the altitude z
        
        arguments:
        - z: altitude (m) - int | float
        - x0: initial distance guess (m) - int | float

        returns:
        - x: distance (m) - int | float
        or
        - None - NoneType

        examples:
        >>> zprofile.solve(1050, 525)

        """
        if not (isinstance(z, (int, float)) and isinstance(x0, (int, float))):
            return None
        elif not min(self.z) <= z <= max(self.z):
            return None
        elif not min(self.x) <= x0 <= max(self.x):
            return None
        else:
            f = interp1d(self.x, self.z, kind='cubic')
            F = lambda x: float(f(x) - z)
            
            try:
                return float(fsolve(F, x0))
            except:
                return None
        
    def translate(self, dx=0., dz=0.):
        """
        translate the profile along X- and/or Z-axis

        arguments:
        - dx: distance (m) - int | float
        - dz: distance (m) - int | float

        returns:
        - new_zprofile: translated profile - zProfile
        or
        - None - NoneType

        examples:
        >>> new_zprofile = zprofile.translate(dx=100.)
        >>> new_zprofile = zprofile.translate(dz=50.)
        >>> new_zprofile = zprofile.translate(dx=20., dz=-10.)
        
        """
        new_zprofile = self.duplicate()
        new_zprofile.name = f"{self._name} translated"
        
        if not (isinstance(dx, (int, float)) and isinstance(dz, (int, float))):
            return None
        else:
            new_zprofile.xz = [(x + dx, z + dz) for x, z in new_zprofile.xz]
            
            return new_zprofile
        
    def truncate(self, **kwargs):
        """
        truncate the profile

        arguments:
        - indexes = (i_start, i_end) - tuple
            - i_start: start index - int
            - i_end: end index - int
        or
        - distances = (x_start, x_end) - tuple
            - x_start: start distance - int | float
            - x_end: end distance - int | float

        returns:
        - new_zprofile: truncated profile - zProfile
        or
        - None - NoneType

        examples:
        >>> new_zprofile = zprofile.truncate(indexes=(10, 20))
        >>> new_zprofile = zprofile.truncate(distances=(50., 1000.))

        """
        new_zprofile = self.duplicate()
        new_zprofile.name = f"{self._name} truncated"

        if 'indexes' in kwargs.keys():
            if not isinstance(kwargs['indexes'], tuple):
                return None
            elif not 1 < len(kwargs['indexes']):
                return None
            else:
                indexes = kwargs['indexes']
            
            if not (isinstance(indexes[0], int) and isinstance(indexes[1], int)):
                return None
            else:
                i_start = indexes[0]
                i_end = indexes[1]
            
            if not 0 <= i_start < i_end < len(self._xz):
                return None
            else:
                new_zprofile.xz = self._xz[i_start:i_end+1]
                
                return new_zprofile                
                
        elif 'distances' in kwargs.keys():            
            if not isinstance(kwargs['distances'], tuple):
                return None
            elif not 1 < len(kwargs['distances']):
                return None
            else:
                distances = kwargs['distances']

            if not (isinstance(distances[0], (int, float)) and isinstance(distances[1], (int, float))):
                return
            else:
                x_start = distances[0]
                x_end = distances[1]

                if not self.x[0] <= x_start < x_end <= self.x[-1]:
                    return None
                else:
                    new_zprofile.add_point((x_start, new_zprofile.interpolate(x_start)))
                    new_zprofile.add_point((x_end, new_zprofile.interpolate(x_end)))

                    i_start = new_zprofile.x.index(x_start)
                    i_end = new_zprofile.x.index(x_end)

                    new_zprofile.xz = new_zprofile.xz[i_start:i_end+1]

                    return new_zprofile
        
        else:
            return None
                
    def update(self):
        """
        update line properties

        returns:
        - None - NoneType

        examples:
        >>> zprofile.update()
        
        """      
        x = self.x
        z = self.z

        self._line.set_data(x, z)

        if self._active and self._visible:
            self._line.set_label(self._label)
        else:
            self._line.set_label("")

        self._line.set_linestyle(line_styles[self._line_style])
        self._line.set_color(colors[self._line_color])
        self._line.set_linewidth(self._line_thickness)

        self._line.set_marker(marker_styles[self._marker_style])
        self._line.set_markeredgecolor(colors[self._marker_color])
        self._line.set_markerfacecolor(colors[self._marker_color])
        self._line.set_markersize(self._marker_size)

        self._line.set_alpha(self._opacity)
        self._line.set_zorder(self._order)
        self._line.set_visible(self._active and self._visible)

    def __add__(self, zprofile):
        """
        merge two profiles

        examples:
        >>> zprofile = zprofile_1 + zprofile_2

        returns:
        - zprofile: merged profile - zProfile
        or
        - None - NoneType
        """

        if not isinstance(zprofile, zProfile):
            return None
        else:
            new_zprofile = self.duplicate()
            new_zprofile.name = f"{self._name} merged"

            for (x, z) in zprofile.xz:
                new_zprofile.add_point((x, z))

            return new_zprofile

    def __sub__(self, zprofile):
        """
        substract two profiles

        examples:
        >>> differences = zprofile_1 - zprofile_2

        returns:
        - differences: signed differences - list
        or
        - None - NoneType
        
        """
        if not isinstance(zprofile, zProfile):
            return None
        else:
            results = []
            for x, z in self.xz:
                if zprofile.interpolate(x):
                    results.append((x, z - zprofile.interpolate(x)))

            for x, z in zprofile.xz:
                if x not in self.x:
                    if self.interpolate(x):
                        results.append((x, self.interpolate(x) - z))

            results.sort()
            return results

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_line"] = mpl_Line([], [])

        return attributes
        
    def __repr__(self):
        return f"{self._name}"
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def xz(self):
        return list(self._xz)

    @xz.setter
    def xz(self, xz):
        if not isinstance(xz, list):
            return
        elif not len(xz) > 1:
            return
        
        xz_new = []
        for item in xz:
            if not isinstance(item, tuple):
                return
            elif not len(item) > 1:
                return
            else:
                x, z = item[0], item[1]
            
            if not (isinstance(x, (int, float)) and isinstance(z, (int, float))):
                return
            elif x not in [x for x, z in xz_new]:
                xz_new.append((item[0], item[1]))
            
        xz_new.sort()
        if not len(xz_new) > 1:
            return
        else:
            self._xz = xz_new

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        if isinstance(active, bool):
            self._active = active

    @property
    def line_style(self):
        return self._line_style

    @line_style.setter
    def line_style(self, style):
        if style in line_styles.keys():
            self._line_style = style

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, color):
        if color in colors.keys():
            self._line_color = color

    @property
    def line_thickness(self):
        return self._line_thickness

    @line_thickness.setter
    def line_thickness(self, thickness):
        if isinstance(thickness, (int, float)):
            if 0 <= thickness:
                self._line_thickness = thickness

    @property
    def marker_style(self):
        return self._marker_style

    @marker_style.setter
    def marker_style(self, style):
        if style in marker_styles.keys():
            self._marker_style = style

    @property
    def marker_color(self):
        return self._marker_color

    @marker_color.setter
    def marker_color(self, color):
        if color in colors.keys():
            self._marker_color = color

    @property
    def marker_size(self):
        return self._marker_size

    @marker_size.setter
    def marker_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._marker_size = size 

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        if isinstance(opacity, (int, float)):
            if 0 <= opacity <= 1:
                self._opacity = opacity
    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        if isinstance(order, int):
            if 0 < order:
                self._order = order

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self._visible = visible

    @property
    def x(self):
        return [x for x, z in self._xz]
    
    @property
    def z_min(self):
        return min(self.z)
    
    @property
    def z_max(self):
        return max(self.z)

    @property
    def z(self):
        return [z for x, z in self._xz]
    
    @property
    def dz(self):
        dz = []
        for i in range(1, len(self._xz)):
            dz.append(self.z[i] - self.z[i-1])
        return dz
