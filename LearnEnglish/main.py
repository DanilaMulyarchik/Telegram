from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import config
from managers.data_manager import *
from managers.time_manager import *
from generator.word_list_generator import get_word_list, update_word_list, get_test_word_list
from os_processing.exist_file import *
from users.new_user import create_new_user
from get_data.get_data import *


class Bot():

    def __init__(self):
        self.minute_difference = 0
        self.difficulty = {'first': 1, 'second': 2}
        self.days = config.day

    def __create_reply_markup(self, *args):
        reply_markup_list = []
        reply_markup_dict = {'learn': "[InlineKeyboardButton('Learn', callback_data='learn')]",
                             'check': "[InlineKeyboardButton('Check', callback_data='check')]",
                             'mark': "[InlineKeyboardButton('Mark', callback_data='mark')]",
                             'setting': "[InlineKeyboardButton('Setting', callback_data='setting')]",
                             'main_test': "[InlineKeyboardButton('Main Test', callback_data='main_test')]",
                             'quantity': "[InlineKeyboardButton('Quantity', callback_data='quantity')]",
                             'difficulty': "[InlineKeyboardButton('Difficulty', callback_data='difficulty')]",
                             'back': "[InlineKeyboardButton('Back', callback_data='back')]",
                             'first': "[InlineKeyboardButton('First', callback_data='first')]",
                             'second': "[InlineKeyboardButton('Second', callback_data='second')]"}
        for key, value in reply_markup_dict.items():
            if key in args:
                reply_markup_list.append(eval(value))
        return InlineKeyboardMarkup(reply_markup_list)

    async def start(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        new_user = {'telegram': update.effective_user.username,
                    'test_date': get_tomorrow_date(get_date(),self.days), 'index': -1, 'action': '', 'day_mark': 0, 'difficulty': 1, 'quantity': 5}
        marks = {}
        test_marks = {}
        if not check_dir_exist('users', update.effective_user.username):
            create_new_user(update.effective_user.username, user=new_user, marks=marks, test_marks=test_marks)
        await update.message.reply_text('Select function: ',
                                        reply_markup=self.__create_reply_markup('learn', 'check', 'mark', 'setting'))

    async def __button_handler(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        action = query.data

        if action == 'learn':
            await query.edit_message_text(text=self.__learn(update.effective_user.username),
                                          reply_markup=self.__create_reply_markup('check', 'mark', 'setting'))
        elif action == 'check':
            if not check_file_exist(f'users/{update.effective_user.username}/words/{get_difficulty(update.effective_user.username)}-level', get_date()):
                await query.edit_message_text(text="You haven't learned the words",
                                              reply_markup=self.__create_reply_markup('learn', 'setting'))
            else:
                update_data(update.effective_user.username,
                            **{'user': {'index': 0, 'action': action, 'day_mark': 0}})
                content.user_data['words'] = get_word_list(update.effective_user.username)
                await query.edit_message_text(text="Translate word: " + content.user_data['words'][0]['english'])
        elif action == 'mark':
            await query.edit_message_text(text=self.__mark(update.effective_user.username),
                                          reply_markup=self.__create_reply_markup('learn', 'check', 'setting'))
        elif action == 'setting':
            await query.edit_message_text(text=f'Difficulty = {get_difficulty(update.effective_user.username)}'
                                               f'\nQuantity = {get_quantity(update.effective_user.username)}',
                                          reply_markup=self.__create_reply_markup('difficulty', 'quantity', 'back'))
        elif action == 'quantity':
            update_data(update.effective_user.username, **{'user': {'action': action}})
            await query.edit_message_text(text='Write the number of words.')
        elif action == 'difficulty':
            update_data(update.effective_user.username, **{'user': {'action': action}})
            await query.edit_message_text(text='Select difficulty level',
                                          reply_markup=self.__create_reply_markup('first', 'second'))
        elif action == 'first' or action == 'second':
            update_data(update.effective_user.username, **{'user': {'difficulty': self.difficulty[action]}})
            await query.edit_message_text('Select function: ',
                                          reply_markup=self.__create_reply_markup('quantity', 'difficulty', 'back'))
        elif action == 'back':
            await query.edit_message_text('Select function: ',
                                          reply_markup=self.__create_reply_markup('learn', 'check', 'mark', 'setting'))

    async def __message_handler(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        try:
            if get_action(update.effective_user.username) == 'check':
                if str(update.message.text.strip()).lower() == content.user_data['words'][get_index(update.effective_user.username)]['russian'].lower():
                    update_data(update.effective_user.username, **{'user': {'index': get_index(update.effective_user.username) + 1, 'day_mark': get_day_mark(update.effective_user.username) + 1}})
                    await update.message.reply_text(text='True')
                else:
                    update_data(update.effective_user.username, **{'user': {'index': get_index(update.effective_user.username) + 1}})
                    await update.message.reply_text(text=f'False. {content.user_data["words"][get_index(update.effective_user.username) - 1]["english"]}'
                                                         f' <--> {content.user_data["words"][get_index(update.effective_user.username) - 1]["russian"]}')
                if get_index(update.effective_user.username) < len(content.user_data['words']):
                    await update.message.reply_text(text='Next word: ' + content.user_data['words'][get_index(update.effective_user.username)]['english'])
                else:
                    update_data(update.effective_user.username, **{'user': {'action': ''}, get_tag_or_value(update.effective_user.username): {get_date(): get_day_mark(update.effective_user.username)}})
                    await update.message.reply_text(text=f'You have completed the word list. Your mark is '
                    f'{get_day_mark(update.effective_user.username)}',
                                                    reply_markup=self.__create_reply_markup('check', 'mark'))
            elif get_action(update.effective_user.username) == 'quantity':
                update_data(update.effective_user.username, **{'user': {'quantity': update.message.text.strip(), 'action': '', get_date(): 0}})
                if check_file_exist(f'users/{update.effective_user.username}/words/{get_difficulty(update.effective_user.username)}-level', get_date()):
                    update_word_list(update.effective_user.username)
                await update.message.reply_text(text=f'Difficulty = {get_difficulty(update.effective_user.username)}\nQuantity = {get_quantity(update.effective_user.username)}',
                                              reply_markup=self.__create_reply_markup('difficulty', 'quantity', 'back'))
        except:
            await update.message.reply_text(text='Select function',
                                            reply_markup=self.__create_reply_markup('learn', 'check', 'mark', 'setting'))

    def __learn(self, telegram: str):
        if not compair_date(get_date(), get_test_date(telegram)):
            if len(get_all_mark(telegram)) / self.days == len(get_all_test_mark(telegram)):
                update_data(telegram, **{'user': {'test_date': get_tomorrow_date(get_date(), self.days)}})
            elif len(get_all_mark(telegram)) // self.days == len(get_all_test_mark(telegram)) + 1:
                update_data(telegram, **{'user': {'test_date': get_date()}})
            else:
                update_data(telegram, **{'user': {'test_date': get_tomorrow_date(
                    get_date(), self.days - 1 - (len(get_all_mark(telegram)) - len(get_all_test_mark(telegram)) * self.days))}})
        if get_date() != get_test_date(telegram):
            word_list = get_word_list(telegram)
            if len(word_list) != get_quantity(telegram):
                update_word_list(telegram)
            text = "Today's set of words\n\n"
            for index in range(len(word_list)):
                text += str(word_list[index]['english'] + ' <--> ' + word_list[index]['russian']) + '\n'
        else:
            get_test_word_list(telegram)
            text = "Today is a test, it consists of words that you have taken over the last 3 days"
        return text

    def __mark(self, telegram: str):
        try:
            mark = int(read_data(f'users/{telegram}', telegram)[get_tag_or_value(telegram)][get_date()])
            return f'Your mark for today is {mark}.'
        except:
            return f"You haven't checked"

    def run(self):
        application = ApplicationBuilder().token(config.token).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CallbackQueryHandler(self.__button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__message_handler))
        application.run_polling()


Bot().run()

