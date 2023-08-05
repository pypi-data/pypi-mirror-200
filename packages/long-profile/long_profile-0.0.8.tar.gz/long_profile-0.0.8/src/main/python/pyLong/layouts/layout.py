import json
import os

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import numpy as np

from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles
from pyLong.layouts.grid import Grid
from pyLong.layouts.legend import Legend
from pyLong.layouts.s_axis import sAxis
from pyLong.layouts.sublayout import Sublayout
from pyLong.layouts.x_axis import xAxis
from pyLong.layouts.z_axis import zAxis


class Layout:
    def __init__(self):
        self._name = "new layout"

        self._width = 29.7

        self._height = 21.

        self._format = "png"

        self._dpi = 300

        self._secondary_axis = False

        self._slope_unit = "%"

        self._as_km = False

        self._subdivisions = 1

        self._hspace = 0.125

        self._pad = 1.08

        self._sublayouts = []

        self._x_axis = xAxis()

        self._z_axis = zAxis()

        self._s_axis = sAxis()

        self._grid = Grid()

        self._legend = Legend()

    """
    Methods:
    - available_subdivisions
    - copy_style
    - duplicate
    - export_style
    - import_style
    - new_figure
    """

    def available_subdivisions(self):
        """
        calculate the number of available sudivisions

        returns:
        - n - number of available subdivisions - int

        examples:
        >>> n = layout.available_subdivisions()

        """
        n = 0
        for sublayout in self._sublayouts:
            n += sublayout.subdivisions

        return self._subdivisions - n - 1
    
    def copy_style(self, layout):
        """
        copy the style of a layout

        arguments:
        - layout: layout whose style is to be copied - Layout

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_layout.copy_style(layout)
        
        """
        if isinstance(layout, Layout):
            self._width = layout.width
            self._height = layout.height
            self._format = layout.format
            self._dpi = layout.dpi
            self._secondary_axis = layout.secondary_axis
            self._slope_unit = layout.slope_unit
            self._as_km = layout.as_km
            self._subdivisions = layout.subdivisions
            self._hspace = layout.hspace
            self._pad = layout.pad
            self._x_axis.copy_style(layout.x_axis)
            self._z_axis.copy_style(layout.z_axis)
            self._s_axis.copy_style(layout.s_axis)
            self._grid.copy_style(layout.grid)
            self._legend.copy_style(layout.legend)
            return True
        else:
            return False
        
    def duplicate(self):
        """
        duplicate the layout

        returns:
        - new_layout: duplicated layout - Layout

        examples:
        >>> new_layout = layout.duplicate()
        
        """
        new_layout = Layout()
        new_layout.copy_style(self)

        new_layout.name = f"{self._name} duplicated"
        new_layout.sublayouts = self._sublayouts

        return new_layout

    def export_style(self, filename):
        """
        export layout style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> layout.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'width': self._width,
                     'height': self._height,
                     'format': self._format,
                     'dpi': self._dpi,
                     'secondary_axis': self._secondary_axis,
                     'slope_unit': self._slope_unit,
                     'as_km': self._as_km,
                     'subdivisions': self._subdivisions,
                     'hspace': self._hspace,
                     'pad': self._pad}
            
            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False
            
    def import_style(self, filename):
        """
        import layout style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> layout.import_style("style.json")

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
                if 'width' in style.keys():
                    self.width = style['width']
                if 'height' in style.keys():
                    self.height = style['height']
                if 'format' in style.keys():
                    self.format = style['format']
                if 'dpi' in style.keys():
                    self.dpi = style['dpi']
                if 'secondary_axis' in style.keys():
                    self.secondary_axis = style['secondary_axis']
                if 'slope_unit' in style.keys():
                    self.slope_unit = style['slope_unit']
                if 'as_km' in style.keys():
                    self.as_km = style['as_km']
                if 'subdivisions' in style.keys():
                    self.subdivisions = style['subdivisions']
                if 'hspace' in style.keys():
                    self.hspace = style['hspace']
                if 'pad' in style.keys():
                    self.pad = style['pad']
                return True
            else:
                return False
            
    def new_figure(self):
        """
        create a new figure

        returns:
        - ax_z: altitude axis - matplotlib.axes._subplots.AxesSubplot
        - ax_s: slope axis - matplotlib.axes._subplots.AxesSubplot
        - axs: subaxis - list of matplotlib.axes._subplots.AxesSubplot
        - figure: figure - matplotlib.figure.Figure

        examples:
        >>> ax_z, ax_s, subaxs, figure = layout.new_figure()

        """
        figure = Figure(figsize=(self.width/2.54, self.height/2.54))

        n_subdivisions = self.subdivisions
        n_sublayouts = len(self.sublayouts)
        n_subdivisions_sublayouts = 0
        for sublayout in self._sublayouts:
            n_subdivisions_sublayouts += sublayout.subdivisions

        gs = GridSpec(n_subdivisions, 1, figure=figure)

        ax_z = figure.add_subplot(gs[0:n_subdivisions - n_subdivisions_sublayouts, :])
        ax_s = ax_z.twinx()

        ax_z.set_xlim((self._x_axis.min - self._x_axis.left_shift,
                       self._x_axis.max + self._x_axis.right_shift))

        ax_z.tick_params(axis='x',
                         colors=colors[self._x_axis.value_color],
                         labelsize=self._x_axis.value_size)

        ax_z.set_xticks(np.linspace(self._x_axis.min,
                        self._x_axis.max,
                        self._x_axis.intervals + 1))

        values = np.linspace(self._x_axis.min,
                             self._x_axis.max,
                             self._x_axis.intervals + 1)
        

        if self._as_km:
            values /= 1000
            values = np.round(values, 2)
            ax_z.set_xticklabels(values)
        else:
            ax_z.set_xticklabels(values.astype(int))

        ax_z.set_ylim((self._z_axis.min - self._z_axis.lower_shift,
                       self._z_axis.max + self._z_axis.upper_shift))

        ax_z.set_ylabel(self._z_axis.label,
                        {'color': colors[self._z_axis.label_color],
                         'fontsize': self._z_axis.label_size})

        ax_z.tick_params(axis='y',
                         colors=colors[self._z_axis.value_color],
                         labelsize=self._z_axis.value_size)

        ax_z.set_yticks(np.linspace(self._z_axis.min,
                                    self._z_axis.max,
                                    self._z_axis.intervals + 1))
        
        if n_subdivisions > 1 and n_sublayouts > 0:
            ax_z.xaxis.set_ticks_position('top')
        else:
            ax_z.set_xlabel(self._x_axis.label,
                            {'color': colors[self._x_axis.label_color],
                             'fontsize': self._x_axis.label_size})
            
        ax_z.grid(visible=self._grid.visible,
                  which='major',
                  axis='both',
                  linestyle=line_styles[self._grid.line_style],
                  color=colors[self._grid.line_color],
                  linewidth=self._grid.line_thickness,
                  alpha=self._grid.opacity,
                  zorder=self._grid.order)
        

        if self._slope_unit == "%":
            ax_s.set_ylim((self._s_axis.min_percent - self._s_axis.lower_shift_percent,
                           self._s_axis.max_percent + self._s_axis.upper_shift_percent))
        else:
            ax_s.set_ylim((self._s_axis.min_degree - self._s_axis.lower_shift_degree,
                           self._s_axis.max_degree + self._s_axis.upper_shift_degree))

        ax_s.set_ylabel(self._s_axis.label,
                        {'color': colors[self._s_axis.label_color],
                         'fontsize': self._s_axis.label_size})

        ax_s.tick_params(axis='y',
                         colors=colors[self._s_axis.value_color],
                         labelsize=self._s_axis.value_size)

        if self._slope_unit == "%":
            ax_s.set_yticks(
                np.linspace(self._s_axis.min_percent,
                            self._s_axis.max_percent,
                            self._s_axis.intervals_percent + 1))
        else:
            ax_s.set_yticks(np.linspace(self._s_axis.min_degree,
                                        self._s_axis.max_degree,
                                        self._s_axis.intervals_degree + 1))

        if self._slope_unit == "%":
            slope_labels = [str(np.round(s, self._s_axis.decimals_percent)) + f"{self.slope_unit}" for s in np.linspace(
                self._s_axis.min_percent,
                self._s_axis.max_percent,
                self._s_axis.intervals_percent + 1)]
        else:
            slope_labels = [str(np.round(s, self._s_axis.decimals_degree)) + f"{self.slope_unit}" for s in np.linspace(
                self._s_axis.min_degree,
                self._s_axis.max_degree,
                self._s_axis.intervals_degree + 1)]

        ax_s.set_yticklabels(slope_labels)

        if self._secondary_axis:
            ax_s.set_visible(True)
        else:
            ax_s.set_visible(False)

        n_start = n_subdivisions - n_subdivisions_sublayouts
        subaxs = []
        for i in range(n_sublayouts):
            subaxs.append(figure.add_subplot(gs[n_start:n_start + self._sublayouts[i].subdivisions], sharex=ax_z))
            n_start += self._sublayouts[i].subdivisions

            subaxs[i].set_ylim((self._sublayouts[i].y_axis.min - self._sublayouts[i].y_axis.lower_shift,
                                self._sublayouts[i].y_axis.max + self._sublayouts[i].y_axis.upper_shift))

            subaxs[i].set_yticks(np.linspace(self._sublayouts[i].y_axis.min,
                                             self._sublayouts[i].y_axis.max,
                                             self._sublayouts[i].y_axis.intervals + 1))

            subaxs[i].set_ylabel(self._sublayouts[i].y_axis.label,
                                 {'color': colors[self._sublayouts[i].y_axis.label_color],
                                  'fontsize': self._z_axis.label_size})

            subaxs[i].tick_params(axis='y',
                                  colors=colors[self._sublayouts[i].y_axis.value_color],
                                  labelsize=self._z_axis.value_size)

            subaxs[i].grid(visible=self._grid.visible,
                           which='major',
                           axis='both',
                           linestyle=line_styles[self._grid.line_style],
                           color=colors[self._grid.line_color],
                           linewidth=self._grid.line_thickness,
                           alpha=self._grid.opacity,
                           zorder=self._grid.order)

            subaxs[i].set_xlim((self._x_axis.min - self._x_axis.left_shift,
                                self._x_axis.max + self._x_axis.right_shift))

            subaxs[i].tick_params(axis='x',
                                  colors=colors[self._x_axis.value_color],
                                  labelsize=self._x_axis.value_size)

            subaxs[i].set_xticks(np.linspace(self._x_axis.min,
                                             self._x_axis.max,
                                             self._x_axis.intervals + 1))

            if i != n_sublayouts - 1:
                plt.setp(subaxs[i].get_xticklabels(), visible=False)
                subaxs[i].tick_params(axis='x', length=0)
            else:
                subaxs[i].set_xlabel(self._x_axis.label,
                                     {'color': colors[self._x_axis.label_color],
                                      'fontsize': self._x_axis.label_size})

        figure.align_ylabels()
        figure.tight_layout(pad=self._pad)
        figure.subplots_adjust(hspace=self.hspace)

        ax_z.set_zorder(ax_s.get_zorder() + 1)
        ax_z.patch.set_visible(False)

        plt.show()

        return ax_z, ax_s, subaxs, figure

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
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        if isinstance(width, (int, float)):
            if 0 < width:
                self._width = width

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        if isinstance(height, (int, float)):
            if 0 < height:
                self._height = height

    @property
    def format(self):
        return self._format
    
    @format.setter
    def format(self, format):
        if format in ["png", "pdf", "eps", "svg"]:
            self._format = format

    @property
    def dpi(self):
        return self._dpi
    
    @dpi.setter
    def dpi(self, dpi):
        if isinstance(dpi, int):
            if 0 < dpi:
                self._dpi = dpi

    @property
    def secondary_axis(self):
        return self._secondary_axis
    
    @secondary_axis.setter
    def secondary_axis(self, secondary_axis):
        if isinstance(secondary_axis, bool):
            self._secondary_axis = secondary_axis

    @property
    def slope_unit(self):
        return self._slope_unit
    
    @slope_unit.setter
    def slope_unit(self, unit):
        if unit in ["%", "°"]:
            self._slope_unit = unit

    @property
    def as_km(self):
        return self._as_km
    
    @as_km.setter
    def as_km(self, as_km):
        if isinstance(as_km, bool):
            self._as_km = as_km

    @property
    def subdivisions(self):
        return self._subdivisions
    
    @subdivisions.setter
    def subdivisions(self, subdivisions):
        if isinstance(subdivisions, int):
            if 1 < subdivisions:
                self._subdivisions = subdivisions

    @property
    def hspace(self):
        return self._hspace
    
    @hspace.setter
    def hspace(self, hspace):
        if isinstance(hspace, (int, float)):
            if 0 <= hspace:
                self._hspace = hspace
                
    @property
    def pad(self):
        return self._pad
    
    @pad.setter
    def pad(self, pad):
        if isinstance(pad, (int, float)):
            if 0 < pad:
                self._pad = pad

    @property
    def sublayouts(self):
        return [sublayout.id for sublayout in self._sublayouts]
    
    @sublayouts.setter
    def sublayouts(self, sublayouts):
        if isinstance(sublayouts, list):
            if len(sublayouts) == 0:
                self._sublayouts = []
            else:
                self._sublayouts = []
                for sublayout in sublayouts:
                    if isinstance(sublayout, Sublayout):
                        if sublayout.id not in self.sublayouts and sublayout.subdivisions <= self.available_subdivisions():
                            self._sublayouts.append(sublayout.duplicate())
    
    @property
    def x_axis(self):
        return self._x_axis
    
    @x_axis.setter
    def x_axis(self, axis):
        if isinstance(axis, xAxis):
            self._x_axis = axis
    
    @property
    def z_axis(self):
        return self._z_axis
    
    @z_axis.setter
    def z_axis(self, axis):
        if isinstance(axis, xAxis):
            self._z_axis = axis
    
    @property
    def s_axis(self):
        return self._s_axis
    
    @s_axis.setter
    def s_axis(self, axis):
        if isinstance(axis, sAxis):
            self._s_axis = axis

    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, grid):
        if isinstance(grid, Grid):
            self._grid = grid

    @property
    def legend(self):
        return self._legend
    
    @legend.setter
    def legend(self, legend):
        if isinstance(legend, Legend):
            self._legend = legend
