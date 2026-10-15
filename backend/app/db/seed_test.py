import uuid
from app.models.role import Role
from app.models.user import User
from app.models.course import Course
from app.models.module import Module
from app.models.question import Question
from app.auth.security import hash_password

def seed_test_data(db):
    """
    Seed mínimo para tests unitarios.
    No genera evaluaciones, resultados previos ni datos contaminantes.
    """

    for role_name in ["student", "teacher", "admin"]:
        if not db.query(Role).filter_by(name=role_name).first():
            db.add(Role(name=role_name))
    db.commit()


    test_user = User(
        name="Test User",
        email=f"{uuid.uuid4()}@test.com",
        password_hash=hash_password("123"),
        role=db.query(Role).filter_by(name="student").first().id
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)


    course = Course(title="Test Course", description="desc", teacher_id=test_user.id)
    db.add(course)
    db.commit()
    db.refresh(course)

    module = Module(title="Test Module", order_index=1, course_id=course.id)
    db.add(module)
    db.commit()
    db.refresh(module)


    for diff in [-2.0, 0.0, 2.0]:
        q = Question(
            content=f"Q{diff}",
            difficulty=diff,
            discrimination=1.0,
            module_id=module.id
        )
        db.add(q)
    db.commit()

    return {
        "user": test_user,
        "course": course,
        "module": module
    }