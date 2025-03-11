# Copyright © 2023-2025, Indiana University
# BSD 3-Clause License
import csv

from flask import Flask, render_template

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

