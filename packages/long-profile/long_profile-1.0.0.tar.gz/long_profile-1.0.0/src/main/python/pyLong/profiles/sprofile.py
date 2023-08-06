import json
import os

from matplotlib.axes import Subplot
from matplotlib.lines import Line2D as mpl_Line
import numpy as np

from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import marker_styles
from pyLong.profiles.zprofile import zProfile


class sProfile:
    def __init__(self):
        self._name = "new slope profile"

        self._label = ""

        self._zprofile = zProfile()

        self._xzs = []

        self._change_sign = False

        self._line = mpl_Line([], [])
        
        self._line_percent = mpl_Line([], [])
        
        self._line_degree = mpl_Line([], [])
        
        self._trick_line = mpl_Line([], [])

        self._marker_style = "cross"

        self._marker_color = "Black"
        
        self._marker_size = 1.
        
        self._value_color = "Black"
        
        self._value_size = 11.

        self._value_shift = 0.
        
        self._value_shift_percent = 0.
        
        self._value_shift_degree = 0.

        self._opacity = 1.
        
        self._order = 1

        self._marker_visible = False
        
        self._value_visible = False

        self._active = True
        
    """
    Methods:
    - clear
    - copy_style
    - duplicate
    - export_style
    - import_style
    - listing
    - mean
    - plot
    - slopes
    - update
    - update_xzs
    """

    def clear(self):
        """
        clear lines

        returns:
        - None - NoneType

        examples:
        >>> sprofile.clear()
        
        """
        self._line = mpl_Line([], [])
        self._line_percent = mpl_Line([], [])
        self._line_degree = mpl_Line([], [])
        self._trick_line = mpl_Line([], [])
        
    def copy_style(self, sprofile):
        """
        copy the style of a slope profile

        arguments:
        - sprofile: slope profile whose style is to be copied - sProfile

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_sprofile.copy_style(sprofile)
        
        """
        if isinstance(sprofile, sProfile):
            self._marker_style = sprofile.marker_style
            self._marker_color = sprofile.marker_color
            self._marker_size = sprofile.marker_size
            self._value_color = sprofile.value_color
            self._value_size = sprofile.value_size
            self._value_shift = sprofile.value_shift
            self._value_shift_percent = sprofile.value_shift_percent
            self._value_shift_degree = sprofile.value_shift_degree
            self._opacity = sprofile.opacity
            self._order = sprofile.order
            return True
        else:
            return False
        
    def duplicate(self):
        """
        duplicate the profile

        returns:
        - new_sprofile: duplicated profile - sProfile

        examples:
        >>> new_sprofile = sprofile.duplicate()

        """
        new_sprofile = sProfile()
        new_sprofile.copy_style(self)
        
        new_sprofile.name = f"{self._name} duplicated"
        new_sprofile.label = self._label
        
        new_sprofile.zprofile = self._zprofile
        
        return new_sprofile
    
    def export_style(self, filename):
        """
        export profile style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> sprofile.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'marker_style': self._marker_style,
                     'marker_color': self._marker_color,
                     'marker_size': self._marker_size,
                     'value_color': self._value_color,
                     'value_size': self._value_size,
                     'value_shift': self._value_shift,
                     'value_shift_percent': self._value_shift_percent,
                     'value_shift_degree': self._value_shift_degree,
                     'opacity': self._opacity,
                     'order': self._order}
            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False
    
    def import_style(self, filename):
        """
        import profile style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> sprofile.import_style("style.json")
        
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
                if 'marker_style' in style.keys():
                    self.marker_style = style['marker_style']
                if 'marker_color' in style.keys():
                    self.marker_color = style['marker_color']
                if 'line_thickness' in style.keys():
                    self.marker_size = style['marker_size']
                if 'values_color' in style.keys():
                    self.values_color = style['value_color']
                if 'value_size' in style.keys():
                    self.values_size = style['value_size']
                if 'value_sift' in style.keys():
                    self.values_shift = style["value_shift"]
                if 'value_shift_percent' in style.keys():
                    self.values_shift_percent = style['value_shift_percent']
                if 'value_shift_degree' in style.keys():
                    self.values_shift_degree = style['value_shift_degree']
                if 'opacity' in style.keys():
                    self.opacity = style['opacity']
                if 'order' in style.keys():
                    self.order = style['order']
                return True
            else:
                return False
    
    def listing(self, unit="%", xz_decimals=3, slope_decimals=3):
        """
        print the list of points

        arguments:
        - unit: slope unit "%" | "°" - str
        - xz_decimals: number of decimals to print for distance and altitude values - int
        - slope_decimals: number of decimals to print for slope values - int

        returns:
        - None - NoneType

        examples:
        >>> sprofile.listing()
        >>> sprofile.listing(unit="°", xz_decimals=2, slope_decimals=1)
        
        """
        if unit not in ["%", "°"]:
            return None
        
        if not (isinstance(xz_decimals, int) and isinstance(slope_decimals, int)):
            return None
        
        for i, (x, z, s) in enumerate(self._xzs):
            if unit == "%":
                print(f"vertice {i}: x = {round(x, xz_decimals)} m ; z = {round(z, xz_decimals)} m ; s = {round(s * 100, slope_decimals)}%")
            else:
                print(f"vertice {i}: x = {round(x, xz_decimals)} m ; z = {round(z, xz_decimals)} m ; s = {round(np.degrees(np.arctan(s)), slope_decimals)}°")
    
    def mean(self, unit="%"):
        """
        calculate the mean slope

        arguments:
        - unit: slope unit "%" | "°" - str

        returns:
        - mean_slope: mean slope - float
        or
        - None - NoneType

        examples:
        >>> mean_slope = sprofile.mean()
        >>> mean_slope = sprofile.mean(unit="°")
        
        """
        if unit not in ["%", "°"]:
            return None
        
        x = np.array(self._zprofile.x)
        z = np.array(self._zprofile.z)

        s = np.array(self.s)
        
        d = np.sqrt((x[1:] - x[:-1])**2 + (z[1:] - z[:-1])**2)
        
        mean_slope = np.sum(s * d) / np.sum(d)
        
        if unit == "percent":
            return float(mean_slope) * 100.
        else:
            return float(np.degrees(np.arctan(mean_slope)))   
        
    def plot(self, ax, unit="%", twin_ax=None, decimals=1):
        """
        plot profile on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot
        - unit: slope unit "%" | "°" - str
        - twin_ax: secondary axis - matplotlib.axes._subplots.AxesSubplot
        - decimals: number of decimals to plot - int

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> sprofile.plot(ax)
        >>> plt.show()
        """
        if not (isinstance(ax, Subplot) and 
                isinstance(twin_ax, (type(None), Subplot)) and 
                isinstance(unit, str)):
            return None
        
        if unit not in ["%", "°"]:
            return None
        
        self.clear()
        self.update()
        
        ax.add_line(self._trick_line)
        
        if not twin_ax:
            ax.add_line(self._line)
            
            if self._value_visible:
                if unit == "%":
                    for i, slope in enumerate(self.slopes(unit="%")):
                        ax.text(self._xzs[i][0],
                                self._xzs[i][1] + self._value_shift,
                                s=f"{round(slope, decimals)}%",
                                fontsize=self._value_size,
                                color=colors[self._value_color],
                                alpha=self._opacity,
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation=0,
                                zorder=self._order)
                        
                elif unit == "°":
                    for i, slope in enumerate(self.slopes(unit="°")):
                        ax.text(self._xzs[i][0],
                                self._xzs[i][1] + self._value_shift,
                                s=f"{round(slope, decimals)}°",
                                fontsize=self._value_size,
                                color=colors[self._value_color],
                                alpha=self._opacity,
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation=0,
                                zorder=self._order)
                        
        else:
            if unit == "%":
                twin_ax.add_line(self._line_percent)
                if self._value_visible:
                    for i, slope in enumerate(self.slopes(unit="%")):
                        if min(twin_ax.get_ylim()) <= slope <= max(twin_ax.get_ylim()):
                            twin_ax.text(self._xzs[i][0],
                                         slope + self._value_shift_percent,
                                         s=f"{round(slope, decimals)}%",
                                         fontsize=self._value_size,
                                         color=colors[self._value_color],
                                         alpha=self._opacity,
                                         horizontalalignment='center',
                                         verticalalignment='center',
                                         zorder=self._order)

            else:
                twin_ax.add_line(self._line_degree)
                if self._value_visible:
                    for i, slope in enumerate(self.slopes(unit="°")):
                        if min(twin_ax.get_ylim()) <= slope <= max(twin_ax.get_ylim()):
                            twin_ax.text(self._xzs[i][0],
                                         slope + self._value_shift_degree,
                                         s=f"{round(slope, decimals)}°",
                                         fontsize=self._value_size,
                                         color=colors[self._value_color],
                                         alpha=self._opacity,
                                         horizontalalignment='center',
                                         verticalalignment='center',
                                         zorder=self._order)
                            
            
    def slopes(self, unit="%"):
        """
        calculate slopes in percent or degree

        arguments:
        - unit: slope unit "%" | "°" - str

        returns:
        - slopes: calculated slopes - list
        or
        - None - NoneType

        examples:
        >>> slopes = sprofile.slopes()
        >>> slopes = sprofile.slopes(unit="°")

        """
        if unit not in ["%", "°"]:
            return None
        
        self.update_xzs()
        
        if unit == "%":
            return [s*100 for x, z, s in self._xzs]
        else:
            return list(np.degrees(np.arctan(np.array(self.s))))
            
    def update(self):
        """
        update lines properties

        returns:
        - None - NoneType

        examples:
        >>> sprofile.update()
        
        """  
        self.update_xzs()

        self._line.set_data(self.x, self.z)
        self._line_percent.set_data(self.x, self.slopes(unit="%"))
        self._line_degree.set_data(self.x, self.slopes(unit="°"))

        self._line.set_label("")
        self._line_percent.set_label("")
        self._line_degree.set_label("")

        if self._active and self._marker_visible:
            self._trick_line.set_label(self._label)
        else:
            self._trick_line.set_label("")

        self._line.set_linestyle("None")
        self._line_percent.set_linestyle("None")
        self._line_degree.set_linestyle("None")
        self._trick_line.set_linestyle("None")

        self._line.set_marker(marker_styles[self._marker_style])
        self._line_percent.set_marker(marker_styles[self._marker_style])
        self._line_degree.set_marker(marker_styles[self._marker_style])
        self._trick_line.set_marker(marker_styles[self._marker_style])

        self._line.set_markeredgecolor(colors[self._marker_color])
        self._line_percent.set_markeredgecolor(colors[self._marker_color])
        self._line_degree.set_markeredgecolor(colors[self._marker_color])
        self._trick_line.set_markeredgecolor(colors[self._marker_color])

        self._line.set_markerfacecolor(colors[self._marker_color])
        self._line_percent.set_markerfacecolor(colors[self._marker_color])
        self._line_degree.set_markerfacecolor(colors[self._marker_color])
        self._trick_line.set_markerfacecolor(colors[self._marker_color])

        self._line.set_markersize(self._marker_size)
        self._line_percent.set_markersize(self._marker_size)
        self._line_degree.set_markersize(self._marker_size)
        self._trick_line.set_markersize(self._marker_size)

        self._line.set_alpha(self._opacity)
        self._line_percent.set_alpha(self._opacity)
        self._line_degree.set_alpha(self._opacity)
        self._trick_line.set_alpha(self._opacity)

        self._line.set_zorder(self._order)
        self._line_percent.set_zorder(self._order)
        self._line_degree.set_zorder(self._order)
        self._trick_line.set_zorder(self._order)

        self._line.set_visible(self._active and self._marker_visible)
        self._line_percent.set_visible(self._active and self._marker_visible)
        self._line_degree.set_visible(self._active and self._marker_visible)
        self._trick_line.set_visible(self._active and self._marker_visible)

    def update_xzs(self):
        """
        update profile data

        returns:
        - None - NoneType

        examples:
        >>> sprofile.update_xzs()
        
        """  
        x = np.array(self._zprofile.x)
        z = np.array(self._zprofile.z)

        if self._change_sign:
            k = -1
        else:
            k = 1

        s = list(k * (z[1:] - z[:-1]) / (x[1:] - x[:-1]))
        x = list((x[1:] + x[:-1]) / 2)
        z = list((z[1:] + z[:-1]) / 2)

        self._xzs = [(x, z, s) for x, z, s in zip(x, z, s)]
    
    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_line"] = mpl_Line([], [])
        attributes["_line_percent"] = mpl_Line([], [])
        attributes["_line_degree"] = mpl_Line([], [])
        attributes["_trick_line"] = mpl_Line([], [])

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
    def zprofile(self):
        return self._zprofile
    
    @zprofile.setter
    def zprofile(self, zprofile):
        if isinstance(zprofile, zProfile):
            self._zprofile = zprofile
            self.update_xzs()

    @property
    def xzs(self):
        self.update_xzs()
        return list(self._xzs)
    
    @property
    def x(self):
        self.update_xzs()
        return [x for x, z, s in self._xzs]
    
    @property
    def z(self):
        self.update_xzs()
        return [z for x, z, s in self._xzs]
    
    @property
    def s(self):
        self.update_xzs()
        return [s for x, z, s in self._xzs]
    
    @property
    def change_sign(self):
        return self._change_sign
    
    @change_sign.setter
    def change_sign(self, change):
        if isinstance(change, bool):
            self._change_sign = change
            self.update_xzs()

    @property
    def line(self):
        return str(self._line)

    @property
    def line_percent(self):
        return str(self._line_percent)

    @property
    def line_degree(self):
        return str(self._line_degree)

    @property
    def trick_line(self):
        return str(self._trick_line)

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
    def value_color(self):
        return self._value_color

    @value_color.setter
    def value_color(self, color):
        if color in colors.keys():
            self._value_color = color

    @property
    def value_size(self):
        return self._value_size

    @value_size.setter
    def value_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._value_size = size

    @property
    def value_shift(self):
        return self._value_shift

    @value_shift.setter
    def value_shift(self, shift):
        if isinstance(shift, (int, float)):
            self._value_shift = shift

    @property
    def value_shift_percent(self):
        return self._value_shift_percent

    @value_shift_percent.setter
    def value_shift_percent(self, shift):
        if isinstance(shift, (int, float)):
            self._value_shift_percent = shift

    @property
    def value_shift_degree(self):
        return self._value_shift_degree

    @value_shift_degree.setter
    def value_shift_degree(self, shift):
        if isinstance(shift, (int, float)):
            self._value_shift_degree = shift

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
    def marker_visible(self):
        return self._marker_visible

    @marker_visible.setter
    def marker_visible(self, visible):
        if isinstance(visible, bool):
            self._marker_visible = visible

    @property
    def value_visible(self):
        return self._value_visible

    @value_visible.setter
    def value_visible(self, visible):
        if isinstance(visible, bool):
            self._value_visible = visible
    
    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        if isinstance(active, bool):
            self._active = active
