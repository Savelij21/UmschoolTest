
from aiogram.fsm.state import StatesGroup, State


class RegisterUserStates(StatesGroup):
    first_name_input = State()
    last_name_input = State()


class EnterScoreStates(StatesGroup):
    select_subject = State()
    score_input = State()
