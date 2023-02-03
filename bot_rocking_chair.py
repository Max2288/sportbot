import datetime
import logging
import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, ContentType
import asyncio
from main import *
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv('TOKEN'))

# Bot_init
bot = aiogram.Bot(token=TOKEN,parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.ERROR, filename="log/{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d")),
                    filemode="w")


class Form(StatesGroup):
    change_key = State()
    value = State()
    workout_set = State()
    save = State()
    group_set = State()


# Handlers
@dp.message_handler(commands="start")
async def start_message(message: Message):
    create_user(message.from_user.id, message.from_user.full_name)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Быстрая тренировка", callback_data="fast_workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Персональная тренировка", callback_data="personal_workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Мои параметры", callback_data="characteristics"))
    keyboard.add(InlineKeyboardMarkup(
        text="Дневник тренировок", callback_data="diary_workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Описание кнопок", callback_data="description"))
    await message.answer(text="Добро пожаловать!\
                             \nВыберите пункт меню", reply_markup=keyboard, )


@dp.callback_query_handler(text='start')
async def start_call(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Быстрая тренировка", callback_data="fast_workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Персональная тренировка", callback_data="personal_workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Мои параметры", callback_data="characteristics"))
    keyboard.add(InlineKeyboardMarkup(
        text="Дневник тренировок", callback_data="diary_workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Описание кнопок", callback_data="description"))
    await call.message.answer(text="Добро пожаловать!\
                             \nВыберите пункт меню", reply_markup=keyboard)


@dp.callback_query_handler(text='description')
async def description_call(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Главное меню", callback_data="start"))
    await call.message.answer(text="Добро пожаловать!\
                                  \nЯ ваш персональный помощник по тренировкам.\n\
                                  \nВсе упражнения берутся из базы и каждый раз будут меняться, чтобы вам было не скучно заниматься.\n\
                                  \n«Быстрая тренировка» - тут доступны тренировки, не учитывающие ваши персональные параметры, но учитывающие место тренировки.\n\
                                  \n«Персональная тренировка» - тут доступны тренировки, учитывающие ваши параметры, цели и место проведения тренировки. Для упражнений будут рассчитаны количество подходов и необходимые веса.\n\
                                  \n«Мои параметры» - ваши персональные параметры, необходимые для подбора оптимальной тренировки.\n\
                                  \n«Дневник тренировок» – тут можно посмотреть историю занятий.",
                              reply_markup=keyboard)


@dp.callback_query_handler(text='fast_workout')
async def fast_workout(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardMarkup(text="Силовая", callback_data="power")
    button_2 = InlineKeyboardMarkup(text="День ног", callback_data="Ноги")
    keyboard.row(button_1, button_2)
    keyboard.add(InlineKeyboardMarkup(text="Кардио", callback_data="Кардио"))
    keyboard.add(InlineKeyboardMarkup(
        text="Функциональная", callback_data="Функциональная"))
    keyboard.add(InlineKeyboardMarkup(
        text="Главное меню", callback_data="start"))
    await call.message.answer(text="Выберите тип тренировки:\
                                \n<b>Силовая тренировка</b>:\
                                  \n\t* Одно упражнение на разминку\
                                  \n\t* Три упражнения на одну группы мышц\
                                  \n\t* Три упражнения на другую группу мышц\
                                  \n\t* Одно упражнение на пресс\
                                \n<b>Тренировка на ноги</b>:\
                                  \n\t* Одно упражнение на разминку\
                                  \n\t* Пять упражнений на ноги\
                                  \n\t* Одно упражнение на пресс\
                                \n<b>Кардио тренировка</b>:\
                                  \n\t* 30 минут упражнения на кардио\
                                  \n\t* Одно упражнение на пресс\
                                \n<b>Функциональная тренировка</b>:\
                                  \n\t* Одно упражнение на разминку\
                                  \n\t* Пять функциональных упражнений\n\
                                \nВсе упражнения подбираются из базы и каждую новую тренировку меняются, чтобы вам было интересно заниматься.",
                              reply_markup=keyboard)


@dp.callback_query_handler(text='power')
async def power(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(text="Грудь", callback_data="Грудь_1"))
    keyboard.add(InlineKeyboardMarkup(text="Ноги", callback_data="Ноги_1"))
    keyboard.add(InlineKeyboardMarkup(text="Спина", callback_data="Спина_1"))
    keyboard.add(InlineKeyboardMarkup(text="Бицепс", callback_data="Бицепс_1"))
    keyboard.add(InlineKeyboardMarkup(text="Плечи", callback_data="Плечи_1"))
    keyboard.add(InlineKeyboardMarkup(
        text="Трицепс", callback_data="Трицепс_!"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="fast_workout"))
    await call.message.answer(text="Выберите первую группу мышц", reply_markup=keyboard)


@dp.callback_query_handler(text='Грудь_1')
@dp.callback_query_handler(text='Ноги_1')
@dp.callback_query_handler(text='Спина_1')
@dp.callback_query_handler(text='Бицепс_1')
@dp.callback_query_handler(text='Плечи_1')
@dp.callback_query_handler(text='Трицепс_1')
async def power_1(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(group_set=call.data[:-2])
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(text="Грудь", callback_data="Грудь_2"))
    keyboard.add(InlineKeyboardMarkup(text="Ноги", callback_data="Ноги_2"))
    keyboard.add(InlineKeyboardMarkup(text="Спина", callback_data="Спина_2"))
    keyboard.add(InlineKeyboardMarkup(text="Бицепс", callback_data="Бицепс_2"))
    keyboard.add(InlineKeyboardMarkup(text="Плечи", callback_data="Плечи_2"))
    keyboard.add(InlineKeyboardMarkup(
        text="Трицепс", callback_data="Трицепс_2"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="fast_workout"))
    await call.message.answer(text="Выберите вторую группу мышц", reply_markup=keyboard)


@dp.callback_query_handler(text='Ноги')
async def power(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    trainings_id = get_trainings_id('Разминка',count=1, user_id=user_id)
    trainings_id += get_trainings_id('Ноги', count=5, user_id=user_id)
    trainings_id += get_trainings_id('Пресс',count=1, user_id=user_id)
    workout_set = "\n\t* ".join(get_trainings(trainings_id))
    await state.update_data(workout_set=workout_set)
    await state.update_data(trainings_id=trainings_id)
    await state.update_data(save=[])
    await state.update_data(dnevnik=None)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Начать тренировку", callback_data="workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="fast_workout"))
    await call.message.answer(
        text="Ваша программа тренировки на сегодня\n<b>{}</b>\n\n\t* {}".format(
            call.data, workout_set),
        reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='Грудь_2')
@dp.callback_query_handler(text='Ноги_2')
@dp.callback_query_handler(text='Спина_2')
@dp.callback_query_handler(text='Бицепс_2')
@dp.callback_query_handler(text='Плечи_2')
@dp.callback_query_handler(text='Трицепс_2')
async def power(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    workout_sets = await state.get_data()
    group_set = workout_sets["group_set"] + " + " + call.data[:-2]
    user_id = call.from_user.id
    trainings_id = get_trainings_id('Разминка',user_id=user_id)
    trainings_id += get_trainings_id(str(workout_sets["group_set"]), count=3,user_id=user_id)
    trainings_id += get_trainings_id(call.data[:-2], count=3,user_id=user_id)
    trainings_id += get_trainings_id('Пресс',user_id=user_id)
    workout_set = "\n\t* ".join(get_trainings(trainings_id))
    await state.update_data(workout_set=workout_set)
    await state.update_data(trainings_id=trainings_id)
    await state.update_data(save=[])
    await state.update_data(dnevnik=None)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Начать тренировку", callback_data="workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="power"))
    await call.message.answer(
        text="Ваша программа тренировки на сегодня\n<b>{}</b>\n\n\t* {}".format(
            group_set, workout_set),
        reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='Кардио')
async def power(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    trainings_id = get_trainings_id('Кардио',user_id= user_id)
    trainings_id += get_trainings_id('Пресс',user_id= user_id)
    trainings = get_trainings(trainings_id)
    trainings[0] = trainings[0] + " - выполнять 30 минут"
    workout_set = "\n\t* ".join(trainings)
    await state.update_data(workout_set=workout_set)
    await state.update_data(trainings_id=trainings_id)
    await state.update_data(save=[])
    await state.update_data(dnevnik=None)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Начать тренировку", callback_data="workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="fast_workout"))
    await call.message.answer(
        text="Ваша программа тренировки на сегодня\n<b>{}</b>\n\n\t*{}".format(
            call.data, workout_set),
        reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='Функциональная')
async def power(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    trainings_id = get_trainings_id('Разминка',user_id= user_id)
    trainings_id += get_trainings_id('Функциональная', count=5,user_id= user_id)
    workout_set = "\n\t* ".join(get_trainings(trainings_id))
    await state.update_data(workout_set=workout_set)
    await state.update_data(trainings_id=trainings_id)
    await state.update_data(save=[])
    await state.update_data(dnevnik=None)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Начать тренировку", callback_data="workout"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="fast_workout"))
    await call.message.answer(
        text="Ваша программа тренировки на сегодня\n<b>{}</b>\n\n\t*{}".format(
            call.data, workout_set),
        reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='workout')
async def workout_set(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    workout_set = await state.get_data()
    save = workout_set["save"]
    if workout_set["dnevnik"] is None:
        await state.update_data(dnevnik=create_dnevnik(call.from_user.id))
    workout_set = await state.get_data()
    dnevnik = int(workout_set["dnevnik"])
    trainings_ids = workout_set["trainings_id"]
    workout_set = workout_set["workout_set"]
    keyboard = InlineKeyboardMarkup()
    if isinstance(workout_set, str):
        workout_set = workout_set.split("\n\t* ")
    workout = workout_set.pop(0)
    # TODO это баг если человек еще не сделал упражнение но она уже записалась в save
    if save:
        set_training_end_time(dnevnik, save[-1], datetime.datetime.now())
    trainings_id = trainings_ids.pop(0)
    add_training_to_dnevnik(dnevnik, trainings_id, datetime.datetime.now())
    save.append(trainings_id)
    await state.update_data(workout_set=workout_set)
    await state.update_data(trainings_id=trainings_ids)
    await state.update_data(save=save)
    if len(workout_set) > 0:
        keyboard.add(InlineKeyboardMarkup(
            text="Следующее упражнение(без отдыха)", callback_data="workout"))
        keyboard.add(InlineKeyboardMarkup(
            text="Следующее упражнение(5 мин. отдыха)", callback_data="timer"))
        keyboard.add(InlineKeyboardMarkup(
            text="Прервать тренировку", callback_data="fast_workout"))
        await call.message.answer(text=workout, reply_markup=keyboard)
    else:
        keyboard.add(InlineKeyboardMarkup(
            text="Закончить тренировку", callback_data="fast_workout"))
        await call.message.answer(text=workout, reply_markup=keyboard)


@dp.callback_query_handler(text='timer')
async def power(call: types.CallbackQuery):
    TIMER = 10
    await call.message.delete()
    new_message = await call.message.answer(text="Оставшееся время отдыха - 2:00")
    for sec in range(TIMER-1, 0, -1):
        sec = sec % (24 * 3600)
        sec %= 3600
        min = sec // 60
        sec %= 60
        string = "Оставшееся время отдыха - 0{}:{}".format(min, sec)
        if sec < 10:
            string = string = "Оставшееся время отдыха - 0{}:0{}".format(min, sec)
        await new_message.edit_text(text = string)
        await asyncio.sleep(1)
    await new_message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(text="Закончить отдыхать", callback_data="workout"))
    await call.message.answer(text="Время вышло!", reply_markup=keyboard)


@dp.callback_query_handler(text='characteristics')
async def characteristic(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Изменить параметры", callback_data="change"))
    keyboard.add(InlineKeyboardMarkup(
        text="Главное меню", callback_data="start"))
    user = get_user_info(call.from_user.id)
    await call.message.answer("Имя: {}\
            \nВозраст: {}\
            \nВес: {}\
            \nПол: {}\
            \nУровень подготовки: {}\
            \nЦель тренировок: {}\
            \nМесто занятий: {}".format(user['name'], user['age'], user['weight'], user['gender'], user['lvl'],
                                        user['training_goal'], get_place(user['place_id'])).replace('None',
                                                                                                    'Не указано'),
                              reply_markup=keyboard)


@dp.callback_query_handler(text='diary_workout')
async def diary_work(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(
        text="Главное меню", callback_data="start"))
    # Нужно получить здесь список тренировок за определёную дату
    # [[data, [workout_set]],]
    #
    dnevniks_id = get_user_dnevniks(call.from_user.id, 7)
    """
    1. Data: tr1, tr2, tr3
    """
    res = []
    for dnevnik in reversed(dnevniks_id):
        wrk = "{}\
            \nВы сделали: \n\t* {}".format(str(get_dnevnik_date(dnevnik))[:-16],
                                           "\n\t* ".join(get_trainings_name_in_dnevnik(dnevnik)))
        res.append(wrk)
    if res:

        await call.message.answer("\n\n".join(res),
                                  reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await call.message.answer("Вы еще не тренеровались!",
                                  reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(text='change')
async def change(call: types.CallbackQuery):
    await call.message.delete()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(text="Имя", callback_data="name"))
    keyboard.row(InlineKeyboardMarkup(text="Возраст", callback_data="age"),
                 InlineKeyboardMarkup(text="Рост", callback_data="height"))
    keyboard.row(InlineKeyboardMarkup(text="Вес", callback_data="weight"),
                 InlineKeyboardMarkup(text="Пол", callback_data="gender"))
    keyboard.row(InlineKeyboardMarkup(text="Уровень", callback_data="level"),
                 InlineKeyboardMarkup(text="Цель тренировки", callback_data="task"))
    keyboard.add(InlineKeyboardMarkup(
        text="Место тренировки", callback_data="place"))
    keyboard.add(InlineKeyboardMarkup(
        text="Вернуться назад", callback_data="characteristics"))
    user = get_user_info(call.from_user.id)
    await call.message.answer("Имя: {}\
            \nВозраст: {}\
            \nРост: {}\
            \nВес: {}\
            \nПол: {}\
            \nУровень подготовки: {}\
            \nЦель тренировок: {}\
            \nМесто занятий: {}".format(user['name'], user['age'],user['height'], user['weight'], user['gender'], user['lvl'],
                                        user['training_goal'], get_place(user['place_id'])), reply_markup=keyboard)


@dp.callback_query_handler(text="place")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(change_key=call)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(text="Дом", callback_data="Дом"),
                 InlineKeyboardMarkup(text="Тренажёрный зал", callback_data="Тренажерный Зал"))
    keyboard.add(
        InlineKeyboardMarkup(text="Спортивная площадка на улице", callback_data="Спортивная площадка на улице"))
    await call.message.answer("Выберите место тренировки", reply_markup=keyboard)


@dp.callback_query_handler(text="Дом")
@dp.callback_query_handler(text="Тренажерный Зал")
@dp.callback_query_handler(text="Спортивная площадка на улице")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    change_key = await state.get_data()
    change_key = change_key["change_key"]
    if call.data == 'Дом':
        g = 1
    elif call.data == 'Тренажерный Зал':
        g = 3
    else:
        g = 2
    set_user_place(call.from_user.id, g)
    await call.message.delete()
    await characteristic(change_key)


@dp.callback_query_handler(text="task")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(change_key=call)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardMarkup(text="Набрать силу", callback_data="Набрать силу"),
                 InlineKeyboardMarkup(text="Сбросить вес", callback_data="Сбросить вес"))
    keyboard.add(InlineKeyboardMarkup(text="Поддерживать форму",
                 callback_data="Поддерживать форму"))
    await call.message.answer("Выберите цель тренировки", reply_markup=keyboard)


@dp.callback_query_handler(text="Набрать силу")
@dp.callback_query_handler(text="Сбросить вес")
@dp.callback_query_handler(text="Поддерживать форму")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    change_key = await state.get_data()
    change_key = change_key["change_key"]
    set_user_training_task(call.from_user.id, call.data)
    await call.message.delete()
    await characteristic(change_key)


@dp.callback_query_handler(text="gender")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(change_key=call)
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardMarkup(text="Мужской", callback_data="Мужской"),
                 InlineKeyboardMarkup(text="Женский", callback_data="Женский"))
    await call.message.answer("Выберите пол", reply_markup=keyboard)


@dp.callback_query_handler(text="Мужской")
@dp.callback_query_handler(text="Женский")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    change_key = await state.get_data()
    change_key = change_key["change_key"]
    set_user_gender(call.from_user.id, call.data)
    await call.message.delete()
    await characteristic(change_key)


@dp.callback_query_handler(text="name")
@dp.callback_query_handler(text="age")
@dp.callback_query_handler(text="weight")
@dp.callback_query_handler(text="level")
@dp.callback_query_handler(text="height")
async def change_key(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(change_key=call)
    await Form.value.set()
    await call.message.answer("Введите значение")


@dp.message_handler(state=Form.value)
async def change_value(message: types.Message, state: FSMContext):
    change_key = await state.get_data()
    change_key = change_key["change_key"]
    await state.finish()
    if change_key.data == "name":
        if len(message.text) > 32:
            await message.answer("Имя не может быть больше 32 символов! \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
    elif change_key.data == "age":
        if not message.text.lstrip("+-").isdigit():
            await message.answer("Я не знаю такой метод счисления, это арабский? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
        elif int(message.text) < 0:
            await message.answer("Вы ещё не родились? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
        elif int(message.text) > 100:
            await message.answer("В таком возрасте принято уходить на покой. \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
    elif change_key.data == "height":
        if not message.text.lstrip("+-").isdigit():
            await message.answer("Я не знаю такой метод счисления, это арабский? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
        elif int(message.text) < 0:
            await message.answer("Как это понимать? Вы вростаете в землю? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
        elif int(message.text) > 272:
            await message.answer("Вы побили рекорд Гиннесса! Или нет? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
    elif change_key.data == "weight":
        if not message.text.lstrip("+-").isdigit():
            await message.answer("Я не знаю такой метод счисления, это арабский? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
        elif int(message.text) < 0:
            await message.answer("Вы чёрная дыра? \nВведите корректную информацию!")
            message_id = message.message_id + 1
            await asyncio.sleep(2)
            await bot.delete_message(message.chat.id, message_id)
            await characteristic(change_key)
            raise asyncio.CancelledError
        elif int(message.text) > 150:
            if int(message.text) > 610:
                await message.answer("Вы побили рекорд Гиннесса! Или нет? \nВведите корректную информацию!")
                message_id = message.message_id + 1
                await asyncio.sleep(2)
                await bot.delete_message(message.chat.id, message_id)
                await characteristic(change_key)
                raise asyncio.CancelledError
            else:
                await message.answer("Мы рекомендуем вам сбросить вес! \nЦель измененна на 'Сбросить вес'")
                set_user_training_task(message.from_user.id, 'Сбросить вес')
                message_id = message.message_id + 1
                await asyncio.sleep(2)
                await bot.delete_message(message.chat.id, message_id)
                raise asyncio.CancelledError
    if change_key.data == 'age':
        set_user_age(message.from_user.id, int(message.text))
    elif change_key.data == 'name':
        set_user_name(message.from_user.id, message.text)
    elif change_key.data == 'weight':
        set_user_weight(message.from_user.id, int(message.text))
    elif change_key.data == 'level':
        set_user_lvl(message.from_user.id, int(message.text))
    elif change_key.data == 'height':
        set_user_height(message.from_user.id, int(message.text))
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await characteristic(change_key)


@dp.message_handler()
@dp.message_handler(content_types=ContentType.ANY)
async def echo(message: types.Message):
    await message.reply("Давайте сделаем вид что этого никогда не было...")
    await asyncio.sleep(1)
    await bot.delete_message(message.chat.id, message.message_id + 1)
    await bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
