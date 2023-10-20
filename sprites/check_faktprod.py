import os
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta

environment = "test"

try:
    environment = sys.argv[1]
except:
    environment = "test"

today = datetime.strftime(datetime.now(), "%Y-%m")
yesterday = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m")

logfile_path = f"//fil.{environment}.kredinor.int/131802{environment}$/FS/prod/temp/faktprod-{today}.log"
position_file_path = f"D:/Prog/fslogcheck/position-{environment}.txt"


def get_last_position():
    # Check if the position file exists
    if os.path.exists(position_file_path):
        with open(position_file_path, "r") as position_file:
            content = position_file.read().strip()

            if content == "" or today != yesterday:
                last_position = 0
                print(f"No content or {today} is not equal to {yesterday} last postition: {last_position}")
                return last_position
            else:
                last_position = int(content)
                print(f"last postition: {last_position}")
                return last_position
    else:
        return 0


def update_last_position(position):
    with open(position_file_path, "w") as position_file:
        # Write the current position to the file
        position_file.write(str(position))
        print("position")
        print(position)


def monitor_logfile():
    last_position = get_last_position()

    with open(logfile_path, "r") as logfile:
        # Move the file pointer to the last position
        logfile.seek(last_position)
        # Read new lines from the file
        new_lines = logfile.readlines()
        email_sender = "sjekk.logg@kredinor.no"
        email_receiver = ["jens.hordvik@kredinor.no", "geir.hoydahl@kredinor.no","froydis.stillingen@kredinor.no"]

        subject = f"Feilmelding i faktprod-logg ({environment.upper()})"

        body = []
        str_body = ""

        # Check for error messages
        for line in new_lines:
            if "**" in line or "err" in line.lower() or "ikke" in line.lower():
                body.append(line)
                str_body = "\n".join(body)

        if str_body != "":
            em = EmailMessage()

            em["From"] = email_sender
            em["To"] = email_receiver
            em["Subject"] = subject
            em.set_content(str_body)

            with smtplib.SMTP("relay.telecomputing.no") as smtp:
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                smtp.quit()

        # Update the last position
        last_position = logfile.tell()  # Returns the current file position
        update_last_position(last_position)


# Run the monitor function
monitor_logfile()
