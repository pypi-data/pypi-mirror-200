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
from pyLong.profiles.zprofile import zProfile


class yProfile:
    def __init__(self):
        self._name = "new yprofile"

        self._label = ""

        self._xy = [(0., 0.), (1000., 1000.)]

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
        - point: (x, y) - tuple
            - x: distance (m) - int | float
            - y: value - int | float

        returns:
        - True if success
        - False else

        examples:
        >>> yprofile.add_point((550., 0.5))

        """
        if not isinstance(point, tuple):
            return False
        elif not len(point) > 1:
            return False
        else:
            x, y = point[0], point[1]
            if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                return False
            elif x in self.x:
                return False
            else:
                self._xy.append((x, y))
                self._xy.sort()
                return True

    def area(self, kind="below"):
        """
        calculate the area below or above the profile

        arguments:
        - kind: "below" | "above" - str

        returns:
        - area: area - float
        or
        - None - NoneType

        examples:
        >>> area = yprofile.area()
        >>> area = yprofile.area(kind="above")
        
        """
        if not isinstance(kind, str):
            return None
        elif kind not in ["above", "below"]:
            return None
        else:
            x = self.x
            y = [y - self.y_min for y in self.y]

            if kind == "below":
                return float(np.trapz(y, x))
            else:
                return (self.length() * (max(y) - min(y))) - float(np.trapz(y, x)) 
                        
    def clear(self):
        """
        clear line

        returns:
        - None - NoneType

        examples:
        >>> yprofile.clear()
        
        """
        self._line = mpl_Line([], [])
        
    def copy_style(self, profile):
        """
        copy the style of a profile

        arguments:
        - profile: profile whose style is to be copied - yProfile | zProfile

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_yprofile.copy_style(profile)
        
        """
        if isinstance(profile, (yProfile, zProfile)):
            self._line_style = profile.line_style
            self._line_color = profile.line_color
            self._line_thickness = profile.line_thickness
            self._marker_style = profile.marker_style
            self._marker_color = profile.marker_color
            self._marker_size = profile.marker_size
            self._opacity = profile.opacity
            self._order = profile.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the profile

        returns:
        - new_yprofile: duplicated profile - yProfile

        examples:
        >>> new_yprofile = yprofile.duplicate()

        """
        new_yprofile = yProfile()
        new_yprofile.copy_style(self)
        
        new_yprofile.name = f"{self._name} duplicated"
        new_yprofile.label = self._label
        
        new_yprofile.xy = list(self._xy)
        
        return new_yprofile
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3, reverse=False, header=["X","Y"]):
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
        >>> yprofile.export("profile.txt")
        >>> yprofile.export("profile.txt", delimiter=";", separator=".", decimals=2)
        
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
            xy = sorted(self._xy, reverse=reverse)
            x = [x for x, y in xy]
            y = [y for x, y in xy]

            x = np.array(x)
            y = np.array(y)
            
            xy = np.array([x, y]).T
            xy = pd.DataFrame(xy) 
            
            try:
                xy.to_csv(filename,
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
        >>> yprofile.export_style("style.json")
        
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
            
    def from_dbf(self, filename, x_field="dist", y_field="Y"):
        """
        import points from a .dbf file

        arguments:
        - filename: .dbf file path - str
        - x_field: distance field name - str
        - y_field: y field name - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> yprofile.from_dbf("profile.dbf")
        >>> yprofile.from_dbf("profile.dbf", x_field="X", y_field="width")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        elif not os.path.isfile(filename):
            return False
        elif not (isinstance(x_field, str) and isinstance(y_field, str)):
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
        elif not (x_field in list(data.columns) and y_field in list(data.columns)):
            return False
        elif not (data.loc[:, x_field].dtype in ['float64', 'int64'] and \
                  data.loc[:, y_field].dtype in ['float64', 'int64']):
            return False
        
        i = list(data.columns).index(x_field)
        x = list(data.values[:, i])
        
        i = list(data.columns).index(y_field)
        y = list(data.values[:, i])
        
        xy = [(float(x), float(y)) for x, y in zip(x, y)]
        
        xy.sort()
        x = [x for x, y in xy]
        dx = np.array(x[1:]) - np.array(x[:-1])
        dx = list(dx)
        
        if 0 in dx:
            return False
        else:
            self._xy = xy
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
        >>> yprofile.from_shp("profile.shp")
        
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

        if shape.shapeType != 23:
            return False
        
        dist = [0]
        for i, (x, y) in enumerate(shape.points):
            if i != 0:
                d = ((x - shape.points[i-1][0])**2 + (y - shape.points[i-1][1])**2)**0.5
                dist.append(d + dist[i-1])
                
        xy = [(float(x), float(y)) for x, y in zip(dist, shape.m)]
        
        xy.sort()
        x = [x for x, y in xy]
        dx = np.array(x[1:]) - np.array(x[:-1])
        dx = list(dx)
        
        if 0 in dx:
            return False
        else:
            self._xy = xy
            return True  

    def from_txt(self, filename, x_field="X", y_field="Y", delimiter="\t", decimal="."):
        """
        import points from a .txt file

        arguments:
        - filename: .txt file path - str
        - x_field: distance field name - str
        - y_field: value field name - str
        - delimiter: column delimiter "\\t" | " " | ";" | "," - str
        - decimal: decimal separator "." |"," - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> yprofile.from_txt("profile.txt")
        >>> yprofile.from_txt("profile.txt", x_field="dist", y_field="width", delimiter=";", decimal=",")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        elif not os.path.isfile(filename):
            return False
        elif not (isinstance(x_field, str) and isinstance(y_field, str)):
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
        elif not (x_field in list(data.columns) and y_field in list(data.columns)):
            return False
        elif not (data.loc[:, x_field].dtype in ['float64', 'int64'] and \
                  data.loc[:, y_field].dtype in ['float64', 'int64']):
            return False
        
        i = list(data.columns).index(x_field)
        x = list(data.values[:, i])
        
        i = list(data.columns).index(y_field)
        y = list(data.values[:, i])
        
        xy = [(x, y) for x, y in zip(x, y)]
        
        xy.sort()
        x = [x for x, y in xy]
        dx = np.array(x[1:]) - np.array(x[:-1])
        dx = list(dx)
        
        if 0 in dx:
            return False
        else:
            self._xy = xy
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
        >>> yprofile.import_style("style.json")
        
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
        - y: interpolated value - float
        or
        - None - NoneType

        examples:
        >>> y = yprofile.interpolate(x=150.)
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
                return float(self.y[0])
            elif x == Xs[-1]:
                return float(self.y[-1])
            else:
                f = interp1d(self.x[i-1:i+1], self.y[i-1:i+1], kind='linear')
                return float(f(x))

    def intersect(self, yprofile):
        """
        calculate the intersections with another profile

        arguments:
        - yprofile: profile - yProfile

        returns:
        - intersections: intersections - list
        or
        - None - NoneType

        examples:
        >>> intersections = yprofile.intersect(new_yprofile)
        
        """
        if not isinstance(yprofile, yProfile):
            return None
        else:
            try:
                xs, ys = intersection(self.x, self.y, yprofile.x, yprofile.y)
            except:
                return None
            
            xy = [(float(x), float(y)) for x, y in zip(xs, ys)]
            return xy
            
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
        >>> length_2d = yprofile.length()
        >>> length_3d = yprofile.length(dim="3D")
        
        """
        if not isinstance(dim, str):
            return
        elif dim.upper() not in ['2D', '3D']:
            return
        elif dim.upper() == '2D':
            return float(self._xy[-1][0] - self._xy[0][0])
        else:
            dist = 0
            for i in range(1, len(self._xy)):
                dist += ((self.x[i] - self.x[i-1])**2 + (self.y[i] - self.y[i-1])**2)**0.5
            return float(dist)
                
    def listing(self, decimals=3, value_decimals=3, value_unit="m"):
        """
        print the list of points

        arguments:
        - decimals: number of decimals to print (distance) - int
        - value_decimals: number of decimals to print (value) - int
        - value_unit: unit to display (value) - str

        returns:
        - None - NoneType

        examples:
        >>> yprofile.listing()
        >>> yprofile.listing(decimals=2, value_decimals=2, value_unit="m/s")
        
        """
        if not (isinstance(decimals, int) and isinstance(value_decimals, int)):
            return None
        else:
            for i, (x, y) in enumerate(self._xy):
                print(f"point {i}: x = {round(float(x), decimals)} m ; y = {round(float(y), value_decimals)} {value_unit}") 
            
    def new_point(self, i, method, **kwargs):
        """
        calculate a new point

        arguments:
        - i: index of the reference point from which the new one will be determined - int
        - method: "dX + dY" | "slope + X" | "slope + dX" | "slope + Y" | "slope + dY" - str
        - X: distance (m) - int | float
        - Y: value - int | float
        - dX: signed distance variation (m) - int | float
        - dY: signed value variation - int | float
        - slope: signed slope in the counterclockwise direction - int | float
        - slope_unit: slope unit "radian" | "degree" | "percent" - str

        returns:
        - x, y: distance, value of the new point - int | float, int | float
        or
        - None, None - NoneType, NoneType

        examples:
        >>> x, y = yprofile.new_point(i=2, method="dX + dY", dX=5, dY=10)
        >>> x, y = yprofile.new_point(i=1, method="slope + X", X=150, slope=45, slope_unit="degree")
        >>> x, y = yprofile.new_point(i=1, method="slope + dY", dY=10, slope=100, slope_unit="percent")
        
        """
        if not (isinstance(i, int) and isinstance(method, str)):
            return None, None
        elif not 0 <= i < len(self._xy):
            return None, None
        elif method not in ["dX + dY", "slope + X", "slope + dX", "slope + Y", "slope + dY"]:
            return None, None
        
        if method == "dX + dY":
            if not ("dX" in kwargs.keys() and "dY" in kwargs.keys()):
                return None, None
            elif not (isinstance(kwargs["dX"], (int, float)) and isinstance(kwargs["dY"], (int, float))):
                return None, None
            else:
                dX = kwargs["dX"]
                dY = kwargs["dY"]
                
                return self.x[i] + dX, self.y[i] + dY
        
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
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.y[i]
                
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
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.y[i]
                
                return self.x[i] + dX, f(self.x[i] + dX)
        
        elif method == "slope + Y":
            if not ("slope" in kwargs.keys() and "Y" in kwargs.keys() and "slope_unit" in kwargs.keys()):
                return None, None
            elif kwargs["slope_unit"] not in ["radian", "degree", "percent"]:
                return None, None
            elif not (isinstance(kwargs["slope"], (int, float)) and isinstance(kwargs["Y"], (int, float))):
                return None, None
            else:
                slope = kwargs["slope"]
                Y = kwargs["Y"]
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
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.y[i]
                
                return self.x[i] + (Y - self.y[i]) / tan(angle), Y
        
        elif method == "slope + dY":
            if not ("slope" in kwargs.keys() and "dY" in kwargs.keys() and "slope_unit" in kwargs.keys()):
                return None, None
            elif kwargs["slope_unit"] not in ["radian", "degree", "percent"]:
                return None, None
            elif not (isinstance(kwargs["slope"], (int, float)) and isinstance(kwargs["dY"], (int, float))):
                return None, None
            else:
                slope = kwargs["slope"]
                dY = kwargs["dY"]
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
                        angle = radians(slope / 100)
                else:
                    angle = atan(slope)
                    
                f = lambda x: tan(angle) * (x - self.x[i]) + self.y[i]
                
                return self.x[i] + dY / tan(angle), self.y[i] + dY

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
        >>> yprofile.plot(ax)
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
        >>> yprofile.remove_point(1)

        """
        if len(self._xy) == 2:
            return False
        elif not isinstance(i, int):
            return False
        elif not 0 <= i < len(self._xy):
            return False
        else:
            self._xy.pop(i)
            return True
                
    def resample(self, d):
        """
        resample the profile

        arguments:
        - d: distance (m) - int | float

        returns:
        - new_yprofile: resampled profile - yProfile
        or
        - None - NoneType

        examples:
        >>> new_yprofile = yprofile.resample(d=10.)
        
        """
        if not isinstance(d, (int, float)):
            return None
        elif d <= 0:
            return None
        else:
            x = self.x
            y = self.y
            
            new_yprofile = self.duplicate()
            new_yprofile.name = f"{self._name} resampled"
            
            for i in range(1, len(x)):
                l = sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2)
                if l / d > 1:
                    n = ceil(l / d)
                    
                    for value in np.linspace(x[i-1], x[i], n+1):
                        value = float(value)
                        new_yprofile.add_point((value, self.interpolate(value)))
                        
            return new_yprofile

    def reverse(self, profile):
        """
        reverse the profile according to a reference profile

        arguments:
        - profile: reference profile to perform the reversing - zProfile | yProfile

        returns:
        - new_yprofile: reversed profile - yProfile
        or
        - None - NoneType

        examples:
        >>> new_yprofile = yprofile.reverse(profile)

        """
        if not isinstance(profile, (zProfile, yProfile)):
            return None
        else:
            new_yprofile = self.duplicate()
            new_yprofile.name = f"{self._name} reversed"
            
            x_start = profile.x[0]
            x_end = profile.x[-1]

            xy = [(-x + x_end + x_start, y) for (x, y) in self._xy]

            xy.sort()
            new_yprofile.xy = xy
            
            return new_yprofile
        
    def scale(self, Lx=1., Ly=1.):
        """
        scale the profile along X- and/or Y-axis

        arguments:
        - Lx: scale factor - int | float
        - Ly: scale factor - int | float

        returns:
        - new_yprofile: scaled profile - yProfile

        examples:
        >>> new_yprofile = yprofile.scale(Ly=2.)
        >>> new_yprofile = yprofile.scale(Lx=0.995, Ly=1.005)
        
        """
        new_yprofile = self.duplicate()
        new_yprofile.name = f"{self._name} scaled"
        
        if not (isinstance(Lx, (int, float)) and isinstance(Ly, (int, float))):
            return
        else:
            new_yprofile.xy = [(x * Lx, y * Ly) for x, y in new_yprofile.xy]
            
            return new_yprofile
    
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
        - xy, stats - simplified points, statistics - list, dict
        or
        - None, None - NoneType, NoneType

        examples:
        >>> xy, stats = profile.simplify(method="vw", ratio=0.5)
        >>> xy, stats = profile.simplify(method="rdp", epsilon=1., algo="iter")

        references:
        - VisvalingamWyatt algorithm: https://pypi.org/project/visvalingamwyatt/
        - Ramer-Douglas-Peucker algorithm: https://rdp.readthedocs.io/en/latest/
        
        """
        def f(xy):
            yprofile = yProfile()
            yprofile.xy = xy
            
            dy = []
            for x, y in self._xy:
                dy.append(abs(y - yprofile.interpolate(x)))
                
            n_input = len(self._xy)
            L_input = self.length(dim="3D")
            n_output = len(xy)
            L_output = yprofile.length(dim="3D")
            n_removed = n_input - n_output
            dL = L_input - L_output
            
            dy = np.array(dy)
            if len(dy[dy != 0]) > 0:                
                max_error = np.max(dy[dy != 0.])
                min_error = np.min(dy[dy != 0.])
                mean_error = np.mean(dy[dy != 0.])
                std_error = np.std(dy[dy != 0.])
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
                    "max |dy|": max_error,
                    "min |dy|": min_error,
                    "mean |dy|": mean_error,
                    "std |dy|": std_error}
        
        if "method" not in kwargs.keys():
            return None, None
        elif kwargs["method"] not in ["vw", "rdp"]:
            return None, None
    
        if kwargs["method"] == "vw":
            xy = np.array([np.array(self.x), np.array(self.y)]).T
            simplifier = vw.Simplifier(xy)
            
            if "ratio" in kwargs.keys():
                if not isinstance(kwargs["ratio"], (int, float)):
                    return None, None
                elif not 0. < kwargs["ratio"] <= 1.:
                    return None, None
                else:
                    xys = simplifier.simplify(ratio=kwargs['ratio'])
                        
                    x = list(xys[:,0])
                    y = list(xys[:,1])
                    
                    xy = [(x, y) for x, y in zip(x, y)]
                    
                    if len(xy) == 0:
                        xy = [self._xy[0], self._xy[-1]]
                    
                    if xy[0][0] != self.x[0]:
                        xy.insert(0, self.xy[0])
                    
                    if xy[-1][0] != self.x[-1]:
                        xy.append(self.xy[-1])
                    
                    return xy, f(xy)
                
            elif "number" in kwargs.keys():
                if not isinstance(kwargs["number"], int):
                    return None, None
                elif not  1 < kwargs["number"] <= len(self.x):
                    return None, None
                else:
                    xys = simplifier.simplify(number=kwargs["number"]-1)
                        
                    x = list(xys[:,0])
                    y = list(xys[:,1])
                    
                    xy = [(x, y) for x, y in zip(x, y)]
                    
                    if len(xy) == 0:
                        xy = [self._xy[0], self._xy[-1]]
                    
                    if xy[0][0] != self.x[0]:
                        xy.insert(0, self.xy[0])
                    
                    if xy[-1][0] != self.x[-1]:
                        xy.append(self.xy[-1])
                    
                    return xy, f(xy)
                
            elif "threshold" in kwargs.keys():
                if not isinstance(kwargs["threshold"], (int, float)):
                    return None, None
                elif not 0 <= kwargs["threshold"]:
                    return None, None
                else:
                    xys = simplifier.simplify(threshold=kwargs["threshold"])
                        
                    x = list(xys[:,0])
                    y = list(xys[:,1])
                    
                    xy = [(x, y) for x, y in zip(x, y)]
                    
                    if len(xy) == 0:
                        xy = [self._xy[0], self._xy[-1]]
                    
                    if xy[0][0] != self.x[0]:
                        xy.insert(0, self._xy[0])
                    
                    if xy[-1][0] != self.x[-1]:
                        xy.append(self._xy[-1])
                        
                    return xy, f(xy)
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
                xys = rdp(self.xy, epsilon=kwargs["epsilon"], algo="iter")
                
                xy = [(x, y) for x, y in xys]
                
                if len(xy) == 0:
                    xy = [self._xy[0], self._xy[-1]]
                
                if xy[0][0] != self.x[0]:
                    xy.insert(0, self.xy[0])

                if xy[-1][0] != self.x[-1]:
                    xy.append(self.xy[-1])

                return xy, f(xy)
                
            else:
                xys = rdp(self.xy, epsilon=kwargs["epsilon"], algo="rec")
                
                xy = [(x, y) for x, y in xys]
                
                if len(xy) == 0:
                    xy = [self._xy[0], self._xy[-1]]
                
                if xy[0][0] != self.x[0]:
                    xy.insert(0, self.xy[0])

                if xy[-1][0] != self.x[-1]:
                    xy.append(self.xy[-1])

                return xy, f(xy)
        
    def solve(self, y, x0):
        """
        try to find the distance x associated to the value y
        
        arguments:
        - y: value - int | float
        - x0: initial distance guess (m) - int | float

        returns:
        - x: distance (m) - int | float
        or
        - None - NoneType

        examples:
        >>> yprofile.solve(1050, 0.5)

        """
        if not (isinstance(y (int, float)) and isinstance(x0, (int, float))):
            return None
        elif not min(self.y) <= y <= max(self.y):
            return None
        elif not min(self.x) <= x0 <= max(self.x):
            return None
        else:
            f = interp1d(self.x, self.y, kind='cubic')
            F = lambda x: float(f(x) - y)
            
            try:
                return float(fsolve(F, x0))
            except:
                return
        
    def translate(self, dx=0., dy=0.):
        """
        translate the profile along X- and/or Y-axis

        arguments:
        - dx: distance (m) - int | float
        - dy: value - int | float

        returns:
        - new_yprofile: translated profile - yProfile

        examples:
        >>> yprofile.translate(dx=100.)
        >>> yprofile.translate(dy=50.)
        >>> yprofile.translate(dx=20., dy=-10.)
        
        """
        new_yprofile = self.duplicate()
        new_yprofile.name = f"{self._name} translated"
        
        if not (isinstance(dx, (int, float)) and isinstance(dy, (int, float))):
            return
        else:
            new_yprofile.xy = [(x + dx, y + dy) for x, y in new_yprofile.xy]
            
            return new_yprofile
        
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
        - new_yprofile: truncated profile - yProfile
        or
        - None - NoneType

        examples:
        >>> new_yprofile = yprofile.truncate(indexes=(10, 20))
        >>> new_yprofile = yprofile.truncate(distances=(50., 1000.))

        """
        new_yprofile = self.duplicate()
        new_yprofile.name = f"{self._name} truncated"

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
            
            if not 0 <= i_start < i_end < len(self._xy):
                return None
            else:
                new_yprofile.xy = self._xy[i_start:i_end+1]
                
                return new_yprofile
                
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
                    new_yprofile.add_point((x_start, new_yprofile.interpolate(x_start)))
                    new_yprofile.add_point((x_end, new_yprofile.interpolate(x_end)))

                    i_start = new_yprofile.x.index(x_start)
                    i_end = new_yprofile.x.index(x_end)

                    new_yprofile.xy = new_yprofile.xy[i_start:i_end+1]

                    return new_yprofile
        
        else:
            return None
                
    def update(self):
        """
        update line properties

        returns:
        - None - NoneType

        examples:
        >>> yprofile.update()
        
        """      
        x = self.x
        y = self.y

        self._line.set_data(x, y)

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
        self._line.set_visible(self._visible and self._active)

    def __add__(self, yprofile):
        """
        merge two profiles

        examples:
        >>> yprofile = yprofile_1 + yprofile_2

        returns:
        - yprofile: merged profile - yProfile
        or
        - None - NoneType
        """

        if not isinstance(yprofile, yProfile):
            return None
        else:
            new_yprofile = self.duplicate()
            new_yprofile.name = f"{self._name} merged"

            for (x, y) in yprofile.xy:
                new_yprofile.add_point((x, y))

            return new_yprofile

    def __sub__(self, yprofile):
        """
        substract two profiles

        examples:
        >>> differences = yprofile_1 - yprofile_2

        returns:
        - differences: signed differences - list
        or
        - None - NoneType
        
        """
        if not isinstance(yprofile, yProfile):
            return None
        else:
            results = []
            for x, y in self.xy:
                if yprofile.interpolate(x):
                    results.append((x, y - yprofile.interpolate(x)))

            for x, y in yprofile.xy:
                if x not in self.x:
                    if self.interpolate(x):
                        results.append(x, self.interpolate(x) - y)

            results.sort()
            return results

    def __repr__(self):
        return f"{self._name}"

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_line"] = mpl_Line([], [])

        return attributes

    @property
    def xy(self):
        return list(self._xy)

    @xy.setter
    def xy(self, xy):
        if not isinstance(xy, list):
            return
        elif not len(xy) > 1:
            return
        
        xy_new = []
        for item in xy:
            if not isinstance(item, tuple):
                return
            elif not len(item) > 1:
                return
            else:
                x, y = item[0], item[1]
            
            if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                return
            elif x not in [x for x, y in xy_new]:
                xy_new.append((item[0], item[1]))
            
        xy_new.sort()
        if not len(xy_new) > 1:
            return
        else:
            self._xy = xy_new

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
        return [x for x, y in self._xy]
    
    @property
    def y_min(self):
        return min(self.y)
    
    @property
    def y_max(self):
        return max(self.y)

    @property
    def y(self):
        return [y for x, y in self._xy]
