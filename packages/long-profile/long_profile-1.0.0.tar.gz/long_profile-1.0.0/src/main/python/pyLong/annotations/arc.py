import json
import os

from matplotlib.axes import Subplot
from matplotlib.patches import Arc as mpl_Arc

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles
from pyLong.lists.hatches import hatch_styles
from pyLong.profiles.yprofile import yProfile
from pyLong.profiles.zprofile import zProfile


class Arc(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new arc"
        
        self._label = ""

        self._xy = (500., 500.)
        
        self._width = 100.
        
        self._height = 100.

        self._rotation = 0.
        
        self._theta_1 = 0.
        
        self._theta_2 = 360.
        
        self._arc = mpl_Arc((0, 0), 0, 0)
        
        self._line_style = "solid"
        
        self._line_thickness = 1.
        
        self._line_color = "Black"
        
        self._hatch_style = "/"
        
        self._hatch_density = 1
        
        self._fill_color = "None"
        
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
        self._arc = mpl_Arc((0, 0),
                            0,
                            0,
                            angle=0.,
                            theta1=self._theta_1,
                            theta2=self._theta_2)

    def copy_style(self, annotation):
        """
        copy the style of an arc annotation

        arguments:
        - annotation: annotation whose style is to be copied - Arc

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, Arc):
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
        - new_annotation: duplicated annotation - Arc

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = Arc()
        new_annotation.copy_style(self)

        new_annotation.name = f"{self._name} duplicated"
        new_annotation.label = self._label

        new_annotation.xy = self._xy
        new_annotation.width = self._width
        new_annotation.height = self._height
        new_annotation.rotation = self._rotation
        new_annotation.theta_1 = self._theta_1
        new_annotation.theta_2 = self._theta_2

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
            
            ax.add_patch(self._arc)

    def reverse(self, profile):
        """
        reverse the annotation according to a reference profile

        arguments:
        - profile: reference profile to perform the reversing - zProfile | yProfile

        returns:
        - new_annotation: reversed annotation - Arc
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

            new_annotation.x = 2 * x_mean - self.x - self.width

            return new_annotation

    def update(self):
        """
        update annotation properties

        returns:
        - None - NoneType

        examples:
        >>> annotation.update()
        
        """ 
        self._arc.set_center(self._xy)
        self._arc.set_width(self._width)
        self._arc.set_height(self._height)
        self._arc.set_angle(self._rotation)

        if self._visible and self._active:
            self._arc.set_label(self._label)
        else:
            self._arc.set_label("")

        self._arc.set_linestyle(line_styles[self._line_style])
        self._arc.set_linewidth(self._line_thickness)
        self._arc.set_edgecolor(colors[self._line_color])
        self._arc.set_fill(True)
        self._arc.set_facecolor(colors[self._fill_color])
        self._arc.set_hatch(self._hatch_density * self._hatch_style)
        self._arc.set_alpha(self._opacity)
        self._arc.set_zorder(self._order)
        self._arc.set_visible(self._visible and self._active)

    def __repr__(self):
        return f"{self._name}"  

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_arc"] = mpl_Arc((0, 0), 0, 0)

        return attributes
    
    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        if not isinstance(xy, tuple):
            return
        elif not len(xy) > 1:
            return
        else:
            for value in xy:
                if not isinstance(value, (int, float)):
                    return
            self._xy = xy[0:2]

    @property
    def x(self):
        return self._xy[0]

    @x.setter
    def x(self, x):
        if isinstance(x, (int, float)):
            self._xy = (x, self._xy[1])

    @property
    def y(self):
        return self._xy[1]

    @y.setter
    def y(self, y):
        if isinstance(y, (int, float)):
            self._xy = (self._xy[0], y)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if isinstance(width, (int, float)):
            if 0 <= width:
                self._width = width
                
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if isinstance(height, (int, float)):
            if 0 <= height:
                self._height = height

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        if isinstance(rotation, (int, float)):
            if 0 <= rotation <= 360:
                self._rotation = rotation
                
    @property
    def theta_1(self):
        return self._theta_1

    @theta_1.setter
    def theta_1(self, theta):
        if isinstance(theta, (int, float)):
            if 0 <= theta <= 360:
                self._theta_1 = theta  
                
    @property
    def theta_2(self):
        return self._theta_2

    @theta_2.setter
    def theta_2(self, theta):
        if isinstance(theta, (int, float)):
            if 0 <= theta <= 360:
                self._theta_2 = theta 
                
    @property
    def arc(self):
        return self._arc

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
