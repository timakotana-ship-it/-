from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.config import STATUS_TRANSACTIONS


def sendPaymentKey(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="💸 Отправить чек", callback_data="sendcheck"))
    key.row(InlineKeyboardButton(text="⬅️ Отменить", callback_data=f"gettrans_{_id}"))
    return key.as_markup()


def activeTicketListKey(
    transactionsList: list[dict], start_count: int = 0, step_count: int = 0, allTransactions: int = 0
) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    for item in transactionsList:
        name_btn = f"{item['phone_number']}"
        key.row(InlineKeyboardButton(text=name_btn, callback_data=f"openwpan_{item['_id']}"))
    key.row(
        InlineKeyboardButton(text="🔎 Поиск", switch_inline_query_current_chat="payment ")
    )
    key.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"list_gp_back_{start_count}"),
        InlineKeyboardButton(text=f"{step_count}/{allTransactions}", callback_data="kkkk"),
        InlineKeyboardButton(text="Вперед ➡️", callback_data=f"list_gp_next_{step_count}")
    )
    return key.as_markup()


def allUserTicketListKey(
    transactionsList: list[dict],
    start_count: int = 0,
    step_count: int = 0,
    allTransactions: int = 0,
    user_id: int = 0
) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    for item in transactionsList:
        name_btn = f"{item['phone_number']}"
        key.row(InlineKeyboardButton(text=name_btn, callback_data=f"openwpan_{item['_id']}"))
    key.row(
        InlineKeyboardButton(
            text="⬅️ Назад", callback_data=f"list_ut_back_{start_count}_{user_id}"
        ),
        InlineKeyboardButton(text=f"{step_count}/{allTransactions}", callback_data="kkkk"),
        InlineKeyboardButton(
            text="Вперед ➡️", callback_data=f"list_ut_next_{step_count}_{user_id}"
        )
    )
    key.row(InlineKeyboardButton(text="👤 К пользователю", callback_data=f"openuser_{user_id}"))
    return key.as_markup()


def sendMailingKey() -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="▶️ Разослать", callback_data="start_spam"))
    key.row(InlineKeyboardButton(text="🔴 Отмена", callback_data="falsespam"))
    return key.as_markup()


def mailingFalseKey() -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="🔴 Отмена", callback_data="falsespam"))
    return key.as_markup()


def transactionsListKey(
    transactionsList: list[dict], start_count: int = 0, step_count: int = 0, allTransactions: int = 0
) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    for item in transactionsList:
        name_btn = (
            f"{STATUS_TRANSACTIONS[item.get('status')]['symbol']} | "
            f"ID: {item.get('_id')} | {item.get('amount')}$"
        )
        key.row(InlineKeyboardButton(text=name_btn, callback_data=f"gettrans_{item['_id']}"))
    key.row(
        InlineKeyboardButton(text="🔎 Поиск", switch_inline_query_current_chat="payment ")
    )
    key.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"list_tr_back_{start_count}"),
        InlineKeyboardButton(text=f"{step_count}/{allTransactions}", callback_data="kkkk"),
        InlineKeyboardButton(text="Вперед ➡️", callback_data=f"list_tr_next_{step_count}")
    )
    return key.as_markup()


def transactionsListUserKey(
    transactionsList: list[dict],
    start_count: int = 0,
    step_count: int = 0,
    allTransactions: int = 0,
    user_id: int = 0
) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    for item in transactionsList:
        name_btn = (
            f"{STATUS_TRANSACTIONS[item.get('status')]['symbol']} | "
            f"ID: {item.get('_id')} | {item.get('amount')}$"
        )
        key.row(InlineKeyboardButton(text=name_btn, callback_data=f"gettrans_{item['_id']}"))
    key.row(
        InlineKeyboardButton(
            text="⬅️ Назад", callback_data=f"list_tru_back_{start_count}_{user_id}"
        ),
        InlineKeyboardButton(text=f"{step_count}/{allTransactions}", callback_data="kkkk"),
        InlineKeyboardButton(
            text="Вперед ➡️", callback_data=f"list_tru_next_{step_count}_{user_id}"
        )
    )
    key.row(InlineKeyboardButton(text="👤 К пользователю", callback_data=f"openuser_{user_id}"))
    return key.as_markup()


def twoFactorFalsePayKey(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(
        InlineKeyboardButton(text="🔴 Да, отменить выплату", callback_data=f"falpays_{_id}")
    )
    key.row(InlineKeyboardButton(text="⬅️ Вернуться", callback_data=f"gettrans_{_id}"))
    return key.as_markup()


def transactionViewerKey(_id: int, status: str, amount: float | None = None) -> InlineKeyboardMarkup:
    """
    Клавиатура просмотра транзакции для админа.
    Если передать amount — кнопка 'Выплатить' будет содержать сумму и callback: payout_<id>_<amount>
    Если amount не передан — callback остаётся payout_<id> и обработчик должен подгрузить сумму из БД.
    """
    key = InlineKeyboardBuilder()
    if status == "wait_withdraft":
        if amount is not None:
            # Передаём сумму прямо в callback (быстрее и удобнее)
            key.row(InlineKeyboardButton(text=f"💸 Выплатить ({amount}$)", callback_data=f"payout_{_id}_{amount}"))
        else:
            # Без суммы — обработчик подгрузит её из БД по id
            key.row(InlineKeyboardButton(text="💸 Выплатить", callback_data=f"payout_{_id}"))
        key.row(InlineKeyboardButton(text="🔴 Отказать", callback_data=f"falsepay_{_id}"))
        key.row(InlineKeyboardButton(text="⬅️ К списку", callback_data="transactions"))
    else:
        key.row(InlineKeyboardButton(text="⬅️ К списку", callback_data="transactions"))
    return key.as_markup()


def workPanel(_id: int, status: str) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    match status:
        case "wait_auth":
            key.row(InlineKeyboardButton(text="📲 Ввести код", callback_data=f"getauthcode_{_id}"))
            key.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"falsenum_{_id}"))
        case "in_proccess":
            key.row(InlineKeyboardButton(text="✅ Выплатить", callback_data=f"sucwork_{_id}"))
            key.row(InlineKeyboardButton(text="❌ Слет", callback_data=f"airfalse_{_id}"))
        case "user_auth":
            key.row(InlineKeyboardButton(text="❌ Отменить", callback_data=f"falsenum_{_id}"))
    return key.as_markup()


def twoFactorSclet(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="❌ Да, отменить", callback_data=f"yfs_{_id}"))
    key.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"openwpan_{_id}"))
    return key.as_markup()


def twoFactorCancleWork(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="❌ Да, отменить", callback_data=f"tffalsework_{_id}"))
    key.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"openwpan_{_id}"))
    return key.as_markup()


def twoFactorSucWork(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="✅ Да, выплатить", callback_data=f"tfsucwork_{_id}"))
    key.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"openwpan_{_id}"))
    return key.as_markup()


def sendCodeUser(_id: int, code: str) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="📨 Отправить код", callback_data=f"sndc|{_id}|{code}"))
    key.row(InlineKeyboardButton(text="⬅️ Вернуться", callback_data=f"openwpan_{_id}"))
    return key.as_markup()


def openWorkPanel(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="⬅️ Вернуться", callback_data=f"openwpan_{_id}"))
    return key.as_markup()


def startPhoneWork(_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data="phoneworklist"),
        InlineKeyboardButton(text="▶️ Начать работу", callback_data=f"startwork_{_id}")
    )
    return key.as_markup()


def phonesListWorks(
    phoneList: list[dict], start_count: int = 0, step_count: int = 0, allPhones: int = 0
) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    for item in phoneList:
        number = f"{item['phone_number']}"
        key.row(InlineKeyboardButton(text=number, callback_data=f"getphone_{item['_id']}"))
    key.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"list_pl_back_{start_count}"),
        InlineKeyboardButton(text=f"{step_count}/{allPhones}", callback_data="kkkk"),
        InlineKeyboardButton(text="Вперед ➡️", callback_data=f"list_pl_next_{step_count}")
    )
    return key.as_markup()


def searchUserKey() -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(
        InlineKeyboardButton(text="🔎 Поиск", switch_inline_query_current_chat="user ")
    )
    return key.as_markup()


def deleteTicketKey(uniq_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delticket_{uniq_id}"))
    return key.as_markup()


def withdraftPanle(_id: int, amount: float | None = None) -> InlineKeyboardMarkup:
    """
    Кнопки вывода/панели. Если передать amount — кнопка будет показывать сумму и callback payout_<id>_<amount>
    """
    key = InlineKeyboardBuilder()
    if amount is not None:
        key.row(InlineKeyboardButton(text=f"💸 Выплатить ({amount}$)", callback_data=f"payout_{_id}_{amount}"))
    else:
        key.row(InlineKeyboardButton(text="💸 Выплатить", callback_data=f"payout_{_id}"))
    key.row(InlineKeyboardButton(text="🔴 Отказать", callback_data=f"falsepay_{_id}"))
    return key.as_markup()


def withdraftChatPanel(url: str) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="↗️ Перейти к выводу", url=url))
    return key.as_markup()


def userOptions(user_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(
        InlineKeyboardButton(text="🔐 Роль", callback_data=f"set_role_{user_id}"),
        InlineKeyboardButton(text="💭 Сообщение", callback_data=f"smsg_{user_id}")
    )
    key.row(
        InlineKeyboardButton(
            text="💸 История транзакций", callback_data=f"transactions_{user_id}"
        )
    )
    key.row(
        InlineKeyboardButton(text="📲 История номеров", callback_data=f"numhistory_{user_id}")
    )
    key.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data=f"statistic_{user_id}")
    )
    return key.as_markup()


def setRoleKey(user_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(
        InlineKeyboardButton(text="🔐 Админ", callback_data=f"updrole_{user_id}_admin"),
        InlineKeyboardButton(text="👤 Юзер", callback_data=f"updrole_{user_id}_user"),
        InlineKeyboardButton(text="🔴 Бан", callback_data=f"updrole_{user_id}_ban")
    )
    key.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"openuser_{user_id}"))
    return key.as_markup()


def sendMsgKey(user_id: int) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="✅ Отправить сообщение", callback_data="sendmsguser"))
    key.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"openuser_{user_id}"))
    return key.as_markup()


def backFunKey(call: str) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="↩️ Назад", callback_data=call))
    return key.as_markup()


def waitKey() -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text="⏳ Подождите", callback_data="wait"))
    return key.as_markup()


def userOpenKey(
    user_id: int, admin: int, moder: int, ban: int
) -> InlineKeyboardMarkup:
    key = InlineKeyboardBuilder()
    key.row(
        InlineKeyboardButton(
            text=f"{'✅' if admin == 1 else '❌'} Админ",
            callback_data=f"usadmin_{user_id}_{'0' if admin == 1 else '1'}"
        ),
        InlineKeyboardButton(
            text=f"{'✅' if moder == 1 else '❌'} Модератор",
            callback_data=f"usmoder_{user_id}_{'0' if moder == 1 else '1'}"
        ),
        InlineKeyboardButton(
            text=f"{'✅' if ban == 1 else '❌'} Бан",
            callback_data=f"usban_{user_id}_{'0' if ban == 1 else '1'}"
        )
    )
    return key.as_markup()


def clear_html(get_text: str) -> str:
    if get_text is not None:
        get_text = (
            get_text.replace("<code>", "")
            .replace("</code>", "")
            .replace("<b>", "")
            .replace("</b>", "")
            .replace("<i>", "")
            .replace("</i>", "")
        )
    else:
        get_text = ""
    return get_text


# Утилита: генерировать клавиатуру payout с суммой удобным вызовом
def make_admin_payout_kb(number_id: int, amount: float | None = None) -> InlineKeyboardMarkup:
    """
    Удобный генератор клавиатуры для уведомления админа.
    Используйте при отправке сообщения админу:
      await bot.send_message(ADMIN_CHAT_ID, text, reply_markup=make_admin_payout_kb(number_id, amount))
    """
    return withdraftPanle(number_id, amount)
