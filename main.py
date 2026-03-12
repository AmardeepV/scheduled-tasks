import smtplib
import datetime as dt
import random
import pandas as pd
import os

password = os.environ.get("GMAIL_PYTHON_PASSWORD")
send_user_email = "amardeepverma03@gmail.com"

LETTER_FILES = ["letter_templates/letter_1.txt",
                "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]
BIRTHDAY_FILE = "birthdays.csv"

user_data = pd.read_csv(BIRTHDAY_FILE)
now = dt.datetime.now()
previous_day = None

current_day = now.day
current_month = now.month
message = random.choice(LETTER_FILES)
if current_day in user_data['day'].values and current_month in user_data['month'].values:
    if current_day != previous_day:
        names = user_data[user_data['day'] == current_day]['name']
        emails = user_data[user_data['day'] == current_day]['email']

        try:
            with open(message, 'r') as file:
                data = file.read()
        except FileNotFoundError:
            print("Letter template files does not exist")

        for pos, name in enumerate(names.values):
            email_content = data.replace("[NAME]", name)
            try:
                # setting up smtp gmail server
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()  # start secure stmp email connection
                    # login details of the sender
                    connection.login(user=send_user_email,
                                     password=password)
                    connection.sendmail(from_addr=send_user_email,
                                        to_addrs=emails.values[pos],
                                        msg=f"Subject:Happy Birthday!\n\n{email_content}")
            except:
                print("Check Username and Password")
            else:
                print(
                    f"Email sent to {name} whose email is: {emails.values[pos]}")
        previous_day = current_day
