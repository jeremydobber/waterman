from datetime import date
import zipfile


def get_prev_len():
    try:
        prev_len = input("Length of previsions in years : ")

        start_date = int(date.today().strftime("%Y"))
        end_date = int(start_date + int(prev_len))

        if end_date >= 2100:
            end_date = 2100

        years = list(map(str, list(range(start_date, end_date))))

        return years

    except ValueError:
        print("Please enter an integer: ")
        get_prev_len()


def extract_zipfile(zipfile_path, destination_path):
    with zipfile.ZipFile(zipfile_path, mode="r") as archive:
        archive.extractall(f"{destination_path}/")