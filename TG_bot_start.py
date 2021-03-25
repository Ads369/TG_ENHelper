"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import TG_ENHelper_main as enh

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
braille_keyboard = {}

@dp.message_handler(commands=['alph', 'алф'])
async def convert_alphabet(message: types.Message):
    txt_message = message.text[message.text.index(' '):]
    result = enh.hendler_alphabet_convert(txt_message)

    result_str = ''
    if result['en_num']:
        result_str += 'EN->NUM: {}\n'.format(result['en_num'])
    elif result['ru_num']:
        result_str += 'RU->NUM: {}\n'.format(result['ru_num'])
    elif result['digit_string']:
        result_str += 'NUM->RU: {}\nNUM->EN: {}\n'.format(result['digit_string']['RU'],
                                                          result['digit_string']['EN'])

    await message.reply(result_str)


@dp.message_handler(commands=['mend', 'менд', 'pt', 'mt', 'tm'])
async def convert_period_table(message: types.Message):
    txt_message = message.text[message.text.index(' '):]
    result = enh.periodic_table_convert(txt_message)

    str_symbol = ''
    str_number = ''
    for item in result:
        str_symbol += item['symbol'] + ' '
        str_number += str(item['number']) + ' '

    await message.reply(str_symbol + '\n' + str_number)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',h
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(commands='key')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness

    btn_1 = (' ', 'btn_1')
    btn_2 = (' ', 'btn_2')
    btn_3 = (' ', 'btn_3')
    btn_4 = (' ', 'btn_4')
    btn_5 = (' ', 'btn_5')
    btn_6 = (' ', 'btn_6')

    rows = [
        (btn_1, btn_4),
        (btn_2, btn_5),
        (btn_3, btn_6),
    ]

    for row in rows:
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in row)
        keyboard_markup.row(*row_btns)

    keyboard_markup.add(
        # url buttons have no callback data
        types.InlineKeyboardButton('aiogram source', url='https://github.com/aiogram/aiogram'),
    )
    await message.reply("Шифр Браиля", reply_markup=keyboard_markup)


# Use multiple registrators. Handler will execute when one of the filters is OK
@dp.callback_query_handler(text='btn_1')  # if cb.data == 'no'
@dp.callback_query_handler(text='btn_2')  # if cb.data == 'yes'
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    # always answer callback queries, even if you have nothing to say
    await query.answer(f'You answered with {answer_data!r}')

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    btn_1 = ('_', 'btn_1')
    btn_2 = ('_', 'btn_2')

    if answer_data == 'btn_1':
        btn_1 = ('*', 'btn_1')
    elif answer_data == 'btn_2':
        btn_2 = ('*', 'btn_2')

    text_and_data = (
        btn_1, btn_2,
    )

    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    keyboard_markup.add(
        # url buttons have no callback data
        types.InlineKeyboardButton('aiogram source', url='https://github.com/aiogram/aiogram'),
    )

    await bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id, reply_markup=keyboard_markup)

# @dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)