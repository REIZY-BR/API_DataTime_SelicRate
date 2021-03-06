#{"data":"17/09/2021","valor":"0.019930"}
from giant_test.modulacao import *


raw = raw_data()
capital = 657.43
start_date = poli_data("2010-01-01")
end_date = poli_data("2021-03-01")

mont = calc_data(raw, start_date, end_date, capital)

while True:
    frequency = str(input("choose the frequency to be show! [day/month/year] [0] to finalize: "))
    if frequency == "0":
        break
    if frequency == "day" or frequency == "month" or frequency == "year":
        print_day(mont) if frequency == "day" else None
        print_month(mont, start_date, end_date) if frequency == "month" else None
        print_year(mont, start_date, end_date) if frequency == "year" else None
    else:
        print("\033[31mInvalid frequency, please try again!\033[m")
print("Program Finalized!")
while True:
    decision = str(input("Want to see the best period[bp] or next 100 average media day[md]?\n [0] to finalize: ")).lower()
    if decision == "0":
        break
    if decision == "bp":
        better_period(raw, start_date=poli_data("2000-01-01"), end_date=poli_data("2022-03-31"))
    elif decision == "md":
        first_day, media_period, period_percent = media_rate(raw)
        new_period = predict_rate(first_day, media_period, period_percent)
        for key, value in enumerate(new_period):
            print(value)
    else:
        print("\033[31mInvalid choice, please try again!\033[m")
print("Program Finalized!")


