# Copyright © 2023-2025, Indiana University
# BSD 3-Clause License
# playin

import csv

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_people():
    with open('people.csv', 'r') as csvf:
        reader = csv.DictReader(csvf)
        return list(reader)

def load_people_id():
    with open('people.csv', 'r') as csvf:
        people = {}
        for row in csv.DictReader(csvf):
            people[row['Name']] = row
        return people
    
def save_people(new_person):
    
    with open("people.csv", mode="a", newline="") as csv_file:
        fieldnames = ["Name", "Email", "Height", "Shoe Size"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        
        writer.writerow(new_person)


def save_equipment(new_equipment):
    with open("misc.csv", mode="a", newline="\n") as csv_file:  
        fieldnames = ["name", "quantity", "max_quantity"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writerow(new_equipment)


def load_miscellaneous():
    with open("misc.csv", "r") as csvf:
        reader = csv.DictReader(csvf)
        return list(reader)

def load_poles():
    with open("poles.csv", "r") as csvf:
        reader = csv.DictReader(csvf)
        return list(reader)

def load_boots():
    with open("boots.csv", "r") as  csvf:
        reader = csv.DictReader(csvf)
        return list(reader)
    
def load_skis():
    with open("skis.csv", "r") as  csvf:
        reader = csv.DictReader(csvf)
        return list(reader)

@app.route("/")
def render_index():
    return render_template("index.html")

@app.route("/people/")
def render_people():
    people = load_people()
    return render_template("people.html", people = people)

@app.route('/people/<person_id>/')
def render_id(person_id): 
    all_people = load_people_id()
    specific_person = all_people[person_id]
    return render_template('person.html', people = specific_person)

@app.route("/equipment/")
def render_equipment():
    miscellaneous = load_miscellaneous()
    poles = load_poles()
    skis = load_skis()
    boots = load_boots()
    return render_template("equipment.html",miscellaneous=miscellaneous, poles=poles, boots = boots, skis = skis)



@app.route("/add-person/", methods=["GET", "POST"])
def handle_new_person():
    if request.method == "GET":
        return render_template("add-person.html")  
    
    
    new_person = {
        "Name": request.form["name"],
        "Email": request.form["email"],
        "Height": request.form["height"],
        "Shoe Size": request.form["shoe_size"]
    }
    
    
    save_people(new_person)
    
    return redirect(url_for("render_people"))


@app.route("/add-equipment/", methods=["GET", "POST"])
def handle_new_equipment():
    if request.method == "GET":
        return render_template("add-equipment.html")
    
    new_equipment = {
        "name": request.form["name"],  
        "quantity": request.form["number"],  
        "max_quantity": request.form["number"]  
    }
    
    save_equipment(new_equipment)
    
    return redirect(url_for("render_equipment"))