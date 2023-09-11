# def manual(tab1):
#
#     def fillin():
#         if mode.get() == 1:
#             df = df_integral
#         elif mode.get() == 2:
#             df = df_village
#         global driver
#         iframe_wait = WebDriverWait(driver, 10)
#         iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'frame1')))
#         driver.switch_to.frame(iframe)
#
#         current_last_name = driver.find_element(by=By.ID,
#                                                 value='ctl00_phFolderContent_ucUBForm_PatLastName').get_attribute(
#             'value')
#         current_first_name = driver.find_element(by=By.ID,
#                                                  value='ctl00_phFolderContent_ucUBForm_PatFirstName').get_attribute(
#             'value')
#
#         current_first_name = current_first_name.replace(" ", "")
#         current_last_name = current_last_name.replace(" ", "")
#
#         current_first_name = current_first_name.lower()
#         current_last_name = current_last_name.lower()
#
#         second_column_values = df.iloc[:, 1].values
#         row_num = 1
#         result_bool = False
#         for name in second_column_values.tolist():
#
#             if ',' in str(name):
#                 temp_list = str(name).split(",")
#
#                 row_last_name = temp_list[0].replace(" ", "").lower()
#                 row_first_name = temp_list[1].replace(" ", "").lower()
#
#                 if row_last_name == current_last_name and row_first_name == current_first_name:
#                     current_ID = driver.find_element(by=By.ID,value='ctl00_phFolderContent_ucUBForm_COBSubID1')
#                     current_ID.clear()
#                     current_ID.send_keys(str(df.iloc[row_num - 1, 3]).replace(".0",""))
#                     current_DiagnosisCode = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_PrimmaryDiagnosisCode')
#                     current_DiagnosisCode.clear()
#                     current_DiagnosisCode.send_keys(df.iloc[row_num-1, 2])
#
#                     result_bool = True
#             else:
#
#                 temp_list = str(name).split(" ", 1)
#
#                 row_last_name = temp_list[0].replace(" ", "").lower()
#                 row_first_name = temp_list[1].replace(" ", "").lower()
#
#                 if row_last_name == current_last_name and row_first_name == current_first_name:
#                     current_ID = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBSubID1')
#                     current_ID.clear()
#                     current_ID.send_keys(str(df.iloc[row_num - 1, 3]).replace(".0",""))
#                     current_DiagnosisCode = driver.find_element(by=By.ID,
#                                                      value='ctl00_phFolderContent_ucUBForm_PrimmaryDiagnosisCode')
#                     current_DiagnosisCode.clear()
#                     current_DiagnosisCode.send_keys(df.iloc[row_num - 1, 2])
#                     result_bool = True
#             row_num = row_num + 1
#
#         if result_bool == False:
#             not_found()
#
#
#         # Print the values
#         driver.switch_to.default_content()
#
#     # Create a function to open the browser
#     def open_browser():
#         global driver
#         webdriver_service = Service(chromedriver_path)
#         driver = webdriver.Chrome(service=webdriver_service)
#         driver.get(url_entry.get())
#
#     # Create the input function
#     def input():
#         global driver
#         date_str = date_entry.get_date().strftime("%Y-%m-%d")
#         date = datetime.strptime(date_str, "%Y-%m-%d")
#         year = date.year
#         month = date.month
#
#         iframe_wait = WebDriverWait(driver, 10)
#         iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'frame1')))
#         driver.switch_to.frame(iframe)
#
#         # Print the selected days of the week
#         selected_days = [day for var, day in zip(day_vars, days) if var.get() == 1]
#         weekdays = [weekday_dict[weekday] for weekday in selected_days]
#
#         if mode.get() == 1:
#
#             start_date = datetime(year, month, 1)
#             end_date = datetime(year, month + 1, 1)
#
#             # the dates would be use
#             dates = []
#
#             current_date = start_date
#
#             while current_date < end_date or current_date == end_date:
#                 if current_date.weekday() in weekdays:
#                     dates.append(current_date)
#                 current_date += timedelta(days=1)
#
#             for day_num in range(1, len(dates)):
#                 if day_num == 1:
#                     part6_from_day = driver.find_element(by=By.ID,
#                                                          value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Day')
#                     part6_from_month = driver.find_element(by=By.ID,
#                                                            value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Month')
#                     part6_from_year = driver.find_element(by=By.ID,
#                                                           value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Year')
#                     part6_from_day.clear()
#                     part6_from_month.clear()
#                     part6_from_year.clear()
#                     part6_from_day.send_keys(dates[day_num - 1].day)
#                     part6_from_month.send_keys(dates[day_num - 1].month)
#                     part6_from_year.send_keys(dates[day_num - 1].year)
#                     part12_day = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Day')
#                     part12_month = driver.find_element(by=By.ID,
#                                                        value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Month')
#                     part12_year = driver.find_element(by=By.ID,
#                                                       value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Year')
#
#                     part12_day.clear()
#                     part12_month.clear()
#                     part12_year.clear()
#
#                     part12_day.send_keys(dates[day_num - 1].day)
#                     part12_month.send_keys(dates[day_num - 1].month)
#                     part12_year.send_keys(dates[day_num - 1].year)
#                 elif day_num == len(dates) - 1:
#                     part6_to_day = driver.find_element(by=By.ID,
#                                                        value='ctl00_phFolderContent_ucUBForm_StatementToDate_Day')
#                     part6_to_month = driver.find_element(by=By.ID,
#                                                          value='ctl00_phFolderContent_ucUBForm_StatementToDate_Month')
#                     part6_to_year = driver.find_element(by=By.ID,
#                                                         value='ctl00_phFolderContent_ucUBForm_StatementToDate_Year')
#
#                     part6_to_day.clear()
#                     part6_to_month.clear()
#                     part6_to_year.clear()
#
#                     part6_to_day.send_keys(dates[day_num - 1].day)
#                     part6_to_month.send_keys(dates[day_num - 1].month)
#                     part6_to_year.send_keys(dates[day_num - 1].year)
#
#                 input_rev_code = driver.find_element(by=By.ID, value='RevCode' + str(day_num))
#                 input_rate = driver.find_element(by=By.ID, value='Rate' + str(day_num))
#                 input_month = driver.find_element(by=By.ID, value='FromDateMonth' + str(day_num))
#                 input_day = driver.find_element(by=By.ID, value='FromDateDay' + str(day_num))
#                 input_year = driver.find_element(by=By.ID, value='FromDateYear' + str(day_num))
#                 input_month_2 = driver.find_element(by=By.ID, value='ToDateMonth' + str(day_num))
#                 input_day_2 = driver.find_element(by=By.ID, value='ToDateDay' + str(day_num))
#                 input_year_2 = driver.find_element(by=By.ID, value='ToDateYear' + str(day_num))
#                 input_units = driver.find_element(by=By.ID, value='Units' + str(day_num))
#                 input_total_charges = driver.find_element(by=By.ID, value='TotalCharge' + str(day_num))
#
#                 input_rev_code.clear()
#                 input_rate.clear()
#                 input_month.clear()
#                 input_day.clear()
#                 input_year.clear()
#                 input_month_2.clear()
#                 input_day_2.clear()
#                 input_year_2.clear()
#                 input_units.clear()
#                 input_total_charges.clear()
#
#                 codes = option_var.get().split(",")
#                 input_rev_code.send_keys('3104')
#                 input_rate.send_keys(codes[0])
#                 input_month.send_keys(dates[day_num - 1].month)
#                 input_day.send_keys(dates[day_num - 1].day)
#                 input_year.send_keys(dates[day_num - 1].year)
#                 input_month_2.send_keys(dates[day_num - 1].month)
#                 input_day_2.send_keys(dates[day_num - 1].day)
#                 input_year_2.send_keys(dates[day_num - 1].year)
#                 input_units.send_keys(codes[1])
#                 input_total_charges.send_keys(codes[2])
#
#             input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerName1')
#             input_field.clear()
#             # Input data into the element
#             input_field.send_keys('Integra Managed Long Term Care')
#
#             input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerID1')
#             input_field.clear()
#             # Input data into the element
#             input_field.send_keys('45302')
#
#             print("integra")
#
#         elif mode.get() == 2:
#             print("Village")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToFullName")
#             element.clear()
#             element.send_keys("Merry Adult Day Care Inc")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToStreetAddr")
#             element.clear()
#             element.send_keys("PO Box 541637")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToCity")
#             element.clear()
#             element.send_keys("Flushing")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToState")
#             element.clear()
#             element.send_keys("NY")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToZip")
#             element.clear()
#             element.send_keys("11354")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$AreaCode")
#             element.clear()
#             element.send_keys("718")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Prefix")
#             element.clear()
#             element.send_keys("767")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Number")
#             element.clear()
#             element.send_keys("2855")
#
#             element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToTaxId")
#             element.clear()
#             element.send_keys("842893085")
#
#             start_date = datetime(year, month, 1)
#             end_date = datetime(year, month + 1, 1)
#
#             # the dates would be use
#             dates = []
#
#             current_date = start_date
#
#             while current_date < end_date or current_date == end_date:
#                 if current_date.weekday() in weekdays:
#                     dates.append(current_date)
#                 current_date += timedelta(days=1)
#
#             for day_num in range(1, len(dates)):
#                 if day_num == 1:
#                     part6_from_day = driver.find_element(by=By.ID,
#                                                          value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Day')
#                     part6_from_month = driver.find_element(by=By.ID,
#                                                            value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Month')
#                     part6_from_year = driver.find_element(by=By.ID,
#                                                           value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Year')
#                     part6_from_day.clear()
#                     part6_from_month.clear()
#                     part6_from_year.clear()
#                     part6_from_day.send_keys(dates[day_num - 1].day)
#                     part6_from_month.send_keys(dates[day_num - 1].month)
#                     part6_from_year.send_keys(dates[day_num - 1].year)
#                     part12_day = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Day')
#                     part12_month = driver.find_element(by=By.ID,
#                                                        value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Month')
#                     part12_year = driver.find_element(by=By.ID,
#                                                       value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Year')
#
#                     part12_day.clear()
#                     part12_month.clear()
#                     part12_year.clear()
#
#                     part12_day.send_keys(dates[day_num - 1].day)
#                     part12_month.send_keys(dates[day_num - 1].month)
#                     part12_year.send_keys(dates[day_num - 1].year)
#                 elif day_num == len(dates) - 1:
#                     part6_to_day = driver.find_element(by=By.ID,
#                                                        value='ctl00_phFolderContent_ucUBForm_StatementToDate_Day')
#                     part6_to_month = driver.find_element(by=By.ID,
#                                                          value='ctl00_phFolderContent_ucUBForm_StatementToDate_Month')
#                     part6_to_year = driver.find_element(by=By.ID,
#                                                         value='ctl00_phFolderContent_ucUBForm_StatementToDate_Year')
#
#                     part6_to_day.clear()
#                     part6_to_month.clear()
#                     part6_to_year.clear()
#
#                     part6_to_day.send_keys(dates[day_num - 1].day)
#                     part6_to_month.send_keys(dates[day_num - 1].month)
#                     part6_to_year.send_keys(dates[day_num - 1].year)
#                 input_rev_code = driver.find_element(by=By.ID, value='RevCode' + str(day_num))
#                 input_rate = driver.find_element(by=By.ID, value='Rate' + str(day_num))
#                 input_month = driver.find_element(by=By.ID, value='FromDateMonth' + str(day_num))
#                 input_day = driver.find_element(by=By.ID, value='FromDateDay' + str(day_num))
#                 input_year = driver.find_element(by=By.ID, value='FromDateYear' + str(day_num))
#                 input_month_2 = driver.find_element(by=By.ID, value='ToDateMonth' + str(day_num))
#                 input_day_2 = driver.find_element(by=By.ID, value='ToDateDay' + str(day_num))
#                 input_year_2 = driver.find_element(by=By.ID, value='ToDateYear' + str(day_num))
#                 input_units = driver.find_element(by=By.ID, value='Units' + str(day_num))
#                 input_total_charges = driver.find_element(by=By.ID, value='TotalCharge' + str(day_num))
#
#                 input_rev_code.clear()
#                 input_rate.clear()
#                 input_month.clear()
#                 input_day.clear()
#                 input_year.clear()
#                 input_month_2.clear()
#                 input_day_2.clear()
#                 input_year_2.clear()
#                 input_units.clear()
#                 input_total_charges.clear()
#
#                 codes = option_var.get().split(",")
#                 input_rev_code.send_keys('3104')
#                 input_rate.send_keys(codes[0])
#                 input_month.send_keys(dates[day_num - 1].month)
#                 input_day.send_keys(dates[day_num - 1].day)
#                 input_year.send_keys(dates[day_num - 1].year)
#                 input_month_2.send_keys(dates[day_num - 1].month)
#                 input_day_2.send_keys(dates[day_num - 1].day)
#                 input_year_2.send_keys(dates[day_num - 1].year)
#                 input_units.send_keys(codes[1])
#                 input_total_charges.send_keys(codes[2])
#
#             input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerName1')
#             input_field.clear()
#             # Input data into the element
#             input_field.send_keys('VillageCareMAX')
#
#             input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerID1')
#             input_field.clear()
#             # Input data into the element
#             input_field.send_keys('26545')
#         else:
#             print(options)
#         driver.switch_to.default_content()
#
#     # Create the clean function
#     def clean():
#         global driver
#         date_str = date_entry.get_date().strftime("%Y-%m-%d")
#         date_chosen = datetime.strptime(date_str, "%Y-%m-%d")
#         year = date_chosen.year
#         month = date_chosen.month
#
#         iframe_wait = WebDriverWait(driver, 10)
#         iframe = iframe_wait.until(EC.presence_of_element_located((By.ID, 'frame1')))
#         driver.switch_to.frame(iframe)
#
#         # Print the selected days of the week
#         selected_days = [day for var, day in zip(day_vars, days) if var.get() == 1]
#         weekdays = [weekday_dict[weekday] for weekday in selected_days]
#
#         start_date = datetime(year, month, 1)
#         end_date = datetime(year, month + 1, 1)
#
#         # the dates would be use
#         dates = []
#
#         current_date = start_date
#
#         while current_date < end_date or current_date == end_date:
#             if current_date.weekday() in weekdays:
#                 dates.append(current_date)
#             current_date += timedelta(days=1)
#
#         for day_num in range(1, len(dates)):
#             input_rev_code = driver.find_element(by=By.ID, value='RevCode' + str(day_num))
#             input_rate = driver.find_element(by=By.ID, value='Rate' + str(day_num))
#             input_month = driver.find_element(by=By.ID, value='FromDateMonth' + str(day_num))
#             input_day = driver.find_element(by=By.ID, value='FromDateDay' + str(day_num))
#             input_year = driver.find_element(by=By.ID, value='FromDateYear' + str(day_num))
#             input_month_2 = driver.find_element(by=By.ID, value='ToDateMonth' + str(day_num))
#             input_day_2 = driver.find_element(by=By.ID, value='ToDateDay' + str(day_num))
#             input_year_2 = driver.find_element(by=By.ID, value='ToDateYear' + str(day_num))
#             input_units = driver.find_element(by=By.ID, value='Units' + str(day_num))
#             input_total_charges = driver.find_element(by=By.ID, value='TotalCharge' + str(day_num))
#
#             input_rev_code.clear()
#             input_rate.clear()
#             input_month.clear()
#             input_day.clear()
#             input_year.clear()
#             input_month_2.clear()
#             input_day_2.clear()
#             input_year_2.clear()
#             input_units.clear()
#             input_total_charges.clear()
#
#         part6_from_day = driver.find_element(by=By.ID,
#                                              value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Day')
#         part6_from_month = driver.find_element(by=By.ID,
#                                                value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Month')
#         part6_from_year = driver.find_element(by=By.ID,
#                                               value='ctl00_phFolderContent_ucUBForm_StatementFromDate_Year')
#         part6_from_day.clear()
#         part6_from_month.clear()
#         part6_from_year.clear()
#
#         part12_day = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Day')
#         part12_month = driver.find_element(by=By.ID,
#                                            value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Month')
#         part12_year = driver.find_element(by=By.ID,
#                                           value='ctl00_phFolderContent_ucUBForm_DateAdmitted_Year')
#
#         part12_day.clear()
#         part12_month.clear()
#         part12_year.clear()
#
#         part6_to_day = driver.find_element(by=By.ID,
#                                            value='ctl00_phFolderContent_ucUBForm_StatementToDate_Day')
#         part6_to_month = driver.find_element(by=By.ID,
#                                              value='ctl00_phFolderContent_ucUBForm_StatementToDate_Month')
#         part6_to_year = driver.find_element(by=By.ID,
#                                             value='ctl00_phFolderContent_ucUBForm_StatementToDate_Year')
#
#         part6_to_day.clear()
#         part6_to_month.clear()
#         part6_to_year.clear()
#
#         input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerName1')
#         input_field.clear()
#
#         input_field = driver.find_element(by=By.ID, value='ctl00_phFolderContent_ucUBForm_COBPayerID1')
#         input_field.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToFullName")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToStreetAddr")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToCity")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToState")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToZip")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$AreaCode")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Prefix")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToPhone$Number")
#         element.clear()
#
#         element = driver.find_element(by=By.NAME, value="ctl00$phFolderContent$ucUBForm$PayToTaxId")
#         element.clear()
#
#         driver.switch_to.default_content()
#         print("Clean function called")
#
#     # Create an IntVar to keep track of the selected mode
#     mode = IntVar()
#     mode.set(1)  # Default mode is Integra
#
#     frame1 = LabelFrame(tab1, text="Payer", padx=10, pady=10)
#
#     # Create radiobuttons to switch between modes in a horizontal layout
#     Radiobutton(frame1, text="Integra", variable=mode, value=1).grid(row=0, column=0, sticky='w')
#     Radiobutton(frame1, text="Village", variable=mode, value=2).grid(row=0, column=1, sticky='w')
#
#     frame1.grid(row=0, column=0, padx=10, pady=10)
#
#     frame2 = LabelFrame(tab1, text="Basic Setting", padx=10, pady=10)
#
#     # Create a label and entry for the URL
#     Label(frame2, text="URL: ").grid(row=0, column=0, sticky='w')
#
#     url_entry = Entry(frame2, width=25)
#     url_entry.insert(0, url)
#     url_entry.grid(row=0, column=1, sticky='w')
#
#     # Create a button to open the browser
#     Button(frame2, text="Open Browser", command=open_browser).grid(row=0, column=2, columnspan=2, sticky='w')
#
#     # Create a DateEntry to select a date
#
#     frame2.grid(row=0, column=1, padx=10, pady=10)
#
#     frame3 = LabelFrame(tab1, text="Dates Setting", padx=10, pady=10)
#     # Create checkboxes for the days of the week
#     Label(frame3, text="Select a date: ").grid(row=0, column=0, sticky='w')
#
#     date_entry = DateEntry(frame3)
#     date_entry.grid(row=0, column=1, sticky='w')
#
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     day_vars = []
#     for i, day in enumerate(days):
#         var = IntVar()
#         day_vars.append(var)
#         Checkbutton(frame3, text=day, variable=var).grid(row=3, column=i, sticky='w')
#
#     # Create radio buttons for the options
#     option_var = StringVar()
#     option_var.set(options[0])  # Default option is the first one
#     for i, option in enumerate(options):
#         Radiobutton(frame3, text=option, variable=option_var, value=option).grid(row=4, column=i, sticky='w')
#
#     frame3.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
#
#     frame4 = LabelFrame(tab1, text="Actions", padx=10, pady=10)
#     # Create buttons for input and clean
#     Button(frame4, text="Input", command=input).grid(row=0, column=0, sticky='w', padx=10, pady=10)
#     Button(frame4, text="Clean", command=clean).grid(row=0, column=2, sticky='w', padx=10, pady=10)
#     Button(frame4, text="Fill Code", command=fillin).grid(row=0, column=1, sticky='w', padx=10, pady=10)
#
#     frame4.grid(row=2, column=0, padx=10, pady=10)
#
