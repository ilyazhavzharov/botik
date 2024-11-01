import logging
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import io
import random
from typing import Union
from sets import *
from klava import *
from mst import *
from db import*
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from typing import Union

class AdminState(StatesGroup):
    waiting_for_new_url = State()
    
logging.basicConfig(level=logging.INFO)

def hlink(label: str, url: str) -> str:
    return f'<a href="{url}">{label}</a>'

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

registration_url = "https://1wpgyc.xyz/casino/list?open=register"

@dp.message_handler(commands=['admin'], state="*")
async def admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await AdminState.waiting_for_new_url.set()
        admin_keyboard = InlineKeyboardMarkup()
        change_url_btn = InlineKeyboardButton("🔗 Сменить ссылку", callback_data='change_url')
        admin_keyboard.add(change_url_btn)
        await message.answer("Выберите действие:", reply_markup=admin_keyboard)
    else:
        await state.finish()
        await message.answer("У вас нет доступа к этой команде.")

@dp.callback_query_handler(lambda c: c.data == 'change_url', state=AdminState.waiting_for_new_url)
async def handle_change_url(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите новый URL для регистрации:")

@dp.message_handler(state=AdminState.waiting_for_new_url)
async def change_registration_url(message: types.Message, state: FSMContext):
    global registration_url
    registration_url = message.text
    await message.answer(f"URL регистрации обновлен: {registration_url}")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def main_menu_handler(callback_query: types.CallbackQuery):
    await send_welcome_message(callback_query.message)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    await send_welcome_message(message)

async def send_welcome_message(message_or_query):
    welcome_text = (
        "Добро пожаловать в 🔸<b>MINES OpenAI</b>🔸!\n\n"
        "💣Mines - это гэмблинг игра в букмекерской конторе 1win, "
        "которая основывается на классическом “Сапёре”.\n"
        "Ваша цель - открывать безопасные ячейки и не попадаться в ловушки.\n\n\n"
        "<b><code style=\"color: blue;\">"
        "Наш бот основан на нейросети от OpenAI.\n"
        "Он может предугадать расположение звёзд с вероятностью 85%."
        "</code></b>"
    )
    keyboard = InlineKeyboardMarkup(row_width=2)
    reg_btn = InlineKeyboardButton("📝 Регистрация", callback_data='registration')
    instr_btn = InlineKeyboardButton("📚 Инструкция", callback_data='instruction')
    signal_btn = InlineKeyboardButton("❗Выдать сигнал❗", callback_data='signal')
    keyboard.add(reg_btn, instr_btn, signal_btn)

    if isinstance(message_or_query, types.Message):
        await message_or_query.answer(welcome_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else: 
        await message_or_query.bot.send_message(chat_id=message_or_query.from_user.id, text=welcome_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    
@dp.callback_query_handler(lambda c: c.data)  
async def handle_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == 'registration':
        reg_text = (
            "✅ Зарегистрируйтесь для работы с ботом и после регистрации введите ваш айди в бота."
        )
        
        link_btn = InlineKeyboardButton("🔗 Регистрация", url=registration_url)
        main_menu_btn = InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')
        reg_keyboard = InlineKeyboardMarkup().add(link_btn, main_menu_btn)
        await bot.send_message(callback_query.from_user.id, reg_text, reply_markup=reg_keyboard)

    elif callback_query.data == 'instruction':
        instruction_text = (
    "Бот основан и обучен на кластере нейросети от OpenA 🖥<b>[ChatGPT-v4]</b>.\n\n"
    "Для тренировки бота было сыграно 🎰8000+ игр.\n"
    "В данный момент пользователи бота успешно делают в день 20-30% от своего 💸капитала!\n\n"
    "<b><code style=\"color: blue;\">В данный момент бот всё ещё обучается и точность\n"
    "бота составляет 85%!</code></b>\n\n"
    "Для получения максимального профита следуйте следующей инструкции:\n\n\n"
    f"🔸 1. Пройти регистрацию в букмекерской конторе {hlink('1WIN', url=registration_url)}\n"
    "Если не открывается - заходим с включенным VPN (Швеция).\n"
    f"Я пользуюсь VPN Super Unlimited Proxy\n{hlink('ANDROID', 'https://play.google.com/store/apps/details?id=com.free.vpn.super.hotspot.open')}\n"
    f"{hlink('IOS', 'https://apps.apple.com/ru/app/vpn-super-vpn-%D0%B2%D0%BF%D0%BD-%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8/id1370293473')}\n"
    "<b><code style=\"color: blue;\">Без регистрации доступ к сигналам не будет открыт!</code></b>\n\n"
    "🔸 2. Пополнить баланс своего аккаунта.\n\n"
    "🔸 3. Перейти в раздел 1win games и выбрать игру 💣\"MINES\".\n\n"
    "🔸 4. Выставить кол-во ловушек в размере трёх. Это важно!\n\n"
    "🔸 5. Запросить сигнал в боте и ставить по сигналам из бота.\n\n"
    "🔸 6. При неудачном сигнале советуем удвоить(Х²) ставку что бы полностью перекрыть потерю при следующием сигнале."
        )
        with open('photos/1.jpg', 'rb') as photo_file:
            photo_stream = io.BytesIO(photo_file.read())
        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo_stream, caption=instruction_text, parse_mode=ParseMode.HTML)
        next_text = "После успешной регистрации введите ваш айди боту.\nВкладка <b>'пополнение'</b> и в правом верхнем углу будет ваш ID\nКоторый вам нужно отправить в нашего бота!"
        with open('photos/2.jpg', 'rb') as photo_file2:
            photo_stream2 = io.BytesIO(photo_file2.read())
            main_menu_btn = InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')
            reg_keyboard = InlineKeyboardMarkup().add(main_menu_btn)
        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo_stream2, caption=next_text, reply_markup=reg_keyboard, parse_mode=ParseMode.HTML)

    elif callback_query.data == 'signal':
        user_code = check_user_code(callback_query.from_user.id)
        if is_code_valid(user_code):
            random_photo_number = random.randint(1, 54)
            photo_path = f'varianty/{random_photo_number}.jpg'
            with open(photo_path, 'rb') as photo_file:
                photo_stream = io.BytesIO(photo_file.read())
            await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo_stream, reply_markup=keyboard)
        else:
            instr_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("📚 Инструкция", callback_data='instruction'))
            await bot.send_message(callback_query.from_user.id, "Для начала, пожалуйста, зарегистрируйтесь", reply_markup=instr_keyboard)


@dp.message_handler(lambda message: message.text.startswith('Регистрация:'))
async def register_user(message: types.Message):
    code = message.text.split('Регистрация:')[1].strip()
    add_code(code)
    await message.answer("Код зарегистрирован!", reply_markup=keyboard)

@dp.message_handler()
async def check_code(message: types.Message):
    user_id = message.from_user.id
    code = message.text.strip()

    if is_code_valid(code):
        add_user(user_id, code)
        await message.answer("Вы успешно зарегистрированы! Теперь у вас есть доступ к сигналам.", reply_markup=keyboard)
    else:
        await message.answer("Неправильный код регистрации.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
