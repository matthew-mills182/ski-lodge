# Copyright © 2023-2025, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, request, redirect, url_for
from flaskapp import database as db  

app = Flask(__name__)

@app.route("/")
def render_index():
    people = db.get_people()

    # Count guests currently checked in with each pass type
    on_slope_count = sum(1 for p in people if p.get("status") == "in" and p.get("pass_type") == "Lift Ticket")
    in_lodge_count = sum(1 for p in people if p.get("status") == "in" and p.get("pass_type") == "Lodge Pass")

    # Load full gear inventory
    boots = db.get_boots()
    skis = db.get_skis()
    poles = db.get_poles()

    rented_boots = [p["boot_size"] for p in people if p["boot_size"]]
    rented_skis = [p["ski_length"] for p in people if p["ski_length"]]
    known_pole_heights = {p["height"] for p in poles}
    rented_poles = [p["pole_height"] for p in people if p["pole_height"] in known_pole_heights]

    for item in boots:
        item["quantity"] = item["max_quantity"] - rented_boots.count(item["name"])
    for item in skis:
        item["quantity"] = item["max_quantity"] - rented_skis.count(item["name"])
    for item in poles:
        item["quantity"] = item["max_quantity"] - rented_poles.count(item["height"])

    return render_template(
        "index.html",
        on_slope_count=on_slope_count,
        in_lodge_count=in_lodge_count,
        boots=boots,
        skis=skis,
        poles=poles,
        miscellaneous=db.get_miscellaneous()
    )



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


@app.route("/reservations/", methods=["GET", "POST"])
def render_reservations():
    people = db.get_people()

    checked_in = [p for p in people if p.get("status") == "in"]
    not_checked_in = [p for p in people if p.get("status") != "in"]

    start_checkin_id = None
    if request.method == "POST":
        start_checkin_id = request.form.get("start_checkin_id")

    return render_template(
        "reservations.html",
        checked_in=checked_in,
        not_checked_in=not_checked_in,
        start_checkin_id=start_checkin_id
    )


@app.route("/checkin/<person_id>/", methods=["POST"])
def handle_checkin(person_id):
    pass_type = request.form.get("pass_type")
    rent_equipment = request.form.get("rent_equipment")

    boot_size = request.form.get("boot_size") if rent_equipment == "yes" else None
    ski_length = request.form.get("ski_length") if rent_equipment == "yes" else None
    pole_height = request.form.get("pole_height") if rent_equipment == "yes" else None

    print("--- CHECK-IN FORM SUBMITTED ---")
    print("person_id:", person_id)
    print("pass_type:", pass_type)
    print("rent_equipment:", rent_equipment)
    print("boot_size:", boot_size)
    print("ski_length:", ski_length)
    print("pole_height:", pole_height)

    db.checkin_guest(person_id, pass_type, boot_size, ski_length, pole_height)

    return redirect(url_for("render_reservations"))



@app.route("/checkout/<person_id>/", methods=["POST"])
def handle_checkout(person_id):
    db.checkout_guest(person_id)
    return redirect(url_for("render_reservations"))


