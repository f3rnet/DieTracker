import psycopg2
import datetime
import random
import radar
from tablecreate import *
import argparse

#here are the arguments required
#--author displays the author info / --git displays the github info / --version displays the version info
parser = argparse.ArgumentParser()
parser.add_argument("--author",
	help="Displays the author information", action="store_true")
parser.add_argument("--git",
	help="Displays the github information", action="store_true")
parser.add_argument("--version",
	help="Displays the version information", action="store_true")
args = parser.parse_args()
if args.author:
	print("D&D Dice Tracker by f3rnet.")
if args.git:
	print("https://github.com/f3rnet/DieTracker.")
if args.version:
	print("Version 1.0")

#okay this is our intro menu that gives users their options. 
def menu():
	print("\nWelcome to the D&D Dice Tracker v1.0. \nPlease choose one of the following options: \n"
			"[1] Manual data entry. \n[2] Random Auto Data Entry \n[3] Generate Pretty Graph \n[4] Show Database Information \n[H] Help & About \n[Q] Quit\n")
	user_choice = input("Select: ")
	return user_choice

#this while loop ensures that after a user selects an option, it will automatically retun them to the main menu
#this prevents then from having to initiate the script each time they run a command. 
while True:
	x = menu()
	new_game = TableCreate()

	if x == "1":
		new_game.manual_data()
	elif x == "2":
		table_choice = new_game.random_data()
		new_game.create_new_table(table_choice)
	elif x =="3":
		table_choice = new_game.graph_generate()
	elif x == "4":
		new_game.table_count()
	elif x.upper() == "H":
		new_game.help()
	elif x.upper() == "Q":
		print("Goodbye!")
		exit()
	else:
		print("Invalid selection. Aborting...")
		exit()








