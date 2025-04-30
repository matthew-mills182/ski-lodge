# Copyright © 2023-2025, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, request, redirect, url_for
from flaskapp import database as db  

app = Flask(__name__)

@app.route("/")
def render_index():
    return render_template("index.html")

@app.route("/people/")
def render_people():
    people = db.get_people()  
    return render_template("people.html", people=people)

@app.route('/people/<person_id>/')
def render_id(person_id): 
    specific_person = db.get_one_person(person_id)
    return render_template('person.html', people=specific_person)

@app.route('/people/<person_id>/edit/', methods=["GET", "POST"])
def edit_person(person_id):
    if request.method == "POST":
        # Get data from the form
        updated_person = {
            "id": person_id,
            "name": request.form["name"],
            "email": request.form["email"],
            "height": request.form["height"],
            "shoe_size": request.form["shoe_size"]
        }
        
        # Call the update function
        db.update_person(updated_person)
        
        # After updating, redirect to the person's profile page
        return redirect(url_for("render_id", person_id=person_id))

    else:
        # GET request: Display the form with current data
        specific_person = db.get_one_person(person_id)
        return render_template('edit-person.html', person=specific_person)



@app.route("/equipment/")
def render_equipment():
    miscellaneous = db.get_miscellaneous()
    boots = db.get_boots()
    skis = db.get_skis()
    poles = db.get_poles()
    return render_template(
        "equipment.html",
        miscellaneous=miscellaneous,
        boots=boots,
        skis=skis,
        poles=poles
    )


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

    db.add_person(new_person)
    
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

    db.add_equipment(new_equipment)
    
    return redirect(url_for("render_equipment"))
