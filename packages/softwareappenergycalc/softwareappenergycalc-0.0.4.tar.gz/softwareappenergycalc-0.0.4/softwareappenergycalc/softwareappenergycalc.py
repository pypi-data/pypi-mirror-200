from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler

csv_handler = CSVHandler('custom_energy_data.csv')

def custom_measure_energy():
	print('Trigger custom measure energy function')


@measure_energy(handler=csv_handler)
def custom_csv_handler():
# Instructions to be evaluated.

    for _ in range(100):
        custom_csv_handler()

csv_handler.save_data()
