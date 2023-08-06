import json
import os

from pyLong.dictionnaries.colors import colors


class yAxis:
    def __init__(self):
        self._min = 0.

        self._max = 1000.

        self._label = ""

        self._intervals = 5

        self._label_color = "Black"

        self._value_color = "Black"

        self._lower_shift = 0.

        self._upper_shift = 0.

    """
    Methods:
    - copy_style
    - duplicate
    - export_style
    - import_style
    """

    def copy_style(self, y_axis):
        """
        copy the style of a value axis

        arguments:
        - y_axis: axis whose style is to be copied - yAxis

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_y_axis.copy_style(y_axis)
        
        """
        if isinstance(y_axis, yAxis):
            self._min = y_axis.min
            self._max = y_axis.max
            self._label = y_axis.label
            self._intervals = y_axis.intervals
            self._label_color = y_axis.label_color
            self._value_color = y_axis.value_color
            self._lower_shift = y_axis.lower_shift
            self._upper_shift = y_axis.upper_shift
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the axis

        returns:
        - new_y_axis: duplicated axis - yAxis

        examples:
        >>> new_y_axis = y_axis.duplicate()
        
        """
        new_y_axis = yAxis()
        new_y_axis.copy_style(self)

        return new_y_axis

    def export_style(self, filename):
        """
        export axis style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> y_axis.export_style("style.json")
        
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
                     'label_color': self._label_color,
                     'value_color': self._value_color,
                     'lower_shift': self._lower_shift,
                     'upper_shift': self._upper_shift}
            
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
        >>> y_axis.import_style("style.json")

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
                if 'label_color' in style.keys():
                    self.label_color = style['label_color']
                if 'value_color' in style.keys():
                    self.value_color = style['value_color']
                if 'lower_shift' in style.keys():
                    self.lower_shift = style['lower_shift']
                if 'upper_shift' in style.keys():
                    self.upper_shift = style['upper_shift']
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
    def label_color(self):
        return self._label_color
    
    @label_color.setter
    def label_color(self, color):
        if color in colors.keys():
            self._label_color = color

    @property
    def value_color(self):
        return self._value_color

    @value_color.setter
    def value_color(self, color):
        if color in colors.keys():
            self._value_color = color

    @property
    def lower_shift(self):
        return self._lower_shift
    
    @lower_shift.setter
    def lower_shift(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._lower_shift = shift

    @property
    def upper_shift(self):
        return self._upper_shift
    
    @upper_shift.setter
    def upper_shift(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._upper_shift = shift
