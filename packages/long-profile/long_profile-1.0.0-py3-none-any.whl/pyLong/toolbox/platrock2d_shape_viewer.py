import os
from math import ceil, pi

import numpy as np
from scipy.interpolate import interp1d
import tables

from pyLong.profiles.zprofile import zProfile
from pyLong.toolbox.trajectory import Trajectory

class PlatRock2DShapeViewer:
    def __init__(self):
        self._name = "new platrock-2D-shape viewer"

        self._terrain = zProfile()
        
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

    @staticmethod
    def radius(V):
        """
        calculate the equivalent sphere radius for a given volume

        arguments:
        - V: volume (m3) - int | float

        returns:
        - r: radius (m) - int | float
        or
        - None - NoneType

        examples:
        >>> r = viewer.radius(2.)

        """
        if not isinstance(V, (int, float)):
            return None
        elif not 0 <= V:
            return None
        else:
            r = ((3. * V) / (4. * pi))**(1./3.)
            return r

    def rocks_number(self):
        """
        extract the number of rocks

        returns:
        - n: number of rocks - int
        or
        - None - NoneType

        examples:
        >>> n = viewer.rocks_number()

        """
        if self._hdf5 is not None:
            return int(self._hdf5.get_node("/rocks/start_data", "").shape[0])
        else:
            return None
        
    def start_data(self):
        """
        extract the start data (Volume, Density, Inertia) of all the rocks

        returns:
        - start_data: volume, density, inertia - list
        or
        - None - NoneType

        examples:
        >>> start_data = viewer.start_data()

        """
        if self._hdf5 is not None:
            data = self._hdf5.get_node("/rocks/start_data", "").read()
            start_data = []

            for item in data:
                volume = float(item[0])
                density = float(item[1])
                inertia = float(item[2])

                start_data.append((volume,
                                   density,
                                   inertia))
                
            return start_data
        else:
            return None
        
    def volumes(self):
        """
        extract the volumes of all the rocks

        returns:
        - volumes: rocks volumes - list
        or
        - None - NoneType

        examples:
        >>> volumes = viewer.volumes()

        """
        start_data = self.start_data()

        if start_data is not None:
            return [v for v, d, i in start_data]
        else:
            return None
        
    def densities(self):
        """
        extract the densities of all the rocks

        returns:
        - densities: rocks densities - list

        examples:
        >>> densities = viewer.densities()

        """
        start_data = self.start_data()

        if start_data is not None:
            return [d for v, d, i in start_data]
        else:
            return None
        
    def inertias(self):
        """
        extract the inertias of all the rocks

        returns:
        - inertias: rocks inertias - list
        or
        - None - NoneType

        examples:
        >>> inertias = viewer.inertias()

        """
        start_data = self.start_data()

        if start_data is not None:
            return [i for v, d, i in start_data]
        else:
            return None
        
    def x_starts(self):
        """
        extract the start distances of all the rocks

        returns:
        - x_starts: start distances - list
        or
        - None - NoneType

        examples:
        >>> x_starts = viewer.x_starts()

        """
        n = self.rocks_number()

        if n is not None:
            x_starts = []
        
            for i in range(n):
                contacts = self.get_contacts(i)
                if contacts is not None:
                    if contacts[0][0] == 0:
                        x_starts.append(contacts[0][1])
            return x_starts
        else:
            return None

    def x_ends(self):
        """
        extract the end distances, if possible, of all the rocks

        returns:
        - x_ends: end distances - list
        or
        - None - NoneType

        examples:
        >>> x_ends = viewer.x_ends()

        """
        n = self.rocks_number()

        if n is not None:
            x_ends = []

            for i in range(n):
                contacts = self.get_contacts(i)
                if contacts is not None:
                    if contacts[-1][0] == 5:
                        x_ends.append(contacts[-1][1])
            return x_ends
        else:
            return None

    def get_contacts(self, i):
        """
        extract the contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - contacts: contacts - list
        or
        - None - NoneType

        examples:
        >>> contacts = viewer.get_contacts(5)

        """
        if self._hdf5 is None:
            return None
        elif not isinstance(i, int):
            return None
        elif self.rocks_number() is None:
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
        
    def get_codes(self, i):
        """
        extract the codes from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - codes: codes - list
        or
        - None - NoneType

        examples:
        >>> codes = viewer.get_codes(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            codes = [code for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return codes
        
    def get_distances(self, i):
        """
        extract the distances from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - distances: distances - list
        or
        - None - NoneType

        examples:
        >>> distances = viewer.get_distances(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            distances = [x for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return distances
        
    def get_altitudes(self, i):
        """
        extract the altitudes from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - altitudes: altitudes - list
        or
        - None - NoneType

        examples:
        >>> altitudes = viewer.get_altitudes(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            altitudes = [z for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return altitudes
        
    def get_x_speeds(self, i):
        """
        extract the horizontal speeds from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - speeds: horizontal speeds - list
        or
        - None - NoneType

        examples:
        >>> speeds = viewer.get_x_speeds(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            speeds = [vx for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return speeds
        
    def get_z_speeds(self, i):
        """
        extract the vertical speeds from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - speeds: vertical speeds - list
        or
        - None - NoneType

        examples:
        >>> speeds = viewer.get_z_speeds(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            speeds = [vz for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return speeds
        
    def get_w_speeds(self, i):
        """
        extract the rotation speeds from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - speeds: rotation speeds - list
        or
        - None - NoneType

        examples:
        >>> speeds = viewer.get_w_speeds(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            speeds = [w for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return speeds

    def get_x_normals(self, i):
        """
        extract the horizontal components of the normal vector from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - normals: horizontal components of the normal vector - list
        or
        - None - NoneType

        examples:
        >>> speeds = viewer.get_x_normals(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            speeds = [Nx for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return speeds
        
    def get_z_normals(self, i):
        """
        extract the vertical components of the normal vector from contacts data of rock n°i

        arguments:
        - i: rock number - int

        returns:
        - normals: vertical components of the normal vector - list
        or
        - None - NoneType

        examples:
        >>> speeds = viewer.get_z_normals(5)

        """
        contacts = self.get_contacts(i)

        if contacts is None:
            return None
        else:
            speeds = [Nz for code, x, z, vx, vz, w, Nx, Nz in contacts]
            return speeds
        
    def has_backtracking(self, i):
        """
        indicate if trajectory of rock n°i has backtracking

        arguments:
        - i: rock number - int

        returns:
        - True | False - bool
        or
        - None - NoneType

        examples:
        >>> has_backtracking = viewer.has_backtracking(5)

        """
        if self._hdf5 is None:
            return None
        
        if not isinstance(i, int):
            return None
        
        n = self.rocks_number()
        if n is None:
            return None
        elif not 0 <= i < n:
            return None

        distances = self.get_distances(i)
        distances = distances[:-1]

        if distances is None:
            return None
        else:
            if True in list(np.diff(distances) <= 0):
                return True
            else:
                return False
        
    def get_z_at(self, x, i):
        """
        extract or interpolates the altitude of rock n°i at a given distance

        arguments:
        - x: distance (m) - int | float
        - i: rock number - int

        returns:
        - z: extrated or interpolated altitude (m) - int | float
        or
        - None: NoneType

        examples:
        >>> z = viewer.get_z_at(10.5, 2)
        
        """
        if self._hdf5 is None:
            return None
        elif not isinstance(i, int):
            return None
        elif self.rocks_number() is None:
            return None
        elif not 0 <= i < self.rocks_number():
            return None
        elif not isinstance(x, (int, float)):
            return None
        
        V = self.volumes()[i]
        if V is None:
            return None
        else:
            radius = PlatRock2DShapeViewer.radius(V)
        
        if radius is None:
            return None
        
        has_backtracking = self.has_backtracking(i)

        if has_backtracking is None:
            return None
        elif has_backtracking is True:
            return None
        
        contacts = self.get_contacts(i)

        if contacts is None:
            return None

        codes = [code for code, x, z, vx, vz, w, Nx, Nz in contacts]
        distances = [x for code, x, z, vx, vz, w, Nx, Nz in contacts]
        altitudes = [z for code, x, z, vx, vz, w, Nx, Nz in contacts]

        if not distances[0] <= x <= distances[-1]:
            return None
        
        d = list(distances)

        if x in d:
            i = d.index(x)
            if codes[i] in [0, 5, 8]:
                return altitudes[i] - radius
            else:
                return None
        else:
            d.append(x)
            d.sort()
            i = d.index(x)

            if codes[i] in [0, 5, 8]:
                a = (altitudes[i] - altitudes[i-1]) / (distances[i] - distances[i-1])
                b = altitudes[i-1]
                z = a * (x - distances[i-1]) + b
                z -= radius

                return z
            else:
                return None
        
    def get_trajectory(self, i, dx=1.):
        """
        generate trajectory of rock n°i

        arguments:
        - i: rock number - int
        - dx: sample distance (m) - int | float

        """
        if self._hdf5 is None:
            return None
        elif not isinstance(i, int):
            return None
        
        n = self.rocks_number()
        if n is None:
            return None
        elif not 0 <= i < n:
            return None
        
        has_backtracking = self.has_backtracking(i)

        if has_backtracking is None:
            return None
        elif has_backtracking is True:
            return None
        
        zprofile = zProfile()

        x_starts = self.x_starts()
        if x_starts is None:
            return None
        else:
            x_start = x_starts[i]

        x_ends = self.x_ends()
        if x_ends is None:
            return None

        d = self.get_distances(i)
        if not d[-1] > d[-2]:
            x_end = x_ends[i]
            distances = list(np.arange(x_start, x_end, dx))
        
            if x_end not in distances:
                distances.append(x_end)
        else:
            x_end = d[-2]
            distances = list(np.arange(x_start, x_end, dx))
        
            if x_end not in distances:
                distances.append(x_end)

        xz = []

        for x in distances:
            x = float(x)
            z = self.get_z_at(x, i)

            if z is not None:
                xz.append((x, z))
            
        zprofile.xz = xz

        return zprofile

    def reset(self):
        self._hdf5 = None

    def from_hdf5(self, filename):
        if not isinstance(filename, str):
            self.reset()
            return False  
        
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