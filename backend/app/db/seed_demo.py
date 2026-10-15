import math
import random
import uuid
from datetime import datetime, timedelta

from sqlalchemy import text

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.auth.security import hash_password

from app.models.role import Role
from app.models.user import User
from app.models.student_ability import StudentAbility
from app.models.irt_session import IRTSession

from app.models.course import Course
from app.models.module import Module

from app.models.question import Question, QuestionType
from app.models.answer import Answer
from app.models.tag import Tag
from app.models.question_tag import QuestionTag

from app.models.learning_resource import (
    LearningResource,
    ResourceType,
)
from app.models.resource_tag import ResourceTag

from app.models.enrollment import Enrollment

from app.models.evaluation import (
    Evaluation,
    EvaluationStatus,
)
from app.models.result import Result
from app.models.evaluation_settings import EvaluationSettings

from app.models.module_progress import ModuleProgress
from app.models.resource_usage import ResourceUsage

from app.models.learning_profile import (
    LearningProfile,
    LearningStyle,
)

from app.ml.prediction.dropout_model import train_model


# ============================================================
# CONFIG
# ============================================================

SEED = 42

NUM_STUDENTS = 100
EVALUATIONS_PER_STUDENT = 10

STUDENT_NAMES = [
    "Lucía García",
    "Mateo Fernández",
    "Sofía Martínez",
    "Hugo López",
    "Martina Sánchez",
    "Daniel Pérez",
    "Valeria Gómez",
    "Alejandro Martín",
    "Paula Rodríguez",
    "Lucas González",
    "Carmen Díaz",
    "Álvaro Moreno",
    "Elena Muñoz",
    "Diego Álvarez",
    "Claudia Romero",
    "Adrián Alonso",
    "Marta Navarro",
    "Pablo Gutiérrez",
    "Sara Torres",
    "Javier Domínguez",
    "Irene Vázquez",
    "Mario Ramos",
    "Nora Gil",
    "Sergio Ramírez",
    "Aitana Serrano",
    "Gonzalo Blanco",
    "Julia Molina",
    "Iván Suárez",
    "Laura Ortega",
    "Bruno Delgado",
    "Ana Castro",
    "Marcos Ortiz",
    "Noa Rubio",
    "David Marín",
    "Carla Iglesias",
    "Álex Núñez",
    "Alba Medina",
    "Jorge Cabrera",
    "Inés Prieto",
    "Raúl Vega",
    "Vega Castillo",
    "Enzo Durán",
    "Marina León",
    "Samuel Pascual",
    "Olivia Santana",
    "Eric Vidal",
    "Alicia Reyes",
    "Joel Ferrer",
    "Natalia Hidalgo",
    "Miguel Crespo",
    "Emma Pastor",
    "Nicolás Peña",
    "Lola Esteban",
    "Óscar Bravo",
    "Candela Gallardo",
    "Víctor Ríos",
    "Mía Soler",
    "Tomás Campos",
    "Daniela Mora",
    "Iker Lozano",
    "Violeta Prieto",
    "Ángel Fuentes",
    "Berta Carmona",
    "Manuel Rey",
    "Jimena Durán",
    "Rodrigo Sáez",
    "Leire Nieto",
    "Fernando Calvo",
    "Celia Montero",
    "Guillermo Pastor",
    "Amaya Nieto",
    "Héctor Vidal",
    "Nerea Ferrer",
    "Alberto Arias",
    "Teresa Cano",
    "Rafael Solís",
    "Lidia Benítez",
    "Andrés Merino",
    "Eva Sanz",
    "Pau Garrido",
    "Cristina Pardo",
    "Ignacio Parra",
    "Aroa Márquez",
    "Ramón Vera",
    "Mónica Valdés",
    "Jaime Roldán",
    "Rocío Calvo",
    "Federico Serra",
    "Silvia Campos",
    "Esteban Cortés",
    "Beatriz Lozano",
    "Luis Segura",
    "Patricia Moya",
    "Arturo Soler",
    "Isabel Galán",
    "Eduardo Nieto",
    "Rebeca Santos",
    "Julián Lara",
    "Teresa Vidal",
    "Gema Serrano",
    "Sergio Molina",
    "Natalia Blanco",
    "Pablo León",
    "Ariadna Torres",
    "Mario Ferrer",
    "Clara Domínguez",
    "Héctor Navarro",
    "Elisa Romero",
    "Álex Martín",
]

random.seed(SEED)


# ============================================================
# RESET
# ============================================================

def reset_database(db):

    db.execute(text("""
        TRUNCATE TABLE
            recommendations,
            resource_usage,
            module_progress,
            learning_profiles,
            resource_tags,
            learning_resources,
            question_tags,
            answers,
            questions,
            enrollments,
            irt_sessions,
            evaluation_settings,
            results,
            evaluations,
            modules,
            courses,
            student_abilities,
            users,
            roles,
            tags
        RESTART IDENTITY CASCADE;
    """))

    db.commit()


# ============================================================
# ROLES
# ============================================================

def create_roles(db):

    roles = {
        "admin": Role(id=1, name="admin"),
        "teacher": Role(id=2, name="teacher"),
        "student": Role(id=3, name="student"),
    }

    db.add_all(roles.values())
    db.commit()

    return roles


# ============================================================
# TEACHERS
# ============================================================

def create_teachers(db, roles):

    teachers = []

    for i in range(3):

        teacher = User(
            id=uuid.uuid4(),
            name=f"Professor {i + 1}",
            email=f"teacher{i + 1}@adaptiq.com",
            password_hash=hash_password("1234"),
            role=roles["teacher"].id,
            is_active=True,
        )

        teachers.append(teacher)

    db.add_all(teachers)
    db.commit()

    return teachers


# ============================================================
# ADMIN
# ============================================================

def create_admin(db, roles):

    admin = User(
        id=uuid.uuid4(),
        name="Administrator",
        email="admin@adaptiq.com",
        password_hash=hash_password("1234"),
        role=roles["admin"].id,
        is_active=True,
    )

    db.add(admin)
    db.commit()

    return admin


# ============================================================
# STUDENT PROFILES
# ============================================================

PROFILE_CONFIG = {

    "excellent": {
        "theta": (1.8, 2.8),
        "learning_rate": (0.05, 0.12),
        "engagement": (0.90, 1.00),
        "accuracy": (0.80, 0.95),
        "dropout": 0.02,
    },

    "fast_learner": {
        "theta": (0.0, 1.2),
        "learning_rate": (0.12, 0.20),
        "engagement": (0.80, 0.98),
        "accuracy": (0.65, 0.85),
        "dropout": 0.05,
    },

    "steady": {
        "theta": (-0.5, 0.8),
        "learning_rate": (0.04, 0.09),
        "engagement": (0.70, 0.90),
        "accuracy": (0.55, 0.75),
        "dropout": 0.08,
    },

    "average": {
        "theta": (-0.5, 0.5),
        "learning_rate": (0.02, 0.07),
        "engagement": (0.60, 0.85),
        "accuracy": (0.50, 0.70),
        "dropout": 0.12,
    },

    "algebra_weak": {
        "theta": (-0.5, 1.0),
        "learning_rate": (0.03, 0.08),
        "engagement": (0.60, 0.85),
        "accuracy": (0.45, 0.70),
        "dropout": 0.14,
    },

    "calculus_weak": {
        "theta": (0.0, 1.2),
        "learning_rate": (0.03, 0.07),
        "engagement": (0.55, 0.80),
        "accuracy": (0.40, 0.65),
        "dropout": 0.16,
    },

    "improving": {
        "theta": (-2.0, -0.8),
        "learning_rate": (0.12, 0.22),
        "engagement": (0.75, 0.95),
        "accuracy": (0.45, 0.65),
        "dropout": 0.06,
    },

    "declining": {
        "theta": (0.5, 1.5),
        "learning_rate": (-0.12, -0.04),
        "engagement": (0.30, 0.65),
        "accuracy": (0.35, 0.60),
        "dropout": 0.30,
    },

    "at_risk": {
        "theta": (-2.8, -1.4),
        "learning_rate": (-0.03, 0.02),
        "engagement": (0.15, 0.45),
        "accuracy": (0.25, 0.50),
        "dropout": 0.60,
    },
}


def create_students(db, roles):

    students = []

    profile_names = list(PROFILE_CONFIG.keys())

    for i in range(NUM_STUDENTS):

        profile_name = random.choices(
            profile_names,
            weights=[
                8,   # excellent
                10,  # fast learner
                15,  # steady
                20,  # average
                10,  # algebra weak
                10,  # calculus weak
                10,  # improving
                7,   # declining
                10,  # at risk
            ],
        )[0]

        config = PROFILE_CONFIG[profile_name]

        learning_style = random.choice([
            LearningStyle.visual,
            LearningStyle.auditory,
            LearningStyle.reading,
            LearningStyle.kinesthetic,
        ])

        student = User(
            id=uuid.uuid4(),
            name=STUDENT_NAMES[i],
            email=f"student{i + 1:03d}@adaptiq.com",
            password_hash=hash_password("1234"),
            role=roles["student"].id,
            learning_style=learning_style.value,
            is_active=True,
        )

        student._demo_profile = profile_name
        student._demo_theta = random.uniform(*config["theta"])
        student._demo_learning_rate = random.uniform(
            *config["learning_rate"]
        )
        student._demo_engagement = random.uniform(
            *config["engagement"]
        )
        student._demo_accuracy = random.uniform(
            *config["accuracy"]
        )
        student._demo_dropout = config["dropout"]

        students.append(student)

    db.add_all(students)
    db.commit()

    return students


# ============================================================
# LEARNING PROFILES
# ============================================================

def create_learning_profiles(db, students):

    for student in students:

        style = LearningStyle(student.learning_style)

        profile = LearningProfile(
            user_id=student.id,
            learning_style=style,
            preferred_difficulty_growth=style,
        )

        db.add(profile)

    db.commit()


# ============================================================
# COURSES
# ============================================================

def create_courses(db, teachers):

    courses = []

    definitions = [
        (
            "Fundamentos de Matemáticas",
            "Curso adaptativo de matemáticas que cubre aritmética y álgebra.",
            0,
        ),
        (
            "Matemáticas Avanzadas",
            "Curso adaptativo de matemáticas que cubre funciones, cálculo y análisis.",
            1,
        ),
    ]

    for title, description, teacher_index in definitions:

        course = Course(
            id=uuid.uuid4(),
            title=title,
            description=description,
            teacher_id=teachers[teacher_index].id,
        )

        db.add(course)
        db.flush()

        courses.append(course)

    modules_by_course = []

    module_names = [
        ["Aritmética", "Fracciones", "Álgebra"],
        ["Funciones", "Derivadas", "Integrales"],
    ]

    for course, names in zip(courses, module_names):

        modules = []

        for index, name in enumerate(names):

            module = Module(
                id=uuid.uuid4(),
                title=name,
                order_index=index + 1,
                course_id=course.id,
            )

            db.add(module)
            modules.append(module)

        modules_by_course.append(modules)

    db.commit()

    return courses, modules_by_course


# ============================================================
# TAGS
# ============================================================

TAG_NAMES = [
    "aritmética",
    "fracciones",
    "álgebra",
    "ecuaciones",
    "funciones",
    "cálculo",
    "derivadas",
    "integrales",
    "límites",
    "resolución_de_problemas",
]


def create_tags(db):

    tags = {}

    for name in TAG_NAMES:

        tag = Tag(
            id=uuid.uuid4(),
            name=name,
        )

        db.add(tag)
        tags[name] = tag

    db.commit()

    return tags


# ============================================================
# QUESTIONS
# ============================================================

# 100 preguntas:
# - Arithmetic:   17
# - Fractions:    16
# - Algebra:      17
# - Functions:    17
# - Derivatives:  17
# - Integrals:    16
#
# Cada pregunta tiene:
#   (enunciado, dificultad, nivel_bloom, [respuesta1, respuesta2,
#    respuesta3, respuesta4], indice_respuesta_correcta)

QUESTION_BANK = {

    "Aritmética": [

        (
            "¿Cuánto es 12 + 7?",
            -3.0, "remember",
            ["17", "18", "19", "20"], 2
        ),
        (
            "¿Cuánto es 25 - 13?",
            -2.7, "remember",
            ["10", "11", "12", "13"], 2
        ),
        (
            "¿Cuánto es 8 × 7?",
            -2.4, "remember",
            ["48", "54", "56", "64"], 2
        ),
        (
            "¿Cuánto es 144 ÷ 12?",
            -2.1, "remember",
            ["10", "11", "12", "14"], 2
        ),
        (
            "¿Cuál es el 15 % de 200?",
            -1.8, "understand",
            ["20", "25", "30", "35"], 2
        ),
        (
            "¿Cuánto es 3² + 4²?",
            -1.5, "understand",
            ["12", "20", "25", "49"], 2
        ),
        (
            "Un producto cuesta 80 € y tiene un descuento del 25 %. ¿Cuál es su precio final?",
            -1.2, "apply",
            ["55 €", "60 €", "65 €", "70 €"], 1
        ),
        (
            "Si 5 cuadernos cuestan 15 €, ¿cuánto cuestan 8 cuadernos al mismo precio unitario?",
            -0.8, "apply",
            ["20 €", "22 €", "24 €", "26 €"], 2
        ),
        (
            "Un tren recorre 180 km en 3 horas. ¿Cuál es su velocidad media?",
            -0.4, "apply",
            ["50 km/h", "60 km/h", "70 km/h", "80 km/h"], 1
        ),
        (
            "Una cantidad aumenta de 200 a 250. ¿Cuál ha sido el porcentaje de aumento?",
            0.0, "apply",
            ["20 %", "25 %", "30 %", "35 %"], 1
        ),
        (
            "Si 4 trabajadores realizan un trabajo en 12 días, ¿cuántos días necesitarían 8 trabajadores al mismo ritmo?",
            0.4, "analyze",
            ["3 días", "6 días", "8 días", "24 días"], 1
        ),
        (
            "Una tienda aplica primero un descuento del 20 % y después otro del 10 %. ¿Cuál es el descuento equivalente?",
            0.8, "analyze",
            ["28 %", "30 %", "32 %", "35 %"], 0
        ),
        (
            "Un depósito contiene 240 litros. Se consume el 35 %. ¿Cuántos litros quedan?",
            1.2, "apply",
            ["144 L", "150 L", "156 L", "168 L"], 2
        ),
        (
            "Un número aumentado en un 40 % se convierte en 84. ¿Cuál era el número original?",
            1.7, "analyze",
            ["56", "60", "64", "70"], 2
        ),
        (
            "Una familia gasta el 30 % de sus ingresos en vivienda y el 20 % en alimentación. Si sus ingresos son 2.000 €, ¿cuánto queda para otros gastos?",
            2.1, "analyze",
            ["800 €", "900 €", "1.000 €", "1.200 €"], 2
        ),
        (
            "Un artículo cuesta 150 € antes de aplicar un IVA del 21 %. ¿Cuál es su precio final?",
            2.6, "apply",
            ["171,50 €", "178,50 €", "181,50 €", "185,00 €"], 2
        ),
        (
            "Un número de tres cifras tiene 4 centenas, 7 decenas y 3 unidades. ¿Qué número es?",
            3.0, "understand",
            ["437", "473", "743", "734"], 1
        ),
    ],

    "Fracciones": [

        (
            "¿Cuánto es 1/2 + 1/2?",
            -2.8, "remember",
            ["0", "1/2", "1", "2"], 2
        ),
        (
            "Simplifica la fracción 4/8.",
            -2.5, "remember",
            ["1/2", "1/4", "2/3", "3/4"], 0
        ),
        (
            "¿Cuánto es 2/3 + 1/3?",
            -2.2, "apply",
            ["1/3", "2/3", "1", "4/3"], 2
        ),
        (
            "¿Cuánto es 3/4 × 2/5?",
            -1.9, "apply",
            ["3/10", "3/20", "6/9", "5/8"], 0
        ),
        (
            "¿Cuánto es 5/6 - 1/4?",
            -1.5, "apply",
            ["1/2", "7/12", "2/3", "3/4"], 1
        ),
        (
            "¿Cuál de estas fracciones es mayor?",
            -1.2, "understand",
            ["1/2", "2/3", "3/5", "5/8"], 1
        ),
        (
            "¿Cuánto es 2/5 de 30?",
            -0.8, "apply",
            ["10", "12", "15", "18"], 1
        ),
        (
            "¿Cuánto es 3/4 + 1/8?",
            -0.4, "apply",
            ["5/8", "7/8", "1", "9/8"], 1
        ),
        (
            "¿Cuánto es 7/10 - 2/5?",
            0.0, "apply",
            ["1/5", "3/10", "1/2", "2/3"], 1
        ),
        (
            "¿Cuál es la fracción equivalente a 3/5 con denominador 20?",
            0.4, "understand",
            ["6/20", "9/20", "12/20", "15/20"], 2
        ),
        (
            "Una pizza se divide en 8 partes iguales. Si se comen 3 partes, ¿qué fracción queda?",
            0.8, "apply",
            ["3/8", "5/8", "6/8", "7/8"], 1
        ),
        (
            "¿Cuánto es 2/3 ÷ 4/5?",
            1.2, "apply",
            ["5/6", "8/15", "10/12", "2/5"], 0
        ),
        (
            "¿Cuál es el resultado de 1/2 + 2/3 - 1/6?",
            1.6, "analyze",
            ["1", "4/3", "5/6", "7/6"], 0
        ),
        (
            "Una receta necesita 3/4 de litro de leche. Si quieres preparar la mitad de la receta, ¿cuánta leche necesitas?",
            2.0, "apply",
            ["1/4 L", "3/8 L", "1/2 L", "5/8 L"], 1
        ),
        (
            "¿Cuál es el resultado de (2/3) × (9/4) × (2/3)?",
            2.5, "analyze",
            ["1", "2", "3/2", "4/3"], 0
        ),
        (
            "¿Qué fracción representa el 37,5 %?",
            3.0, "analyze",
            ["1/4", "3/8", "2/5", "5/12"], 1
        ),
    ],

    "Álgebra": [

        (
            "Resuelve: x + 3 = 7.",
            -1.8, "understand",
            ["2", "3", "4", "5"], 2
        ),
        (
            "Resuelve: 2x = 10.",
            -1.5, "apply",
            ["2", "4", "5", "8"], 2
        ),
        (
            "Resuelve: 3x + 2 = 11.",
            -1.2, "apply",
            ["2", "3", "4", "5"], 1
        ),
        (
            "Resuelve: 2x + 5 = 17.",
            -0.9, "apply",
            ["5", "6", "7", "8"], 1
        ),
        (
            "Resuelve: 3(x + 2) = 18.",
            -0.5, "apply",
            ["3", "4", "5", "6"], 1
        ),
        (
            "Resuelve: 2x - 4 = x + 6.",
            -0.2, "apply",
            ["8", "9", "10", "12"], 2
        ),
        (
            "Si 5x - 3 = 2x + 12, ¿cuánto vale x?",
            0.2, "apply",
            ["3", "4", "5", "6"], 2
        ),
        (
            "Resuelve el sistema: x + y = 10, x - y = 2.",
            0.6, "analyze",
            ["x=5, y=5", "x=6, y=4", "x=7, y=3", "x=8, y=2"], 1
        ),
        (
            "¿Cuál es la solución de x² - 9 = 0?",
            1.0, "apply",
            ["x=3", "x=-3", "x=±3", "x=9"], 2
        ),
        (
            "Resuelve: x² - 5x + 6 = 0.",
            1.4, "apply",
            ["x=1 y x=6", "x=2 y x=3", "x=-2 y x=-3", "x=0 y x=6"], 1
        ),
        (
            "¿Cuál es el valor de x si 2(x - 3) + 4 = 14?",
            1.8, "apply",
            ["6", "7", "8", "9"], 2
        ),
        (
            "¿Qué expresión es equivalente a 3(x + 2) - 2x?",
            2.1, "analyze",
            ["x + 6", "x + 2", "5x + 6", "x - 6"], 0
        ),
        (
            "¿Cuáles son las raíces de x² + x - 6 = 0?",
            2.5, "analyze",
            ["2 y -3", "3 y -2", "1 y -6", "-1 y 6"], 0
        ),
        (
            "Si a + b = 10 y ab = 21, ¿cuánto vale a² + b²?",
            2.8, "analyze",
            ["42", "58", "79", "100"], 1
        ),
        (
            "¿Para qué valor de x se cumple 2x² = 18?",
            3.0, "apply",
            ["x=3", "x=-3", "x=±3", "x=9"], 2
        ),
        (
            "¿Cuál es el desarrollo de (x + 3)²?",
            3.3, "understand",
            ["x² + 3x + 9", "x² + 6x + 9", "x² + 9", "x² + 6"], 1
        ),
        (
            "Si x + 1/x = 3, ¿cuánto vale x² + 1/x²?",
            3.7, "evaluate",
            ["6", "7", "8", "9"], 1
        ),
    ],

    "Funciones": [

        (
            "Si f(x) = x + 1, ¿cuánto vale f(2)?",
            -1.5, "understand",
            ["2", "3", "4", "5"], 1
        ),
        (
            "Si f(x) = 2x, ¿cuánto vale f(3)?",
            -1.2, "apply",
            ["3", "5", "6", "9"], 2
        ),
        (
            "Si f(x) = x², ¿cuánto vale f(-3)?",
            -0.9, "apply",
            ["-9", "-6", "6", "9"], 3
        ),
        (
            "¿Cuál es el dominio de f(x) = 1/x?",
            -0.5, "understand",
            ["Todos los números reales", "Todos salvo x=0", "Solo los positivos", "Solo los enteros"], 1
        ),
        (
            "¿Cuál es el dominio de f(x) = √x?",
            -0.2, "understand",
            ["x ≤ 0", "x < 0", "x ≥ 0", "Todos los reales"], 2
        ),
        (
            "¿Cuál es la pendiente de la función f(x) = 3x + 2?",
            0.1, "understand",
            ["2", "3", "5", "-3"], 1
        ),
        (
            "¿Cuál es la ordenada en el origen de f(x) = 4x - 7?",
            0.4, "understand",
            ["4", "-4", "7", "-7"], 3
        ),
        (
            "¿La función f(x) = 2x + 1 es creciente o decreciente?",
            0.7, "analyze",
            ["Creciente", "Decreciente", "Constante", "No está definida"], 0
        ),
        (
            "Si f(x)=x+2 y g(x)=2x, ¿cuánto vale (f∘g)(3)?",
            1.0, "apply",
            ["6", "7", "8", "10"], 2
        ),
        (
            "Si f(x)=3x-2, ¿cuál es su función inversa?",
            1.4, "apply",
            ["(x-2)/3", "(x+2)/3", "3x+2", "3x-2"], 1
        ),
        (
            "¿Cuál es el vértice de f(x) = x² - 4x + 3?",
            1.8, "analyze",
            ["(2,-1)", "(-2,-1)", "(2,1)", "(-2,1)"], 0
        ),
        (
            "¿En qué punto corta al eje Y la función f(x)=x²+2x+5?",
            2.1, "understand",
            ["(0,0)", "(0,2)", "(0,5)", "(5,0)"], 2
        ),
        (
            "¿Cuál es el recorrido de f(x)=x² para x real?",
            2.5, "analyze",
            ["Todos los reales", "y ≥ 0", "y > 0", "y ≤ 0"], 1
        ),
        (
            "¿Dónde se anula la función f(x)=2x-8?",
            2.8, "apply",
            ["x=2", "x=3", "x=4", "x=8"], 2
        ),
        (
            "Si f(x)=x² y g(x)=x+1, ¿cuánto vale (g∘f)(2)?",
            3.0, "apply",
            ["4", "5", "6", "9"], 1
        ),
        (
            "¿Cuál de las siguientes funciones es par?",
            3.3, "analyze",
            ["f(x)=x", "f(x)=x³", "f(x)=x²", "f(x)=x+1"], 2
        ),
        (
            "Una función lineal pasa por los puntos (1,3) y (3,7). ¿Cuál es su expresión?",
            3.7, "evaluate",
            ["f(x)=2x+1", "f(x)=2x-1", "f(x)=3x", "f(x)=x+2"], 0
        ),
    ],

    "Derivadas": [

        (
            "¿Cuál es la derivada de x²?",
            -1.2, "remember",
            ["x", "2x", "x²", "2"], 1
        ),
        (
            "¿Cuál es la derivada de x³?",
            -0.9, "remember",
            ["x²", "2x²", "3x²", "3x"], 2
        ),
        (
            "¿Cuál es la derivada de sen(x)?",
            -0.6, "remember",
            ["cos(x)", "-cos(x)", "sen(x)", "-sen(x)"], 0
        ),
        (
            "¿Cuál es la derivada de eˣ?",
            -0.4, "remember",
            ["1", "x·eˣ", "eˣ", "ln(x)"], 2
        ),
        (
            "¿Cuál es la derivada de 5x?",
            -0.1, "remember",
            ["5", "x", "5x", "0"], 0
        ),
        (
            "¿Cuál es la derivada de x⁴?",
            0.2, "apply",
            ["4x", "4x³", "x³", "3x⁴"], 1
        ),
        (
            "¿Cuál es la derivada de f(x)=3x²+2x?",
            0.5, "apply",
            ["3x+2", "6x+2", "6x", "6x²+2"], 1
        ),
        (
            "¿Cuál es la derivada de f(x)=x²+5x+1?",
            0.8, "apply",
            ["2x+5", "x+5", "2x+1", "x²+5"], 0
        ),
        (
            "Aplicando la regla del producto, ¿cuál es la derivada de f(x)=x·sen(x)?",
            1.2, "apply",
            ["sen(x)+x·cos(x)", "cos(x)+x·sen(x)", "x·cos(x)", "sen(x)"], 0
        ),
        (
            "¿Cuál es la derivada de f(x)=x²eˣ?",
            1.5, "apply",
            ["2xeˣ", "x²eˣ", "eˣ(x²+2x)", "2xeˣ+x²"], 2
        ),
        (
            "¿Cuál es la derivada de ln(x)?",
            1.8, "remember",
            ["x", "1/x", "ln(x)/x", "eˣ"], 1
        ),
        (
            "¿Cuál es la derivada de sen(2x)?",
            2.0, "apply",
            ["cos(2x)", "2cos(2x)", "sen(2x)", "-2cos(2x)"], 1
        ),
        (
            "¿En qué puntos puede tener un máximo o mínimo local una función derivable?",
            2.3, "analyze",
            ["Donde f(x)=0", "Donde f'(x)=0 o no existe", "Donde f'(x)=1", "Solo donde x=0"], 1
        ),
        (
            "¿Cuál es la derivada de f(x)=(3x+1)⁵?",
            2.6, "apply",
            ["5(3x+1)⁴", "15(3x+1)⁴", "(3x+1)⁴", "15(3x+1)⁵"], 1
        ),
        (
            "La función f(x)=x²-4x+3 tiene un mínimo. ¿En qué valor de x ocurre?",
            3.0, "analyze",
            ["x=1", "x=2", "x=3", "x=4"], 1
        ),
        (
            "¿Cuál es la derivada de f(x)=1/x?",
            3.3, "apply",
            ["1/x²", "-1/x²", "-x²", "x⁻¹"], 1
        ),
        (
            "¿Cuál es el máximo de f(x)=-x²+4x+1?",
            3.7, "evaluate",
            ["3", "4", "5", "6"], 2
        ),
    ],

    "Integrales": [

        (
            "¿Cuál es una primitiva de x?",
            -1.0, "remember",
            ["x²", "x²/2 + C", "2x + C", "x + C"], 1
        ),
        (
            "¿Cuál es una primitiva de 1?",
            -0.8, "remember",
            ["1", "x + C", "x² + C", "0"], 1
        ),
        (
            "¿Cuál es una primitiva de x²?",
            -0.5, "apply",
            ["x³/2 + C", "x³/3 + C", "2x + C", "3x² + C"], 1
        ),
        (
            "¿Cuál es una primitiva de 3x²?",
            -0.2, "apply",
            ["x³ + C", "3x³ + C", "x² + C", "6x + C"], 0
        ),
        (
            "¿Cuál es una primitiva de cos(x)?",
            0.1, "remember",
            ["sen(x)+C", "-sen(x)+C", "cos(x)+C", "-cos(x)+C"], 0
        ),
        (
            "¿Cuál es una primitiva de eˣ?",
            0.4, "remember",
            ["eˣ+C", "xeˣ+C", "ln(x)+C", "x²eˣ+C"], 0
        ),
        (
            "Calcula ∫₀² x dx.",
            0.7, "apply",
            ["1", "2", "3", "4"], 1
        ),
        (
            "Calcula ∫₀¹ x² dx.",
            1.0, "apply",
            ["1/2", "1/3", "1/4", "1"], 1
        ),
        (
            "Calcula ∫₂³ 1 dx.",
            1.3, "apply",
            ["1", "2", "3", "5"], 0
        ),
        (
            "¿Cuál es una primitiva de 1/x?",
            1.6, "remember",
            ["ln|x|+C", "1/x²+C", "x·ln(x)+C", "eˣ+C"], 0
        ),
        (
            "Calcula ∫ 2x(x²+1)³ dx.",
            2.0, "apply",
            ["(x²+1)³+C", "(x²+1)⁴/4+C", "2(x²+1)⁴+C", "(x²+1)⁴+C"], 1
        ),
        (
            "¿Cuál es el área bajo f(x)=x entre x=0 y x=4?",
            2.3, "analyze",
            ["4", "6", "8", "16"], 2
        ),
        (
            "¿Cuál es una primitiva de x·eˣ?",
            2.6, "apply",
            ["xeˣ+C", "eˣ(x-1)+C", "eˣ(x+1)+C", "x²eˣ+C"], 2
        ),
        (
            "Calcula ∫₀^π sen(x) dx.",
            3.0, "apply",
            ["0", "1", "2", "π"], 2
        ),
        (
            "¿Qué representa geométricamente una integral definida de una función positiva?",
            3.3, "understand",
            ["La pendiente", "El área bajo la curva", "La derivada", "El punto máximo"], 1
        ),
        (
            "Calcula ∫₁² 1/x dx.",
            3.7, "evaluate",
            ["1", "ln(2)", "ln(3)", "2"], 1
        ),
    ],
}


def generate_answers(question_definition):

    return question_definition[3]


def create_questions(db, modules_by_course, tags):

    questions = []

    module_tag_map = {
        "Aritmética": ["aritmética", "resolución_de_problemas"],
        "Fracciones": ["fracciones", "resolución_de_problemas"],
        "Álgebra": ["álgebra", "ecuaciones"],
        "Funciones": ["funciones", "resolución_de_problemas"],
        "Derivadas": ["cálculo", "derivadas"],
        "Integrales": ["cálculo", "integrales"],
    }

    total_questions = 0

    for modules in modules_by_course:

        for module in modules:

            definitions = QUESTION_BANK[module.title]

            for (
                content,
                difficulty,
                bloom,
                answer_options,
                correct_index,
            ) in definitions:

                question = Question(
                    id=uuid.uuid4(),
                    module_id=module.id,
                    content=content,
                    type=QuestionType.single,
                    difficulty=difficulty,
                    discrimination=random.uniform(0.8, 1.8),
                    bloom_level=bloom,
                )

                db.add(question)
                db.flush()

                for answer_index, content_answer in enumerate(
                    answer_options
                ):

                    db.add(
                        Answer(
                            question_id=question.id,
                            content=content_answer,
                            is_correct=(
                                answer_index == correct_index
                            ),
                        )
                    )

                for tag_name in module_tag_map[module.title]:

                    db.add(
                        QuestionTag(
                            question_id=question.id,
                            tag_id=tags[tag_name].id,
                        )
                    )

                questions.append(question)
                total_questions += 1

    db.commit()

    print(f"       {total_questions} questions created")

    return questions


# ============================================================
# RESOURCES
# ============================================================

def create_resources(db, modules_by_course, tags, teachers):

    resources = []

    resource_templates = [
        (ResourceType.video, "video"),
        (ResourceType.article, "article"),
        (ResourceType.pdf, "pdf"),
        (ResourceType.exercise, "exercise"),
    ]

    tag_by_module = {
        "Aritmética": "aritmética",
        "Fracciones": "fracciones",
        "Álgebra": "álgebra",
        "Funciones": "funciones",
        "Derivadas": "derivadas",
        "Integrales": "integrales",
    }

    for modules in modules_by_course:

        for module in modules:

            main_tag = tags[tag_by_module[module.title]]

            for index, (resource_type, prefix) in enumerate(
                resource_templates
            ):

                difficulty = random.uniform(
                    max(-3.5, index - 2.5),
                    min(3.5, index - 1.0),
                )

                resource = LearningResource(
                    id=uuid.uuid4(),
                    title=f"{prefix}: {module.title} {index + 1}",
                    description=(
                        f"Recurso de aprendizaje centrado en "
                        f"{module.title.lower()}."
                    ),
                    url=(
                        f"https://example.com/adaptiq/"
                        f"{module.title.lower()}/{index + 1}"
                    ),
                    type=resource_type,
                    difficulty=difficulty,
                    estimated_time=random.randint(10, 60),
                    module_id=module.id,
                    created_by=random.choice(teachers).id,
                )

                db.add(resource)
                db.flush()

                db.add(
                    ResourceTag(
                        resource_id=resource.id,
                        tag_id=main_tag.id,
                    )
                )

                resources.append(resource)

    db.commit()

    return resources


# ============================================================
# ENROLLMENTS
# ============================================================

def create_enrollments(db, students, courses):

    for student in students:

        # Most students follow both courses.
        # A small percentage only follows one.
        selected_courses = courses

        if random.random() < 0.15:
            selected_courses = [random.choice(courses)]

        for course in selected_courses:

            db.add(
                Enrollment(
                    user_id=student.id,
                    course_id=course.id,
                )
            )

    db.commit()


# ============================================================
# IRT ABILITIES
# ============================================================

def create_abilities(db, students):

    for student in students:

        db.add(
            StudentAbility(
                user_id=student.id,
                theta=student._demo_theta,
            )
        )

    db.commit()


# ============================================================
# IRT SESSIONS
# ============================================================

def create_irt_session(
    db,
    student,
    course,
    theta_start,
    theta_end,
):

    started = datetime.utcnow() - timedelta(
        days=random.randint(1, 180)
    )

    finished = started + timedelta(
        minutes=random.randint(10, 35)
    )

    db.add(
        IRTSession(
            id=uuid.uuid4(),
            user_id=student.id,
            course_id=course.id,
            theta_start=theta_start,
            theta_end=theta_end,
            started_at=started,
            finished_at=finished,
        )
    )


# ============================================================
# RESPONSE SIMULATION
# ============================================================

def probability_correct(theta, difficulty, discrimination):

    x = discrimination * (theta - difficulty)

    x = max(-20, min(20, x))

    return 1 / (1 + math.exp(-x))


def choose_questions(
    questions,
    theta,
    number,
    weak_tags,
):

    scored = []

    for q in questions:

        gap = abs(q.difficulty - theta)

        fit = max(0.0, 1.0 - gap / 4.0)

        weakness_bonus = 0.0

        for qt in q.tags:

            tag_name = qt.tag.name

            if tag_name in weak_tags:

                weakness_bonus += weak_tags[tag_name]

        score = (
            fit * 0.75
            + weakness_bonus * 0.25
            + random.uniform(0, 0.15)
        )

        scored.append((q, score))

    scored.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    selected = []

    for q, _ in scored:

        if len(selected) >= number:
            break

        existing_tags = {
            qt.tag_id
            for selected_q in selected
            for qt in selected_q.tags
        }

        q_tags = {
            qt.tag_id
            for qt in q.tags
        }

        if existing_tags.intersection(q_tags):
            if random.random() < 0.55:
                continue

        selected.append(q)

    return selected


# ============================================================
# EVALUATIONS
# ============================================================

def create_evaluations(
    db,
    students,
    courses,
    modules_by_course,
    questions,
):

    for student in students:

        theta = student._demo_theta

        profile = student._demo_profile

        weak_tags = {}

        if profile == "algebra_weak":
            weak_tags["álgebra"] = 1.0
            weak_tags["ecuaciones"] = 1.0

        elif profile == "calculus_weak":
            weak_tags["cálculo"] = 1.0
            weak_tags["derivadas"] = 1.0
            weak_tags["integrales"] = 0.8

        elif profile == "at_risk":
            weak_tags["álgebra"] = 0.7
            weak_tags["cálculo"] = 0.7
            weak_tags["resolución_de_problemas"] = 0.6

        elif profile == "improving":
            weak_tags["álgebra"] = 0.5

        enrollments = student.enrollments

        if not enrollments:
            continue

        for session_index in range(EVALUATIONS_PER_STUDENT):

            enrollment = random.choice(enrollments)

            course = enrollment.course

            modules = [
                m
                for m in course.modules
            ]

            module = random.choice(modules)

            module_questions = [
                q
                for q in questions
                if q.module_id == module.id
            ]

            if not module_questions:
                continue

            adaptive_theta = theta

            selected = choose_questions(
                module_questions,
                adaptive_theta,
                random.randint(6, 12),
                weak_tags,
            )

            if not selected:
                continue

            started = datetime.utcnow() - timedelta(
                days=(EVALUATIONS_PER_STUDENT - session_index) * 7
                + random.randint(0, 5)
            )

            should_abandon = (
                random.random()
                < student._demo_dropout
                and session_index >= 2
            )

            evaluation = Evaluation(
                id=uuid.uuid4(),
                user_id=student.id,
                course_id=course.id,
                module_id=module.id,
                status=(
                    EvaluationStatus.abandoned
                    if should_abandon
                    else EvaluationStatus.completed
                ),
                current_theta=theta,
                final_theta=None,
                score=None,
                started_at=started,
                finished_at=None,
            )

            db.add(evaluation)
            db.flush()

            db.add(
                EvaluationSettings(
                    id=uuid.uuid4(),
                    evaluation_id=evaluation.id,
                    min_questions=6,
                    max_questions=20,
                    theta_stability_threshold=0.05,
                    stability_window=3,
                    max_uncertainty=0.25,
                )
            )

            correct_count = 0
            answered = 0

            previous_theta = theta

            for q in selected:

                if should_abandon and answered >= random.randint(2, 5):
                    break

                p = probability_correct(
                    theta,
                    q.difficulty,
                    q.discrimination,
                )


                p += (
                    student._demo_accuracy - 0.5
                ) * 0.25

                p = max(0.05, min(0.95, p))

                correct = random.random() < p

                if correct:
                    correct_count += 1

                answered += 1

                base_time = 15 + q.difficulty * 2

                response_time = max(
                    3,
                    random.gauss(
                        base_time + (10 if not correct else 0),
                        5,
                    )
                )

                delta = (
                    0.08
                    if correct
                    else -0.08
                )

                theta_after = max(
                    -4.0,
                    min(
                        4.0,
                        theta + delta
                    )
                )

                db.add(
                    Result(
                        id=uuid.uuid4(),
                        evaluation_id=evaluation.id,
                        question_id=q.id,
                        is_correct=correct,
                        response_time=response_time,
                        theta_before=previous_theta,
                        theta_after=theta_after,
                        question_difficulty=q.difficulty,
                        question_discrimination=q.discrimination,
                    )
                )

                previous_theta = theta_after

            if answered == 0:
                continue

            accuracy = correct_count / answered

            theta_change = (
                (accuracy - 0.5)
                * 0.35
                + student._demo_learning_rate
            )

            theta += theta_change

            theta = max(-4.0, min(4.0, theta))

            score = max(
                0.0,
                min(
                    10.0,
                    10 * accuracy
                )
            )

            evaluation.current_theta = theta
            evaluation.final_theta = theta
            evaluation.score = score

            if should_abandon:

                evaluation.finished_at = None

            else:

                evaluation.finished_at = (
                    started
                    + timedelta(
                        minutes=random.randint(8, 35)
                    )
                )

            create_irt_session(
                db,
                student,
                course,
                previous_theta,
                theta,
            )

            db.flush()

        ability = (
            db.query(StudentAbility)
            .filter_by(user_id=student.id)
            .first()
        )

        if ability:
            ability.theta = theta

    db.commit()


# ============================================================
# MODULE PROGRESS
# ============================================================

def create_module_progress(
    db,
    students,
    courses,
):

    for student in students:

        evaluations = student.evaluations

        for course in courses:

            enrolled = any(
                e.course_id == course.id
                for e in student.enrollments
            )

            if not enrolled:
                continue

            for module in course.modules:

                module_evals = [
                    e
                    for e in evaluations
                    if e.module_id == module.id
                    and e.status == EvaluationStatus.completed
                ]

                if not module_evals:

                    progress = random.uniform(
                        0,
                        25
                    )

                else:

                    scores = [
                        e.score
                        for e in module_evals
                        if e.score is not None
                    ]

                    avg_score = (
                        sum(scores) / len(scores)
                        if scores
                        else 0
                    )

                    progress = min(
                        100,
                        max(
                            5,
                            avg_score * 8
                            + len(module_evals) * 5
                            + random.uniform(-10, 10)
                        )
                    )

                db.add(
                    ModuleProgress(
                        user_id=student.id,
                        module_id=module.id,
                        progress_percentage=progress,
                        completed=progress >= 80,
                    )
                )

    db.commit()


# ============================================================
# RESOURCE USAGE
# ============================================================

def create_resource_usage(
    db,
    students,
    resources,
):

    for student in students:

        base = int(
            3
            + student._demo_engagement * 20
        )

        usage_count = random.randint(
            max(1, base // 2),
            max(2, base),
        )

        for _ in range(usage_count):

            resource = random.choice(resources)

            completed_probability = (
                student._demo_engagement * 0.8
            )

            completed = (
                random.random()
                < completed_probability
            )

            time_spent = random.uniform(
                5,
                resource.estimated_time or 30,
            )

            db.add(
                ResourceUsage(
                    id=uuid.uuid4(),
                    user_id=student.id,
                    resource_id=resource.id,
                    opened_at=(
                        datetime.utcnow()
                        - timedelta(
                            days=random.randint(0, 180)
                        )
                    ),
                    completed=completed,
                    time_spent=time_spent,
                )
            )

    db.commit()

# ============================================================
# MAIN
# ============================================================

def seed_database():

    print("\n========================================")
    print("      ADAPTIQ DEMO DATASET")
    print("========================================\n")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        print("[1/12] Resetting database...")
        reset_database(db)

        print("[2/12] Creating roles...")
        roles = create_roles(db)

        print("[3/12] Creating admin and teachers...")
        create_admin(db, roles)
        teachers = create_teachers(db, roles)

        print("[4/12] Creating students...")
        students = create_students(db, roles)

        print(f"       {len(students)} students created")

        print("[5/12] Creating learning profiles...")
        create_learning_profiles(db, students)

        print("[6/12] Creating courses and modules...")
        courses, modules = create_courses(db, teachers)

        print("[7/12] Creating tags...")
        tags = create_tags(db)

        print("[8/12] Creating questions...")
        questions = create_questions(db, modules, tags)

        print(f"       {len(questions)} questions created")

        print("[9/12] Creating resources...")
        resources = create_resources(
            db,
            modules,
            tags,
            teachers,
        )

        print(f"       {len(resources)} resources created")

        print("[10/12] Creating enrollments and IRT...")

        create_enrollments(
            db,
            students,
            courses,
        )

        create_abilities(
            db,
            students,
        )

        print("[11/12] Generating learning history...")

        create_evaluations(
            db,
            students,
            courses,
            modules,
            questions,
        )

        create_module_progress(
            db,
            students,
            courses,
        )

        create_resource_usage(
            db,
            students,
            resources,
        )

        print("[12/12] Training dropout model...")

        train_model(db)

        print("\n========================================")
        print("       DATASET READY")
        print("========================================")

        print(f"Students:       {len(students)}")
        print(f"Questions:      {len(questions)}")
        print(f"Resources:      {len(resources)}")
        print(f"Evaluations:    {db.query(Evaluation).count()}")
        print(f"Results:        {db.query(Result).count()}")
        print(f"Resource usage: {db.query(ResourceUsage).count()}")
        print(f"Module progress: {db.query(ModuleProgress).count()}")

        print("\nDemo accounts:")
        print("  admin@adaptiq.com / 1234")
        print("  teacher1@adaptiq.com / 1234")
        print("  student001@adaptiq.com / 1234")
        print("  student002@adaptiq.com / 1234")

        print("\nDataset generated successfully.\n")

    except Exception as e:

        db.rollback()

        print("\nERROR generating dataset:")
        print(e)

        raise

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()
