from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import config
from managers.data_manager import *
from managers.time_manager import *
from generator.word_list_generator import get_word_list
from file_processing.exist_file import check_file_exist
from users.new_user import create_new_user


class Bot():

    def __init__(self):
        self.difficulty = 1
        self.coll = 5
        self.minute_difference = 10

    def __create_reply_markup(self, *args):
        reply_markup_list = []
        reply_markup_dict = {'learn': "[InlineKeyboardButton('Learn', callback_data='learn')]",
                             'check': "[InlineKeyboardButton('Check', callback_data='check')]",
                             'mark': "[InlineKeyboardButton('Mark', callback_data='mark')]",
                             'setting': "[InlineKeyboardButton('Setting', callback_data='setting')]"}
        for key, value in reply_markup_dict.items():
            if key in args:
                reply_markup_list.append(eval(value))
        return InlineKeyboardMarkup(reply_markup_list)

    async def start(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        new_user = {'telegram': update.effective_user.username, 'time': '', 'index': -1}
        marks = {get_date(): 0}
        if check_file_exist('users', update.effective_user.username) is None:
            create_new_user('users', update.effective_user.username, user=new_user, marks=marks)
        await update.message.reply_text('Select function: ', reply_markup=self.__create_reply_markup('learn', 'check'
                                                                                                     ,'mark','setting'))

    async def __button_handler(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        action = query.data

        if action == 'learn':
            start_time = read_data('users', update.effective_user.username)['user']['time']
            if start_time == '':
                update_data(update.effective_user.username, time=get_time())
            await query.edit_message_text(text=self.__learn(),
                                          reply_markup=self.__create_reply_markup('check', 'mark', 'setting'))
        elif action == 'check':
            start_time = read_data('users', update.effective_user.username)['user']['time']
            if start_time == '':
                await query.edit_message_text(text="You haven't learned the words",
                                              reply_markup=self.__create_reply_markup('learn', 'setting'))
            elif get_time_difference(start_time, 0, self.minute_difference, 0):
                update_data(update.effective_user.username, **{get_date(): 0, 'index': 0, 'time': get_time()})
                content.user_data['words'] = get_word_list(self.coll, self.difficulty)
                await query.edit_message_text(text="Translate word: " + content.user_data['words'][0]['english'])
            else:
                await query.edit_message_text(text=f"Time to study has not passed yet, "
                                                   f"{get_time_out(start_time, self.minute_difference)} minutes left",
                                              reply_markup=self.__create_reply_markup('learn', 'setting'))
        elif action == 'mark':
            await query.edit_message_text(text=self.__mark(update.effective_user.username),
                                          reply_markup=self.__create_reply_markup('learn', 'check', 'setting'))
        elif action == 'setting':
            await query.edit_message_text(text='Coming soon', reply_markup=self.__create_reply_markup('learn',
                                                                                                      'check', 'mark'))

    async def __message_handler(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        try:
            user_answer = update.message.text.strip()
            index, mark = read_data('users', update.effective_user.username)['user']['index'], read_data('users', update.effective_user.username)['marks'][get_date()]
            if user_answer.lower() == content.user_data['words'][index]['russian'].lower():
                update_data(update.effective_user.username, **{get_date(): mark+1, 'index': index + 1})
                await update.message.reply_text(text='True')
            else:
                update_data(update.effective_user.username, index=index+1)
                await update.message.reply_text(text=f'False. {content.user_data["words"][index]["english"]}'
                                                     f' <--> {content.user_data["words"][index]["russian"]}')
            if index + 1 < len(content.user_data['words']):
                await update.message.reply_text(text='Next word: ' + content.user_data['words'][index+1]['english'])
            else:
                await update.message.reply_text(text=f'You have completed the word list. Your mark is {read_data("users", update.effective_user.username)["marks"][get_date()]}',
                                                reply_markup=self.__create_reply_markup('check', 'mark'))
        except:
            await update.message.reply_text(text='Select function', reply_markup=self.__create_reply_markup('learn', 'check',
                                                                                                            'mark', 'setting'))

    def __learn(self):
        word_list = get_word_list(self.coll, self.difficulty)
        text = "Today's set of words\n\n"
        for index in range(len(word_list)):
            text += str(word_list[index]['english'] + ' <--> ' + word_list[index]['russian']) + '\n'
        return text

    def __mark(self, telegram: str):
        try:
            mark = int(read_data('users', telegram)['marks'][get_date()])
            word_list = get_word_list(self.coll, self.difficulty)
            return f'Your mark for today is {mark}. All {len(word_list)} words'
        except:
            return f"You haven't checked"

    def run(self):
        application = ApplicationBuilder().token(config.token).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CallbackQueryHandler(self.__button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__message_handler))
        application.run_polling()


Bot().run()