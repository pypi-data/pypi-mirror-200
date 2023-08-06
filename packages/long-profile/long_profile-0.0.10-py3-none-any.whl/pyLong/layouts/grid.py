import json
import os

from pyLong.dictionnaries.colors import colors
from pyLong.dictionnaries.styles import line_styles


class Grid:
    def __init__(self):
        self._line_style = "dashed"

        self._line_color = "Gray"

        self._line_thickness = 0.8

        self._opacity = 0.6

        self._order = 1

        self._visible = True

    """
    Methods:
    - copy_style
    - duplicate
    - export_style
    - import_style
    """

    def copy_style(self, grid):
        """
        copy the style of a grid

        arguments:
        - grid: grid whose style is to be copied - Grid

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_grid.copy_style(grid)
        
        """
        if isinstance(grid, Grid):
            self._line_style = grid.line_style
            self._line_color = grid.line_color
            self._line_thickness = grid.line_thickness
            self._opacity = grid.opacity
            self._order = grid.order            
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the grid

        returns:
        - new_grid: duplicated grid - Grid

        examples:
        >>> new_grid = grid.duplicate()
        
        """
        new_grid = Grid()
        new_grid.copy_style(self)

        return new_grid

    def export_style(self, filename):
        """
        export grid style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> grid.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'line_style': self._line_style,
                     'line_color': self._line_color,
                     'line_thickness': self._line_thickness,
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
        import grid style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> grid.import_style("style.json")

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
                if 'opacity' in style.keys():
                    self.opacity = style['opacity']
                if 'order' in style.keys():
                    self.order = style['order']
                return True
            else:
                return False

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
