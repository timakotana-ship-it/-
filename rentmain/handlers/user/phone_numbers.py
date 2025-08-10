from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import *
from typing import Any, Dict, Union
from loader import *
from datetime import datetime
from keyboards.reply.usermainkey import *
from keyboards.inline.userinlinekey import *
from loguru import logger
from utils.misc_func.bot_models import *


from typing import *
from keyboards.inline.adminkeyinline import *

from data.config import ROLES
from states.user_state import *
from utils.misc_func.otherfunc import format_phone_number



# ---- заменить существующую number_rent_start_page ----
@userRouter.callback_query(F.data=='number_rent')
async def number_rent_start_page(call: CallbackQuery, state):
    # показываем выбор тарифов, не устанавливаем сразу состояние phone_number
    await state.clear()
    await call.message.delete()
    await call.message.answer(
        "<b>Выберите тариф для сдачи номера:</b>",
        reply_markup=rent_price_kb()
    )
    await call.answer()

# ---- добавить: обработчик выбора тарифа ----
@userRouter.callback_query(lambda c: c.data and c.data.startswith("tariff|"))
async def tariff_selected(call: CallbackQuery, state):
    # формат callback_data: tariff|<price>|<label>
    try:
        _, price_str, label = call.data.split("|")
    except Exception:
        await call.answer("Ошибка выбора тарифа", show_alert=True)
        return

    # сохраняем тариф в FSM (aiogram v3: FSMContext-like API)
    # state здесь в твоём проекте уже передаётся и поддерживает set_state()/update_data()/get_data()
    await state.update_data(tariff_price=float(price_str), tariff_label=f"{price_str}$/{label}min")

    # переводим пользователя в состояние ввода номера (используем существующий state addPhoneNumber.phone_number)
    await state.set_state(addPhoneNumber.phone_number)

    await call.message.edit_text(
        f"Вы выбрали тариф: {price_str}$ / {label}min.\n\nОтправьте номер в формате <code>79999999999</code>.",
        parse_mode="HTML",
        reply_markup=backFunKey('backMainMenu')
    )
    await call.answer()

    text = f'''
<b>📲 Сдать номер</b>

<i>ℹ️ Что бы сдать свой номер в аренду введите его в формате:</i>

<code>79999999999</code>

<i>🔔 После этого вы попадете в очередь, когда очередь дойдет до вас придет уведомление.</i>
'''

    await call.message.delete()

    return call.message.answer(text, reply_markup=backFunKey('backMainMenu'))



# ---- заменить/подправить существующую функцию addPhoneNumber_phone_number_handler ----
@userRouter.message(addPhoneNumber.phone_number)
async def addPhoneNumber_phone_number_handler(msg: Message, state):
    phone_number = format_phone_number(msg.text)
    logger.warning(phone_number)

    if phone_number is False:
        await state.set_state(addPhoneNumber.phone_number)
        return msg.answer(
            'Неправильный формат номер телефона, пожалуйста, введите номер телефона в формате:\n\n<code>79999999999</code>',
            reply_markup=backFunKey('backMainMenu'),
            parse_mode="HTML"
        )

    # берем тариф из FSM (если есть)
    data = await state.get_data()
    tariff_price = data.get("tariff_price")  # может быть None
    tariff_label = data.get("tariff_label")

    # === Важно: обновите db.add_phone_number чтобы принимать tariff (см. ниже) ===
    # пример: add = await db.add_phone_number(user_id, phone_number, tariff_price, tariff_label)
    # если db.add_phone_number не принимает тариф — поменяй реализацию в db или вызови отдельный метод
    add = await db.add_phone_number(msg.from_user.id, phone_number, tariff_price)

    await state.clear()

    if add['status']:
        text = f'''
<b>✅ Номер телефона</b> {msg.text} <b>был успешно добавлен в очередь!</b>

<i>📄 Место в очереди для этого номера телефона:</i> <code>{add["msg"]}</code>
'''
    else:
        text = f'''
<b>⚠️ Не удалось добавить номер телефона в очередь</b>

📄 Причина: <code>{add["msg"]}</code>
'''
    await msg.answer(text, reply_markup=backFunKey('backMainMenu'), parse_mode="HTML")

    # === уведомление админа: отправляем admin сообщение с кнопкой payout, передаём сумму ===
    # number_id = add.get("number_id")  # если db возвращает id
    # if number_id:
    #     await bot.send_message(ADMIN_CHAT_ID,
    #         f"Новый номер в очереди: {phone_number}\nТариф: {tariff_label or 'не указан'}\nID: {number_id}",
    #         reply_markup=make_admin_payout_kb(number_id, tariff_price)
    #     )
    