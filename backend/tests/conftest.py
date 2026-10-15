import sys
import os
import uuid
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app.main import app

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.auth.security import hash_password
from app.db.deps import get_db

from app.models.role import Role
from app.models.user import User
from app.models.course import Course
from app.models.module import Module
from app.models.question import Question
from app.models.answer import Answer
from app.models.student_ability import StudentAbility
from app.models.evaluation import Evaluation


# =====================================================
# DB SETUP
# =====================================================

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# =====================================================
# SEED ROLES
# =====================================================

@pytest.fixture(scope="session", autouse=True)
def seed_roles():
    connection = engine.connect()
    session = Session(bind=connection)

    for name in ["student", "teacher", "admin"]:
        exists = session.query(Role).filter_by(name=name).first()
        if not exists:
            session.add(Role(name=name))

    session.commit()
    session.close()


# =====================================================
# DB SESSION
# =====================================================

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# =====================================================
# CLIENT
# =====================================================

@pytest.fixture
def client():
    return TestClient(app)


# =====================================================
# FIXTURES BASE
# =====================================================

@pytest.fixture
def test_role(db):
    return db.query(Role).filter_by(name="student").first()


@pytest.fixture
def test_user(db, test_role):
    user = User(
        name="Test User",
        email=f"{uuid.uuid4()}@test.com",
        password_hash=hash_password("123"),
        role=test_role.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_course(db, test_user):
    course = Course(
        title="Course",
        description="desc",
        teacher_id=test_user.id
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@pytest.fixture
def test_module(db, test_course):
    module = Module(
        title="Module",
        order_index=1,
        course_id=test_course.id
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


@pytest.fixture
def test_question(db, test_module):
    q = Question(
        content="Q",
        difficulty=0.0,
        discrimination=1.0,
        module_id=test_module.id
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@pytest.fixture
def test_ability(db, test_user):
    ability = StudentAbility(
        user_id=test_user.id,
        theta=0.0
    )
    db.add(ability)
    db.commit()
    return ability

# =====================================================
# EVALUATION
# =====================================================

@pytest.fixture
def test_evaluation(
    db,
    test_user,
    test_module
):

    evaluation = Evaluation(
        user_id=test_user.id,
        module_id=test_module.id,
        course_id=test_module.course_id,
        status="in_progress",
        current_theta=0.0
    )

    db.add(evaluation)

    db.commit()

    db.refresh(evaluation)

    return evaluation


# =====================================================
# STUDENT ABILITY FACTORY
# =====================================================

@pytest.fixture
def student_ability_factory(db):

    created = []

    def factory(user_id=None, theta=0.0):

        if not user_id:

            role = db.query(Role).filter_by(name="student").first()

            user = User(
                name="Factory User",
                email=f"{uuid.uuid4()}@test.com",
                password_hash=hash_password("123"),
                role=role.id
            )

            db.add(user)

            db.commit()

            db.refresh(user)

            user_id = user.id

        ability = StudentAbility(
            user_id=user_id,
            theta=theta
        )

        db.add(ability)
        db.commit()
        db.refresh(ability)

        created.append(ability)

        return ability

    return factory