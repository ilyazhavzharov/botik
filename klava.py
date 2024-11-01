from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

signal_btn = InlineKeyboardButton("❗Выдать сигнал❗", callback_data='signal')
instr_btn = InlineKeyboardButton("📚 Инструкция", callback_data='instruction')

keyboard = InlineKeyboardMarkup()
keyboard.add(signal_btn) 
keyboard.add(instr_btn)


main_menu_btn = InlineKeyboardButton("🏠 Главное меню", callback_data='main_menu')
keyboard.add(main_menu_btn)