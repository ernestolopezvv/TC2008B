from .vehicle import Vehicle
from numpy.random import randint

class VehicleGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self.init_properties()

    def set_default_config(self):
        """Set default configuration"""
        self.vehicle_rate = 20
        self.vehicles = [
            (1, {})
        ]
        self.last_added_time = 0

    def init_properties(self):
        self.upcoming_vehicle = self.generate_vehicle()

    def generate_vehicle(self):
        """Returns a random vehicle from self.vehicles with random proportions"""
        total = sum(pair[0] for pair in self.vehicles)
        r = randint(1, total+1)
        for (weight, config) in self.vehicles:
            r -= weight
            if r <= 0:
                return Vehicle(config)

    def update(self):
        """Add vehicles"""
        if self.sim.t - self.last_added_time >= 60 / self.vehicle_rate:
        
            road = self.sim.roads[self.upcoming_vehicle.path[0]]      
            if len(road.vehicles) == 0\
               or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.l:
                
                self.upcoming_vehicle.time_added = self.sim.t
                road.vehicles.append(self.upcoming_vehicle)
                
                self.last_added_time = self.sim.t
            self.upcoming_vehicle = self.generate_vehicle()

