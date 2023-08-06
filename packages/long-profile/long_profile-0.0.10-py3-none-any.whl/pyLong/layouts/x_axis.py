import json
import os

from pyLong.dictionnaries.colors import colors


class xAxis:
    def __init__(self):
        self._min = 0.

        self._max = 1000.

        self._label = "distance (m)"

        self._intervals = 10

        self._label_size = 11.

        self._label_color = "Black"

        self._value_size = 11.

        self._value_color = "Black"

        self._left_shift = 0.

        self._right_shift = 0.

    """
    Methods:
    - copy_style
    - duplicate
    - export_style
    - import_style
    """

    def copy_style(self, x_axis):
        """
        copy the style of a distance axis

        arguments:
        - x_axis: axis whose style is to be copied - xAxis

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_x_axis.copy_style(x_axis)
        
        """
        if isinstance(x_axis, xAxis):
            self._min = x_axis.min
            self._max = x_axis.max
            self._label = x_axis.label
            self._intervals = x_axis.intervals
            self._label_size = x_axis.label_size
            self._label_color = x_axis.label_color
            self._value_size = x_axis.value_size
            self._value_color = x_axis.value_color
            self._left_shift = x_axis.left_shift
            self._right_shift = x_axis.right_shift
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the axis

        returns:
        - new_x_axis: duplicated axis - xAxis

        examples:
        >>> new_x_axis = x_axis.duplicate()
        
        """
        new_x_axis = xAxis()
        new_x_axis.copy_style(self)

        return new_x_axis

    def export_style(self, filename):
        """
        export axis style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> x_axis.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'min': self._min,
                     'max': self._max,
                     'label': self._label,
                     'intervals': self._intervals,
                     'label_size': self._label_size,
                     'label_color': self._label_color,
                     'value_size': self._value_size,
                     'value_color': self._value_color,
                     'left_shift': self._left_shift,
                     'right_shift': self._right_shift}
            
            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False
            
    def import_style(self, filename):
        """
        import axis style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> x_axis.import_style("style.json")

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
                if 'min' in style.keys():
                    self.min = style['min']
                if 'max' in style.keys():
                    self.max = style['max']
                if 'label' in style.keys():
                    self.label = style['label']
                if 'intervals' in style.keys():
                    self.intervals = style['intervals']
                if 'label_size' in style.keys():
                    self.label_size = style['label_size']
                if 'label_color' in style.keys():
                    self.label_color = style['label_color']
                if 'value_size' in style.keys():
                    self.value_size = style['value_size']
                if 'value_color' in style.keys():
                    self.value_color = style['value_color']
                if 'left_shift' in style.keys():
                    self.left_shift = style['left_shift']
                if 'right_shift' in style.keys():
                    self.right_shift = style['right_shift']
                return True
            else:
                return False

    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, min):
        if isinstance(min, (int, float)):
            self._min = min

    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, max):
        if isinstance(max, (int, float)):
            self._max = max

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def intervals(self):
        return self._intervals
    
    @intervals.setter
    def intervals(self, intervals):
        if isinstance(intervals, int):
            if 0 < intervals:
                self._intervals = intervals

    @property
    def label_size(self):
        return self._label_size
    
    @label_size.setter
    def label_size(self, label_size):
        if isinstance(label_size, (int, float)):
            if 0 <= label_size:
                self._label_size = label_size

    @property
    def label_color(self):
        return self._label_color
    
    @label_color.setter
    def label_color(self, color):
        if color in colors.keys():
            self._label_color = color

    @property
    def value_size(self):
        return self._value_size
    
    @value_size.setter
    def value_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._value_size = size

    @property
    def value_color(self):
        return self._value_color

    @value_color.setter
    def value_color(self, color):
        if color in colors.keys():
            self._value_color = color

    @property
    def left_shift(self):
        return self._left_shift
    
    @left_shift.setter
    def left_shift(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._left_shift = shift

    @property
    def right_shift(self):
        return self._right_shift
    
    @right_shift.setter
    def right_shift(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._right_shift = shift
