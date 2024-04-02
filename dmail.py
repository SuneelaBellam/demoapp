import smtplib
from email.message import EmailMessage

def sendmail(to,subject,body):
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('bellamsuneela76@gmail.com','gtjb ahwd ecgo sfjr')
    msg = EmailMessage()
    msg['From']='bellamsuneela76@gmail.com'
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)
    server.send_message(msg)
    server.quit()


sendmail('gunjaanuradha02@gmail.com','hi this is suni','have u finish u r dinner,take care')
print('mail sended')
