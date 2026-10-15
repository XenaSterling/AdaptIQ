import uuid

from app.auth.security import hash_password
from app.models.user import User
from app.models.role import Role
from app.models.course import Course
from app.models.module import Module
from app.models.question import Question
from app.models.answer import Answer


def get_role(db, name):
    role = db.query(Role).filter_by(name=name).first()
    if role:
        return role
    role = Role(name=name)
    db.add(role)
    db.commit()
    return role


def create_user(db, role_name="student"):
    role = get_role(db, role_name)

    user = User(
        name="User",
        email=f"{uuid.uuid4()}@test.com",
        password_hash=hash_password("x"),
        role=role.id
    )

    db.add(user)
    db.commit()
    return user


def create_course(db, user):
    course = Course(
        title="Course",
        description="desc",
        teacher_id=user.id
    )
    db.add(course)
    db.commit()
    return course


def create_module(db, course):
    module = Module(
        title="Module",
        order_index=1,
        course_id=course.id
    )
    db.add(module)
    db.commit()
    return module


def create_question(db, module, difficulty=0.0, with_answers=True):

    q = Question(
        content="Q",
        difficulty=difficulty,
        discrimination=1.0,
        module_id=module.id
    )

    db.add(q)
    db.commit()
    db.refresh(q)

    if with_answers:

        a1 = Answer(
            question_id=q.id,
            content="Correct",
            is_correct=True
        )

        a2 = Answer(
            question_id=q.id,
            content="Incorrect",
            is_correct=False
        )

        db.add_all([a1, a2])
        db.commit()

    return q