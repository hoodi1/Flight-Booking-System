from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from datetime import datetime

#Flask app and api app created
app = Flask(__name__)
api = Api(app)

#CORS connection for connecting with angular
CORS(app,origins="*",supports_credentials=True)

#db connection estabilished
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Hoodi/Desktop/pj/Angular-FlightBooking/database.db'
db = SQLAlchemy(app)


#creating database table for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'password':self.password,
        }

#creating database table for Flights
class Flight(db.Model):
    fno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    source_destination = db.Column(db.String(80))
    final_destination = db.Column(db.String(80))
    date_travel = db.Column(db.Date)
    total_seats = db.Column(db.Integer) 

    def to_dict(self):
        return {
            'fno': self.fno,
            'fname': self.fname,
            'source_destination': self.source_destination,
            'final_destination': self.final_destination,
            'date_travel': self.date_travel.strftime('%Y-%m-%d'),
            'total_seats': self.total_seats
        }

# Creating database table for bookings done   
class Booking(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    fid = db.Column(db.Integer, db.ForeignKey('flight.fno'))

    def to_dict(self):
        return {
            'bid':self.bid,
            'uid':self.uid,
            'fid':self.fid
        }

#Cancel Flight Logic 
class CancelFlights(Resource):
    @cross_origin(supports_credentials=True)
    def delete(self):
        bid = request.args.get("bid")
        bookings_list = Booking.query.filter(Booking.bid == bid).first()
        bookings_list = bookings_list.to_dict()
        flights = Flight.query.filter(Flight.fno == bookings_list['fid']).first()
        flights.total_seats += 1
        db.session.commit()
        delete_status = Booking.query.filter(Booking.bid == bid).delete()
        db.session.commit()
        if delete_status:
            return {"status": True, "message": "Flight Cancelled Successfully.", "deleteStatus": str(delete_status)}
        else:
            return {"status": True, "message": "Something went wrong. Please try again later.", "deleteStatus": str(delete_status)}

# Display Bookings on my bookings page logic
class ShowBookings(Resource):
    @cross_origin(supports_credentials=True)
    def get(self):
        uid = request.args.get("userId")
        user_details = User.query.filter(User.id == uid).first().to_dict()
        all_bookings = Booking.query.filter(Booking.uid == uid).all()
        all_bookings = [b.to_dict() for b in all_bookings]
        flights_list = []
        if len(all_bookings):
            for i in all_bookings:
                flights = Flight.query.filter(Flight.fno == i['fid']).all()
                for f in flights:
                    temp = f.to_dict()
                    temp["bid"] = i['bid']
                    flights_list.append(temp)
            return {"status": True, "message": "Successfully fetched", "data": [user_details, flights_list]}
        else:
            return {"status": True, "message": "No Flights booked to display!", "data": []}

# Logic to book flights from dashboard/search
class BookFlight(Resource):
    @cross_origin(supports_credentials=True)
    def put(self):
        data = request.get_json()
        fno = data['fno']
        userId = data['userId']
        booking_details = Booking(uid=userId, fid=fno)
        db.session.add(booking_details)
        db.session.commit()
        flights = Flight.query.filter(Flight.fno == fno).first()
        flights.total_seats -= 1
        db.session.commit()
        return {"status": True, "message": "Booking success.."}

#Searching for a flight in dashboard logic         
class SearchFlights(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.get_json()
        source_dest = data['source']
        final_dest = data['destination']
        date_travel = data['date']
        flights = Flight.query.filter(
            Flight.source_destination.like(f'%{source_dest}%') if source_dest else True,
            Flight.final_destination.like(f'%{final_dest}%') if final_dest else True,
            Flight.date_travel == datetime.strptime(date_travel, '%Y-%m-%d').date() if date_travel else True
        ).all()
        flights_dict = [f.to_dict() for f in flights]
        if len(flights_dict):
            return flights_dict
        else:
            return {"search": True, "message": "No Flights available."}

#User login verifies a user in database - logic
class UserLogin(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.get_json()
        uname = data["username"]
        passw = data["password"]
        login = User.query.filter_by(username=uname, password=passw).first()
        if login:
            user_dict = login.to_dict()
            return {"userExist": True, "message": "User Logged In.", "userId": user_dict['id']}
        else:
            return {"userExist": False, "message": "Error while login"}

# registering a new user in database - logic
class UserRegister(Resource):
    @cross_origin(supports_credentials=True)
    def post(self):
        data = request.get_json()
        uname = data['username']
        mail = data['email']
        passw = data['password']
        register = User(username=uname, email=mail, password=passw)
        db.session.add(register)
        db.session.commit()
        user_dict = register.to_dict()
        return {"userExist": True, "message": "User Created.", "userId": user_dict['id']}

#all the routing for backend api's
api.add_resource(CancelFlights, '/cancelFlights')
api.add_resource(ShowBookings, '/bookings')
api.add_resource(BookFlight, '/book_flight')
api.add_resource(SearchFlights, '/search')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')

#to run the backend file
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)