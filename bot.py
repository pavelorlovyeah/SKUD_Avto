from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold
#from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
#from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import TOKEN
import json
import os

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

storage = MemoryStorage()

# Объявляем состояния
class Condi(StatesGroup):
    Init = State()
    fio_ = State()
    adress_ = State()
    plates_ = State()


@dp.message_handler(commands=['start'], state = '*')
async def process_start_command(message: types.Message):
    await message.reply("Бот необходим для формирования заявки для пропуска автомобиля.\n"
                        "Нажмите /zayavka")

@dp.message_handler(commands=['zayavka'], state = '*')
async def process_zayavka_command_1(message: types.Message, state: FSMContext):
    await Condi.Init.set()
    await message.reply("Укажите ФИО:")

@dp.message_handler(state = Condi.Init)
async def process_zayavka_command_2(msg: types.Message, state: FSMContext):
    global fio
    fio = msg.text
    await Condi.fio_.set()
    await msg.answer('Укажите адрес:')

@dp.message_handler(state = Condi.fio_)
async def process_zayavka_command_3(msg: types.Message, state: FSMContext):
    global adress
    adress = msg.text
    await Condi.adress_.set()
    await msg.answer('Укажите номер автомобиля:')

@dp.message_handler(state = Condi.adress_)
async def process_zayavka_command_4(msg: types.Message, state: FSMContext):
    global plates
    plates = msg.text.upper()
    await bot.send_message(msg.from_user.id, text(fio, adress, plates, sep='\n'))
    final_message = 'Для формирования новой заявки щелкните\n /zayavka'
    await bot.send_message(msg.from_user.id, final_message)

    # Проверка наличия request_list.json в директории
    if os.path.exists(os.path.join(os.getcwd(), 'request_list.json')):
        print(f'Adding request from {fio}, id: {msg.from_user.id}')
        # Cчитываем из готового json данные
        with open('request_list.json', 'r') as f:
            loaded_data = json.load(f)
        # Обновляем/добавляем новую запись в словарь
        new_record = {str(msg.from_user.id):
                    {'fio': fio, 'adress': adress, 'plates': plates}}
        loaded_data.update(new_record)
        # Записываем новый json с обновленными данными
        with open('request_list.json', 'w') as f:
            json.dump(loaded_data, f, ensure_ascii=False)

    # Создаем json, если он еще не был создан
    else:
        with open('request_list.json', 'w') as f:
            json.dump({
                msg.from_user.id:
                    {"fio": fio,
                "adress": adress,
                "plates": plates
            }}, f, ensure_ascii=False)

if __name__ == '__main__':
    executor.start_polling(dp)