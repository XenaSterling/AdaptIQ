"""
Módulo: __init__.py
Descripción: Centraliza las importaciones de los modelos de datos
             para facilitar su acceso desde otros módulos.
Autor: Raquel Del Castillo Pérez
"""

from .user import User
from .role import Role
from .course import Course
from .module import Module
from .enrollment import Enrollment
from .question import Question
from .answer import Answer
from .tag import Tag
from .question_tag import QuestionTag
from .evaluation import Evaluation
from .evaluation_settings import EvaluationSettings
from .result import Result
from .result_answer import ResultAnswer
from .student_ability import StudentAbility
from .recommendation import Recommendation
from .irt_session import IRTSession
from .adaptive_log import AdaptiveLog
from .module_progress import ModuleProgress
from .learning_profile import LearningProfile
from .learning_resource import LearningResource
from .resource_tag import ResourceTag
from .resource_usage import ResourceUsage