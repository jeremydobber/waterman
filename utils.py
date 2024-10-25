import shutil
from datetime import date
from matplotlib import pyplot as plt

def get_prev_len():
    prev_len = int(input("Length of previsions in years : "))

    start_date = int(date.today().strftime("%Y"))
    end_date = int(start_date + prev_len)

    if end_date >= 2100:
        end_date = 2100

    years = list(map(str, list(range(start_date,end_date))))

    return years

def get_user_input():
    people = int(input("Number of people in the household: "))

    # Add other questions about water usage.

    data = {"people": people}

    return data

def draw_chart(series, call):
    plt.plot(series.index, series.values)
    plt.show()
    plt.savefig(f"test_{call}.png")

def clean_tmp_files():
    try:
        shutil.rmtree("./data")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))