# Dictionary to recommend basic outfits based on weather forecast
clothing = {
	83: ['fTshirt.png', 'Shorts.png'],
 	67: ['polo.png', 'jeans.png'],
 	53: ['hoodie.png', 'seatpants.png'],
 	52: ['jacket.png', 'sweatpants.png'],
 	'rain': ['rainCoat.png', 'jeans.png']
 	}
def recommendation(temperature, description):
	temperature = int(temperature)
	# Conditional statements give outfit recommendations based on temperature
	# from hot, warm, mild, and cold
	if temperature >= 75:
		items = {'top': clothing[83][0], 'bottom': clothing[83][1]}
		
		return items

	elif temperature >= 67 and temperature <= 74:
		items = {'top': clothing[67][0], 'bottom': clothing[67][1]}
		return items

	elif temperature >= 53 and temperature <= 66:
		items = {'top': clothing[67][0], 'bottom': clothing[67][1]}
		return items

	elif temperature <= 52:
		return clothing[52]