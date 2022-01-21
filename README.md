<img align="left" src="https://i.ibb.co/m6zFXhM/logo.png" width="80" height="80" style="padding: 10px"/>
<h1>WMS</h1>
<h3>Matteo Golin</h3>

[![License: MIT](https://img.shields.io/badge/License-MIT-09b8db.svg)](https://opensource.org/licenses/MIT)

A warehouse management system designed using Flask, HTML, SCSS & CSS. The software is intended to be run as a desktop
application at a fixed size using FlaskWebGUI.

## Using the application

### Command Line Arguments
The only command line argument that is meant for general use is the `-clear` command, which empties the database of all
existing information.

The other command line arguments are meant to be used for [debugging](#debugging).

### Main Dashboard
Users can add new warehouses from this page, as well as new item templates. It also displays statistics pertaining to
the entire warehouse system.

### View Warehouses
Users can add new warehouses from this page, and view statistics pertaining to each warehouse in the list. The
individual warehouse view can be accessed from this page using the 'edit button'.

### View Items
Users can add new item templates from this page, and view statistics pertaining to each item in the list. The individual
item view can be accessed from this page using the 'edit button'.

### Individual Warehouse View
Users can change the information related to a warehouse from this page. They may also add items that will be attributed
to the warehouse from this page. Statistics about the given warehouse will be displayed. A list of all the items stored
at the given warehouse can be accessed using the 'view all' button.

### Individual Item View
Users can change the information related to an item template from this page. Statistics about the given item template 
will be displayed.

### View Warehouse Items
Users can view the items that are stored in the given warehouse. Here, they can also add an item to be stored at the
given warehouse and the quantity of the item to be stored. A brief overview of the number of unique items and the total
possible revenue is given on the right.

## Debugging
Command line arguments for debugging include:
- `-warehouses`
- `-itemTemplates`
- `-items`

These commands load CSV files placed in the 'resources' directory. They are designed to provide some base information to
the application so a developer can debug, but can technically also be used to load pre-existing data from a spreadsheet
so it can be viewed and manipulated within the GUI.

---

The `-warehouses` command will load data from a CSV file named 'warehouses.csv'. It must be of the following format:
```
Name,Capacity
Ottawa,7500000
Toronto,9450875
Sudbury,750000
...
```
This data describes the name and capacity of warehouses that will be visible within the application.
Of course, the data is subject to validation rules, i.e. a warehouse's name must not be less than two characters, etc.

The `-itemTemplates` command will load data from a CSV file named 'item-templates.csv'. It must be of the following
format:

```
Name,Price,Cost,Size,Low threshold
Keyboard,69.99,8.22,7,15
Headphones,54.59,4.69,5,20
16GB USB,7.99,0.06,1,50
...
```
This data describes different types of items that will be available to select from within the application.

The `-items` command will load data from a CSV file named 'items.csv'. It must be of the following
format:

```
Template name,Quantity,Warehouse
Keyboard,56,Sudbury
Headphones,32,Toronto
...
```
This data describes which items are stored at which warehouse, and how many. The template names must be existing 
templates.

## Installation
Python 3.9.8 or later must be installed. This software makes use of the following modules:
- Flask
- SQLAlchemy
- Flask-WTF
- WTF Forms
- Flask Web GUI