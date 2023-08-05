import json
import os

from matplotlib.axes import Subplot
from matplotlib.lines import Line2D as mpl_Line

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles, marker_styles
from pyLong.profiles.yprofile import yProfile
from pyLong.profiles.zprofile import zProfile


class Line(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new line"
        
        self._label = ""

        self._xy = [(0., 0.), (1000., 1000.)]
        
        self._line = mpl_Line([], [])
        
        self._line_style = "solid"
        
        self._line_thickness = 1.
        
        self._line_color = "Black"

        self._marker_style = "none"
        
        self._marker_color = "Black"
        
        self._marker_size = 1.
        
    """
    Methods:
    - clear
    - copy_style
    - duplicate
    - export_style
    - import_style
    - plot
    - reverse
    - update
    """

    def clear(self):
        """
        clear annotation

        returns:
        - None - NoneType
        
        """
        self._line = mpl_Line([], [])

    def copy_style(self, annotation):
        """
        copy the style of a line annotation

        arguments:
        - annotation: annotation whose style is to be copied - Line

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, Line):
            self._line_style = annotation.line_style
            self._line_color = annotation.line_color
            self._line_thickness = annotation.line_thickness
            self._marker_style = annotation.marker_style
            self._marker_color = annotation.marker_color
            self._marker_size = annotation.marker_size
            self._opacity = annotation.opacity
            self._order = annotation.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the annotation

        returns:
        - new_annotation: duplicated annotation - Line

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = Line()
        new_annotation.copy_style(self)

        new_annotation.name = f"{self._name} duplicated"
        new_annotation.label = self._label

        new_annotation.xy = self._xy

        return new_annotation

    def export_style(self, filename):
        """
        export annotation style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> annotation.export_style("style.json")
        
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

    def import_style(self, filename):
        """
        import annotation style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> annotation.import_style("style.json")

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
                if 'marker_size' in style.keys():
                    self.marker_size = style['marker_size']
                if 'opacity' in style.keys():
                    self.opacity = style['opacity']
                if 'order' in style.keys():
                    self.order = style['order']
                return True
            else:
                return False

    def plot(self, ax):
        """
        plot annotation on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> annotation.plot(ax)
        >>> plt.show()
        
        """
        if isinstance(ax, Subplot):
            self.clear()
            self.update()
            
            ax.add_line(self._line)

    def reverse(self, profile):
        """
        reverse the annotation according to a reference profile

        arguments:
        - profile: reference profile to perform the reversing - zProfile | yProfile

        returns:
        - new_annotation: reversed annotation - Line
        or
        - None - NoneType

        examples:
        >>> new_annotation = annotation.reverse(profile)

        """
        if not isinstance(profile, (zProfile, yProfile)):
            return
        else:
            new_annotation = self.duplicate()
            new_annotation.name = f"{self._name} reversed" 

            x_mean = (min(profile.x) + max(profile.x)) / 2

            new_annotation.xy = [(2 * x_mean - x, y) for x, y in self._xy]

            return new_annotation

    def update(self):
        """
        update annotation properties

        returns:
        - None - NoneType

        examples:
        >>> annotation.update()
        
        """
        self._line.set_data(self.x, self.y)

        if self.visible and self._active:
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
        elif not len(xy) == 2:
            return
        
        for item in xy:
            if not isinstance(item, tuple):
                return
            elif not len(item) > 1:
                return
            else:
                x, y = item[0], item[1]
            
            if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                return
            
        xy.sort()
        self._xy = [(item[0], item[1]) for item in xy]

    @property
    def x(self):
        return [x for x, y in self._xy]

    @property
    def y(self):
        return [y for x, y in self._xy]

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label
                
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
