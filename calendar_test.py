import telebot
import calendar
import datetime

def get_month_days(year, month):
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    dayArr = []

    first_day_weekday, last_day = calendar.monthrange(year, month)

    first_day_offset = (first_day_weekday) % 7  

    for i in range(first_day_offset):
        dayArr.append('.')

    for day in range(1, last_day + 1):
        if year < current_year or (year == current_year and month < current_month):
            dayArr.append('*')
        elif year == current_year and month == current_month and day < current_day:
            dayArr.append('*')
        elif year == current_year and month == current_month and day == current_day and now.hour > 20:
            dayArr.append('*')
        elif year == current_year and month == current_month and day == current_day:
            dayArr.append(day)
        else:
            dayArr.append(day)

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


def deliveryDateButtons(orderID, year, month, dayy):
    """Create an InlineKeyboardMarkup with calendar day buttons.

    Disabled/past days use callback_data='ignore'.
    """
    btns = []

    markup = telebot.types.InlineKeyboardMarkup(row_width=7)

    daysArray, monthh, yearr = getDateAttributes(year, month)

    for day in daysArray:
        if day == '*' or day == '.':
            btns.append(telebot.types.InlineKeyboardButton(text=day, callback_data='ignore'))
        else:
            btns.append(
                telebot.types.InlineKeyboardButton(text=str(day), callback_data=f'selectOrderDay_{orderID}_{day}_{month}_{yearr}')
            )

    # Normalize month bounds
    if month <= 0:
        month = 12
    elif month >= 13:
        month = 1

    markup.add(*btns)
    markup.row(
        telebot.types.InlineKeyboardButton(text='<<<', callback_data=f'setOrderDate_{orderID}_{dayy}_{month - 1}_{yearr}'),
        telebot.types.InlineKeyboardButton(text=f'{monthh} {yearr}', callback_data='ignore'),
        telebot.types.InlineKeyboardButton(text='>>>', callback_data=f'setOrderDate_{orderID}_{dayy}_{month + 1}_{yearr}')
    )

    return markup


if __name__ == '__main__':
    year = 2023
    month = 9
    get_month_days(year, month)
    print(getDateAttributes(year, month))

