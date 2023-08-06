import json
import os

from pyLong.layouts.legend import Legend
from pyLong.layouts.y_axis import yAxis


class Sublayout:
    def __init__(self):
        self._id = ""

        self._subdivisions = 1

        self._y_axis = yAxis()

        self._legend = Legend()

    """
    Methods:
    - copy_style
    - duplicate
    - export_style
    - import_style
    """

    def copy_style(self, sublayout):
        """
        copy the style of a sublayout

        arguments:
        - sublayout: sublayout whose style is to be copied - Sublayout

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_sublayout.copy_style(sublayout)
        
        """
        if isinstance(sublayout, Sublayout):
            self._subdivisions = sublayout.subdivisions
            self._y_axis.copy_style(sublayout.y_axis)
            self._legend.copy_style(sublayout.legend)
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the sublayout

        returns:
        - new_sublayout: duplicated sublayout - Sublayout

        examples:
        >>> new_sublayout = sublayout.duplicate()
        
        """
        new_sublayout = Sublayout()
        new_sublayout.copy_style(self)
        new_sublayout.id = self._id

        return new_sublayout

    def export_style(self, filename):
        """
        export sublayout style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> sublayout.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'subdivisions': self._subdivisions}
            
            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False
            
    def import_style(self, filename):
        """
        import sublayout style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> sublayout.import_style("style.json")

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
                if 'subdivisions' in style.keys():
                    self.subdivisions = style['subdivisions']
                return True
            else:
                return False

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if isinstance(id, str):
            self._id = id.upper()

    @property
    def subdivisions(self):
        return self._subdivisions
    
    @subdivisions.setter
    def subdivisions(self, subdivisions):
        if isinstance(subdivisions, int):
            if 0 < subdivisions:
                self._subdivisions = subdivisions

    @property
    def y_axis(self):
        return self._y_axis
    
    @y_axis.setter
    def y_axis(self, axis):
        if isinstance(axis, yAxis):
            self._y_axis = axis

    @property
    def legend(self):
        return self._legend
    
    @legend.setter
    def legend(self, legend):
        if isinstance(legend, Legend):
            self._legend = Legend
