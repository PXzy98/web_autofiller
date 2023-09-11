import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta, date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.by import By
from tkcalendar import DateEntry
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time


# Create a function to close the browser
def close_browser():
    global driver
    if driver is not None:
        driver.quit()


weekday_dict = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

# Parse the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the URL, Chromedriver path, and options
url = config['DEFAULT']['URL']
chromedriver_path = config['DEFAULT']['Chromedriver_Path']
options = [config['DEFAULT']['Option1'], config['DEFAULT']['Option2'], config['DEFAULT']['Option3'],
           config['DEFAULT']['Option4']]
excel_file_path = config.get('DEFAULT', 'ExcelFile')

# Read the Excel file
df_village = pd.read_excel(excel_file_path, sheet_name="Merry_Village")
df_integral = pd.read_excel(excel_file_path, sheet_name="Merry_Integral")

# print(df_integral)

df_village.dropna(subset=[df_village.columns[1]], inplace=True)
df_integral.dropna(subset=[df_integral.columns[1]], inplace=True)

# Create a global variable to store the driver
driver = None

# Create the root window
root = Tk()
root.protocol("WM_DELETE_WINDOW", close_browser)  # Quit the driver when the app is closed

notebook = ttk.Notebook(root)

tab2 = ttk.Frame(notebook)
# tab1 = ttk.Frame(notebook)
# tab3 = ttk.Frame(notebook)

# Add tabs to the Notebook

notebook.add(tab2, text="semi-manul")


# notebook.add(tab3, text="semi-auto")
# notebook.add(tab1, text="manul")


def days_in_month(year, month):
    # Dictionary that maps month numbers to the number of days in that month
    days_in_non_leap_year = {
        1: 31,  # January
        2: 28,  # February (29 in a leap year)
        3: 31,  # March
        4: 30,  # April
        5: 31,  # May
        6: 30,  # June
        7: 31,  # July
        8: 31,  # August
        9: 30,  # September
        10: 31,  # October
        11: 30,  # November
        12: 31  # December
    }

    # Function to determine if a year is a leap year
    def is_leap_year(year):
        if year % 4 != 0:
            return False
        elif year % 100 != 0:
            return True
        elif year % 400 != 0:
            return False
        else:
            return True

    # Check if the year is a leap year and adjust February's days accordingly
    if is_leap_year(year):
        days_in_non_leap_year[2] = 29

    # Return the number of days in the specified month
    return days_in_non_leap_year[month]


'''
the part of the code for manual
'''


def error_mes(mes):
    global root
    popup = tk.Toplevel()
    popup.title("Pop-up Window")

    # Display the message in a label
    message_label = tk.Label(popup, text=mes, padx=20, pady=20)
    message_label.pack()

    # Create a button to close the window
    close_button = tk.Button(popup, text="Close", command=lambda: close_popup(popup))
    close_button.pack()

    # Prevent interaction with the main window
    root.grab_set()


def not_found():
    global root
    popup = tk.Toplevel()
    popup.title("Pop-up Window")

    # Display the message in a label
    message_label = tk.Label(popup, text="No related person found", padx=20, pady=20)
    message_label.pack()

    # Create a button to close the window
    close_button = tk.Button(popup, text="Close", command=lambda: close_popup(popup))
    close_button.pack()

    # Prevent interaction with the main window
    root.grab_set()


def close_popup(popup):
    global root
    # Release the grab on the main window
    root.grab_release()
    # Close the pop-up window
    popup.destroy()


'''
the part of the code for semi-manual
'''


def semi_manual(tab1):
    def fillin():
        try:
            fillin_actions()
        except AttributeError as e:
            error_mes("No related fields found, make sure it's the correct web page")

        except Exception as e:
            error_mes(e)

    def fillin_actions():
        if mode.get() == 1:
            df = df_integral
        elif mode.get() == 2:
            df = df_village
        global driver
        iframe_wait = WebDriverWait(driver, 10)
        iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'frame1')))
        driver.switch_to.frame(iframe)

        current_last_name = driver.find_element(by=By.ID,
                                                value='ctl00_phFolderContent_ucUBForm_PatLastName').get_attribute(
            'value')
        current_first_name = driver.find_element(by=By.ID,
                                                 value='ctl00_phFolderContent_ucUBForm_PatFirstName').get_attribute(
            'value')

        current_first_name = current_first_name.replace(" ", "")
        current_last_name = current_last_name.replace(" ", "")

        current_first_name = current_first_name.lower()
        current_last_name = current_last_name.lower()

        current_first_name = current_first_name.replace(".", "")
        current_last_name = current_last_name.replace(".", "")

        second_column_values = df.iloc[:, 1].values
        row_num = 1
        result_bool = False
        for name in second_column_values.tolist():
            name = name.replace(".", "")
            if ',' in str(name):
                temp_list = str(name).split(",")

                row_last_name = temp_list[0].replace(" ", "").lower()
                row_first_name = temp_list[1].replace(" ", "").lower()

                if row_last_name == current_last_name and row_first_name == current_first_name:
                    current_ID = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBSubID1')
                    current_ID.clear()
                    current_ID.send_keys(str(df.iloc[row_num - 1, 3]).replace(".0", ""))
                    current_DiagnosisCode = driver.find_element(by=By.ID,
                                                                value='ctl00_phFolderContent_ucUBForm_PrimmaryDiagnosisCode')
                    current_DiagnosisCode.clear()
                    current_DiagnosisCode.send_keys(df.iloc[row_num - 1, 2])

                    result_bool = True
            else:
                temp_list = str(name).split(" ", 1)

                row_last_name = temp_list[0].replace(" ", "").lower()
                row_first_name = temp_list[1].replace(" ", "").lower()
                if row_last_name == current_last_name and row_first_name == current_first_name:
                    current_ID = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBSubID1')
                    current_ID.clear()
                    current_ID.send_keys(str(df.iloc[row_num - 1, 3]).replace(".0", ""))
                    current_DiagnosisCode = driver.find_element(by=By.ID,
                                                                value='ctl00_phFolderContent_ucUBForm_PrimmaryDiagnosisCode')
                    current_DiagnosisCode.clear()
                    current_DiagnosisCode.send_keys(df.iloc[row_num - 1, 2])
                    result_bool = True
            row_num = row_num + 1

        if result_bool == False:
            not_found()

        # Print the values
        driver.switch_to.default_content()

    def passinto():
        try:
            passinto_actions()
        except AttributeError as e:
            error_mes("No related fields found, make sure it's the correct web page")

        except Exception as e:
            error_mes(e)

    def passinto_actions():

        global driver
        iframe_wait = WebDriverWait(driver, 10)
        iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'Iframe24')))
        driver.switch_to.frame(iframe)

        """
        first
        """

        select_element1 = driver.find_element(by=By.ID, value='ctl00_phFolderContent_PayerId')
        select_element2 = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ProviderId')
        select_element3 = driver.find_element(by=By.ID, value='ctl00_phFolderContent_TemplateId')
        select_element4 = driver.find_element(by=By.ID, value='ctl00_phFolderContent_AttendingPhysicianId')

        # Extract the options from the select element
        options1 = [option.text.strip() for option in select_element1.find_elements(by=By.TAG_NAME, value='option')]
        options2 = [option.text.strip() for option in select_element2.find_elements(by=By.TAG_NAME, value='option')]
        options3 = [option.text.strip() for option in select_element3.find_elements(by=By.TAG_NAME, value='option')]
        options4 = [option.text.strip() for option in select_element4.find_elements(by=By.TAG_NAME, value='option')]

        selected_options1 = None
        selected_options2 = None
        selected_options3 = None
        selected_options4 = None

        if mode.get() == 1:
            for s1 in options1:
                if "Integra" in s1:
                    selected_options1 = s1

            for s2 in options2:
                if "Merry Adult" in s2:
                    selected_options2 = s2

            codes = option_var.get().split(",")
            option_found = False
            for s3 in options3:
                if "Integra" in s3 and codes[0] in s3:
                    selected_options3 = s3
                    option_found = True
                    break

            if option_found == False:
                selected_options3 = options3[0]

            for s4 in options4:
                if "Merry Adult" in s4:
                    selected_options4 = s4

        if mode.get() == 2:
            for s1 in options1:
                if "VillageCare" in s1:
                    selected_options1 = s1

            for s2 in options2:
                if "Merry Adult" in s2:
                    selected_options2 = s2

            codes = option_var.get().split(",")
            option_found = False
            for s3 in options3:
                if "VillegeCare" in s3 and codes[0] in s3:
                    selected_options3 = s3
                    option_found = True
                    break

            if option_found == False:
                selected_options3 = options3[0]

            for s4 in options4:
                if "Merry Adult" in s4:
                    selected_options4 = s4

        select = Select(select_element1)
        select.select_by_visible_text(selected_options1)
        select = Select(select_element2)
        select.select_by_visible_text(selected_options2)
        select = Select(select_element3)
        select.select_by_visible_text(selected_options3)
        select = Select(select_element4)
        select.select_by_visible_text(selected_options4)

        button_element = driver.find_element(by=By.ID, value='btnCreateClaim')
        button_element.click()

        driver.switch_to.default_content()

        autoinput()

    # Create a function to open the browser
    def open_browser():
        try:
            open_browser_actions()
        except Exception as e:
            error_mes(e)

    def open_browser_actions():
        global driver
        webdriver_service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=webdriver_service)
        driver.get(url_entry.get())

    # Create the input function
    def autoinput():
        try:
            autoinput_actions()
        except AttributeError as e:
            error_mes("No related fields found, make sure it's the correct web page")

        except Exception as e:
            error_mes(e)

    def autoinput_actions():
        global driver
        date_str = date_entry.get_date().strftime("%Y-%m-%d")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year = date.year
        month = date.month

        iframe_wait = WebDriverWait(driver, 10)
        iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'frame1')))
        driver.switch_to.frame(iframe)

        selected_days = [day for var, day in zip(day_vars, days) if var.get() == 1]
        weekdays = [weekday_dict[weekday] for weekday in selected_days]

        if mode.get() == 1:

            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1)

            # the dates would be use
            dates = []

            current_date = start_date

            while current_date < end_date:
                if current_date.weekday() in weekdays:
                    dates.append(current_date)
                current_date += timedelta(days=1)

            for day_num in range(1, len(dates) + 1):
                if day_num == 1:
                    part6_from_day = driver.find_element(by=By.ID,
                                                         value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Day')
                    part6_from_month = driver.find_element(by=By.ID,
                                                           value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Month')
                    part6_from_year = driver.find_element(by=By.ID,
                                                          value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Year')
                    part6_from_day.clear()
                    part6_from_month.clear()
                    part6_from_year.clear()
                    part6_from_day.send_keys(dates[day_num - 1].day)
                    part6_from_month.send_keys(dates[day_num - 1].month)
                    part6_from_year.send_keys(dates[day_num - 1].year)
                    part12_day = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Day')
                    part12_month = driver.find_element(by=By.ID,
                                                       value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Month')
                    part12_year = driver.find_element(by=By.ID,
                                                      value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Year')

                    part12_day.clear()
                    part12_month.clear()
                    part12_year.clear()

                    part12_day.send_keys(dates[day_num - 1].day)
                    part12_month.send_keys(dates[day_num - 1].month)
                    part12_year.send_keys(dates[day_num - 1].year)
                elif day_num == len(dates):
                    part6_to_day = driver.find_element(by=By.ID,
                                                       value='ctl00_phFolderContent_ucUBForm_StatementToDate_Day')
                    part6_to_month = driver.find_element(by=By.ID,
                                                         value='ctl00_phFolderContent_ucUBForm_StatementToDate_Month')
                    part6_to_year = driver.find_element(by=By.ID,
                                                        value='ctl00_phFolderContent_ucUBForm_StatementToDate_Year')

                    part6_to_day.clear()
                    part6_to_month.clear()
                    part6_to_year.clear()

                    part6_to_day.send_keys(dates[day_num - 1].day)
                    part6_to_month.send_keys(dates[day_num - 1].month)
                    part6_to_year.send_keys(dates[day_num - 1].year)
                input_rev_code = driver.find_element(by=By.ID, value='RevCode' + str(day_num))
                input_rate = driver.find_element(by=By.ID, value='Rate' + str(day_num))
                input_month = driver.find_element(by=By.ID, value='FromDateMonth' + str(day_num))
                input_day = driver.find_element(by=By.ID, value='FromDateDay' + str(day_num))
                input_year = driver.find_element(by=By.ID, value='FromDateYear' + str(day_num))
                input_month_2 = driver.find_element(by=By.ID, value='ToDateMonth' + str(day_num))
                input_day_2 = driver.find_element(by=By.ID, value='ToDateDay' + str(day_num))
                input_year_2 = driver.find_element(by=By.ID, value='ToDateYear' + str(day_num))
                input_units = driver.find_element(by=By.ID, value='Units' + str(day_num))
                input_total_charges = driver.find_element(by=By.ID, value='TotalCharge' + str(day_num))

                input_rev_code.clear()
                input_rate.clear()
                input_month.clear()
                input_day.clear()
                input_year.clear()
                input_month_2.clear()
                input_day_2.clear()
                input_year_2.clear()
                input_units.clear()
                input_total_charges.clear()

                codes = option_var.get().split(",")
                input_rev_code.send_keys('3104')
                input_rate.send_keys(codes[0])
                input_month.send_keys(dates[day_num - 1].month)
                input_day.send_keys(dates[day_num - 1].day)
                input_year.send_keys(dates[day_num - 1].year)
                input_month_2.send_keys(dates[day_num - 1].month)
                input_day_2.send_keys(dates[day_num - 1].day)
                input_year_2.send_keys(dates[day_num - 1].year)
                input_units.send_keys(codes[1])
                input_total_charges.send_keys(codes[2])

            input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerName1')
            input_field.clear()
            # Input data into the element
            input_field.send_keys('Integra Managed Long Term Care')

            input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerID1')
            input_field.clear()
            # Input data into the element
            input_field.send_keys('45302')

            print("integra")

        elif mode.get() == 2:
            print("Village")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToFullName")
            element.clear()
            element.send_keys("Merry Adult Day Care Inc")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToStreetAddr")
            element.clear()
            element.send_keys("PO Box 541637")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToCity")
            element.clear()
            element.send_keys("Flushing")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToState")
            element.clear()
            element.send_keys("NY")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToZip")
            element.clear()
            element.send_keys("11354")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$AreaCode")
            element.clear()
            element.send_keys("718")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Prefix")
            element.clear()
            element.send_keys("767")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Number")
            element.clear()
            element.send_keys("2855")

            element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToTaxId")
            element.clear()
            element.send_keys("842893085")

            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1)

            # the dates would be use
            dates = []

            current_date = start_date

            while current_date < end_date:
                if current_date.weekday() in weekdays:
                    dates.append(current_date)
                current_date += timedelta(days=1)

            for day_num in range(1, len(dates) + 1):
                if day_num == 1:
                    part6_from_day = driver.find_element(by=By.ID,
                                                         value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Day')
                    part6_from_month = driver.find_element(by=By.ID,
                                                           value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Month')
                    part6_from_year = driver.find_element(by=By.ID,
                                                          value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Year')
                    part6_from_day.clear()
                    part6_from_month.clear()
                    part6_from_year.clear()
                    part6_from_day.send_keys(dates[day_num - 1].day)
                    part6_from_month.send_keys(dates[day_num - 1].month)
                    part6_from_year.send_keys(dates[day_num - 1].year)
                    part12_day = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Day')
                    part12_month = driver.find_element(by=By.ID,
                                                       value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Month')
                    part12_year = driver.find_element(by=By.ID,
                                                      value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Year')

                    part12_day.clear()
                    part12_month.clear()
                    part12_year.clear()

                    part12_day.send_keys(dates[day_num - 1].day)
                    part12_month.send_keys(dates[day_num - 1].month)
                    part12_year.send_keys(dates[day_num - 1].year)
                elif day_num == len(dates):
                    part6_to_day = driver.find_element(by=By.ID,
                                                       value='ctl00_phFolderContent_ucUBForm_StatementToDate_Day')
                    part6_to_month = driver.find_element(by=By.ID,
                                                         value='ctl00_phFolderContent_ucUBForm_StatementToDate_Month')
                    part6_to_year = driver.find_element(by=By.ID,
                                                        value='ctl00_phFolderContent_ucUBForm_StatementToDate_Year')

                    part6_to_day.clear()
                    part6_to_month.clear()
                    part6_to_year.clear()

                    part6_to_day.send_keys(dates[day_num - 1].day)
                    part6_to_month.send_keys(dates[day_num - 1].month)
                    part6_to_year.send_keys(dates[day_num - 1].year)
                input_rev_code = driver.find_element(by=By.ID, value='RevCode' + str(day_num))
                input_rate = driver.find_element(by=By.ID, value='Rate' + str(day_num))
                input_month = driver.find_element(by=By.ID, value='FromDateMonth' + str(day_num))
                input_day = driver.find_element(by=By.ID, value='FromDateDay' + str(day_num))
                input_year = driver.find_element(by=By.ID, value='FromDateYear' + str(day_num))
                input_month_2 = driver.find_element(by=By.ID, value='ToDateMonth' + str(day_num))
                input_day_2 = driver.find_element(by=By.ID, value='ToDateDay' + str(day_num))
                input_year_2 = driver.find_element(by=By.ID, value='ToDateYear' + str(day_num))
                input_units = driver.find_element(by=By.ID, value='Units' + str(day_num))
                input_total_charges = driver.find_element(by=By.ID, value='TotalCharge' + str(day_num))

                input_rev_code.clear()
                input_rate.clear()
                input_month.clear()
                input_day.clear()
                input_year.clear()
                input_month_2.clear()
                input_day_2.clear()
                input_year_2.clear()
                input_units.clear()
                input_total_charges.clear()

                codes = option_var.get().split(",")
                input_rev_code.send_keys('3104')
                input_rate.send_keys(codes[0])
                input_month.send_keys(dates[day_num - 1].month)
                input_day.send_keys(dates[day_num - 1].day)
                input_year.send_keys(dates[day_num - 1].year)
                input_month_2.send_keys(dates[day_num - 1].month)
                input_day_2.send_keys(dates[day_num - 1].day)
                input_year_2.send_keys(dates[day_num - 1].year)
                input_units.send_keys(codes[1])
                input_total_charges.send_keys(codes[2])

            input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerName1')
            input_field.clear()
            # Input data into the element
            input_field.send_keys('VillageCareMAX')

            input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerID1')
            input_field.clear()
            # Input data into the element
            input_field.send_keys('26545')
        else:
            print(options)
        driver.switch_to.default_content()
        fillin()

    # Create the clean function
    def clean():
        try:
            clean_actions()
        except AttributeError as e:
            error_mes("No related fields found, make sure it's the correct web page")

        except Exception as e:
            error_mes(e)

    def clean_actions():
        global driver
        date_str = date_entry.get_date().strftime("%Y-%m-%d")
        date_chosen = datetime.strptime(date_str, "%Y-%m-%d")
        year = date_chosen.year
        month = date_chosen.month

        iframe_wait = WebDriverWait(driver, 10)
        iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'frame1')))
        driver.switch_to.frame(iframe)

        # Print the selected days of the week
        selected_days = [day for var, day in zip(day_vars, days) if var.get() == 1]
        weekdays = [weekday_dict[weekday] for weekday in selected_days]

        start_date = datetime(year, month, 1)
        end_date = datetime(year, month + 1, 1)

        # the dates would be use
        dates = []

        current_date = start_date

        while current_date < end_date:
            if current_date.weekday() in weekdays:
                dates.append(current_date)
            current_date += timedelta(days=1)

        for day_num in range(1, len(dates) + 1):
            input_rev_code = driver.find_element(by=By.ID, value='RevCode' + str(day_num))
            input_rate = driver.find_element(by=By.ID, value='Rate' + str(day_num))
            input_month = driver.find_element(by=By.ID, value='FromDateMonth' + str(day_num))
            input_day = driver.find_element(by=By.ID, value='FromDateDay' + str(day_num))
            input_year = driver.find_element(by=By.ID, value='FromDateYear' + str(day_num))
            input_month_2 = driver.find_element(by=By.ID, value='ToDateMonth' + str(day_num))
            input_day_2 = driver.find_element(by=By.ID, value='ToDateDay' + str(day_num))
            input_year_2 = driver.find_element(by=By.ID, value='ToDateYear' + str(day_num))
            input_units = driver.find_element(by=By.ID, value='Units' + str(day_num))
            input_total_charges = driver.find_element(by=By.ID, value='TotalCharge' + str(day_num))

            input_rev_code.clear()
            input_rate.clear()
            input_month.clear()
            input_day.clear()
            input_year.clear()
            input_month_2.clear()
            input_day_2.clear()
            input_year_2.clear()
            input_units.clear()
            input_total_charges.clear()

        part6_from_day = driver.find_element(by=By.ID,
                                             value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Day')
        part6_from_month = driver.find_element(by=By.ID,
                                               value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Month')
        part6_from_year = driver.find_element(by=By.ID,
                                              value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Year')
        part6_from_day.clear()
        part6_from_month.clear()
        part6_from_year.clear()

        part12_day = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Day')
        part12_month = driver.find_element(by=By.ID,
                                           value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Month')
        part12_year = driver.find_element(by=By.ID,
                                          value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Year')

        part12_day.clear()
        part12_month.clear()
        part12_year.clear()

        part6_to_day = driver.find_element(by=By.ID,
                                           value='ctl00_phFolderContent_ucUBForm_StatementToDate_Day')
        part6_to_month = driver.find_element(by=By.ID,
                                             value='ctl00_phFolderContent_ucUBForm_StatementToDate_Month')
        part6_to_year = driver.find_element(by=By.ID,
                                            value='ctl00_phFolderContent_ucUBForm_StatementToDate_Year')

        part6_to_day.clear()
        part6_to_month.clear()
        part6_to_year.clear()

        input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerName1')
        input_field.clear()

        input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerID1')
        input_field.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToFullName")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToStreetAddr")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToCity")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToState")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToZip")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$AreaCode")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Prefix")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Number")
        element.clear()

        element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToTaxId")
        element.clear()

        driver.switch_to.default_content()

    # Create an IntVar to keep track of the selected mode
    mode = IntVar()
    mode.set(1)  # Default mode is Integra

    frame1 = LabelFrame(tab1, text="Payer", padx=10, pady=10)

    # Create radiobuttons to switch between modes in a horizontal layout
    Radiobutton(frame1, text="Integra", variable=mode, value=1).grid(row=0, column=0, sticky='w')
    Radiobutton(frame1, text="Village", variable=mode, value=2).grid(row=0, column=1, sticky='w')

    frame1.grid(row=0, column=0, padx=10, pady=10)

    frame2 = LabelFrame(tab1, text="Basic Setting", padx=10, pady=10)

    # Create a label and entry for the URL
    Label(frame2, text="URL: ").grid(row=0, column=0, sticky='w')

    url_entry = Entry(frame2, width=25)
    url_entry.insert(0, url)
    url_entry.grid(row=0, column=1, sticky='w')

    # Create a button to open the browser
    Button(frame2, text="Open Browser", command=open_browser).grid(row=0, column=2, columnspan=2, sticky='w')

    # Create a DateEntry to select a date

    frame2.grid(row=0, column=1, padx=10, pady=10)

    frame3 = LabelFrame(tab1, text="Dates Setting")
    # Create checkboxes for the days of the week
    Label(frame3, text="Select a date: ").grid(row=0, column=0, sticky='w')

    date_entry = DateEntry(frame3)
    date_entry.grid(row=0, column=1, sticky='w')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_vars = []
    for i, day in enumerate(days):
        var = IntVar()
        day_vars.append(var)
        Checkbutton(frame3, text=day, variable=var).grid(row=3, column=i, sticky='w')

    # Create radio buttons for the options
    option_var = StringVar()
    option_var.set(options[0])  # Default option is the first one
    for i, option in enumerate(options):
        Radiobutton(frame3, text=option, variable=option_var, value=option).grid(row=4, column=i, sticky='w')

    frame3.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    frame4 = LabelFrame(tab1, text="Actions")
    # Create buttons for input and clean
    Button(frame4, text="AutoInput", command=autoinput).grid(row=0, column=0, sticky='w', padx=10, pady=10)
    Button(frame4, text="Passthrough", command=passinto).grid(row=0, column=1, sticky='w', padx=10, pady=10)
    Button(frame4, text="Clean", command=clean).grid(row=0, column=2, sticky='w', padx=10, pady=10)
    Button(frame4, text="FillCode", command=fillin).grid(row=0, column=3, sticky='w', padx=10, pady=10)
    Button(frame4, text="Quit", command=lambda: (close_browser(), root.destroy())).grid(row=0, column=4, sticky='w',
                                                                                        padx=10, pady=10)

    frame4.grid(row=2, column=0, padx=10, pady=10, columnspan=2)


# Create a quit button

# manual(tab1)
semi_manual(tab2)

notebook.grid()
root.mainloop()
