import pandas as pd
import datetime as dt
import smtplib
import random

MY_EMAIL = "sender_email"
PASSWORD = "sender_password"
birthdays = pd.read_csv("birthdays.csv")


today = (dt.datetime.now().month, dt.datetime.now().day)

birthdays_dict = {(row.month, row.day): row for (index, row) in birthdays.iterrows()}

if today in birthdays_dict:
    with open(f"letter_templates/letter_{random.randint(1, 3)}.txt") as letter:
        letter_content = letter.readlines()
        letter_content[0] = letter_content[0].replace("[NAME]", birthdays_dict[today]["name"])

    with open(f"ReadyToSend/letter_for_{birthdays_dict[today]["name"]}.txt", mode="w") as birthday_card:
        for line in letter_content:
            birthday_card.write(line)

    with open(f"ReadyToSend/letter_for_{birthdays_dict[today]["name"]}.txt") as to_send:
        message = to_send.read()
        print(message)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthdays_dict[today]["email"],
            msg=f"Subject: subject\n\n{message}"
        )
