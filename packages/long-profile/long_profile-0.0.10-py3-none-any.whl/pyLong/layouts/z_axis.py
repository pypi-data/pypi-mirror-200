import os
import json

from pyLong.dictionnaries.colors import colors


class zAxis:
    def __init__(self):
        self._min = 0.

        self._max = 1000.

        self._label = "altitude (m)"

        self._intervals = 10

        self._label_size = 11.

        self._label_color = "Black"

        self._value_size = 11.

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

    def copy_style(self, z_axis):
        """
        copy the style of an altitude axis

        arguments:
        - z_axis: axis whose style is to be copied - zAxis

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_z_axis.copy_style(z_axis)
        
        """
        if isinstance(z_axis, zAxis):
            self._min = z_axis.min
            self._max = z_axis.max
            self._label = z_axis.label
            self._intervals = z_axis.intervals
            self._label_size = z_axis.label_size
            self._label_color = z_axis.label_color
            self._value_size = z_axis.value_size
            self._value_color = z_axis.value_color
            self._lower_shift = z_axis.lower_shift
            self._upper_shift = z_axis.upper_shift
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the axis

        returns:
        - new_z_axis: duplicated axis - zAxis

        examples:
        >>> new_z_axis = z_axis.duplicate()
        
        """
        new_z_axis = zAxis()
        new_z_axis.copy_style(self)

        return new_z_axis

    def export_style(self, filename):
        """
        export axis style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> z_axis.export_style("style.json")
        
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
        >>> z_axis.import_style("style.json")

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
