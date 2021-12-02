from trafficSimulator import *


sim = Simulation()

sim.create_roads([
    ((0, 100), (148, 100)),
    ((148, 100), (300, 100)),

    ((300, 95), (158, 95)),
    ((158, 95), (0, 95)),
    
    ((150, 0), (150, 92)),
    ((150, 92), (150, 200)),

    ((155, 200), (155, 102)),
    ((155, 102), (155, 0))
])

sim.create_gen({
    'vehicle_rate': 12,
    'vehicles': [
        [1, {"path": [0, 1]}],
        [1, {"path": [2, 3]}],
        [1, {"path": [4, 5]}],
        [1, {"path": [6, 7]}]
    ]
})

sim.create_signal([[0], [4]])
sim.create_signal([[2], [6]])


win = Window(sim)
win.offset = (-150, -110)
win.run(steps_per_update=5)