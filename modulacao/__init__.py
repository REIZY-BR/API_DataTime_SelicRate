import requests
import json
import datetime
import pytz

def raw_data():
    """
    :return: Database reformat in a list to manipulate.
    """
    #creating a string with API datas
    req = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=dd/mm/yy&dataFinal=dd/mm/yy")
    # using json to translate a string to unce a list with dicionaries
    return json.loads(req.content)


def poli_data(data_str):
    """
    :param data_str: String whith date data.
    :return: A object .data to manipulate.
    """
    start_year, start_month, start_day = data_str.split('-')
    poli_date = datetime.date(int(start_year), int(start_month), int(start_day))
    #returning a object data to use in another functions
    return poli_date


def calc_data(raw_data, start_date, end_date, capital):
    """
    :param raw_data: List with API data.
    :param start_date: init object .data.
    :param end_date: end object .data.
    :param capital: Capital to be invested
    :return: A calculated list with dicionary's to every day in start_date to end_date.
    """
    tot_ae = 0
    amount_earned = 0
    move = dict() #temporary dicionary to save data
    result = list() #list to add "move"
    for dicionary in raw_data:
        #decomposing the dicionary to easy manipulate
        data_day, data_month, data_year = dicionary["data"].split('/')
        fdata = datetime.date(int(data_year), int(data_month), int(data_day))
        #comparing the dates to filter valid dates.
        if end_date >= fdata >= start_date:
            capital += amount_earned #variable to insert amount earned + capital
            tot_ae += amount_earned #variable to insert amount earned
            #calculating the selic rate
            amount_earned = float(capital) * (float(dicionary["valor"])/100)
            move["Date"] = fdata
            move["Capital"] = round(capital, 6)
            move["Amount earned"] = round(tot_ae, 6)
            result.append(move.copy())
    return result


def print_day(calc_data):
    """
    :param calc_data: The Calculated e formated list creat in function "calc_data".
    :return: show every day in "calc_data".
    """
    #iterating every dicionary to show for user
    for ind, item in enumerate(calc_data):
        date = calc_data[ind]["Date"]
        capital = calc_data[ind]["Capital"]
        am_earned = calc_data[ind]["Amount earned"]
        #creating a variable to save a format string to show
        format_str = f'|Date: {date}| Capital: {capital:.6f}| Amount earned {am_earned:.6f}|'
        print(format_str)
        print("-" * len(format_str))
    print("\033[42m<<<<<<<<<<<< End Process >>>>>>>>>>>>\033[m")


def print_month(calc_data, start_date, end_date):
    """
    :param calc_data: The Calculated e formated list creat in function "calc_data".
    :param start_date: init object .data.
    :param end_date: end object .data.
    :return: show all last day of months in period between in start_date and end_date.
    """
    cont_month = int(start_date.month) #variable to save current month
    #iterating every dicionary to manipulate
    for ind, item in enumerate(calc_data):
        #decomposing every dicionary to easy manipulate
        date = calc_data[ind]["Date"]
        capital = calc_data[ind]["Capital"]
        am_earned = calc_data[ind]["Amount earned"]
        if date.month == cont_month:
            #if current month is the same, the program ignored
            pass
        else:
            #the last day of a month is the same as the day before the next month
        #creating a variable to save a format string to show
            format_str = f'|Date: {calc_data[ind-1]["Date"]}| Capital: {calc_data[ind-1]["Capital"]:.6f}| Amount earned {calc_data[ind-1]["Amount earned"]:.6f}|'
            print(format_str)
            print("-" * len(format_str))
            #taking the last date in the select period
            if date == end_date:
                format_str = f'|Date: {date}| Capital: {capital}| Amount earned {am_earned}|'
                print(format_str)
                print("-" * len(format_str))
            cont_month += 1 #changing the current month
            #turning the year
            if cont_month == 13:
                cont_month = 1
    print("\033[42m<<<<<<<<<<<< End Process >>>>>>>>>>>>\033[m")


def print_year(calc_data, start_date, end_date):
    """
    :param calc_data: The Calculated e formated list creat in function "calc_data".
    :param start_date: init object .data.
    :param end_date: end object .data.
    :return: show all last day of years in period between in start_date and end_date.
    """
    #decomposing date in variables
    cont_year, end_year = start_date.year, end_date.year
    #iterating every dicionary to manipulate
    for ind, item in enumerate(calc_data):
        #decomposing every dicionary to easy manipulate
        date = calc_data[ind]["Date"]
        capital = calc_data[ind]["Capital"]
        am_earned = calc_data[ind]["Amount earned"]
        if date.year == cont_year:
            #if the current year is the same and the current year is diferent to end_date, the program ignored.
            if date == end_date:
                format_str = f'|Date: {date}| Capital: {capital:.6f}| Amount earned {am_earned:.6f}|'
                print(format_str)
                print("-" * len(format_str))
        else:
            #the last day of a year is the same as the day before the next year
        #creating a variable to save a format string to show
            format_str = f'|Date: {calc_data[ind-1]["Date"]}| Capital: {calc_data[ind-1]["Capital"]:.6f}| Amount earned {calc_data[ind-1]["Amount earned"]:.6f}|'
            print(format_str)
            print("-" * len(format_str))
            #turning the year
            cont_year += 1
    print("\033[42m<<<<<<<<<<<< End Process >>>>>>>>>>>>\033[m")


def better_period(raw_data, start_date, end_date, amount_exemple=657.43):
    max_amount = 0
    tot_period_list = list()
    for ind, item in enumerate(raw_data):
        day, month, year = item["data"].split('/')
        actual_date = datetime.date(int(year), int(month), int(day))
        if start_date <= actual_date <= end_date:
            tot_period_list.append(item)
    max_pos = len(tot_period_list)
    for ind, item in enumerate(tot_period_list):
        if ind + 500 < max_pos:
            sday, smonth, syear = item["data"].split('/')
            initial_period = datetime.date(int(syear), int(smonth), int(sday))
            fday, fmonth, fyear = tot_period_list[ind + 500]["data"].split('/')
            final_period = datetime.date(int(fyear), int(fmonth), int(fday))
            tot_amount = 0
            for dicionary in tot_period_list:
                day, month, year = dicionary["data"].split('/')
                actual_date = datetime.date(int(year), int(month), int(day))
                if initial_period <= actual_date <= final_period:
                    tot_amount += amount_exemple * float(dicionary["valor"])
                    if actual_date == final_period:
                        break
        if tot_amount > max_amount:
            max_amount = tot_amount
            better = f"the best period was between {initial_period} / {final_period}"
    print(better)
# the best period was between 2001-10-26 / 2003-10-22


def calc_percent(first_value, last_value):
    percent = ((last_value / first_value) - 1) * 100
    return round(percent)


#{"data":"01/07/2022","valor":"0.049037"}
def media_rate(raw_data):
    media = 0
    invert_raw_data = raw_data[::-1]
    first_rate = float(invert_raw_data[0]["valor"])
    change_day = 0
    list_frequency_days = list()
    list_peridod_rate = list()
    for indice, item in enumerate(invert_raw_data):
        current_rate = float(item["valor"])
        media += current_rate
        if indice >= 100:
            break
        else:
            if first_rate == current_rate:
                change_day += 1
            else:
                period_percent = calc_percent(first_value=current_rate, last_value=first_rate)
                list_peridod_rate.append(period_percent)
                list_frequency_days.append(change_day)
                first_rate = current_rate
                change_day = 0
    media = round((media/100), 6)
    del list_frequency_days[0]
    list_frequency_days.pop()
    del list_peridod_rate[0]
    list_peridod_rate.pop()
    media_change_days = sum(list_frequency_days) / len(list_frequency_days)
    media_change_days = round(media_change_days)
    media_rate_period = sum(list_peridod_rate) / len(list_peridod_rate)
    return media, media_change_days, media_rate_period


































