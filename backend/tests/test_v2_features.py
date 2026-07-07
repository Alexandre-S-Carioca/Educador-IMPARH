import pytest
import uuid
from app.infrastructure.db.models.user import UserLevel

def test_create_and_list_classroom(client):
    # 1. Criar sala de aula
    response = client.post(
        "/api/v1/classrooms/",
        json={
            "name": "9º Ano - Português",
            "level": "FUNDAMENTAL_II",
            "series": 9
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "9º Ano - Português"
    assert data["level"] == "FUNDAMENTAL_II"
    assert data["series"] == 9
    assert "id" in data
    assert "teacher_id" in data
    
    classroom_id = data["id"]

    # 2. Listar salas de aula do professor
    response = client.get("/api/v1/classrooms/")
    assert response.status_code == 200
    list_data = response.json()
    assert len(list_data) >= 1
    assert any(c["id"] == classroom_id for c in list_data)

    # 3. Buscar sala de aula específica
    response = client.get(f"/api/v1/classrooms/{classroom_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "9º Ano - Português"


def test_create_assignment(client):
    # Primeiro criamos uma sala de aula
    classroom_resp = client.post(
        "/api/v1/classrooms/",
        json={
            "name": "8º Ano - Redação",
            "level": "FUNDAMENTAL_II",
            "series": 8
        }
    )
    classroom_id = classroom_resp.json()["id"]

    # Criar tarefa para esta sala
    response = client.post(
        "/api/v1/assignments/",
        json={
            "classroom_id": classroom_id,
            "title": "Redação sobre Redes Sociais",
            "type": "essay",
            "description": "Escreva sobre os impactos positivos e negativos.",
            "due_date": "2026-12-31T23:59:59",
            "rubric": {"coerencia": 5, "ortografia": 5}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Redação sobre Redes Sociais"
    assert data["classroom_id"] == classroom_id
    assert data["type"] == "essay"
    assert data["rubric"]["coerencia"] == 5
    assert "id" in data

    assignment_id = data["id"]

    # Listar tarefas por sala de aula
    response = client.get(f"/api/v1/assignments/classroom/{classroom_id}")
    assert response.status_code == 200
    list_data = response.json()
    assert len(list_data) == 1
    assert list_data[0]["id"] == assignment_id


def test_submit_and_list_essay(client):
    # Criamos sala e tarefa para associar à redação
    classroom_resp = client.post(
        "/api/v1/classrooms/",
        json={
            "name": "Ensino Médio - 3º Ano",
            "level": "HIGH_SCHOOL",
            "series": 3
        }
    )
    classroom_id = classroom_resp.json()["id"]

    assignment_resp = client.post(
        "/api/v1/assignments/",
        json={
            "classroom_id": classroom_id,
            "title": "Tema do ENEM 2026",
            "type": "essay",
            "description": "Escreva um texto dissertativo-argumentativo.",
            "due_date": "2026-11-01T12:00:00"
        }
    )
    assignment_id = assignment_resp.json()["id"]

    # Enviar a redação do aluno
    essay_content = "Esta é uma redação de teste com algumas palavras para validar o contador de palavras."
    response = client.post(
        "/api/v1/essays/",
        json={
            "assignment_id": assignment_id,
            "content": essay_content
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["assignment_id"] == assignment_id
    assert data["content"] == essay_content
    # "Esta é uma redação de teste com algumas palavras para validar o contador de palavras." -> 15 palavras
    assert data["word_count"] == 15
    assert data["status"] == "reviewed"  # revisado/corrigido por IA
    assert "grade" in data
    assert "ai_feedback" in data
    assert "id" in data

    essay_id = data["id"]

    # Listar redações do aluno
    response = client.get("/api/v1/essays/")
    assert response.status_code == 200
    list_data = response.json()
    assert len(list_data) >= 1
    assert any(e["id"] == essay_id for e in list_data)

    # Detalhes da redação
    response = client.get(f"/api/v1/essays/{essay_id}")
    assert response.status_code == 200
    assert response.json()["content"] == essay_content

    # Professor dá feedback e atualiza nota
    response = client.put(
        f"/api/v1/essays/{essay_id}/feedback?grade=9.5&teacher_feedback=Excelente+trabalho"
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["grade"] == 9.5
    assert updated_data["teacher_feedback"] == "Excelente trabalho"
    assert updated_data["status"] == "graded"

def test_classroom_stats(client, db):
    # 0. Criar o estudante mock no banco de dados de teste
    import uuid
    from app.infrastructure.db.models.user import User, UserRole
    student_id = uuid.uuid5(uuid.NAMESPACE_DNS, "mock_student_user")
    
    user = db.query(User).filter(User.id == student_id).first()
    if not user:
        user = User(
            id=student_id,
            email="aluno_teste@educador.com",
            password_hash="senha_mock",
            role=UserRole.STUDENT
        )
        db.add(user)
        db.commit()

    # 1. Criar sala de aula
    classroom_resp = client.post(
        "/api/v1/classrooms/",
        json={
            "name": "Estatísticas - 1º Ano",
            "level": "HIGH_SCHOOL",
            "series": 1
        }
    )
    classroom_id = classroom_resp.json()["id"]

    # 2. Criar uma tarefa
    assignment_resp = client.post(
        "/api/v1/assignments/",
        json={
            "classroom_id": classroom_id,
            "title": "Redação de Análise Estatística",
            "type": "essay",
            "description": "Texto descritivo."
        }
    )
    assignment_id = assignment_resp.json()["id"]

    # 3. Adicionar o estudante mockado à turma
    add_student_resp = client.post(f"/api/v1/classrooms/{classroom_id}/students/{student_id}")
    assert add_student_resp.status_code == 200

    # 4. Enviar redação do aluno
    client.post(
        "/api/v1/essays/",
        json={
            "assignment_id": assignment_id,
            "content": "Esta é uma redação com exatamente quinze palavras para validar a contagem do contador."
        }
    )

    # 5. Obter estatísticas da turma
    stats_resp = client.get(f"/api/v1/classrooms/{classroom_id}/stats")
    assert stats_resp.status_code == 200
    stats_data = stats_resp.json()
    assert stats_data["classroom_id"] == classroom_id
    assert stats_data["students_count"] == 1
    assert len(stats_data["assignments_stats"]) == 1
    
    stat = stats_data["assignments_stats"][0]
    assert stat["assignment_id"] == assignment_id
    assert stat["submissions_count"] == 1
    assert stat["submissions_percentage"] == 100.0
    assert stat["average_grade"] is not None

def test_wiki_summary_api(client):
    response = client.get("/api/v1/wiki/summary?query=Metáfora")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "summary" in data
    assert "url" in data

def test_audio_pronunciation_api(client):
    # 1. Criar sala de aula e tópico
    # Usaremos um tópico semeado ou criaremos no banco de testes.
    # Como os cursos de teste são semeados nas fixtures, vamos buscar
    course_resp = client.get("/api/v1/courses/")
    assert course_resp.status_code == 200
    courses = course_resp.json()
    assert len(courses) > 0
    
    topic_id = None
    for course in courses:
        for module in course.get("modules", []):
            for unit in module.get("units", []):
                for topic in unit.get("topics", []):
                    topic_id = topic["id"]
                    break
                if topic_id: break
            if topic_id: break
        if topic_id: break
        
    assert topic_id is not None
    
    # 2. Criar áudio
    create_resp = client.post(
        f"/api/v1/audio/?topic_id={topic_id}&word_or_phrase=Morfologia&audio_url=http://exemplo.com/morfologia.mp3&ipa_phonetic=/moɾ.fo.lo.ˈʒi.ɐ/&language_level=fundamental_ii"
    )
    assert create_resp.status_code == 200
    audio_data = create_resp.json()
    assert audio_data["word_or_phrase"] == "Morfologia"
    assert audio_data["ipa_phonetic"] == "/moɾ.fo.lo.ˈʒi.ɐ/"
    
    # 3. Listar áudios do tópico
    list_resp = client.get(f"/api/v1/audio/topic/{topic_id}")
    assert list_resp.status_code == 200
    audios = list_resp.json()
    assert len(audios) >= 1
    assert any(a["id"] == audio_data["id"] for a in audios)

def test_youtube_search_api(client):
    response = client.get("/api/v1/youtube/search?query=Metáfora")
    assert response.status_code == 200
    videos = response.json()
    assert len(videos) >= 3
    assert all("id" in v and "title" in v and "thumbnail" in v and "video_url" in v for v in videos)

def test_library_classics_api(client):
    response = client.get("/api/v1/library/classics")
    assert response.status_code == 200
    books = response.json()
    assert len(books) >= 5
    assert books[0]["title"] == "Dom Casmurro"
    assert "download_url" in books[0]

def test_activity_logs_api(client):
    post_resp = client.post(
        "/api/v1/activity-logs/",
        json={
            "action": "VIEW_TOPIC",
            "details": "Visualizou o tópico teste"
        }
    )
    assert post_resp.status_code == 200
    log_data = post_resp.json()
    assert log_data["action"] == "VIEW_TOPIC"
    
    get_resp = client.get("/api/v1/activity-logs/")
    assert get_resp.status_code == 200
    logs = get_resp.json()
    assert len(logs) >= 1
    assert any(l["id"] == log_data["id"] for l in logs)
