import numpy as np

from pyLong.misc.intersect import intersection
from pyLong.profiles.zprofile import zProfile


class Mezap:    
    def __init__(self):        
        self._name = "new mezap"

        self._results = {'zprofile': zProfile(),
                         'reverse': False,
                         'x_start': 0.,
                         'z_start': 0.,
                         'distances': [],
                         'angles': [],
                         'areas': [],
                         'cumulated_area': [],
                         'denominators': [],
                         'normalized_areas': [],
                         'intersections': [],
                         'success': False}
        
    """
    Methods:
    - check_limits
    - reset
    - run
    """

    @staticmethod
    def check_limits(limits):
        try:
            limits = np.loadtxt(limits)
        except:
            return False
        
        if np.shape(limits)[0] < 2 or np.shape(limits)[1] < 4:
            return False
        
        areas = limits[:, 0]
        if len(areas[areas < 0]) != 0 or len(areas[areas > 1]) != 0:
            return False
        
        diff_areas = np.diff(areas)

        if len(diff_areas[diff_areas <= 0]) != 0:
            return False
        
        for i in range(1, 4):
            angles = limits[:, i]

            if sorted(angles, reverse=True) != list(angles):
                return False
            
            if len(angles[angles <= 0]) != 0 or len(angles[angles >= 90]) != 0:
                return False
            
        return True
    
    def reset(self):
        """
        clear results

        returns:
        - None - NoneType

        examples:
        >>> mezap.reset()
        
        """
        self._results = {'zprofile': zProfile(),
                         'reverse': False,
                         'x_start': 0.,
                         'z_start': 0.,
                         'distances': [],
                         'angles': [],
                         'areas': [],
                         'cumulated_area': [],
                         'denominators': [],
                         'normalized_areas': [],
                         'intersections': [],
                         'success': False}
    
    def run(self, zprofile, limits, reverse=False, x_start=0.):
        """
        run calculation

        arguments:
        - zprofile: profile - zProfile
        - limits: threshold values filename - str
        - reverse: reverse the profile - bool
        - x_start: start distance (m) - int | float

        returns:
        - True if succes - bool
        - False else - bool

        examples:
        >>> mezap.run(zprofile, limits, x_start=0.)
        
        """
        if not (isinstance(x_start, (int, float)) and isinstance(zprofile, zProfile) and isinstance(reverse, bool)):
            self.reset()
            return False
        
        if not zprofile.x[0] <= x_start <= zprofile.x[-1]:
            self.reset()
            return False
        
        if not Mezap.check_limits(limits):
            self.reset()
            return False
        else:
            limits = np.loadtxt(limits)

        if reverse:
            new_zprofile = zprofile.reverse(zprofile)
            x_mean = (min(zprofile.x) + max(zprofile.x)) / 2
            x_start = 2 * x_mean - x_start
        else:
            new_zprofile = zprofile.duplicate()

        new_zprofile = new_zprofile.truncate(distances=(x_start, new_zprofile.x[-1]))

        if not isinstance(new_zprofile, zProfile):
            self.reset()
            return False
        
        new_zprofile = new_zprofile.translate(dx=-x_start)
        z_start = new_zprofile.z[0]
            
        x = np.array(new_zprofile.x)
        z = np.array(new_zprofile.z)
        
        z_start = z[0]
        
        distances = np.zeros(len(x))
        distances[1:] = np.sqrt((x[1:] - x[:-1])**2 + (z[1:] - z[:-1])**2)
        distances = np.cumsum(distances)
        
        energy_angles = np.zeros(len(x))
        
        energy_angles[1:] = np.degrees([np.arctan2(np.abs(z_start - z), np.abs(0. - x)) for x, z in zip(x[1:], z[1:])])
        
        areas = np.zeros(len(x))
        
        areas[1:] = (x[1:] + x[:-1]) * (z[:-1] - z[1:])
        areas /= 2.
        
        cumulated_areas = np.cumsum(areas)
        
        denominators = np.ones(len(x))
        denominators[1:] = (z_start - z[1:])**2
        
        normalized_areas = cumulated_areas / denominators
        
        intersections = []

        areas, angles = intersection(normalized_areas[1:], energy_angles[1:], limits[:,0], limits[:,3])

        for area, angle in zip(areas, angles):
            intersections.append(("high", float(angle), float(area)))

        areas, angles = intersection(normalized_areas[1:], energy_angles[1:], limits[:,0], limits[:,2])

        for area, angle in zip(areas, angles):
            intersections.append(("medium", float(angle), float(area)))

        areas, angles = intersection(normalized_areas[1:], energy_angles[1:], limits[:,0], limits[:,1])

        for area, angle in zip(areas, angles):
            intersections.append(("low", float(angle), float(area)))

        if reverse:
            x_start = 2 * x_mean - x_start
            
        self._results = {'zprofile': zprofile,
                         'reverse': reverse,
                         'x_start': x_start,
                         'z_start': z_start,
                         'distances': list(distances),
                         'angles': list(energy_angles),
                         'areas': list(areas),
                         'cumulated_area': list(cumulated_areas),
                         'denominators': list(denominators),
                         'normalized_areas': list(normalized_areas),
                         'intersections': intersections,
                         'success': True}
        return True
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name
            
    @property
    def results(self):
        if self._results['success']:
            return self._results
        else:
            return {'success': False}
        
    def __repr__(self):
        return f"{self._name}"
