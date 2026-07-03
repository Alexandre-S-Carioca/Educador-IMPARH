def test_create_course(client):
    response = client.post(
        "/api/v1/courses/",
        json={
            "name": "Português Avançado - IMPARH",
            "description": "Curso focado na interpretação de texto e gramática."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Português Avançado - IMPARH"
    assert "id" in data

def test_get_courses(client):
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    # Verifica que o curso criado está na lista (independente da ordem)
    names = [course["name"] for course in data]
    assert "Português Avançado - IMPARH" in names

def test_get_course_not_found(client):
    import uuid
    fake_id = str(uuid.uuid4())
    response = client.get(f"/api/v1/courses/{fake_id}")
    assert response.status_code == 404
