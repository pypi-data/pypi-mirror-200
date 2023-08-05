import os
from pickle import Pickler, Unpickler

from objects import layout, group

from pyLong.profiles import zprofile, sprofile


class Project:
    def __init__(self):      
        self.version = "dev"
        
        self.path = ""
        
        self.layouts = []
        
        self.subplots = []
        
        self.profiles = []

        self.groups = []
        
        self.calculations = []
        
        self.extra_data = []
        
        self.reminder_lines = []
        
    """
    Methods:
    - clear(self)
    - load(self, filename)
    """
            
    def clear(self):
        self.path = ""
        
        self.layouts.clear()
        layout_0 = layout.Layout()
        layout_0.title = "layout 0"
        self.layouts.append(layout_0)
        
        self.subplots.clear()
        
        self.groups.clear()
        group_0 = group.Group()
        group_0.title = "group 0"
        self.groups.append(group_0)
        
        self.profiles.clear()
        self.calculations.clear()
        self.extra_data.clear()
        self.reminder_lines.clear()
        
    def load(self, filename):
        if not isinstance(filename, str):
            return False
        if not filename[-6:] == "pyLong":
            return False
        if not os.path.isfile(filename):
            return False
        
        with open(filename, 'rb') as file:
            try:
                my_unpickler = Unpickler(file)
                project = my_unpickler.load()
            except:
                return False
        
        if not "version" in dir(project):
            return False
        
        if not project.version == "dev":
            return False
        
        if project.version == "dev":
            self.clear()
            
            self.version = project.version
            self.path = filename
            self.layouts = project.layouts
            self.subplots = project.subplots
            self.groups = project.groups
            self.profiles = project.profiles
            self.calculations = project.calculations
            self.extra_data = project.extra_data
            
            return True