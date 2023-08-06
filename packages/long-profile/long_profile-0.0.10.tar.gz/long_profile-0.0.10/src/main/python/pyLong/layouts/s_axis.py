import json
import os

from pyLong.dictionnaries.colors import colors


class sAxis:
    def __init__(self):
        self._min_percent = 0.

        self._max_percent = 100.

        self._min_degree = 0.

        self._max_degree = 90.

        self._label = "slope"

        self._intervals_percent = 10

        self._intervals_degree = 9

        self._decimals_percent = 1

        self._decimals_degree = 1

        self._label_size = 11.

        self._label_color = "Black"

        self._value_size = 11.

        self._value_color = "Black"

        self._lower_shift_percent = 0.

        self._upper_shift_percent = 0.

        self._lower_shift_degree = 0.

        self._upper_shift_degree = 0.

    """
    Methods:
    - copy_style
    - duplicate
    - export_style
    - import_style
    """

    def copy_style(self, s_axis):
        """
        copy the style of a slope axis

        arguments:
        - s_axis: axis whose style is to be copied - sAxis

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_s_axis.copy_style(s_axis)
        
        """
        if isinstance(s_axis, sAxis):
            self._min_percent = s_axis.min_percent
            self._max_percent = s_axis.max_percent
            self._min_degree = s_axis.min_degree
            self._max_degree = s_axis.max_degree
            self._label = s_axis.label
            self._intervals_percent = s_axis.intervals_percent
            self._intervals_degree = s_axis.intervals_degree
            self._label_size = s_axis.label_size
            self._label_color = s_axis.label_color
            self._value_size = s_axis.value_size
            self._value_color = s_axis.value_color
            self._lower_shift_percent = s_axis.lower_shift_percent
            self._upper_shift_percent = s_axis.upper_shift_percent
            self._lower_shift_degree = s_axis.lower_shift_degree
            self._upper_shift_degree = s_axis.upper_shift_degree
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the axis

        returns:
        - new_s_axis: duplicated axis - sAxis

        examples:
        >>> new_s_axis = s_axis.duplicate()
        
        """
        new_s_axis = sAxis()
        new_s_axis.copy_style(self)

        return new_s_axis

    def export_style(self, filename):
        """
        export axis style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> s_axis.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'min_percent': self._min_percent,
                     'max_percent': self._max_percent,
                     'min_degree': self._min_degree,
                     'max_degree': self._max_degree,
                     'label': self._label,
                     'intervals_percent': self._intervals_percent,
                     'intervals_degree': self._intervals_degree,
                     'label_size': self._label_size,
                     'label_color': self._label_color,
                     'value_size': self._value_size,
                     'value_color': self._value_color,
                     'lower_shift_percent': self._lower_shift_percent,
                     'upper_shift_percent': self._upper_shift_percent,
                     'lower_shift_degree': self._lower_shift_degree,
                     'upper_shift_degree': self._upper_shift_degree}            
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
        >>> s_axis.import_style("style.json")

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
                if 'min_percent' in style.keys():
                    self.min_percent = style['min_percent']
                if 'max_percent' in style.keys():
                    self.max_percent = style['max_percent']
                if 'min_degree' in style.keys():
                    self.min_degree = style['min_degree']
                if 'max_degree' in style.keys():
                    self.max_degree = style['max_degree']
                if 'label' in style.keys():
                    self.label = style['label']
                if 'intervals_percent' in style.keys():
                    self.intervals_percent = style['intervals_percent']
                if 'intervals_degree' in style.keys():
                    self.intervals_degree = style['intervals_degree']
                if 'decimals_percent' in style.keys():
                    self.decimals_percent = style['decimals_percent']
                if 'decimals_degree' in style.keys():
                    self.decimals_degree = style['decimals_degree']    
                if 'label_size' in style.keys():
                    self.label_size = style['label_size']
                if 'label_color' in style.keys():
                    self.label_color = style['label_color']
                if 'value_color' in style.keys():
                    self.value_color = style['value_color']
                if 'value_size' in style.keys():
                    self.value_size = style['value_size']
                if 'lower_shift_percent' in style.keys():
                    self.lower_shift_percent = style['lower_shift_percent']
                if 'upper_shift_percent' in style.keys():
                    self.upper_shift_percent = style['upper_shift_percent']
                if 'lower_shift_degree' in style.keys():
                    self.lower_shift_degree = style['lower_shift_degree']
                if 'upper_shift_degree' in style.keys():
                    self.upper_shift_degree = style['upper_shift_degree']
                return True
            else:
                return False

    @property
    def min_percent(self):
        return self._min_percent
    
    @min_percent.setter
    def min_percent(self, min):
        if isinstance(min, (int, float)):
            self._min_percent = min

    @property
    def max_percent(self):
        return self._max_percent
    
    @max_percent.setter
    def max_percent(self, max):
        if isinstance(max, (int, float)):
            self._max_percent = max

    @property
    def min_degree(self):
        return self._min_degree
    
    @min_degree.setter
    def min_degree(self, min):
        if isinstance(min, (int, float)):
            self._min_degree = min

    @property
    def max_degree(self):
        return self._max_degree
    
    @max_degree.setter
    def max_degree(self, max):
        if isinstance(max, (int, float)):
            self._max_degree = max

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def intervals_percent(self):
        return self._intervals_percent
    
    @intervals_percent.setter
    def intervals_percent(self, intervals):
        if isinstance(intervals, int):
            if 0 < intervals:
                self._intervals_percent = intervals

    @property
    def intervals_degree(self):
        return self._intervals_degree
    
    @intervals_degree.setter
    def intervals_degree(self, intervals):
        if isinstance(intervals, int):
            if 0 < intervals:
                self._intervals_degree = intervals

    @property
    def decimals_percent(self):
        return self._decimals_percent
    
    @decimals_percent.setter
    def decimals_percent(self, decimals):
        if isinstance(decimals, int):
            if 0 <= decimals:
                self._decimals_percent = decimals
    
    @property
    def decimals_degree(self):
        return self._decimals_degree
    
    @decimals_degree.setter
    def decimals_degree(self, decimals):
        if isinstance(decimals, int):
            if 0 <= decimals:
                self._decimals_degree = decimals

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
    def lower_shift_percent(self):
        return self._lower_shift_percent
    
    @lower_shift_percent.setter
    def lower_shift_percent(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._lower_shift_percent = shift

    @property
    def upper_shift_percent(self):
        return self._upper_shift_percent
    
    @upper_shift_percent.setter
    def upper_shift_percent(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._upper_shift_percent = shift

    @property
    def lower_shift_degree(self):
        return self._lower_shift_degree
    
    @lower_shift_degree.setter
    def lower_shift_degree(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._lower_shift_degree = shift

    @property
    def upper_shift_degree(self):
        return self._upper_shift_degree
    
    @upper_shift_degree.setter
    def upper_shift_degree(self, shift):
        if isinstance(shift, (int, float)):
            if 0 <= shift:
                self._upper_shift_degree = shift
