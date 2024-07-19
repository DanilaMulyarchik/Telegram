from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import config
from managers.data_manager import *
from managers.time_manager import *
from generator.word_list_generator import get_word_list
from file_processing.exist_file import check_file_exist


class Bot():

    def __init__(self):
        self.difficulty = 1
        self.coll = 5
        self.minute_difference = 10

    def __create_reply_markup(self, *args):
        reply_markup_list = []
        reply_markup_dict = {'learn': "[InlineKeyboardButton('Learn', callback_data='learn')]",
                             'check': "[InlineKeyboardButton('Check', callback_data='check')]",
                             'mark': "[InlineKeyboardButton('Mark', callback_data='mark')]",}
        for key, value in reply_markup_dict.items():
            if key not in args:
                reply_markup_list.append(eval(value))
        return InlineKeyboardMarkup(reply_markup_list)

    async def start(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        new_user = {'telegram': update.effective_user.username, 'mark': -1, 'time': '', 'index': -1}
        if check_file_exist('users', update.effective_user.username) is None:
            save_data('users', update.effective_user.username, telegram=update.effective_user.username, uswr=new_user)
        await update.message.reply_text('Select function: ', reply_markup=self.__create_reply_markup(''))

    async def __button_handler(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        action = query.data

        if action == 'learn':
            update_data(update.effective_user.username, time=get_time())
            await query.edit_message_text(text=self.__learn(),
                                          reply_markup=self.__create_reply_markup(action))
        elif action == 'check':
            start_time = read_data('users', update.effective_user.username)['user']['time']
            if start_time == '':
                await query.edit_message_text(text="You haven't learned the words",
                                              reply_markup=self.__create_reply_markup(action, 'mark', 'time'))
            elif get_time_difference(start_time, 0, self.minute_difference, 0):
                update_data(update.effective_user.username, index=0, mark=0)
                content.user_data['words'] = get_word_list(self.coll, self.difficulty)
                await query.edit_message_text(text="Translate word: " + content.user_data['words'][0]['english'])
            else:
                await query.edit_message_text(text=f"Time to study has not passed yet, "
                                                   f"{get_time_out(start_time, self.minute_difference)} minutes left",
                                              reply_markup=self.__create_reply_markup(action, 'time', 'mark'))
        elif action == 'mark':
            await query.edit_message_text(text=self.__mark(update.effective_user.username),
                                          reply_markup=self.__create_reply_markup(action))

    async def __message_handler(self, update: Update, content: ContextTypes.DEFAULT_TYPE):
        try:
            user_answer = update.message.text.strip()
            index, mark = read_data('users', update.effective_user.username)['user']['index'], read_data('users', update.effective_user.username)['user']['mark']
            if user_answer.lower() == content.user_data['words'][index]['russian'].lower():
                update_data(update.effective_user.username, mark=mark+1, index=index+1)
                await update.message.reply_text(text='True')
            else:
                update_data(update.effective_user.username, index=index+1)
                await update.message.reply_text(text=f'False. {content.user_data["words"][index]["english"]}'
                                                     f' <--> {content.user_data["words"][index]["russian"]}')
            if index + 1 < len(content.user_data['words']):
                await update.message.reply_text(text='Next word: ' + content.user_data['words'][index+1]['english'])
            else:
                await update.message.reply_text(text=f'You have completed the word list. Your mark is {read_data("users", update.effective_user.username)["user"]["mark"]}',
                                                reply_markup=self.__create_reply_markup('check', 'mark', 'time'))
        except:
            await update.message.reply_text(text='Select function', reply_markup=self.__create_reply_markup(''))

    def __learn(self):
        word_list = get_word_list(self.coll, self.difficulty)
        text = "Today's set of words\n\n"
        for index in range(len(word_list)):
            text += str(word_list[index]['english'] + ' <--> ' + word_list[index]['russian']) + '\n'
        return text

    def __mark(self, telegram: str):
        mark = int(read_data('users', telegram)['user']['mark'])
        word_list = get_word_list(self.coll, self.difficulty)
        if mark == -1:
            return f"You haven't checked"
        else:
            return f'Your mark for today is {mark}. All {len(word_list)} words'

    def run(self):
        application = ApplicationBuilder().token(config.token).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CallbackQueryHandler(self.__button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__message_handler))
        application.run_polling()


Bot().run()