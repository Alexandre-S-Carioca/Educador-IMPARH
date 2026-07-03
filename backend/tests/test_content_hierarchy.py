import uuid
import pytest

@pytest.fixture
def course_data():
    return {
        "name": "Curso de Teste Conteúdo",
        "description": "Descrição do curso"
    }

def test_full_content_hierarchy(client):
    # 1. Criar curso
    response = client.post("/api/v1/courses/", json={"name": "Matemática", "description": "Matemática Básica"})
    assert response.status_code == 200
    course_id = response.json()["id"]

    # 2. Criar Módulo
    module_res = client.post(f"/api/v1/courses/{course_id}/modules/", json={"title": "Módulo 1", "order_index": 1})
    assert module_res.status_code == 200
    module_id = module_res.json()["id"]

    # 3. Criar Unidade
    unit_res = client.post(f"/api/v1/modules/{module_id}/units/", json={"title": "Unidade 1", "order_index": 1})
    assert unit_res.status_code == 200
    unit_id = unit_res.json()["id"]

    # 4. Criar Tópico
    topic_res = client.post(f"/api/v1/units/{unit_id}/topics/", json={
        "title": "Adição e Subtração", 
        "difficulty": 1, 
        "order_index": 1,
        "objectives": "Entender somas",
        "introduction": "A introdução da soma."
    })
    assert topic_res.status_code == 200
    topic_id = topic_res.json()["id"]
    
    # Validações GET
    assert len(client.get(f"/api/v1/courses/{course_id}/modules/").json()) == 1
    assert len(client.get(f"/api/v1/modules/{module_id}/units/").json()) == 1
    assert len(client.get(f"/api/v1/units/{unit_id}/topics/").json()) == 1
