import json
import os

from matplotlib.axes import Subplot
from matplotlib.lines import Line2D as mpl_Line2D
from matplotlib.text import Text as mpl_Text

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles
from pyLong.lists.arrows import arrow_styles
from pyLong.lists.fonts import font_styles, font_weights
from pyLong.profiles.yprofile import yProfile
from pyLong.profiles.zprofile import zProfile


class Interval(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new interval"
        
        self._text = ""

        self._limits = ((100., 500.), (800., 500.), 0)

        self._text_y = 250.
        
        self._text_rotation = 0

        self._annotation = mpl_Text(0,
                                    0,
                                    "",
                                    horizontalalignment='center',
                                    verticalalignment='center',
                                    bbox=dict(facecolor='w')
                                    )

        self._start_line = mpl_Line2D([], [])

        self._end_line = mpl_Line2D([], [])

        self._font_size = 11.

        self._font_color = "Black"

        self._font_style = "normal"

        self._font_weight = "normal"

        self._frame_style = "solid"

        self._frame_color = "Black"

        self._frame_thickness = 1.

        self._fill_color = "None"

        self._limits_style = "solid"

        self._limits_color = "Black"
        
        self._limits_thickness = 1.

    """
    Methods:
    - adjust
    - clear
    - copy_style
    - duplicate
    - export_style
    - import_style
    - plot
    - reverse
    - update
    """

    def adjust(self, profile):
        """
        adjust the annotation position on a profile

        arguments:
        - profile: profile on which the annotation is to be adjusted - zProfile | yProfile

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> annotation.adjust(profile)
        
        """
        if not isinstance(profile, (zProfile, yProfile)):
            return False
        elif profile.interpolate(self.x_start) and profile.interpolate(self.x_end):
            self.y_start = profile.interpolate(self.x_start)
            self.y_end = profile.interpolate(self.x_end)
            return True
        else:
            return False  

    def clear(self):
        """
        clear annotation

        returns:
        - None - NoneType
        
        """
        self._annotation = mpl_Text(0,
                                    0,
                                    "",
                                    horizontalalignment='center',
                                    verticalalignment='center',
                                    bbox=dict(facecolor='w')
                                    )

        self._start_line = mpl_Line2D([], [])

        self._end_line = mpl_Line2D([], [])

    def copy_style(self, annotation):
        """
        copy the style of a interval annotation

        arguments:
        - annotation: annotation whose style is to be copied - Interval

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, Interval):
            self._font_size = annotation.font_size
            self._font_color = annotation.font_color
            self._font_style = annotation.font_style
            self._font_weight = annotation.font_weight
            self._frame_style = annotation.frame_style
            self._frame_color = annotation.frame_color
            self._frame_thickness = annotation.frame_thickness
            self._fill_color = annotation.fill_color
            self._limits_style = annotation.limits_style
            self._limits_color = annotation.limits_color
            self._limits_thickness = annotation.limits_thickness
            self._opacity = annotation.opacity
            self._order = annotation.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the annotation

        returns:
        - new_annotation: duplicated annotation - Interval

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = Interval()
        new_annotation.copy_style(self)

        new_annotation.name = f"{self._name} duplicated"
        new_annotation.text = self._text

        new_annotation.limits = self._limits
        new_annotation.text_y = self._text_y
        new_annotation.text_rotation = self._text_rotation

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
                     'frame_style': self._frame_style,
                     'frame_color': self._frame_color,
                     'frame_thickness': self._frame_thickness,
                     'fill_color': self._fill_color,
                     'limits_style': self._limits_style,
                     'limits_color': self._limits_color,
                     'limits_thickness': self._limits_thickness,
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
            if 'frame_style' in style.keys():
                self.frame_style = style['frame_style']
            if 'frame_color' in style.keys():
                self.frame_color = style['frame_color']
            if 'frame_thickness' in style.keys():
                self.frame_thickness = style['frame_thickness']
            if 'fill_color' in style.keys():
                self.fill_color = style['fill_color']
            if 'limits_style' in style.keys():
                self.limits_style = style['limits_style']
            if 'limits_colors' in style.keys():
                self.limits_color = style['limits_color']
            if 'limits_thickness' in style.keys():
                self.limits_thickness = style['limits_thickness']
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

            ax.add_line(self._start_line)
            ax.add_line(self._end_line)
            ax.add_artist(self._annotation)

    def reverse(self, profile):
        """
        reverse the annotation according to a reference profile

        arguments:
        - profile: reference profile to perform the reversing - zProfile | yProfile

        returns:
        - new_annotation: reversed annotation - Interval
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

            x_start = 2 * x_mean - self.x_end
            x_end = 2 * x_mean - self.x_start

            new_annotation.x_start = x_start
            new_annotation.x_end = x_end

            new_annotation.y_start = self.y_end
            new_annotation.y_end = self.y_start

            return new_annotation

    def update(self):
        """
        update annotation properties

        returns:
        - None - NoneType

        examples:
        >>> annotation.update()
        
        """  
        self._annotation.set_text(self._text)
        self._annotation.set_x(self._x_mean())
        self._annotation.set_y(self._text_y)
        self._annotation.set_fontsize(self._font_size)
        self._annotation.set_color(colors[self._font_color])
        self._annotation.set_fontweight(self._font_weight)
        self._annotation.set_fontstyle(self._font_style)
        self._annotation.set_rotation(self._text_rotation)
        self._annotation.set_alpha(self._opacity)
        self._annotation.set_zorder(self._order)
        self._annotation.set_bbox(dict(linestyle=line_styles[self._frame_style],
                                       edgecolor=colors[self._frame_color],
                                       linewidth=self._frame_thickness,
                                       facecolor=self._fill_color,
                                       alpha=self._opacity,
                                       zorder=self._order))
        
        self._annotation.set_visible(self._visible and self._active)
        
        self._start_line.set_data([self._limits[0][0], self._limits[0][0]],
                                  [self._limits[2], self._limits[0][1]])
        self._start_line.set_linestyle(line_styles[self._limits_style])
        self._start_line.set_color(colors[self._limits_color])
        self._start_line.set_linewidth(self._limits_thickness)
        self._start_line.set_alpha(self._opacity)
        self._start_line.set_zorder(self._order)
        self._start_line.set_visible(self._visible and self._active)
        
        self._end_line.set_data([self._limits[1][0], self._limits[1][0]],
                                [self._limits[2], self._limits[1][1]])
        self._end_line.set_linestyle(line_styles[self._limits_style])
        self._end_line.set_color(colors[self._limits_color])
        self._end_line.set_linewidth(self._limits_thickness)
        self._end_line.set_alpha(self._opacity)
        self._end_line.set_zorder(self._order)
        self._end_line.set_visible(self._visible and self._active)

    def _x_mean(self):
        return (self._limits[0][0] + self._limits[1][0]) / 2

    def __repr__(self):
        return f"{self._name}"

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_annotation"] = mpl_Text(0,
                                             0,
                                             "",
                                             horizontalalignment='center',
                                             verticalalignment='center',
                                             bbox=dict(facecolor='w'))

        attributes["_start_line"] = mpl_Line2D([], [])

        attributes["_end_line"] = mpl_Line2D([], [])

        return attributes

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, limits):
        if not isinstance(limits, tuple):
            return
        elif not len(limits) > 2:
            return
        elif not (isinstance(limits[0], tuple) and isinstance(limits[1], tuple) and isinstance(limits[2], (int, float))):
            return
        else:
            for value_start, value_end in zip(limits[0], limits[1]):
                if not (isinstance(value_start, (int, float)) and isinstance(value_end, (int, float))):
                    return     
            self._limits = limits

    @property
    def x_start(self):
        return self._limits[0][0]

    @x_start.setter
    def x_start(self, x):
        if isinstance(x, (int, float)):
            self._limits = ((x, self._limits[0][1]), self._limits[1], self._limits[2])

    @property
    def y_start(self):
        return self._limits[0][1]

    @y_start.setter
    def y_start(self, y):
        if isinstance(y, (int, float)):
            self._limits = ((self._limits[0][0], y), self._limits[1], self._limits[2])

    @property
    def x_end(self):
        return self._limits[1][0]

    @x_end.setter
    def x_end(self, x):
        if isinstance(x, (int, float)):
            self._limits = ((self._limits[0]), (x, self._limits[1][1]), self._limits[2])       

    @property
    def y_end(self):
        return self._limits[1][1]

    @y_end.setter
    def y_end(self, y):
        if isinstance(y, (int, float)):
            self._limits = (self._limits[0], (self._limits[1][0], y), self._limits[2])

    @property
    def y_ref(self):
        return self._limits[2]

    @y_ref.setter
    def y_ref(self, y):
        if isinstance(y, (int, float)):
            self._limits = (self._limits[0], self._limits[1], y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if isinstance(text, str):
            self._text = text

    @property
    def text_y(self):
        return self._text_y

    @text_y.setter
    def text_y(self, y):
        if isinstance(y, (int, float)):
            self._text_y = y

    @property
    def text_rotation(self):
        return self._text_rotation

    @text_rotation.setter
    def text_rotation(self, rotation):
        if isinstance(rotation, (int)):
            if rotation in [0, 90]:
                self._text_rotation = rotation
                
    @property
    def annotation(self):
        return self._annotation

    @property
    def start_line(self):
        return self._start_line

    @property
    def end_line(self):
        return self._end_line

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
    def frame_style(self):
        return self._frame_style

    @frame_style.setter
    def frame_style(self, style):
        if style in line_styles.keys():
            self._frame_style = style   

    @property
    def frame_thickness(self):
        return self._frame_thickness

    @frame_thickness.setter
    def frame_thickness(self, thickness):
        if isinstance(thickness, (int, float)):
            if 0 <= thickness:
                self._frame_thickness = thickness

    @property
    def frame_color(self):
        return self._frame_color

    @frame_color.setter
    def frame_color(self, color):
        if color in colors.keys():
            self._frame_color = color
                
    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color):
        if color in colors.keys():
            self._fill_color = color

    @property
    def limits_style(self):
        return self._limits_style

    @limits_style.setter
    def limits_style(self, style):
        if style in line_styles.keys():
            self._limits_style = style  

    @property
    def limits_thickness(self):
        return self._limits_thickness

    @limits_thickness.setter
    def limits_thickness(self, thickness):
        if isinstance(thickness, (int, float)):
            if 0 <= thickness:
                self._limits_thickness = thickness
                
    @property
    def limits_color(self):
        return self._limits_color

    @limits_color.setter
    def limits_color(self, color):
        if color in colors.keys():
            self._limits_color = color
