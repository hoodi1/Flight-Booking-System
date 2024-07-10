from app import app, db, User, Flight, Booking  # Update with your actual module name
from datetime import datetime
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_login(client):
    # Create a test user
    test_user = User(username="testuser", email="test@example.com", password="password")
    db.session.add(test_user)
    db.session.commit()

    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['userExist'] is True
    assert data['message'] == "User Logged In."

def test_register(client):
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['userExist'] is True
    assert data['message'] == "User Created."

def test_search(client):
    # Create a test flight
    test_flight = Flight(fname="Test Flight", source_destination="City A", final_destination="City B", date_travel=datetime(2023, 8, 15), total_seats=100)
    db.session.add(test_flight)
    db.session.commit()

    response = client.post('/search', json={
        'source': 'City A',
        'destination': 'City B',
        'date': '2023-08-15'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert data[0]['fname'] == "Test Flight"

def test_book_flight(client):
    # Create a test user and flight
    test_user = User(username="testuser", email="test@example.com", password="password")
    test_flight = Flight(fname="Test Flight", source_destination="City A", final_destination="City B", date_travel=datetime(2023, 8, 15), total_seats=100)
    db.session.add(test_user)
    db.session.add(test_flight)
    db.session.commit()

    response = client.put('/book_flight', json={
        'fno': test_flight.fno,
        'userId': test_user.id
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] is True
    assert data['message'] == "Booking success.."

def test_cancel_flight(client):
    # Create a test user, flight, and booking
    test_user = User(username="testuser", email="test@example.com", password="password")
    test_flight = Flight(fname="Test Flight", source_destination="City A", final_destination="City B", date_travel=datetime(2023, 8, 15), total_seats=100)
    db.session.add(test_user)
    db.session.add(test_flight)
    db.session.commit()

    test_booking = Booking(uid=test_user.id, fid=test_flight.fno)
    db.session.add(test_booking)
    db.session.commit()

    response = client.delete('/cancelFlights', query_string={'bid': test_booking.bid})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] is True
    assert data['message'] == "Flight Cancelled Successfully."
