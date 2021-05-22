from flask import Flask, jsonify, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random, json

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "map_url":self.map_url,
            "img_url":self.img_url,
            "location":self.location,
            "seats":self.seats,
            "has_toilet":self.has_toilet,
            "has_wifi":self.has_wifi,
            "has_sockets":self.has_sockets,
            "can_take_calls":self.can_take_calls,
            "coffee_price":self.coffee_price,
        }


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

@app.route("/all")
def get_all_cafes():
    cafes = Cafe.query.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/random")
def get_random_cafe():
    cafes = Cafe.query.all()
    ran_cafe = random.choice(cafes)
    return jsonify(id=ran_cafe.id,name=ran_cafe.name,map_url=ran_cafe.map_url,img_url=ran_cafe.img_url,location=ran_cafe.location,seats=ran_cafe.seats,has_toilet=ran_cafe.has_toilet,has_wifi=ran_cafe.has_wifi,has_sockets=ran_cafe.has_sockets,can_take_calls=ran_cafe.can_take_calls,coffee_price=ran_cafe.coffee_price)

## HTTP POST - Create Record

@app.route("/add",methods=["post"])
def add_cafe():
    name = request.form["name"]
    map_url = request.form["map_url"]
    img_url = request.form["img_url"]
    location = request.form["location"]
    seats = request.form["seats"]
    has_toilet = request.form["has_toilet"]
    has_wifi = request.form["has_wifi"]
    has_sockets = request.form["has_sockets"]
    can_take_calls = request.form["can_take_calls"]
    coffee_price = request.form["coffee_price"]

    cafe = Cafe(name=name,map_url=map_url,img_url=img_url,location=location,seats=seats,has_toilet=int(has_toilet),
                has_wifi=int(has_wifi),has_sockets=int(has_sockets),can_take_calls=int(can_take_calls),coffee_price=coffee_price)
    db.session.add(cafe)
    db.session.commit()
    return cafe.to_dict()


## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<id>",methods=["Patch"])
def update(id):
    try:
        cafe = Cafe.query.filter_by(id=int(id)).first()
        cafe.coffee_price = request.form["coffee_price"]
        db.session.commit()
        return {"code":200,"message":"Cafe updated successfully"}
    except:
        return {"code":500,"message": "Something went wrong, couldn't update cafe, please try again later"}

## HTTP DELETE - Delete Record
@app.route("/delete-cafe/<id>",methods=["Delete"])
def delete(id):
    if request.args.get("api-key") == "Ilovepython":
        try:
            cafe = Cafe.query.filter_by(id=int(id)).first()
            db.session.delete(cafe)
            db.session.commit()
            return {"code":200,"message":"Cafe deleted successfully"}
        except:
            return {"code":500,"message": "Something went wrong, couldn't delete cafe, please try again later"}
    else:
        return {"code":403,"message":"Not authorized"}

if __name__ == '__main__':
    app.run(debug=True)
