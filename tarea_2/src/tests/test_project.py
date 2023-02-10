import responses 

from auth.models.user import User
from flask import url_for

#def test_home(client):
#    response = client.get("/")
#    assert b"<title>Home</title>" in response.data


def test_passwords_do_not_match(client):
    response = client.post("/signup/", data={"username": "admeneses", "password": "testpassword", "confirmpassword": "Testpassword"}, follow_redirects=True)

    assert b"The passwords do not match" in response.data

def test_username_empty(client):
    response = client.post("/signup/", data={"username": "", "password": "testpassword", "confirmpassword": "Testpassword"}, follow_redirects=True)

    assert b"Username, Password or Confirm Password cannot be empty" in response.data

def test_password_empty(client):
    response = client.post("/signup/", data={"username": "admemeses", "password": "", "confirmpassword": "Testpassword"}, follow_redirects=True)

    assert b"Username, Password or Confirm Password cannot be empty" in response.data

def test_all_field_empty(client):
    response = client.post("/signup/", data={"username": "", "password": "", "confirmpassword": ""}, follow_redirects=True)

    assert b"Username, Password or Confirm Password cannot be empty" in response.data

def test_signup(client):
    response = client.post("/signup/", data={"username": "admeneses", "password": "testpassword", "confirmpassword": "testpassword"}, follow_redirects=True)

    assert b"User account has been created." in response.data

def test_login(client, app):
    response = client.post("/login/", data={"username": "admeneses", "password": "testpassword"})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().username == "admeneses"

def test_empty_username_and_password(client):
    response = client.post("/login/", data={"username": "", "password": ""}, follow_redirects=True)
    assert b"Username or Password cannot be empty." in response.data

def test_empty_username(client):
    response = client.post("/login/", data={"username": "", "password": "testpassword"}, follow_redirects=True)
    assert b"Username or Password cannot be empty." in response.data

def test_empty_password(client):
    response = client.post("/login/", data={"username": "testuser", "password": ""}, follow_redirects=True)
    assert b"Username or Password cannot be empty." in response.data

def test_user_not_found(client):
    response = client.post("/login/", data={"username": "nonexistentuser", "password": "password"}, follow_redirects=True)
    assert b"Invalid username or password." in response.data

def test_incorrect_credentials(client):
    response = client.post("/login/", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert b"Invalid username or password." in response.data

#def test_correct_credentials(client, app):
#    response = client.post("/login/", data={"username": "admeneses", "password": "testpassword"}, follow_redirects=True)
#
#    assert response.status_code == 200
#    assert response.location == "http://localhost/user/admeneses"

def test_correct_credentials(client, app):
    response = client.post("/login/", data={"username": "admeneses", "password": "testpassword"}, follow_redirects=True)

    with app.test_request_context():
        assert response.status_code == 200
    #    assert url_for('main.user_home', username='admeneses') in response.location

#@responses.activate
#def test_age(client):
#    responses.add(
#        responses.GET,
#        "https://api.agify.io",
#        json={"age": 33, "count": 1049384, "name": "Anthony"},
#        status=200
#    )
#    client.post("/register", data={"email": "test@test.com", "password": "testpassword"})
#    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
#
#    response = client.post("/age", data={"name": "Anthony"})
#
#    assert b"You are 33 years old" in response.data
#
#def test_invalid_login(client):
#    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})
#
#    response = client.get("/city")
#
#    assert response.status_code == 401
