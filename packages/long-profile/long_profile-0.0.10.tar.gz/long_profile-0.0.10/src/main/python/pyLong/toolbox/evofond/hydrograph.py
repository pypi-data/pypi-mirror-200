import numpy as np
from matplotlib.lines import Line2D
from matplotlib.axes import Subplot
import pandas as pd
from scipy.interpolate import interp1d

from pyLong.dictionnaries.styles import line_styles, marker_styles
from pyLong.dictionnaries.colors import colors
from pyLong.misc.duration import hms_to_s


class Hydrograph:
    def __init__(self):
        
        self._name = "new hydrograph"
        
        self._label = ""
        
        self._data = [(0., 1.), (3600., 1.)]
        
        self._line = Line2D([], [])

        self._line_style = "solid"

        self._line_color = "Black"
        
        self._line_thickness = 1.

        self._marker_style = "none"
        
        self._marker_color = "Black"
        
        self._marker_size = 1.

        self._opacity = 1.
        
        self._order = 1

        self._visible = True
        
    """
    Methods:
    - area
    - clear
    - copy_style
    - duplicate
    - export
    - export_style
    - from_lavabre
    - from_txt
    - import_style
    - interpolate
    - plot
    - resample
    - update
    """
    
    def area(self):
        """
        calculate the area below the hydrograph

        returns:
        - area: area (m3) - float
        or
        - None - NoneType

        examples:
        >>> area = hydrograph.area()
        
        """
        t = self.times
        q = self.discharges

        return float(np.trapz(q, t))
        
    def clear(self):
        """
        clear line

        returns:
        - None - NoneType

        examples:
        >>> hydrograph.clear()
        
        """
        self._line = Line2D([], [])
        
    def copy_style(self, hydrograph):
        """
        copy the style of a hydrograph

        arguments:
        - hydrograph: hydrograph whose style is to be copied - Hydrograph

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_hydrograph.copy_style(hydrograph)
        
        """
        if isinstance(hydrograph, Hydrograph):
            self._line_style = hydrograph.line_style
            self._line_color = hydrograph.line_color
            self._line_thickness = hydrograph.line_thickness
            self._marker_style = hydrograph.marker_style
            self._marker_color = hydrograph.marker_color
            self._marker_size = hydrograph.marker_size
            self._opacity = hydrograph.opacity
            self._order = hydrograph.order
            return True
        else:
            return False
        
    def duplicate(self):
        """
        duplicate the hydrograph

        returns:
        - new_hydrograph: duplicated hydrograph - Hydrograph

        examples:
        >>> new_hydrograph = hydrograph.duplicate()

        """
        new_hydrograph = Hydrograph()
        new_hydrograph.copy_style(self)
        
        new_hydrograph.name = f"{self._name} duplicated"
        new_hydrograph.label = self._label
        
        new_hydrograph.data = list(self._data)
        
        return new_hydrograph
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3):
        """
        export hydrograph data

        arguments:
        - filename: file path - str
        - delimiter: columns delimiter "\\t" | " " | ";" | "," - str
        - separator: decimal separator "." | ";" - str
        - decimals: number of decimals to export - int

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> hydrograph.export("hydrograph.txt")
        >>> hydrograph.export("hydrograph.txt", delimiter=";", separator=".", decimals=2)
        
        """
        if not (isinstance(filename, str) and isinstance(decimals, int)):
            return False
        elif delimiter not in ["\t", " ", ";", ","] or separator not in [".", ","]:
            return False
        elif delimiter == separator:
            return False
        elif not len(filename) > 0:
            return False
        else:
            t = np.array(self.times)
            q = np.array(self.discharges)
            
            data = np.array([t, q]).T
            data = pd.DataFrame(data) 
            
            try:
                data.to_csv(filename,
                           sep = delimiter,
                           float_format = f"%.{decimals}f",
                           decimal = separator,
                           index = False,
                           header = ['time','discharge'])
                return True
            except:
                return False
            
    def export_style(self, filename):
        """
        export hydrograph style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> hydrograph.export_style("style.json")
        
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
        
    def from_lavabre(self, duration, discharge_max, discharge_min, peak, order, dt=(0., 0., 1.)):
        """
        calculate a hydrograph from Lavabre formula
        
        arguments:
        - duration: duration (h, m, s) - tuple
            - h: hours - int | float
            - m: minutes - int | float
            - s: seconds - int | float
        - discharge_max: maximum discharge (m3/s) - int | float
        - discharge_min: minimum discharge (m3/s) - int | float
        - peak: flood peak time (h, m, s) - tuple
            - h: hours - int | float
            - m: minutes - int | float
            - s: seconds - int | float
        - order: polynomial order of Lavabre formula - int
        - dt: time step (h, m, s) - tuple
            - h: hours - int | float
            - m: minutes - int | float
            - s: seconds - int | float
        
        examples:
        >>> hydrograph.from_lavabre((12., 0., 0.), 10., 2., (3., 30., 0.), 2)
        >>> hydrograph.from_lavabre((6., 30., 0.), 20., 5., (1., 0., 0.), 2, (0., 0., 30.))
        
        """
        duration = hms_to_s(duration)
        peak = hms_to_s(peak)
        dt = hms_to_s(dt)
        
        if not (duration and peak and dt):
            return False
        elif not dt < peak < duration:
            return False
        elif not (isinstance(discharge_max, (int, float)) and isinstance(discharge_min, (int, float)) and isinstance(order, int)):
            return False
        elif not 0 <= discharge_min <= discharge_max:
            return False
        elif not 0 <= order:
            return False
        
        times = np.arange(0, duration, dt)
        if duration not in times:
            times = np.append(times, duration)
            
        discharges = (times / peak)**order
        discharges *= 2
        discharges /= 1 + (times / peak)**(2*order)
        discharges *= discharge_max - discharge_min
        discharges += discharge_min
        
        data = [(t, q) for t, q in zip(times, discharges)]
        
        self._data = data
        return True
        
    def from_txt(self, filename, time_field="t", discharge_field="Q", delimiter="\t", decimal="."):
        """
        import data from a .txt file
        
        arguments:
        - filename: .txt file path - str
        - time_field: time field name - str
        - discharge_field: discharge field name - str
        - delimiter: column delimiter "\\t" | " " | ";" | "," - str
        - decimal: decimal separator "." |"," - str
        
        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> hydrograph.from_txt("hydrograph.txt")
        >>> hydrograph.from_txt("hydrograph.txt", time_field="time", discharge_field="discharge", delimiter=";", decimal=",")
        
        """
        if not (isinstance(filename, str) and isinstance(time_field, str) and isinstance(discharge_field, str)):
            return False
        elif not (delimiter in [' ', '\t', ';', ','] and decimal in ['.', ',']):
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
        
        if data.shape[0] < 2 or data.shape[1] < 2:
            return False
        elif not (time_field in list(data.columns) and discharge_field in list(data.columns)):
            return False
        elif not (data.loc[:, time_field].dtype in ['float64', 'int64'] and \
                  data.loc[:, discharge_field].dtype in ['float64', 'int64']):
            return False
        
        data = data.dropna()
        
        i = list(data.columns).index(time_field)
        times = list(data.values[:, i])
        
        i = list(data.columns).index(discharge_field)
        discharges = list(data.values[:, i])
        
        data = [(t, q) for t, q in zip(times, discharges)]
        
        data.sort()
        t = np.array([t for t, q in data])
        q = np.array([q for t, q in data])
        
        dt = t[1:] - t[:-1]
        dq = q[1:] - q[:-1] 
        
        if 0 in dt or 0 in dq:
            return False
        elif np.min(t) < 0 or np.min(q) < 0:
            return False
        else:
            self._data = data
            return True
                  
    def import_style(self, filename):
        """
        import hydrograph style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> hydrograph.import_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
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
    
    def interpolate(self, t):
        """
        interpolate the hydrograph

        arguments:
        - t: time (h, m, s) - tupe
            - h: hours - int | float
            - m: minutes - int | float
            - s: seconds - int | float

        returns:
        - q: interpolated discharge (m3/s) - float
        or
        - None - NoneType

        examples:
        >>> q = hydrograph.interpolate(t=(1., 25., 15.))
        
        """
        t = hms_to_s(t)
        
        if not t:
            return None
        elif not min(self.times) <= t <= max(self.times):
            return None
            
        times = self.times
        times.append(t)
        times.sort()
        i = times.index(t)
        
        if t == times[0]:
            return float(self.discharges[0])
        elif t == times[-1]:
            return float(self.discharges[-1])
        else:
            f = interp1d(self.times[i-1:i+1], self.discharges[i-1:i+1], kind='linear')
            return float(f(t))
                  
    def plot(self, ax):
        """
        plot hydrograph on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> hydrograph.plot(ax)
        >>> plt.show()
        """
        if isinstance(ax, Subplot):
            self.clear()
            self.update()

            ax.add_line(self._line)
                  
    def resample(self, dt):
        """
        resample the hydrograph

        arguments:
        - dt: duration (h, m, s) - tuple
            - h: hours - int | float
            - m: minutes - int | float
            - s: seconds - int | float

        returns:
        - new_hydrograph: resampled hydrograph - Hydrograph
        or
        - None - NoneType

        examples:
        >>> new_hydrograph = hydrograph.resample(dt=(0., 1., 0.))
        
        """
        dt = hms_to_s(dt)
                  
        if not dt:
            return None
        else:
            times = self.times
            
            new_hydrograph = Hydrograph()
            new_hydrograph.data = list(self._data)
            
            for i in range(1, len(times)):
                if (times[i] - times[i-1]) / dt > 1:
                    n = ceil((times[i] - times[i-1]) / dt)
                    
                    for value in np.linspace(times[i-1], times[i], n+1):
                        value = float(value)
                        new_hydrograph.add_point((value, self.interpolate(value)))
                        
            return new_hydrograph
                  
    def update(self):
        """
        update line properties

        returns:
        - None - NoneType

        examples:
        >>> hydrograph.update()
        
        """      
        t = self.times
        q = self.discharges

        self._line.set_data(t, q)

        if self.visible:
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
        self._line.set_visible(self._visible)
        
    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_line"] = Line2D([], [])

        return attributes
    
    def __repr__(self):
        return self._name
        
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
    def data(self):
        return list(self._data)
    
    @data.setter
    def data(self, data):
        if not isinstance(data, list):
            return
        elif not len(data) > 1:
            return
        
        for item in data:
            if not isinstance(item, tuple):
                return
            elif not len(item) > 1:
                return
            else:
                t, q = item[0], item[1]
            
            if not (isinstance(t, (int, float)) and isinstance(q, (int, float))):
                return
            
        data.sort()
        t = np.array([t for t, q in data])
        q = np.array([q for t, q in data])

        dt = t[1:] - t[:-1]
        dq = q[1:] - q[:-1] 

        if 0 in dt or 0 in dq:
            return False
        elif np.min(t) < 0 or len(q[q<0]) > 0:
            return False
        else:
            self._data = [(item[0], item[1]) for item in data]
        
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
            if 0 <= thickness <= 100:
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
            if 0 <= size <= 100:
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
            if 0 < order <= 100:
                self._order = order

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self._visible = visible
        
    @property
    def times(self):
        return [t for t, q in self._data]
        
    @property
    def discharges(self):
        return [q for t, q in self._data]
