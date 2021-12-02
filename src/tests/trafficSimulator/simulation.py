from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal

class Simulation:
    def __init__(self, config={}):
        
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            
        self.frame_count = 0    
        self.dt = 1/60          
        self.roads = []         
        self.generators = []
        self.traffic_signals = []

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def create_signal(self, roads, config={}):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(roads, config)
        self.traffic_signals.append(sig)
        return sig

    def update(self):
        for road in self.roads:
            road.update(self.dt)

        for gen in self.generators:
            gen.update()

        for signal in self.traffic_signals:
            signal.update(self)

        for road in self.roads:
            
            if len(road.vehicles) == 0: continue
            
            vehicle = road.vehicles[0]
            
            if vehicle.x >= road.length:
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    
                    vehicle.current_road_index += 1
                    
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                   
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                
                road.vehicles.popleft() 
       
        self.t += self.dt
        self.frame_count += 1


    def run(self, steps):
        for _ in range(steps):
            self.update()