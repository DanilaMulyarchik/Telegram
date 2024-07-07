from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from generator import get_random_word_list
from data_manager import settings_save


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Учить", callback_data='Учить'),
         InlineKeyboardButton("Проверить", callback_data='Проверить')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'Учить':

        word_list = get_random_word_list()

        message_text = "Список слов для изучения:\n"
        for i in range(len(word_list)):
            message_text += f"\n {word_list[i][0]} --- {word_list[i][1]}"

        await query.edit_message_text(text=message_text)
    elif query.data == 'Проверить':

        context.user_data['words'] = get_random_word_list()
        context.user_data['index'] = 0
        word_list = context.user_data.get('words')
        current_index = context.user_data.get('index')
        if current_index < len(word_list):
            current_word = word_list[current_index][0]
            await query.edit_message_text(text=f"Переведите слово:\n{current_word}")
            context.user_data['waiting_for_answer'] = True
        else:
            await query.edit_message_text(text="Вы закончили список слов!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data['waiting_for_answer'] == True:
        context.user_data['waiting_for_answer'] = False
        user_answer = update.message.text.strip()
        current_index = context.user_data.get('index')
        word_list = context.user_data.get('words')

        if current_index < len(word_list):
            correct_translation = word_list[current_index][1]
            if user_answer.lower() == correct_translation.lower():
                await update.message.reply_text("Правильно!")
            else:
                await update.message.reply_text(f"Неправильно. Правильный ответ: {correct_translation}")

            current_index += 1
            context.user_data['index'] = current_index

            if current_index < len(word_list):
                next_word = word_list[current_index][0]
                await update.message.reply_text(f"Следующее слово: {next_word}")
                context.user_data['waiting_for_answer'] = True
            else:
                await update.message.reply_text("Вы закончили список слов!")
        else:
            await update.message.reply_text("Неожиданная ошибка при проверке.")

    else:
        await update.message.reply_text(update.message.text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Используйте /start для начала или отправьте любое сообщение.')


def main() -> None:
    token = 'token'

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()


if __name__ == '__main__':
    main()
