"""
Loader genérico para os módulos de conteúdo definidos como dados em `seed_data/*.py`.

Cada arquivo de conteúdo (ex: `fund_i_silabas_ortografia.py`) define apenas uma
variável `MODULES`, uma lista de dicionários no formato:

    MODULES = [
        {
            "module_title": "Módulo 2: ...",
            "module_order_index": 2,
            "units": [
                {
                    "unit_title": "Unidade 1: ...",
                    "unit_order_index": 1,
                    "topics": [
                        {
                            "title": "...",
                            "difficulty": 1,
                            "order_index": 1,
                            "introduction": "...",
                            "subsubject": "...",
                            "theory_markdown": "...",
                            "questions": [
                                {
                                    "statement": "...", "option_a": "...", "option_b": "...",
                                    "option_c": "...", "option_d": "...", "correct_option": "A",
                                    "justification_correct": "...", "justification_incorrect": "...",
                                    "difficulty": 1,
                                },
                                ...
                            ],
                            "flashcards": [
                                {"front": "...", "back": "..."},
                                ...
                            ],
                        },
                        ...
                    ],
                },
                ...
            ],
        },
        ...
    ]

Esse formato de dados puros (em vez de instanciar objetos SQLAlchemy diretamente)
permite escrever/gerar conteúdo novo sem tocar em código de infraestrutura, e
mantém a validação de estrutura simples (basta checar as chaves do dicionário).

Este loader converte essa estrutura em registros reais de Module -> Unit -> Topic
-> Question/Flashcard, associados a um Course já existente.
"""

import importlib

from app.infrastructure.db.models.course import Module, Unit, Topic
from app.infrastructure.db.models.content import Question, Flashcard

DEFAULT_SUBJECT = "Língua Portuguesa"
DEFAULT_BOARD = "Educador"


def load_modules_from_file(db, course, module_filename, subject=DEFAULT_SUBJECT, board=DEFAULT_BOARD):
    """Importa `seed_data.<module_filename>` e cria todo o conteúdo (Module/Unit/
    Topic/Question/Flashcard) associado ao `course` informado.

    Retorna um dicionário com contadores do que foi criado, útil para logging.
    """
    mod = importlib.import_module(f"seed_data.{module_filename}")
    modules_data = mod.MODULES

    created = {"modules": 0, "units": 0, "topics": 0, "questions": 0, "flashcards": 0}

    for module_data in modules_data:
        module = Module(
            course_id=course.id,
            title=module_data["module_title"],
            order_index=module_data["module_order_index"],
        )
        db.add(module)
        db.commit()
        db.refresh(module)
        created["modules"] += 1

        for unit_data in module_data["units"]:
            unit = Unit(
                module_id=module.id,
                title=unit_data["unit_title"],
                order_index=unit_data["unit_order_index"],
            )
            db.add(unit)
            db.commit()
            db.refresh(unit)
            created["units"] += 1

            for topic_data in unit_data["topics"]:
                topic = Topic(
                    unit_id=unit.id,
                    title=topic_data["title"],
                    difficulty=topic_data.get("difficulty", 1),
                    order_index=topic_data.get("order_index", 0),
                    introduction=topic_data.get("introduction"),
                    theory_markdown=topic_data.get("theory_markdown"),
                )
                db.add(topic)
                db.commit()
                db.refresh(topic)
                created["topics"] += 1

                subsubject = topic_data.get("subsubject", module_data["module_title"])
                topic_difficulty = topic_data.get("difficulty", 1)

                questions = [
                    Question(
                        topic_id=topic.id,
                        statement=q["statement"],
                        option_a=q["option_a"],
                        option_b=q["option_b"],
                        option_c=q["option_c"],
                        option_d=q["option_d"],
                        correct_option=q["correct_option"],
                        justification_correct=q["justification_correct"],
                        justification_incorrect=q["justification_incorrect"],
                        difficulty=q.get("difficulty", topic_difficulty),
                        subject=subject,
                        subsubject=subsubject,
                        board=board,
                    )
                    for q in topic_data.get("questions", [])
                ]
                if questions:
                    db.add_all(questions)
                    created["questions"] += len(questions)

                flashcards = [
                    Flashcard(topic_id=topic.id, front=f["front"], back=f["back"])
                    for f in topic_data.get("flashcards", [])
                ]
                if flashcards:
                    db.add_all(flashcards)
                    created["flashcards"] += len(flashcards)

                db.commit()

    return created


def load_modules_from_files(db, course, module_filenames, subject=DEFAULT_SUBJECT, board=DEFAULT_BOARD):
    """Chama `load_modules_from_file` para vários arquivos em sequência e soma os totais."""
    totals = {"modules": 0, "units": 0, "topics": 0, "questions": 0, "flashcards": 0}
    for filename in module_filenames:
        result = load_modules_from_file(db, course, filename, subject=subject, board=board)
        for key in totals:
            totals[key] += result[key]
    return totals
