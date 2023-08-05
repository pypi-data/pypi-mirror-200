import json

from matplotlib.lines import Line2D
from matplotlib.axes import Subplot
import pandas as pd
from scipy.interpolate import interp1d
import numpy as np

from pyLong.dictionnaries.styles import line_styles, marker_styles
from pyLong.dictionnaries.colors import colors

class Trajectory:
    def __init__(self):
        self._xz = [(0, 1000), (1000, 0)]

        self._title = "new trajectory"

        self._label = ""

        self._visible = True

        self._line = Line2D([], [])

        self._line_style = 'solid'

        self._line_color = 'Black'
        
        self._line_thickness = 1.

        self._marker_style = 'none'
        
        self._marker_color = 'Black'
        
        self._marker_size = 1.

        self._opacity = 1.
        
        self._order = 1
        
    """
    Methods:
    - add_point --> OK
    - clear --> OK
    - copy_style --> OK
    - duplicate --> OK
    - export --> OK
    - export_style --> OK
    - import_style --> OK
    - interpolate --> OK
    - plot --> OK
    - reverse --> OK
    - update --> OK
    """
        
    def add_point(self, point):
        if not isinstance(point, tuple):
            return False
        
        if not len(point) > 1:
            return False
        
        x, z = point[0], point[1]
        if not isinstance(x, (int, float)) or not isinstance(z, (int, float)):
            return False
        
        if x in [x for x, z in self._xz]:
            return False
 
        self._xz.append((x, z))
        self._xz.sort()
        return True
        
    def clear(self):
        self._line = Line2D([], [])
        
    def copy_style(self, trajectory):
        if not isinstance(trajectory, Trajectory):
            return False
        
        self._line_style = trajectory.line_style
        self._line_color = trajectory.line_color
        self._line_thickness = trajectory.line_thickness
        self._marker_style = trajectory.marker_style
        self._marker_color = trajectory.marker_color
        self._marker_size = trajectory.marker_size
        self._opacity = trajectory.opacity
        self._order = trajectory.order
        return True

    def duplicate(self):
        trajectory = Trajectory()
        trajectory.copy_style(self)
        
        trajectory.title += " duplicated"
        trajectory.label = self._label
        
        trajectory.xz = list(self._xz)
        
        return trajectory
    
    def export(self, filename, delimiter="\t", separator=".", decimals=3):
        if not isinstance(filename, str) or not isinstance(decimals, int):
            return False
        
        if delimiter not in ["\t", " ", ";", ","] or separator not in [".", ","]:
            return False
        
        if delimiter == separator:
            return False
        
        if not len(filename) > 0:
            return False
        
        x = np.array(self.x)
        z = np.array(self.z)
        
        xz = np.array([x, z]).T
        xz = pd.DataFrame(xz) 
        
        try:
            xz.to_csv(filename,
                      sep = delimiter,
                      float_format = f"%.{decimals}f",
                      decimal = separator,
                      index = False,
                      header = ['X','Z'])
            return True
        except:
            return False
    
    def export_style(self, filename):
        style = {'line_style': self._line_style,
                 'line_color': self._line_color,
                 'line_thickness': self._line_thickness,
                 'marker_style': self._marker_style,
                 'marker_color': self._marker_color,
                 'marker_size': self._marker_size,
                 'visible': self._visible,
                 'opacity': self._opacity,
                 'order': self._order}

        if not isinstance(filename, str):
            return False
        
        if not len(filename) > 0:
            return False
        
        with open(filename, 'w') as file:
            json.dump(style, file, indent=0)
            return True
        
    def import_style(self, filename):
        if not isinstance(filename, str):
            return False
        
        if not len(filename) > 0:
            return False
        
        with open(filename, 'r') as file:
            try:
                style = json.load(file)
            except json.JSONDecodeError:
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
            if 'visible' in style.keys():
                self.visible = style['visible']
            if 'opacity' in style.keys():
                self.opacity = style['opacity']
            if 'order' in style.keys():
                self.order = style['order']
            return True
        else:
            return False

    def interpolate(self, x):
        if isinstance(x, (int, float)):
            if min(self.x) <= x <= max(self.x):
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
                
    def plot(self, ax):
        if isinstance(ax, Subplot):
            self.clear()
            self.update()

            ax.add_line(self._line)  
            
    def reverse(self, zprofile):
        if not isinstance(zprofile, zProfile):
            return False

        reversed_trajectory = self.duplicate()
        reversed_trajectory.title += " reversed"
        
        x_start = zprofile.xz[0][0]
        x_end = zprofile.xz[-1][0]

        xz = [(-x + x_end + x_start, z) for (x, z) in self._xz]

        xz.sort()
        reversed_trajectory.xz = xz
        
        return reversed_trajectory
    
    def update(self):
        x = [x for x, z in self._xz]
        z = [z for x, z in self._xz]

        self._line.set_data(x, z)

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
        
    @property
    def xz(self):
        return list(self._xz)

    @xz.setter
    def xz(self, xz):
        if isinstance(xz, list):
            if len(xz) > 1:
                valid = True
                for x, z in xz:
                    if not (isinstance(x, (int, float)) and isinstance(z, (int, float))):
                        valid = False
                        break
                if valid:
                    xz.sort()
                    self._xz = xz

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str):
            self._title = title

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if isinstance(visible, bool):
            self._visible = visible

    @property
    def line(self):
        return self._line

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
            if 0 <= thickness < 100:
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
            if 0 <= size < 100:
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
            if 0 < order < 100:
                self._order = order

    @property
    def x(self):
        return [x for x, z in self._xz]

    @property
    def z(self):
        return [z for x, z in self._xz]