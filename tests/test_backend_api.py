def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"].startswith("Learn")


def test_signup_for_activity_registers_participant(client):
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }

    activities_response = client.get("/activities")
    data = activities_response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_unregister_removes_existing_participant(client):
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed michael@mergington.edu from Chess Club"
    }

    activities_response = client.get("/activities")
    data = activities_response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_participant(client):
    response = client.delete(
        "/activities/Chess Club/unregister?email=missing@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
