import telebot
import calendar  # pip install calendar
import datetime

def get_month_days(year, month):
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    dayArr = []

    # Get the first and last day of the selected month
    first_day_weekday, last_day = calendar.monthrange(year, month)

    # Adjust the first day if it is not Monday (0: Monday, 6: Sunday)
    first_day_offset = (first_day_weekday) % 7   # Convert to 0: Monday, 6: Sunday

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


def getDateAttributes(year, month):
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

    daysArr = get_month_days(year, month)
    month = month_translation[calendar.month_name[month]]
    year = year

    return daysArr, month, year


def deliveryDateButtons(self, orderID, year, month, dayy):  # <-<-<----- FIX FIX FIX FIX FIX FIX FIX FIX FIX FIX FIX FIX FIX FIX
    btns = []

    deliveryDateButtons = telebot.types.InlineKeyboardMarkup(row_width=7)

    daysArray, monthh, yearr = getDateAttributes(year, month)

    for day in daysArray:
        if day == '*' or day == '.':
            btns.append(telebot.types.InlineKeyboardButton(text=day, callback_data=f'*'))
        else:
            btns.append(telebot.types.InlineKeyboardButton(text=day, callback_data=f'selectOrderDay_{orderID}_{day}_{month}_{yearr}'))

    if month <= 0:
        month = 12
    elif month >= 13:
        month = 1

    deliveryDateButtons.add(*btns)
    deliveryDateButtons.row(telebot.types.InlineKeyboardButton(text='<<<', callback_data=f'setOrderDate_{orderID}_{dayy}_{month - 1}_{yearr}'),
                            telebot.types.InlineKeyboardButton(text=f'{monthh} {yearr}', callback_data='*'),
                            telebot.types.InlineKeyboardButton(text='>>>', callback_data=f'setOrderDate_{orderID}_{dayy}_{month + 1}_{yearr}'))
    # deliveryDateButtons.row(telebot.types.InlineKeyboardButton(text='✅ Підтвердити дату', callback_data=f"acceptDelivaryDate_{day}_{month}_{yearr}"))

    return deliveryDateButtons


if __name__ == '__main__':
    # Example usage: for September 2023
    year = 2023
    month = 9
    get_month_days(year, month)
    print(getDateAttributes(year, month))

