from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from generator import get_random_word_list
from Db import DataBase
from date import get_date
import constant
from datetime import datetime, time, timedelta
from time_manager import get_time_difference, get_time, get_time_out


class EnglishLeane():

    def __init__(self):
        self.keyboard = [
            [InlineKeyboardButton("Учить", callback_data='Учить'),
             InlineKeyboardButton("Проверить", callback_data='Проверить'),
             InlineKeyboardButton("Отметка", callback_data='Отметка'),
             InlineKeyboardButton("Время", callback_data='Время')]
        ]
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Выберите опцию:', reply_markup=self.reply_markup)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        word_list = get_random_word_list()

        if query.data == 'Учить':
            start = str(DataBase().Get('users', {'telegram': update.effective_user.username}, 'time')[0][0])
            if get_time_difference(start, 12, 0, 0) or start == '00:00:00':
                DataBase().Add('users', {'telegram': update.effective_user.username, 'word_index': 0, 'time': get_time()})
            message_text = "Список слов для изучения:\n"
            for i in range(len(word_list)):
                message_text += f"\n {word_list[i]['english']} --- {word_list[i]['russian']}"
            try:
                await query.edit_message_text(text=message_text, reply_markup=self.reply_markup)
            except:
                pass

        elif query.data == 'Проверить':
            start = str(DataBase().Get('users', {'telegram': update.effective_user.username}, 'time')[0][0])
            if get_time_difference(start, 0, 30, 0):
                DataBase().Add('users', {'telegram': update.effective_user.username, 'word_index': 0})
                DataBase().Add('marks', {'telegram': update.effective_user.username, 'data': get_date(), 'mark': 0})
                current_word = word_list[0]['english']
                context.user_data['words'] = word_list
                await query.edit_message_text(text=f"Переведите слово:\n{current_word}")
            else:
                try:
                    await query.edit_message_text(text=f"Вы сможете приступить к тесту через " + get_time_out(start), reply_markup=self.reply_markup)
                except:
                    pass
        elif query.data == 'Время':
            start = str(DataBase().Get('users', {'telegram': update.effective_user.username}, 'time')[0][0])
            if start == '00:00:00':
                try:
                    await query.edit_message_text(text='Вы не получили список слов!', reply_markup=self.reply_markup)
                except:
                    pass
            else:
                try:
                    await query.edit_message_text(text=f"Вы сможете приступить к тесту через " + get_time_out(start), reply_markup=self.reply_markup)
                except:
                    pass
        elif query.data == 'Отметка':
            user_id = update.effective_user.username if update.effective_user else None
            if user_id and DataBase().Find('marks', {'telegram': user_id}):
                try:
                    await query.edit_message_text(text=f'Сегодняшняя отметка == {DataBase().Get("marks", {"telegram": update.effective_user.username, "data": get_date()},"mark")[0][0]}', reply_markup=self.reply_markup)
                except Exception as e:
                    try:
                        await query.edit_message_text(text='Сегодняшняя отметка == 0', reply_markup=self.reply_markup)
                    except:
                        pass

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            user_answer = update.message.text.strip()
            index = DataBase().Get('users', {'telegram': update.effective_user.username}, 'word_index')[0][0]
            mark = DataBase().Get('marks', {'telegram': update.effective_user.username, 'data': get_date()}, 'mark')[0][0]
            if index <= len(context.user_data['words']):
                correct_translation = context.user_data['words'][index]['russian']
                if user_answer.lower() == correct_translation.lower():
                    mark += 1
                    DataBase().Add('marks', {'telegram': update.effective_user.username,'data': get_date(), 'mark': mark})
                    await update.message.reply_text("Правильно!")
                else:
                    await update.message.reply_text(f"Неправильно. Правильный ответ: {correct_translation}")

                index += 1
                DataBase().Add('users', {'telegram': update.effective_user.username, 'word_index': index})

                if index < len(context.user_data['words']):
                    next_word = context.user_data['words'][index]['english']
                    await update.message.reply_text(f"Следующее слово: {next_word}")
                else:
                    DataBase().Add('marks', {'telegram': update.effective_user.username, 'data': get_date(), 'mark': mark})
                    await update.message.reply_text(f"Вы закончили список слов! Вы ответили на {mark} из 5!", reply_markup=self.reply_markup)
            else:
                await update.message.reply_text("Неожиданная ошибка при проверке.", reply_markup=self.reply_markup)
        except:
            await update.message.reply_text(text='Выберите опцию', reply_markup=self.reply_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Используйте /start для начала или отправьте любое сообщение.')

    def build(self) -> None:
        token = constant.token

        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CallbackQueryHandler(self.button))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        app.run_polling()


if __name__ == '__main__':
    EnglishLeane().build()
