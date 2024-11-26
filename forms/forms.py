from aiogram.fsm.state import State, StatesGroup

class TaskForm(StatesGroup):
    task_condition = State()
    currency_pair = State()
    

