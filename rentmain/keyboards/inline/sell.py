# handlers/sell.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import /* имя_файла_который_ты_прислал */  # <- подставь реальное имя модуля, например keyboards.inline_keys
# пример: from keyboards import inline_keys as kb_module
from keyboards import rent_price_kb  # если вынес в отдельный файл — подкорректируй импорт

router = Router()

class SellStates(StatesGroup):
    waiting_for_tariff = State()
    waiting_for_number = State()

# 1) Кнопка "Сдать номер" уже есть в mainKeyInline: callback_data="number_rent"
@router.callback_query(F.data == "number_rent")
async def on_number_rent(cb: CallbackQuery, state: FSMContext):
    # показываем клавиатуру тарифов
    await cb.message.edit_text("Выберите тариф, по которому вы сдаёте номер:", reply_markup=rent_price_kb())
    await cb.answer()

# 2) Пользователь выбирает тариф
@router.callback_query(lambda c: c.data and c.data.startswith("tariff|"))
async def tariff_selected(cb: CallbackQuery, state: FSMContext):
    # формат: tariff|9|20
    _, price_str, label = cb.data.split("|")
    price = float(price_str)
    await state.update_data(tariff_price=price, tariff_label=f"{price_str}$/{label}min")
    await state.set_state(SellStates.waiting_for_number)
    await cb.message.edit_text(f"Вы выбрали тариф: {price_str}$ / {label}min.\nТеперь отправьте номер, который хотите сдать.")
    await cb.answer()

# 3) Получаем номер и сохраняем в БД
@router.message(SellStates.waiting_for_number)
async def receive_number(message: Message, state: FSMContext):
    data = await state.get_data()
    tariff_price = data.get("tariff_price")
    tariff_label = data.get("tariff_label")
    user_id = message.from_user.id
    phone = message.text.strip()

    # === TODO: заменить на вашу логику вставки в БД ===
    # Пример (псевдо):
    # number_id = await db.insert_number(user_id=user_id, number=phone, tariff_price=tariff_price, tariff_label=tariff_label)
    # ================================================

    # отправляем подтверждение пользователю
    await message.answer("Номер принят в очередь. Ожидайте подтверждения от админа.")
    await state.clear()

    # === TODO: уведомление админа ===
    # Нужно отправить в админ-чат/канал сообщение с деталями и кнопкой "Выплатить" с callback_data=f"payout|{number_id}"
    # Пример:
    # await bot.send_message(ADMIN_CHAT_ID, f"Новый номер: {phone}\nТариф: {tariff_label}\nUser: {user_id}", reply_markup=make_admin_payout_kb(number_id))
    # =================================
