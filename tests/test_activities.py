def test_get_activities_returns_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity(client):
    email = "test.student@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activity_response = client.get("/activities")
    assert email in activity_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_email_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_404(client):
    email = "unknown.student@mergington.edu"
    response = client.post("/activities/Unknown Club/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity(client):
    email = "john@mergington.edu"
    response = client.post("/activities/Gym Class/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Gym Class"}

    activity_response = client.get("/activities")
    assert email not in activity_response.json()["Gym Class"]["participants"]


def test_unregister_nonexistent_email_returns_400(client):
    email = "not.enrolled@mergington.edu"
    response = client.post("/activities/Gym Class/unregister", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up"


def test_unregister_unknown_activity_returns_404(client):
    email = "test.student@mergington.edu"
    response = client.post("/activities/Unknown Club/unregister", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
