import enum
import json
import os

from matplotlib.axes import Subplot
from matplotlib.patches import Polygon as mpl_Polygon
import numpy as np

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles
from pyLong.lists.hatches import hatch_styles
from pyLong.profiles.yprofile import yProfile
from pyLong.profiles.zprofile import zProfile


class Polygon(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new polygon"

        self._label = ""

        self._xy = [(200, 200), (800, 200), (500, 800)]

        self._polygon = mpl_Polygon(np.random.rand(3, 2), closed=True)

        self._line_style = "solid"

        self._line_color = "Black"
        
        self._line_thickness = 1.

        self._hatch_style = "/"

        self._hatch_density = 1

        self._fill_color = "None"

    """
    Methods:
    - area
    - clear
    - copy_style
    - duplicate
    - export_style
    - from_profile
    - from_profiles
    - import_style
    - plot
    - reverse
    - update
    """

    def area(self):
        """
        calculate the polygon area

        returns:
        area: polygon area - float

        examples:
        >>> area = annotation.area()
        
        """        
        area = 0.
        
        x = [xy[0] for xy in self._xy]
        y = [xy[1] for xy in self._xy]
        
        for i in range(len(self._xy)):
            if i < len(self._xy) - 1:
                area += (x[i] * y[i+1] - x[i+1] * y[i])
            else:
                area += (x[-1] * y[0] - x[0] * y[-1])
                
        return area / 2.

    def clear(self):
        """
        clear annotation

        returns:
        - None - NoneType
        
        """
        self._polygon = mpl_Polygon(np.random.rand(3, 2), closed=True)

    def copy_style(self, annotation):
        """
        copy the style of a polygon annotation

        arguments:
        - annotation: annotation whose style is to be copied - Polygon

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, Polygon):
            self._line_style = annotation.line_style
            self._line_color = annotation.line_color
            self._line_thickness = annotation.line_thickness
            self._hatch_style = annotation.hatch_style
            self._hatch_density = annotation.hatch_density
            self._fill_color = annotation.fill_color
            self._opacity = annotation.opacity
            self._order = annotation.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the annotation

        returns:
        - new_annotation: duplicated annotation - Polygon

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = Polygon()
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
                     'hatch_style': self._hatch_style,
                     'hatch_density': self._hatch_density,
                     'fill_color': self._fill_color,
                     'opacity': self._opacity,
                     'order': self._order}

            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False
            
    def from_profile(self, profile, ref):
        """
        fill in between a profile and a reference altitude or value

        arguments:
        - profile: profile - zProfile | yProfile
        - ref: reference altitude or value - int | float

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> polygon.from_profile(profile, 0.)
        
        """
        if not (isinstance(profile, (zProfile, yProfile)) and isinstance(ref, (int, float))):
            return False
        else:
            xy = []
            if isinstance(profile, zProfile):
                xy += profile.xz
            else:
                xy += profile.xy

            xy += [(xy[-1][0], ref), (xy[0][0], ref)]

            self._xy = xy
            return True
            
    def from_profiles(self, profile1, profile2):
        """
        fill in between two profiles
        
        arguments:
        - profile1: profile - zProfile | yProfile
        - profile2: profile - zProfile | yProfile

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> polygon.from_profiles(profile1, profile2)
        
        """
        if not (isinstance(profile1, (zProfile, yProfile)) and isinstance(profile2, (zProfile, yProfile))):
            return False
        else:
            xy = []
            if isinstance(profile1, zProfile):
                xy += profile1.xz
            else:
                xy += profile1.xy

            if isinstance(profile2, zProfile):
                xy += sorted(profile2.xz, reverse=True)
            else:
                xy += sorted(profile2.xy, reverse=True)

            self._xy = xy
            return True

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
                if 'hatch_style' in style.keys():
                    self.hatch_style = style['hatch_style']
                if 'hatch_density' in style.keys():
                    self.hatch_density = style['hatch_density']
                if 'fill_color' in style.keys():
                    self.fill_color = style['fill_color']
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

            ax.add_patch(self._polygon)

    def reverse(self, profile):
        """
        reverse the annotation according to a reference profile

        arguments:
        - profile: reference profile to perform the reversing - zProfile | yProfile

        returns:
        - new_annotation: reversed annotation - Polygon
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

            xy = self.xy
            for i in range(len(xy)):
                xy[i] = (2 * x_mean - xy[i][0], xy[i][1])

            new_annotation.xy = xy

            return new_annotation

    def update(self):
        """
        update annotation properties

        returns:
        - None - NoneType

        examples:
        >>> annotation.update()
        
        """  
        xy = np.zeros((len(self._xy), 2))
        for i, (x, y) in enumerate(self._xy):
            xy[i, 0], xy[i, 1] = x, y

        self._polygon.set_xy(xy)

        if self._visible and self._active:
            self._polygon.set_label(self._label)
        else:
            self._polygon.set_label("")

        self._polygon.set_linestyle(line_styles[self._line_style])
        self._polygon.set_linewidth(self._line_thickness)
        self._polygon.set_edgecolor(colors[self._line_color])
        self._polygon.set_fill(True)
        self._polygon.set_facecolor(colors[self._fill_color])
        self._polygon.set_hatch(self._hatch_density * self._hatch_style)
        self._polygon.set_alpha(self._opacity)
        self._polygon.set_zorder(self._order)
        self._polygon.set_visible(self._visible and self._active)  

    def __repr__(self):
        return f"{self._name}"  

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_polygon"] = mpl_Polygon(np.random.rand(3, 2), closed=True)

        return attributes 

    @property
    def xy(self):
        return list(self._xy)

    @xy.setter
    def xy(self, xy):
        if not isinstance(xy, list):
            return

        for item in xy:
            if not isinstance(item, tuple):
                return
            elif not len(item) == 2:
                return
            elif not (isinstance(item[0], (int, float)) and isinstance(item[1], (int, float))):
                return           
        
        self._xy = xy

    @property
    def x(self):
        return [xy[0] for xy in self._xy]

    @property
    def y(self):
        return [xy[1] for xy in self._xy]

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def polygon(self):
        return self._polygon

    @property
    def line_style(self):
        return self._line_style

    @line_style.setter
    def line_style(self, style):
        if style in line_styles.keys():
            self._line_style = style

    @property
    def line_thickness(self):
        return self._line_thickness

    @line_thickness.setter
    def line_thickness(self, thickness):
        if isinstance(thickness, (int, float)):
            if 0 <= thickness:
                self._line_thickness = thickness
            
    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, color):
        if color in colors.keys():
            self._line_color = color

    @property
    def hatch_style(self):
        return self._hatch_style

    @hatch_style.setter
    def hatch_style(self, style):
        if style in hatch_styles:
            self._hatch_style = style

    @property
    def hatch_density(self):
        return self._hatch_density

    @hatch_density.setter
    def hatch_density(self, density):
        if isinstance(density, int):
            if 0 < density:
                self._hatch_density = density

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color):
        if color in colors.keys():
            self._fill_color = color
