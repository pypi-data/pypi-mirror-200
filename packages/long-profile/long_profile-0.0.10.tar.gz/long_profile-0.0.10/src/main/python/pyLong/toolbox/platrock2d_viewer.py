import os
from math import ceil

import numpy as np
from scipy.interpolate import interp1d
import tables

from pyLong.profiles.zprofile import zProfile
from pyLong.toolbox.trajectory import Trajectory

class PlatRock2DViewer:
    def __init__(self):
        self._name = "new platrock-2D viewer"

        self._terrain = zProfile()

        self._isTwoDShape = False
        
        self._hdf5 = None
        
        self.reset()
        
        self._g = 9.81
        
    """
    Methods:
    - from_hdf5
    - get_ends
    - get_starts
    - trajectory
    - get_trajectories
    - reset
    """
    def rocks_number(self):
        if self._hdf5 is not None:
            return int(self._hdf5.get_node("/rocks/start_data", "").shape[0])
        else:
            return None
        
    def start_data(self):
        if self._hdf5 is not None:
            data = self._hdf5.get_node("/rocks/start_data", "").read()
            start_data = []

            for item in data:
                volume = float(item[0])
                density = float(item[1])
                inertia = float(item[2])
                start_data.append([volume,
                                   density,
                                   inertia])
                
            return start_data
        else:
            return None
        
    def volumes(self):
        start_data = self.start_data()

        if start_data is not None:
            return [v for v, d, i in start_data]
        else:
            return None
        
    def densities(self):
        start_data = self.start_data()

        if start_data is not None:
            return [d for v, d, i in start_data]
        else:
            return None
        
    def inertias(self):
        start_data = self.start_data()

        if start_data is not None:
            return [i for v, d, i in start_data]
        else:
            return None
        
    def x_starts(self):
        n = self.rocks_number()
        if n is not None:
            x_starts = []
            for i in range(n):
                contacts = self.contacts(i)
                if contacts[0][0] == 0:
                    x_starts.append(contacts[0][1])
            return x_starts
        else:
            return None

    def x_ends(self):
        n = self.rocks_number()
        if n is not None:
            x_ends = []
            for i in range(n):
                contacts = self.contacts(i)
                if contacts[-1][0] == 5:
                    x_ends.append(contacts[-1][1])
            return x_ends
        else:
            return None

    def contacts(self, i):
        if self._hdf5 is None:
            return None
        elif not isinstance(i, int):
            return None
        elif not 0 <= i < self.rocks_number():
            return None
        else:
            data = self._hdf5.get_node(f"/rocks/contacts/{i}", "").read()
            contacts = []
            for code, x, z, vx, vz, w, Nx, Nz in data:
                contacts.append([int(code),
                                 float(x),
                                 float(z),
                                 float(vx),
                                 float(vz),
                                 float(w),
                                 float(Nx),
                                 float(Nz)])
                
            return contacts
        
    def get_z_at(self, x, i):
        if self._hdf5 is None:
            return None
        elif not isinstance(i, int):
            return None
        elif not 0 <= i < self.rocks_number():
            return None
        elif not isinstance(x, (int, float)):
            return None
        else:
            contacts = self.contacts(i)

        codes = [code for code, x, z, vx, vz, w, Nx, Nz in contacts]
        distances = [x for code, x, z, vx, vz, w, Nx, Nz in contacts]
        altitudes = [z for code, x, z, vx, vz, w, Nx, Nz in contacts]

        if not distances[0] <= x <= distances[-1]:
            return None

        if x not in distances:
            distances.append(x)
            distances.sort()

        try:
            i = distances.index(x)
        except:
            return None
        
        i -= 1

        # if codes[i] == 

        return altitudes[i]

    def reset(self):
        self._isTwoDShape = False
        self._hdf5 = None

    def from_hdf5(self, filename, isTwoDShape=False):
        if not (isinstance(filename, str) and isinstance(isTwoDShape, bool)):
            self.reset()
            return False
        else:
            self._isTwoDShape = isTwoDShape    
        
        if not 0 < len(filename):
            self.reset()
            return False
        elif not os.path.isfile(filename):
            self.reset()
            return False
        else:
            try:
                hdf5 = tables.open_file(filename)
            except:
                self.reset()
                return False
            
        try:
            children = hdf5.root.__members__
        except:
            self.reset()
            return False
        
        if "rocks" not in children:
            self.reset()
            return False
        
        try:
            children = hdf5.get_node("/rocks")
        except:
            return False
        
        if not ("start_data" in children and "contacts" in children):
            self.reset()
            return False
        else:
            self._hdf5 = hdf5
            return True
        

    
    # def from_hdf5(self, filename, zprofile, dx=1.):
    #     if not isinstance(filename, str) or not isinstance(zprofile, zProfile) or not isinstance(dx, (int, float)):
    #         return False
        
    #     if not os.path.isfile(filename):
    #         return False
        
    #     if not 0 < dx:
    #         return False
        
    #     try:
    #         hdf5 = tables.open_file(filename)
    #     except:
    #         hdf5 = None
    #         return False
        
    #     try:
    #         children = hdf5.root.__members__
    #     except:
    #         children = []
    #         return False
        
    #     if 'rocks' not in children:
    #         return False
        
    #     try:
    #         children = hdf5.get_node("/rocks")
    #     except:
    #         children = []
    #         return False
        
    #     if 'start_data' not in children or 'contacts' not in children:
    #         return False
        
    #     start_data = hdf5.get_node("/rocks/start_data")
    #     n = len(start_data)
        
    #     if not 1 < n:
    #         return False
        
    #     self._dx = dx
    #     self._hdf5 = hdf5
    #     self._n = n
        
    #     self._starts = self.get_starts()
    #     self._ends = self.get_ends()
        
    #     if not len(self._starts) == self._n or not len(self._ends) == self._n:
    #         self.reset()
    #         return False
        
    #     if not zprofile.x[0] <= min(self._starts) or not max(self._ends) <= zprofile.x[-1]:
    #         self.reset()
    #         return False
        
    #     self._zprofile = zprofile
        
    #     trajectories = self.get_trajectories()
    #     self._trajectories = trajectories
        
    #     if not len(self._trajectories) == self._n:
    #         self.reset()
    #         return False
        
    #     heights = self.get_heights()
    #     self._heights = heights
        
    #     if not len(self._heights) == self._n:
    #         self.reset()
    #         return False
        
    #     return True
    
    def get_starts(self):
        if self._hdf5:
            starts = []
            for i in range(self._n):
                data = self._hdf5.get_node(f"/rocks/contacts/{i}").read()
                if int(data[0,0]) == 0:
                    start = float(data[0, 1])
                    starts.append(start)
        else:
            starts = []
            
        return starts
    
    def get_ends(self):
        if self._hdf5:
            ends = []
            for i in range(self._n):
                data = self._hdf5.get_node(f"/rocks/contacts/{i}").read()
                if int(data[-1, 0]) in [5, 6]:
                    end = float(data[-1, 1])
                    ends.append(end)
        else:
            ends = []
            
        return ends
    
    def get_heights(self):
        heights = []
        
        for trajectory in self._trajectories:
            height = trajectory.duplicate()
            
            height.xz = [(x, z - self._zprofile.interpolate(x)) for x, z in trajectory.xz]
            
            heights.append(height)
            
        return heights
    
    def get_trajectories(self):
        trajectories = []
        
        for i in range(self._n):
            trajectory = Trajectory()
            
            data = self._hdf5.get_node(f"/rocks/contacts/{i}").read()
            
            trajectory.xz = [(float(data[0, 1]), float(data[0, 2])),
                             (float(data[-1, 1]), float(data[-1, 2]))]
            
            n = len(data)
            
            for j in range(n-1):
                code = int(data[j, 0])

                x_start = float(data[j, 1])
                x_end = float(data[j+1, 1])

                z_start = float(data[j, 2])
                z_end = float(data[j+1, 2])

                vx_start = float(data[j, 3])
                vz_start = float(data[j, 4])

                trajectory.add_point((x_start, z_start))
                trajectory.add_point((x_end, z_end))

                if (x_end - x_start) / self._dx > 1:
                    n = ceil((x_end - x_start) / self._dx)

                    for x in np.linspace(x_start, x_end, n+1):
                        if x == x_start or x == x_end:
                            continue

                        x = float(x)

                        if code in [0, 1, 2]:
                            z = -0.5 * self._g * ((x - x_start) / vx_start)**2 + vz_start * ((x - x_start) / vx_start) + z_start
                            trajectory.add_point((x, z))

                        elif code in [3, 4, 8]:
                            trajectory.add_point((x, self._zprofile.interpolate(x)))

            trajectories.append(trajectory)
        
        return trajectories
    
    def reset(self):
        self._hdf5 = None
        
        self._n = 0
        
        self._dx = 1.
        
        self._zprofile = None
        
        self._starts = []
        
        self._ends = []
        
        self._trajectories = []
        
        self._heights = []
        
    def trajectory(self, i):
        if not self._hdf5:
            return
        
        if not 0 <= i < self._n:
            return
        
        return self._trajectories[i]
    
    def height(self, i):
        if not self._hdf5:
            return
        
        if not 0 <= i < self._n:
            return
        
        return self._heights[i]
    
    def heights_at(self, x, stats=True):
        if not isinstance(x, (int, float)):
            return
        
        if not self._zprofile.x[0] <= x <= self._zprofile.x[-1]:
            return
        
        if not min(self._starts) <= x <= max(self._ends):
            return
        
        if not isinstance(stats, bool):
            return
        
        heights = []
        
        for height in self._heights:
            h = height.interpolate(x)
            if h is not None:
                heights.append(h)
            
        if stats:
            statistics = {}
            statistics['size'] = len(heights)
            statistics['maximum'] = max(heights)
            statistics['minimum'] = min(heights)
            statistics['mean'] = np.mean(heights)
            statistics['std'] = np.std(heights)
            statistics['median'] = np.median(heights)
            
            return heights, statistics
        else:
            return heights
    
    def heights_between(self, x_start, x_end, dx, stats=True):
        if not isinstance(x_start, (int, float)) or not isinstance(x_end, (int, float)) or not isinstance(dx, (int, float)):
            return
        
        if not self._zprofile.x[0] <= x_start < x_end <= self._zprofile.x[-1]:
            return
        
        if not min(self._starts) <= x_start < x_end <= max(self._ends):
            return
        
        if not 0 < dx <= x_end - x_start:
            return
        
        if not isinstance(stats, bool):
            return
        
        heights = []
        
        if (x_end - x_start) / dx > 1:
            n = ceil((x_end - x_start) / dx)

            for x in np.linspace(x_start, x_end, n+1):
                heights += self.heights_at(x, stats=False)
                
        if stats:
            statistics = {}
            statistics['size'] = len(heights)
            statistics['maximum'] = max(heights)
            statistics['minimum'] = min(heights)
            statistics['mean'] = np.mean(heights)
            statistics['std'] = np.std(heights)
            statistics['median'] = np.median(heights)
            
            return heights, statistics
        else:
            return heights
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name

    @property
    def terrain(self):
        return self._terrain
    
    @terrain.setter
    def terrain(self, zprofile):
        if isinstance(zprofile, zProfile):
            self._terrain = zProfile

    @property
    def isTwoDShape(self):
        return self._isTwoDShape
    
    @isTwoDShape.setter
    def isTwoDShape(self, isTwoDShape):
        if isinstance(isTwoDShape, bool):
            self._isTwoDShape = isTwoDShape
            
    @property
    def n(self):
        return self._n 
    
    def __repr__(self):
        return self._title
    
    @property
    def starts(self):
        return list(self._starts)
    
    @property
    def ends(self):
        return list(self._ends)