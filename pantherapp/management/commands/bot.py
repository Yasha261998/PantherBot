import django.db.utils
from django.core.management.base import BaseCommand
from django.conf import settings
from pantherapp.models import CustomUser
from datetime import timedelta, datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asgiref.sync import sync_to_async
from aiogram.utils import executor
from django.contrib.auth.hashers import make_password
import re

bot = Bot(settings.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())        # Диспетчер
dp.middleware.setup(LoggingMiddleware())

error_db = 'Error DB'


class StatesBot(StatesGroup):
    name = State()
    password = State()


@dp.message_handler(commands=["start"], state=None)
async def _start(message: types.Message, state: FSMContext):
    """Обработка команды /start
    :param message: входящее сообщение
    """

    chat_id = message.chat.id
    username = message.from_user.username
    name = message.from_user.first_name
    if name is not None:
        await state.update_data(name=name)
        #############################
        await bot.send_message(chat_id, f'Здравствуйте, {username}, '
                                        f'укажите пожалуйста пароль для регистрации:')
        await StatesBot.password.set()
    else:
        await bot.send_message(chat_id, f'Здравствуйте, {username}, укажите пожалуйста ваше имя')
        await StatesBot.name.set()


@dp.message_handler(state=StatesBot.name)
async def _get_first_name(message: types.Message, state: FSMContext):
    """Обработка сообщения о имени пользователя
    :param message: входящее сообщение
    :param state: текущее состояние - имя пользователя
    """

    await state.update_data(name=message.text)
    await bot.send_message(message.chat.id, f'Укажите пожалуйста пароль для регистрации:')
    await StatesBot.password.set()


@dp.message_handler(state=StatesBot.password)
async def _get_password(message: types.Message, state: FSMContext):
    """Обработка сообщения пароля
        :param message: входящее сообщение
        :param state: текущее состояние - пароль
    """

    id_telegram = message.from_user.id
    username = message.chat.username
    chat_id = message.chat.id
    data = await state.get_data()
    name = data.get('name')
    password = make_password(message.text)

    if re.search(r"[ :'\"]", password):
        await bot.send_message(chat_id, f'Пароль не должен содержать пробелы, двоеточия и кавычки. \n'
                                        f'Введите пароль ещё раз')
        await StatesBot.password.set()
    else:
        try:
            obj, created = await sync_to_async(CustomUser.objects.update_or_create)(id_telegram=id_telegram,
                                                                                    username=username,
                                                                                    defaults={'first_name': name,
                                                                                              'password': password})
            if created or obj:
                #############################
                await bot.send_message(chat_id, f'Спасибо за регистрацию, {username}.\n'
                                                f'Ссылка для авторизации: ')
                await state.finish()
            else:
                await bot.send_message(chat_id, error_db)
        except django.db.utils.IntegrityError:
            print("Ошибка обновления данных")


class Command(BaseCommand):
    help = 'Телеграмм бот регистрации пользователей'

    def handle(self, *args, **options):
        executor.start_polling(dp)

