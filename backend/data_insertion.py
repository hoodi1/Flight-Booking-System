from datetime import datetime
from app import app, db, Flight  # Import your Flask app instance, db, and flight model

# Ensure app context is active
with app.app_context():
    # Drop existing tables (if any)
    db.drop_all()
    
    # Create tables based on defined models
    db.create_all()

    # Sample data for flights
    flights_data = [
        {
            'fname': 'Flight 001',
            'source_destination': 'New York',
            'final_destination': 'London',
            'date_travel': datetime(2024, 8, 15),
            'total_seats': 200
        },
        {
            'fname': 'Flight 002',
            'source_destination': 'Paris',
            'final_destination': 'Tokyo',
            'date_travel': datetime(2024, 8, 20),
            'total_seats': 180
        },
        {
            'fname': 'Flight 003',
            'source_destination': 'Dubai',
            'final_destination': 'Sydney',
            'date_travel': datetime(2024, 8, 25),
            'total_seats': 220
        },
    ]

    # Add flights to the database
    for flight_data in flights_data:
        flight_instance = Flight(
            fname=flight_data['fname'],
            source_destination=flight_data['source_destination'],
            final_destination=flight_data['final_destination'],
            date_travel=flight_data['date_travel'],
            total_seats=flight_data['total_seats']
        )
        db.session.add(flight_instance)

    # Commit the changes to the database
    db.session.commit()

    print("Flights data added successfully!")
