import psycopg2
import random
import radar
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go 

class TableCreate():
	pass
		
	
	#This is where we generate data for auto created tables. 
	#This function will connect to the db and generate 88 rows or random rolls and dates. 
	#We also take the average of the sessions (rolls) and insert that into the database as well.
	def create_new_table(self, die_table):
		conn = psycopg2.connect("dbname=dnd user=postgres host=localhost")
		curs = conn.cursor()
		try:
			curs.execute("CREATE TABLE {} (id serial PRIMARY KEY, avg integer, rolls integer ARRAY, date varchar);".format(die_table))
		except psycopg2.Error as e:
		 	print(e.pgcode)
		x = 0
		#this ensures that the max length of the random numbers is not greater than the die
		max_len = int(die_table[1:]) + 1
		#while loop will generate random rolls for our database - 88 rows always. 
		while x != 88:
			y = 0
			rolls = []
			listlen = random.randrange(8, 29)
			while listlen != y:
				rolls.append(random.randrange(1,max_len))
				y += 1
			avg = sum(rolls) / len(rolls)
			date = radar.random_datetime(start='2016-01-01', stop='2017-12-31')
			x += 1
			curs.execute("INSERT INTO {} (avg, rolls, date) VALUES (%s, %s, %s)".format(die_table),(avg, rolls, date)) 
		conn.commit()
		conn.close()
		#confirmation that the post to database was successful
		print("Okay you should have your table filled with test data now. If that didn't work, ¯\_(ツ)_/¯ \n\n")

	#This is where we query the database to ensure we have enough tables to generate a graph. 
	def table_count(self):
		conn = psycopg2.connect("dbname=dnd user=postgres host=localhost")
		curs = conn.cursor()
		curs.execute("select table_name from information_schema.tables where table_schema='public';")
		num_of_tables = curs.fetchall()
		print("There are {} tables in your database. \n{}".format(len(num_of_tables), num_of_tables))
		conn.close()
		if len(num_of_tables) < 6:
			print("You only have {} tables in your database. You will need a full database to generate pretty graphs. Select Help in the options menu for details.\n\n".format(len(num_of_tables)))
		elif len(num_of_tables) == 6:
			print("Your database is ready to go! Let's print pretty graphs.\n\n")
		else:
			print("Not sure why you're seeing this. You may have too many tables in your databse. See Help in the options menu for details.\n\n")
		
	#This is where you would manually input data into your database. 
	#Normal use would be to use this function mainly. For demo purposes we will not.
	def manual_data(self):
		conn = psycopg2.connect("dbname=dnd user=postgres host=localhost")
		curs = conn.cursor()
		#user selects die, inputs rolls, inputs date, we calculate the avg - then it is sent to the db.
		die = input("Which die do you want to start with? ")
		user_input = input("Enter your die rolls separated by commas: ")
		rolls = user_input.split(",")
		int_rolls = []
		for i in rolls:
			int_rolls.append(int(i))
		date = input("Enter session date in MM/DD/YYYY format: ")
		avg = len(int_rolls) / sum(int_rolls)
		try:
			curs.execute("CREATE TABLE {} (id serial PRIMARY KEY, avg integer, rolls integer ARRAY, date varchar);".format(die))
		except psycopg2.Error as e:
		 	print(e.pgcode)
		curs.execute("INSERT INTO {} (avg, rolls, date) VALUES (%s, %s, %s)".format(die),(avg, int_rolls, date))
		conn.commit()
		conn.close()
		#confirmation of success!
		print("Table created and data entered with no errors (probably). Select 'Show Database' at the options menu to confirm.\n")

	#This prints a long help message similar to a readme file.
	def help(self):
		print("""Welcome to the D&D Dice Tracker. The Dice Tracker will take all of your data and make a graph. The Dice Tracker requires that you have a Postgres database. It may be compatible with other SQL type databases. I have no idea. You will need to have SIX tables in your database - d4 , d6 , d8 , d10 , d12 , and d20 to use the Graph function. You can get the Graph function to work with a single table or even multiple tables! However, you will need to edit the graph_generate() in the tablecreate file. Best of luck and thank you for using the D&D Dice Tracker. \n\n
			""")
	#This is where we select the die for auto creating tables. there is error checking for input sanitization built-in.
	def random_data(self):
		table_options = ["d4", "d6", "d8", "d10", "d12", "d20"]
		die_table = input("Select table to create: [d4, d6, d8, d10, d12, d20]\n")
		if die_table.lower() not in table_options:
			print("Error. Invalid selection. Aborting...")
			exit()
		else:
			return die_table


	#Okay this is where we generate the graph. Lots of repeating code coming in here. 
	#We will be pulling data from the corresponding db and adding it to a list. then generating graph.
	def graph_generate(self):
		

		def plotly():
			#d4 data here
			curs.execute("SELECT avg, rolls, date FROM d4 ORDER BY date")

			event_avgs_d4 = []
			event_rolls_d4 = []
			event_dates_d4 = []

			#here we are adding the data to list to prep for graphing
			for row in curs.fetchall():
				event_avgs_d4.append(row[0])
				event_rolls_d4.append(row[1])
				event_dates_d4.append(row[2])
			print("#" * 50)

			#formatting the lines and entering data to be graphed.
			d4 = go.Scatter(y=event_avgs_d4 , x=event_dates_d4, name="d4  data", line=dict(color=('rgb(2,6,82)'), width=3))


			#d6 data here
			curs.execute("SELECT avg, rolls, date FROM d4 ORDER BY date")

			event_avgs_d6 = []
			event_rolls_d6 = []
			event_dates_d6 = []

			for row in curs.fetchall():
				event_avgs_d6.append(row[0])
				event_rolls_d6.append(row[1])
				event_dates_d6.append(row[2])
			print("#" * 50)

			d6 = go.Scatter(y=event_avgs_d6 , x=event_dates_d6, name="d6 data", line=dict(color=('rgb(91,117,100)'), width=3))

			#d8 data here
			curs.execute("SELECT avg, rolls, date FROM d8 ORDER BY date")

			event_avgs_d8 = []
			event_rolls_d8 = []
			event_dates_d8 = []

			for row in curs.fetchall():
			    event_avgs_d8.append(row[0])
			    event_rolls_d8.append(row[1])
			    event_dates_d8.append(row[2])
			print("#" * 50)

			d8 = go.Scatter(y=event_avgs_d8 , x=event_dates_d8, name="d8 data", line=dict(color=('rgb(242,203,189)'), width=3))

			#d10 data here
			curs.execute("SELECT avg, rolls, date FROM d10 ORDER BY date")

			event_avgs_d10 = []
			event_rolls_d10 = []
			event_dates_d10 = []

			for row in curs.fetchall():
			    event_avgs_d10.append(row[0])
			    event_rolls_d10.append(row[1])
			    event_dates_d10.append(row[2])
			print("#" * 50)

			d10 = go.Scatter(y=event_avgs_d10 , x=event_dates_d10, name="d10 data", line=dict(color=('rgb(89,2,2)'), width=3))

			#d12 data here
			curs.execute("SELECT avg, rolls, date FROM d12 ORDER BY date")

			event_avgs_d12 = []
			event_rolls_d12 = []
			event_dates_d12 = []

			for row in curs.fetchall():
			    event_avgs_d12.append(row[0])
			    event_rolls_d12.append(row[1])
			    event_dates_d12.append(row[2])
			print("#" * 50)

			d12 = go.Scatter(y=event_avgs_d12 , x=event_dates_d12, name="d12 data", line=dict(color=('rgb(20,22,189)'), width=3))

			#d20 data here
			curs.execute("SELECT avg, rolls, date FROM d20 ORDER BY date")

			event_avgs_d20 = []
			event_rolls_d20 = []
			event_dates_d20 = []

			for row in curs.fetchall():
			    event_avgs_d20.append(row[0])
			    event_rolls_d20.append(row[1])
			    event_dates_d20.append(row[2])
			print("#" * 50)

			d20 = go.Scatter(y=event_avgs_d20 , x=event_dates_d20, name="d20 data", line=dict(color=('rgb(240,72,141)'), width=3))

			#finally we can draw the graph!
			data = [d4, d6, d8, d10, d12, d20]
			layout = dict(
			    title='Time series with range slider and selectors',
			    xaxis=dict(
			        rangeselector=dict(
			            buttons=list([
			                dict(count=1,
			                     label='1m',
			                     step='month',
			                     stepmode='backward'),
			                dict(count=6,
			                     label='6m',
			                     step='month',
			                     stepmode='backward'),
			                dict(count=1,
			                    label='YTD',
			                    step='year',
			                    stepmode='todate'),
			                dict(count=1,
			                    label='1y',
			                    step='year',
			                    stepmode='backward'),
			                dict(step='all')
			            ])
			        ),
			        rangeslider=dict(),
			        type='date'
			    )
			)

			fig = dict(data=data, layout=layout)
			plot(fig)

		conn = psycopg2.connect("dbname=dnd user=postgres host=localhost")
		curs = conn.cursor()
		#Error checking to make sure we have the correct number of tables in the database.
		curs.execute("select table_name from information_schema.tables where table_schema='public';")
		num_of_tables = curs.fetchall()
		if len(num_of_tables) == 6:
			plotly()
		else:
			print("You have {} tables in your database. The required number is 6. Select the Help option at the main menu for more details.".format(len(num_of_tables)))



