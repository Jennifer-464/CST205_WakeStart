import pyowm

API_KEY = '20a45fcdfc49bcb5926c0da719e6768b'

class Weather:
	"""Class weather request"""
	def __init__(self, city, state, country):
		self.location = city +","+ state + "," + country
		#API call
		self.owm = pyowm.OWM(API_KEY)

	def current_weather(self):
		#search for current given location 
		observ = self.owm.weather_at_place(self.location)
		self.current_details = observ.get_weather()


	def three_hour(self):
		#search for three forecast 
		fc = self.owm.three_hours_forecast(self.location)
		forecast_three_Hr = fc.get_forecast()
		self.three_hr_weather = forecast_three_Hr.get_weathers()

	def get_weather(self,type_forecast):
		list_temps = []
		#conditonal to see what type of is being returned
		if 'current' == type_forecast:
			current_weather_info = {}
			self.current_weather()
		
			current_weather_info.update({'temperature':
				self.current_details.get_temperature('fahrenheit') })

			current_weather_info.update({'humidity':
				self.current_details.get_humidity()})

			current_weather_info.update({'wind':
				self.current_details.get_wind()})

			current_weather_info.update({'status':
				self.current_details.get_detailed_status()})

			current_weather_info.update({'url':
				self.current_details.get_weather_code()})

			current_weather_info.update({'time':
				self.current_details.get_reference_time('iso')})
			return current_weather_info
		elif 'three' == type_forecast:
			self.three_hour()

			for temp in self.three_hr_weather:
				list_temps.append([temp.get_temperature('fahrenheit'),
					temp.get_humidity(),
					temp.get_wind(),
					temp.get_detailed_status(),
					temp.get_weather_code(),
					temp.get_reference_time('iso')])

			return list_temps