
from aiogram.fsm.state import StatesGroup, State


class RegisterUserStates(StatesGroup):
    """
    Стейты для процесса регистрации пользователя
    """
    first_name_input = State()
    last_name_input = State()


class EnterScoreStates(StatesGroup):
    """
    Стейты для процесса ввода результата ЕГЭ по предмету
    """
    select_subject = State()
    score_input = State()
