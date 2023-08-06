import json
import os

from matplotlib.axes import Subplot
from matplotlib.text import Text as mpl_Text
from matplotlib.text import Annotation as mpl_Annotation

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles
from pyLong.lists.arrows import arrow_styles
from pyLong.lists.fonts import font_styles, font_weights
from pyLong.profiles.yprofile import yProfile
from pyLong.profiles.zprofile import zProfile


class HorizontalAnnotation(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new horizontal annotation"

        self._text = ""

        self._position = (300., 700., 500.)
        
        self._vertical_shift = 0.
        
        self._arrow = mpl_Annotation("",
                                     xy=(0, 0),
                                     xytext=(0, 0),
                                     xycoords='data',
                                     arrowprops=dict(arrowstyle='->'))

        self._annotation = mpl_Text(0,
                                    0,
                                    "",
                                    horizontalalignment='center',
                                    verticalalignment='center')

        self._font_size = 11.

        self._font_color = "Black"

        self._font_style = "normal"

        self._font_weight = "normal"

        self._arrow_style = "-|>"

        self._arrow_line_style = "solid"

        self._arrow_color = "Black"
        
        self._arrow_thickness = 1.

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
        self._arrow = mpl_Annotation("",
                                     xy=(0, 0),
                                     xytext=(0, 0),
                                     xycoords='data',
                                     arrowprops=dict(arrowstyle='->'))

        self._annotation = mpl_Text(0,
                                    0,
                                    "",
                                    horizontalalignment='center',
                                    verticalalignment='center')

    def copy_style(self, annotation):
        """
        copy the style of a horizontal annotation

        arguments:
        - annotation: annotation whose style is to be copied - HorizontalAnnotation

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, HorizontalAnnotation):
            self._font_size = annotation.font_size
            self._font_color = annotation.font_color
            self._font_style = annotation.font_style
            self._font_weight = annotation.font_weight
            self._arrow_style = annotation.arrow_style
            self._arrow_line_style = annotation.arrow_line_style
            self._arrow_color = annotation.arrow_color
            self._arrow_thickness = annotation.arrow_thickness
            self._opacity = annotation.opacity
            self._order = annotation.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the annotation

        returns:
        - new_annotation: duplicated annotation - HorizontalAnnotation

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = HorizontalAnnotation()
        new_annotation.copy_style(self)

        new_annotation.name = f"{self._name} duplicated"
        new_annotation.text = self._text

        new_annotation.position = self._position

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
            style = {'font_size': self._font_size,
                     'font_color': self._font_color,
                     'font_style': self._font_style,
                     'font_weight': self._font_weight,
                     'arrow_style': self._arrow_style,
                     'arrow_line_style': self._arrow_line_style,
                     'arrow_color': self._arrow_color,
                     'arrow_thickness': self._arrow_thickness,
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
            if 'font_size' in style.keys():
                self.font_size = style['font_size']
            if 'font_color' in style.keys():
                self.font_color = style['font_color']
            if 'font_style' in style.keys():
                self.font_style = style['font_style']
            if 'font_weight' in style.keys():
                self.font_weight = style['font_weight']
            if 'arrow_style' in style.keys():
                self.arrow_style = style['arrow_style']
            if 'line_style' in style.keys():
                self.line_style = style['line_style']
            if 'arrow_color' in style.keys():
                self.arrow_color = style['arrow_color']
            if 'arrow_thickness' in style.keys():
                self.arrow_thickness = style['arrow_thickness']
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

            ax.add_artist(self._annotation)
            ax.add_artist(self._arrow)

    def reverse(self, profile):
        """
        reverse the annotation according to a reference profile

        arguments:
        - profile: reference profile to perform the reversing - zProfile | yProfile

        returns:
        - new_annotation: reversed annotation - HorizontalAnnotation
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
            x_start = 2 * x_mean - self.x_start
            x_end = 2 * x_mean - self.x_end

            new_annotation.x_start = x_end
            new_annotation.x_end = x_start

            return new_annotation

    def update(self):
        """
        update annotation properties

        returns:
        - None - NoneType

        examples:
        >>> annotation.update()
        
        """  
        self._arrow.arrow_patch.set_arrowstyle(self._arrow_style)
        self._arrow.arrow_patch.set_linestyle(line_styles[self._arrow_line_style])
        self._arrow.arrow_patch.set_linewidth(self._arrow_thickness)
        self._arrow.arrow_patch.set_color(colors[self._arrow_color])
        self._arrow.arrow_patch.set_alpha(self._opacity)
        self._arrow.arrow_patch.set_zorder(self._order)        
        self._arrow.xy = (self._position[0], self._position[2])
        self._arrow.set_x(self._position[1])
        self._arrow.set_y(self._position[2])
        self._arrow.set_alpha(self._opacity)
        self._arrow.set_zorder(self._order)
        self._arrow.set_visible(self._visible)
        
        self._annotation.set_text(self._text)
        self._annotation.set_x(self._x_mean)
        self._annotation.set_y(self._position[2] + self._vertical_shift)
        self._annotation.set_fontsize(self._font_size)
        self._annotation.set_color(colors[self._font_color])
        self._annotation.set_fontweight(self._font_weight)
        self._annotation.set_fontstyle(self._font_style)
        self._annotation.set_alpha(self._opacity)
        self._annotation.set_zorder(self._order)
        self._annotation.set_visible(self._visible and self._active)

    def __repr__(self):
        return f"{self._name}"

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_arrow"] = mpl_Annotation("",
                                              xy=(0, 0),
                                              xytext=(0, 0),
                                              xycoords='data',
                                              arrowprops=dict(arrowstyle='->'))

        attributes["_annotation"] = mpl_Text(0,
                                             0,
                                             "",
                                             horizontalalignment='center',
                                             verticalalignment='bottom')

        return attributes

    @property
    def _x_mean(self):
        return (self._position[0] + self._position[1]) / 2

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if not isinstance(position, tuple):
            return
        elif not len(position) > 2:
            return
        else:
            for value in position:
                if not isinstance(value, (int, float)):
                    return
            self._position = position[0:3]

    @property
    def x_start(self):
        return self._position[0]

    @x_start.setter
    def x_start(self, x):
        if isinstance(x, (int, float)):
            self._position = (x, self.x_end, self.y)

    @property
    def x_end(self):
        return self._position[1]

    @x_end.setter
    def x_end(self, x):
        if isinstance(x, (int, float)):
            self._position = (self.x_start, x, self.y)

    @property
    def y(self):
        return self._position[2]

    @y.setter
    def y(self, y):
        if isinstance(y, (int, float)):
            self._position = (self.x_start, self.x_end, y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if isinstance(text, str):
            self._text = text
            
    @property
    def vertical_shift(self):
        return self._vertical_shift

    @vertical_shift.setter
    def vertical_shift(self, shift):
        if isinstance(shift, (int, float)):
            self._vertical_shift = shift

    @property
    def arrow(self):
        return self._arrow
    
    @property
    def annotation(self):
        return self._annotation

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._font_size = size

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color):
        if color in colors.keys():
            self._font_color = color

    @property
    def font_style(self):
        return self._font_style

    @font_style.setter
    def font_style(self, style):
        if style in font_styles:
            self._font_style = style

    @property
    def font_weight(self):
        return self._font_weight

    @font_weight.setter
    def font_weight(self, weight):
        if weight in font_weights:
            self._font_weight = weight

    @property
    def arrow_style(self):
        return self._arrow_style

    @arrow_style.setter
    def arrow_style(self, style):
        if style in arrow_styles:
            self._arrow_style = style

    @property
    def arrow_line_style(self):
        return self._arrow_line_style

    @arrow_line_style.setter
    def arrow_line_style(self, style):
        if style in line_styles.keys():
            self._arrow_line_style = style
            
    @property
    def arrow_color(self):
        return self._arrow_color

    @arrow_color.setter
    def arrow_color(self, color):
        if color in colors.keys():
            self._arrow_color = color

    @property
    def arrow_thickness(self):
        return self._arrow_thickness

    @arrow_thickness.setter
    def arrow_thickness(self, thickness):
        if isinstance(thickness, (int, float)):
            if 0 <= thickness:
                self._arrow_thickness = thickness
