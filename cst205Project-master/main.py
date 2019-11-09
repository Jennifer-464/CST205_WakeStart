from flask import Flask, render_template, redirect, request, url_for, session
from flask_bootstrap import Bootstrap
import weather
from db import Database
import os
import alarm
from threading import Thread
import clothing


list_l = None

data_base = Database()

alarm_active = False
alarm_usr = None
process = None
cloth = None

# Function calls the weather API and alarm to generate the weather forecast and
# set alarm for user
def api_call():
	global list_l
	global process
	global cloth
	global alarm_usr

	# Collects the location of the user
	location = data_base.get_location()

	# Gives the weather forecast to the user
	weather_i = weather.Weather(location['city'],
	 location['state'],'United States')

	# Gives the weather forecast to the user
	list_l = weather_i.get_weather('current')

	# Gives the user an outfit recommendation for the day based on temperature
	cloth = clothing.recommendation(list_l
		['temperature']['temp'], list_l['status'])

	# Sets alarm
	if data_base.field_exist('alarm'):
		alarm_usr = data_base.get_alarm()


app = Flask(__name__)

Bootstrap = Bootstrap(app)

# Checks if user is logged in
app.secret_key = os.urandom(12)

@app.route('/', methods=['GET','POST'])
def home():
	global process

	# Starts up home page
	if not session.get('logged_in'):
		return redirect(url_for('login'))

	# If the user is not logged in, user is redirected to the login page
	elif session['logged_in'] == False:
		return redirect(url_for('login'))

	# If login succeeds, user is redirected to settings page
	elif not data_base.field_exist('location'):
		return redirect(url_for('settings'))
		# api_call() function is called to show weather info for location and outfit
	# recommendation for the day based on forecast. Alarm is also set
	api_call()
	if alarm_usr is not None:
		process = Thread(target=alarm.timeUser,
			 args = [alarm_usr])
		process.start()

	if request.method == 'POST':

		if request.form.get('Stop Alarm'):
			alarm.stopAlarm()
			data_base.alarm_none()


	return render_template('home.html', weather_info = list_l, cloth = cloth, alarm = alarm_usr)
@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['submit_button'] == 'Login':

		# Checks database for user information
			data_base.set_credentials(request.form['username'], request.form['password'])

			# If user information is correct to database information, then user
			# is redirected to the home page
			if data_base.user_exist():
				session['logged_in'] = True

				return redirect(url_for('home'))
			else:
			# If user information is correct to database information, then user
			# is redirected to the home page
				error = 'Invalid credentials. Pleaase try again.'

		if request.form['submit_button'] == 'Create Account':
			return redirect(url_for('create_account'))
	return render_template('login.html', error=error)

@app.route('/logout')
# Redircted to login page once signed out
def logout():
	session['logged_in'] = False
	return home()

@app.route('/create_account', methods=['GET','POST'])
def create_account():
	error = None
	if request.method == 'POST':
		# Checks for username and password in database
		data_base.set_credentials(request.form['username'],request.form['password'])
		# If user information is not in database, then create user
		if not data_base.user_exist():
			data_base.create_user()
			session['logged_in'] = True
			return redirect(url_for('home'))
		else:
			error = 'User with that username already exsist'
	return render_template('create_account.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
		# Sets the inputted location from user
		data_base.set_location(request.form['city'],request.form['state'],'US')
		# Sets alarm inputted by user
		data_base.set_alarm(request.form['usr_time'])
	return render_template('settings.html')

if __name__ == "__main__":
	app.run(debug=True)