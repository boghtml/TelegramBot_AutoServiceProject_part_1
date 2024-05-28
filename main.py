import calendar  # pip install calendar
import datetime

import bson
import pyperclip
from bson import ObjectId
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, CommandHandler, filters

from DataBase.DataBase import get_services_base, save_appointment_to_db, get_order_info_by_id

NAME, SURNAME, PHONE_OPTION, PHONE_MANUAL, BRAND, MODEL, YEAR, COMMENT, DATE, SUBMIT = range(10)
CHECK_ORDER = range(1)

class AutoServiceBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()

        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))

        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('aboutus', self.about))
        self.application.add_handler(CommandHandler('mycontact', self.contact))
        self.application.add_handler(CommandHandler('ourservices', self.services))

        self.application.add_handler(CallbackQueryHandler(self.handle_button_click))

        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))

        self.get_month_days(2024, 3)


        try:
            self.setup_conv_handler2()
            self.setup_conv_handler()
        except Exception as e:
            print(e)

    def setup_conv_handler2(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('checkMyOrder', self.start_check_order)],
            states={
                CHECK_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.check_order)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel),
                       CommandHandler('endOfconversation', self.endOfconversation)]
        )

        self.application.add_handler(conv_handler)

    async def start_check_order(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Будь ласка, введіть ID вашого замовлення:")
        return CHECK_ORDER

    async def check_order(self, update: Update, context: CallbackContext) -> int:
        order_id = update.message.text

        if not bson.ObjectId.is_valid(order_id):
            await update.message.reply_text(f"Некоректний ID замовлення: {order_id}.")
            return ConversationHandler.END

        order_info = get_order_info_by_id(order_id)

        if order_info:
            print(order_info)
            message = f"Інформація про замовлення №{order_id}:\n\n"
            message += f"Ім'я: {order_info['name']}\n"
            message += f"Прізвище: {order_info['surname']}\n"
            message += f"Номер телефону: {order_info['phone']}\n"
            message += f"Марка: {order_info['brand']}\n"
            message += f"Модель: {order_info['model']}\n"
            message += f"Рік випуску: {order_info['year']}\n"

            if not order_info['comment']:
                message += "Коментар: Ви не вказали\n"
            else:
                message += f"Коментар: {order_info['comment']}\n"

            message += f"Дата запису: {order_info['date']}\n"
            message += f"\nСтатус: {order_info['status']}"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("Замовлення з таким ID не знайдено.")
        return ConversationHandler.END

    async def cancel(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Запис скасовано.")
        return ConversationHandler.END

    async def endOfconversation(self, update: Update, context: CallbackContext) -> int:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Запис завершено.")
        return ConversationHandler.END
    async def ask_name(self, update: Update, context: CallbackContext) -> int:
        keyboard = []  # Створюємо порожній список для кнопок
        if context.user_data:  # Перевіряємо, чи був розпочатий процес запису
            keyboard = [[KeyboardButton("Відмінити запис")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text("Почнемо запис, Якщо ви захочете припити запис, то введіть команду /cancel.\n")
        await update.message.reply_text("Введіть ваше ім'я:", reply_markup=reply_markup)
        return NAME

    async def ask_surname(self, update: Update, context: CallbackContext) -> int:
        context.user_data['name'] = update.message.text  # Збереження імені перед запитом прізвища
        await update.message.reply_text("Введіть ваше прізвище:")
        return SURNAME

    async def ask_phone_option(self, update, context):
        context.user_data['surname'] = update.message.text
        keyboard = [
            [KeyboardButton("Ввести власноруч")],
            [KeyboardButton("Підключити автоматично", request_contact=True)]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text("Будь ласка, оберіть як ви хочете задати номер телефону:",
                                        reply_markup=reply_markup)
        return PHONE_OPTION

    async def phone_option_handler(self, update, context):
        if update.message.contact is not None:
            # Користувач надав номер через контакт
            context.user_data['phone'] = update.message.contact.phone_number
            await update.message.reply_text(f"Ми отримали ваш номер: {context.user_data['phone']}",
                                            reply_markup=ReplyKeyboardRemove())
            # Переходимо до наступного кроку
            return await self.ask_brand(update, context)
        else:
            # Ця частина буде виконана, якщо користувач вибере "Ввести власноруч"
            await update.message.reply_text("Будь ласка, введіть ваш номер телефону вручну(наприклад +380962813659):",
                                            reply_markup=ReplyKeyboardRemove())
            return PHONE_MANUAL

    async def ask_brand(self, update: Update, context: CallbackContext) -> int:
        if 'phone' not in context.user_data:
            # Якщо номер телефону не було встановлено автоматично, читаємо його з тексту повідомлення
            context.user_data['phone'] = update.message.text
        await update.message.reply_text("Введіть марку вашого авто:")
        return BRAND

    async def ask_model(self, update: Update, context: CallbackContext) -> int:
        context.user_data['brand'] = update.message.text
        await update.message.reply_text("Введіть модель вашого авто:")
        return MODEL

    async def ask_year(self, update: Update, context: CallbackContext) -> int:
        context.user_data['model'] = update.message.text
        await update.message.reply_text("Введіть рік випуску вашого авто (РРРР):")
        return YEAR

    async def validate_year(self, update: Update, context: CallbackContext) -> int:
        user_input = update.message.text

        try:
            year = int(user_input)
            if year < 1900 or year > datetime.datetime.now().year:
                await update.message.reply_text(
                    "Некоректний рік випуску. Будь ласка, введіть дійсний рік випуску:")
                return YEAR
        except ValueError:
            await update.message.reply_text("Некоректний рік випуску. Будь ласка, введіть число:")
            return YEAR

        context.user_data['year'] = year
        return await self.ask_comment(update, context)
    async def handle_callback_query(self, update: Update, context: CallbackContext) -> None:
        print("Потрапило в handle_callback_query")

        query = update.callback_query
        data = query.data.split('_')
        action = data[0]

        if action == 'setOrderDate':
            await self.handle_month_change(update, context)

        # Обробка вибору дня
        elif action == 'selectOrderDay':
            await self.handle_date_selection(update, context)

        else:
            await query.answer("Ця дія не підтримується.", show_alert=True)

        # Завжди викликайте query.answer() для відповіді на запит
        await query.answer()

    async def handle_month_change(self, update: Update, context: CallbackContext) -> None:
        print("Потрапило в handle_month_change")

        query = update.callback_query
        data = query.data.split('_')
        order_id, day, month, year = data[1], int(data[2]), int(data[3]), int(data[4])

        if month < 1:
            month = 12
            year -= 1
        elif month > 12:
            month = 1
            year += 1

        keyboard = self.deliveryDateButtons(order_id, year, month, day)
        await query.edit_message_reply_markup(reply_markup=keyboard)
        await query.answer()

    async def ask_date(self, update: Update, context: CallbackContext) -> int:
        now = datetime.datetime.now()
        keyboard = self.deliveryDateButtons(update.effective_chat.id, now.year, now.month, now.day)
        await update.message.reply_text("Виберіть дату запису:", reply_markup=keyboard)
        return DATE

    def deliveryDateButtons(self, orderID, year, month, dayy):
        daysArray, monthh, yearr = self.getDateAttributes(year, month)

        btns = []  # Основний список для всіх кнопок
        week_btns = []  # Тимчасовий список для кнопок поточного тижня

        for i, day in enumerate(daysArray, start=1):
            if day == '*' or day == '.':
                week_btns.append(InlineKeyboardButton(text=day, callback_data='ignore'))
            else:
                week_btns.append(
                    InlineKeyboardButton(text=str(day), callback_data=f'selectOrderDay_{orderID}_{day}_{month}_{yearr}')
                )
            # Перевірка чи завершено тиждень або чи це останній день місяця
            if i % 7 == 0 or i == len(daysArray):
                btns.append(week_btns)
                week_btns = []  # Очищення тимчасового списку для наступного тижня

        # Додавання кнопок для переходу між місяцями
        month_switch_buttons = [
            InlineKeyboardButton(text='<<<', callback_data=f'setOrderDate_{orderID}_{dayy}_{month - 1}_{yearr}'),
            InlineKeyboardButton(text=f'{monthh} {yearr}', callback_data='ignore'),
            InlineKeyboardButton(text='>>>', callback_data=f'setOrderDate_{orderID}_{dayy}_{month + 1}_{yearr}')
        ]
        btns.append(month_switch_buttons)

        deliveryDateButtons = InlineKeyboardMarkup(btns)

        return deliveryDateButtons

    def getDateAttributes(self, year, month):
        month_translation = {
            'January': 'Січень',
            'February': 'Лютий',
            'March': 'Березень',
            'April': 'Квітень',
            'May': 'Травень',
            'June': 'Червень',
            'July': 'Липень',
            'August': 'Серпень',
            'September': 'Вересень',
            'October': 'Жовтень',
            'November': 'Листопад',
            'December': 'Грудень'
        }
        if month <= 0:
            month = 12
            year -= 1
        elif month >= 13:
            month = 1
            year += 1

        daysArr = self.get_month_days(year, month)
        month = month_translation[calendar.month_name[month]]
        year = year

        return daysArr, month, year
    def get_month_days(self, year, month):
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        current_day = now.day

        dayArr = []

        # Get the first and last day of the selected month
        first_day_weekday, last_day = calendar.monthrange(year, month)

        # Adjust the first day if it is not Monday (0: Monday, 6: Sunday)
        first_day_offset = (first_day_weekday) % 7  # Convert to 0: Monday, 6: Sunday

        # Fill the previous month's days if needed
        for i in range(first_day_offset):
            dayArr.append('.')

        # Print the days for the selected month
        for day in range(1, last_day + 1):
            if year < current_year or (year == current_year and month < current_month):
                # Print past months' days as "*"
                dayArr.append('*')
            elif year == current_year and month == current_month and day < current_day:
                # Print past days of the current month as "*"
                dayArr.append('*')
            elif year == current_year and month == current_month and day == current_day and now.hour > 20:
                # Print past days of the current month as "*"
                dayArr.append('*')
            elif year == current_year and month == current_month and day == current_day:
                # Print the current date
                dayArr.append(day)
            else:
                # Print future days of the current month with their actual date
                dayArr.append(day)

        # Fill the remaining days of the week with "."
        remaining_days = ((7 - (first_day_offset + last_day) % 7) % 7)
        for i in range(remaining_days):
            dayArr.append('.')

        return dayArr

    async def submit_appointment(self, update: Update, context: CallbackContext) -> int:
        try:
            date = context.user_data.get('date')
            if not date:
                return ConversationHandler.END

            user_data = context.user_data
            order_id = save_appointment_to_db(user_data)  # Збереження замовлення і отримання ID

            if order_id:

                msg = (
                    f"Дякуємо, ваше замовлення відправлено і обробляється.\nID вашого замовлення: {order_id}, яке скопійовано вам в буфер\n"
                    "Інформацію про ваше замовлення скопійовано в буфер обміну.\n"
                    "Ви можете перевірити стан вашого замовлення, використовуючи команду /checkMyOrder. \n"
                    "Для завершення використайте /endOfconversation"
                )
                pyperclip.copy(order_id)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="Сталася помилка під час обробки вашого замовлення.")

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Запис завершено.")
            return ConversationHandler.END
        except Exception as e:
            print(f"Помилка при збереженні замовлення: {e}")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Сталася помилка під час обробки вашого замовлення.")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Запис завершено.")
            return ConversationHandler.END

    async def comment_handler(self, update: Update, context: CallbackContext) -> int:
        try:
            user_text = update.message.text
            if user_text.lower() == "так":
                await update.message.reply_text("Будь ласка, введіть ваш коментар:")
                return COMMENT
            elif user_text.lower() == "ні":
                return await self.ask_date(update, context)
            else:
                context.user_data['comment'] = user_text  # Зберігаємо коментар
                return await self.ask_date(update, context)
        except Exception as e:
            print(e)

    async def ask_comment(self, update: Update, context: CallbackContext) -> int:
        context.user_data['year'] = update.message.text
        try:
            keyboard = [
                [KeyboardButton("Так")],
                [KeyboardButton("Ні")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text("Чи хочете ви залишити коментар до замовлення?", reply_markup=reply_markup)
            return COMMENT
        except Exception as e:
            print(e)

    def setup_conv_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('signupforcarservice', self.ask_name)],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.ask_surname)],
                SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.ask_phone_option)],
                PHONE_OPTION: [
                    MessageHandler(filters.CONTACT, self.phone_option_handler),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.phone_option_handler)
                ],
                PHONE_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.ask_brand)],
                BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.ask_model)],
                MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.ask_year)],
                YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.validate_year)],
                COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.comment_handler)],
                DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.submit_appointment)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        self.application.add_handler(conv_handler)


    async def handle_date_selection(self, update: Update, context: CallbackContext) -> int:
        print("Потрапило в handle_date_selection")
        query = update.callback_query
        data = query.data.split('_')
        order_id, day, month, year = data[1], int(data[2]), int(data[3]), int(data[4])
        # Форматування дати для виведення
        formatted_date = f"{day:02d}-{month:02d}-{year}"
        context.user_data['date'] = formatted_date

        # Відправлення повідомлення про вибір дати
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Ви записалися на {formatted_date}. Дякуємо за вибір нашого сервісу!"
        )

        await query.answer()
        await query.edit_message_reply_markup(reply_markup=None)
        # Можливо, тут вам захочеться викликати submit_appointment або іншу логіку
        return await self.submit_appointment(update, context)

    # інші методи
    async def start(self, update: Update, context: CallbackContext) -> None:

        message = ("👋 Вітаємо у нашому автосервісі! Ми раді вітати вас.\n\n"
                   "ℹ️ Використовуйте команди в меню для доступу до наших послуг. "
                   "Ви можете знайти меню команд внизу чату або використовуючи спеціальну кнопку меню (зазвичай знаходиться поруч з полем введення тексту).\n\n"
                   "📌 Доступні команди:\n"
                   "/aboutus - дізнатись більше про нас\n"
                   "/mycontact - наші контакти\n"
                   "/ourservices - переглянути список послуг\n"
                   "/signupforcarservice - записатись на прийом\n")
        await update.message.reply_text(message)
        await self.send_welcome_photo(update, context)
    async def handle_button_click(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == 'about':
            about_text = """
                    Ласкаво просимо до нашого автосервісу! Ми - команда професіоналів, яка забезпечує повний спектр послуг для вашого автомобіля. Від простого ТО до складних ремонтних робіт. Наш пріоритет - якість та задоволення клієнтів. Довірте ваш автомобіль професіоналам!
                    """

            await query.edit_message_text(text=about_text)

        elif query.data == 'contact':

            contact_info = """
                    Контакти:
                    Ім'я: Андрій
                    Прізвище: Рибак
                    Телефон: +380962813659
                    Gmail: boghtml@gmailm.com
                    Telegram: @AndreyRybakk
                    Instagram: https://www.instagram.com/andrey_rybak1/
                    """

            await query.edit_message_text(text=contact_info)


    # Додаткові методи для обробки команд, аналогічні до методів для обробки натискань кнопок
    async def about(self, update: Update, context: CallbackContext) -> None:
        about_text = ("🚗 Ласкаво просимо до AutoServicePro!\n\n"
                      "Ми надаємо повний спектр послуг для обслуговування та ремонту вашого автомобіля. "
                      "Наші майстри - це висококваліфіковані професіонали, що використовують лише найкращі матеріали та інструменти.\n\n"
                      "🔧 Від простої заміни масла до комплексного ремонту двигуна - ми забезпечимо, "
                      "що ваш автомобіль буде у відмінному стані.\n"
                      "📈 Ми пишаємось своєю репутацією надійного сервісу та стремимось до повного задоволення кожного клієнта.")
        await update.message.reply_text(about_text)

    async def contact(self, update: Update, context: CallbackContext) -> None:
        contact_info =  """Контакти:\nІм'я: Андрій\nПрізвище: Рибак\nТелефон: +380962813659\nGmail: boghtml@gmailm.com\nTelegram: @AndreyRybakk\nInstagram: https://www.instagram.com/andrey_rybak1/
                        """

        await update.message.reply_text(contact_info)

    async def services(self, update: Update, context: CallbackContext) -> None:
        services_list = get_services_base()

        services_message = "<b>🔧 Наші послуги:</b>\n\n"
        services_message += "Послуга" + " " * 55 + "Ціна\n"
        services_message += "- " * 43 + "\n"

        for service in services_list:
            # Вирівнювання тексту використовуючи форматування
            service_line = f"{service['name']:<30} {service['price']:>5} грн"
            services_message += f"<pre>{service_line}</pre>\n"

        # Відправлення повідомлення з використанням HTML
        await update.message.reply_text(services_message, parse_mode='HTML')

    async def send_welcome_photo(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        photo_url = 'D:\Qt_designer\TelegramBotAutoService\WelcomePicture.jpg'
        await context.bot.send_photo(chat_id=chat_id, photo=photo_url, caption="Ласкаво просимо до нашого автосервісу!")

    async def book(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("Почнемо запис, Якщо ви захочете припити запис, то введіть команду /cancel.\nБудь ласка, введіть ваше ім'я.")
        return NAME

        # Ваш код для відповіді на команду /signupforcarservice
    def run(self):
        self.application.run_polling()

if __name__ == '__main__':
    token = '7023889386:AAHlRfbpLCfgEYsWN9As6ACdhlQhqKpanzE'
    bot = AutoServiceBot(token)
    bot.run()

# 7023889386:AAHlRfbpLCfgEYsWN9As6ACdhlQhqKpanzE
