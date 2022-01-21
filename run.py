# Imports
from wms import desktopApp, db, app
from wms.functions import load_data
import argparse

# Parsing command line arguments
description = """IMPORTANT: When loading information to the database, please ensure that all files are stored in the 
resources folder and that the file format matches that described in the application documentation."""

parser = argparse.ArgumentParser(description=description)

# Arguments
parser.add_argument("-warehouses",
                    help="Loads the supplied warehouses.csv file into the database when the program is run.",
                    action="store_true")
parser.add_argument("-itemTemplates",
                    help="Loads the supplied item_templates.csv file into the database when the program is run.",
                    action="store_true")
parser.add_argument("-items",
                    help="Loads the supplied items.csv file into the database when the program is run.",
                    action="store_true")
parser.add_argument("-clear",
                    help="Clears the existing database.",
                    action="store_true")

args = parser.parse_args()

# Clear database
if args.clear:
    while True:
        confirmation = input("Are you sure you want to clear the database? (y/n): ")

        if confirmation.lower() in ["yes", "y"]:
            # Drop db logic
            db.drop_all()
            db.create_all()
            print("Database cleared.")
            break
        elif confirmation.lower() in ["no", "n"]:
            print("Good thing we double checked.")
            break
        else:
            pass

successful = load_data(args.warehouses, args.itemTemplates, args.items)

if not successful:
    quit()

if __name__ == '__main__':
    #app.run(debug=True)  # For debugging
    desktopApp.run()
    desktopApp.keep_server_running()
