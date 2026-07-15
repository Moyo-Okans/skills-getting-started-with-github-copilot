def test_unregister_participant_removes_email_from_activity(client):
    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Chess Club/unregister?email=student@mergington.edu"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    data = activities_response.json()
    assert "student@mergington.edu" not in data["Chess Club"]["participants"]
