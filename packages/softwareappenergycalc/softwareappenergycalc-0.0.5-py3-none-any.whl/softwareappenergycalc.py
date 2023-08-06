from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler

csv_handler = CSVHandler('custom_energy_data.csv')

def custom_measure_energy():
	print('Trigger custom measure energy function')


@measure_energy(handler=csv_handler)
def custom_csv_handler():
    print('Trigger custom csv handler function')
    for _ in range(10):
        custom_csv_handler()

csv_handler.save_data()
