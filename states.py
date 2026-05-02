from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_product_price = State()
    waiting_for_product_desc = State()
    waiting_for_product_stock = State()
