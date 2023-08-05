import json
import os

from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.legend import locations
from pyLong.lists.fonts import font_styles, font_weights


class Legend:
    def __init__(self):
        self._position = "upper left"

        self._columns = 6

        self._font_size = 11.

        self._font_color = "Black"

        self._font_style = "normal"

        self._font_weight = "normal"

        self._frame = True

        self._opacity = 0.6

        self._order = 100

        self._visible = True

    """
    Methods
    - copy_style
    - duplicate
    - export_style
    - import_style
    """
    
    def copy_style(self, legend):
        """
        copy the style of a legend

        arguments:
        - legend: legend whose style is to be copied - Legend

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_legend.copy_style(legend)
        
        """
        if isinstance(legend, Legend):
            self._position = legend.position
            self._columns = legend.columns
            self._font_size = legend.font_size
            self._font_color = legend.font_color
            self._font_style = legend.font_style
            self._font_weight = legend.font_weight
            self._frame = legend.frame
            self._opacity = legend.opacity
            self._order = legend.order           
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the legend

        returns:
        - new_legend: duplicated legend - Legend

        examples:
        >>> new_legend = legend.duplicate()
        
        """
        new_legend = Legend()
        new_legend.copy_style(self)

        return new_legend

    def export_style(self, filename):
        """
        export legend style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> legend.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'position': self._position,
                     'columns': self._columns,
                     'font_size': self._font_size,
                     'font_color': self._font_color,
                     'font_style': self._font_style,
                     'font_weight': self._font_weight,
                     'frame': self._frame,
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
        import legend style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> legend.import_style("style.json")

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
                if 'position' in style.keys():
                    self.position = style['position']
                if 'columns' in style.keys():
                    self.columns = style['columns']
                if 'font_size' in style.keys():
                    self.font_size = style['font_size']
                if 'font_color' in style.keys():
                    self.font_color = style['font_color']
                if 'font_style' in style.keys():
                    self.font_style = style['font_style']
                if 'font_weight' in style.keys():
                    self.font_weight = style['font_weight']
                if 'frame' in style.keys():
                    self.frame = style['frame']
                if 'opacity' in style.keys():
                    self.opacity = style['opacity']
                if 'order' in style.keys():
                    self.order = style['order']
                return True
            else:
                return False

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        if position in locations.keys():
            self._position = position

    @property
    def columns(self):
        return self._columns
    
    @columns.setter
    def columns(self, columns):
        if isinstance(columns, int):
            if 0 < columns:
                self._columns = columns

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
    def frame(self):
        return self._frame
    
    @frame.setter
    def frame(self, frame):
        if isinstance(frame, bool):
            self._frame = frame

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
