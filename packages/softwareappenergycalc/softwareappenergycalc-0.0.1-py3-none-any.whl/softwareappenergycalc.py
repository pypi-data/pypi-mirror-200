from pyJoules.energy_meter import measure_energy

@measure_energy
def custom_measure_energy():
	print('Trigger custom measure energy function')

custom_measure_energy()