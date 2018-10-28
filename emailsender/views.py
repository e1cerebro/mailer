from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import time

# Create your views here.
def index(request):

    if request.method == "POST":
        status = email_sender(request.POST.get('to',''), request.POST.get('subject',''), request.POST.get('message', ''), request.POST.get('usernames', ''), request.POST.get('passwords', ''))

        print(request.POST.get('to',''), request.POST.get('subject',''), request.POST.get('message',''))
        return render(request, "index.html", {'status': status, 'to':request.POST.get('to',''), 'subject': request.POST.get('subject',''),'message': request.POST.get('message',''), "usernames": request.POST.get('usernames', ''), "passwords": request.POST.get('passwords', '') })
    else:
        return render(request, "index.html", {})


def email_sender(mail_to, email_subject, message, usernames, passwords):

    auth_emails = split_email(usernames)
    auth_passwords = split_email(passwords)
    rand_length = len(auth_emails) - 1

    # Start the loop here:
    status = ''
    count = 1
    for email_single in split_email(mail_to):

        try:
            key = random.randint(0, rand_length)

            print("Username: ", auth_emails[key])
            print("Password: ", auth_passwords[key])
            print("To: ", email_single)
            s_domain = auth_emails[key]
            parts = s_domain.split("@")
            sender = auth_emails[key]
            password = auth_passwords[key]

            user_name = get_username(email_single)
            # print("Email: ", email_single)
            # print("Username: ", user_name)
            # print("Message: ", prep_message(message, email_single, user_name))

            to = email_single
            subject = email_subject

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = to
            msg['subject'] = subject

            body = prep_message(message, email_single, user_name)

            msg.attach(MIMEText(body, 'html'))

            content = msg.as_string()

            if parts[1] != 'gmail.com':

                server = smtplib.SMTP('smtp-mail.outlook.com:587')
            else:
                server = smtplib.SMTP('smtp.gmail.com:587')

            server.starttls()

            server.login(sender, password)
            server.sendmail(sender, to, content)

            print("count: ", count)
            count += 1
            status += "\n Successfully sent email "+to
            print("\n Successfully sent email "+to)
            server.quit()
            time.sleep(10)
        except smtplib.SMTPException as e:
            print("Error: unable to send email")
            print(str(e))
            status = "\n There was a problem sending your email to "+to

    return status


def split_email(email_str):
    email_list = email_str.split(",")
    return email_list


def get_username(email_add):
    email_user = email_add.split("@")
    email_user = email_user[0]

    if email_user.find("_") != -1:
        username = max(email_user.split("_"), key=len)
    elif email_user.find(".") != -1:
        username = max(email_user.split("."), key=len)
    else:
        username = email_user

    final_username = ''.join([i for i in username if not i.isdigit()])

    return final_username.capitalize()


def prep_message(message, to_email, to_username):
    # replace the email tag
    prep_msg = message.replace("[email]", to_email, 6)
    # replace the username tag
    prep_msg = prep_msg.replace("[user]", to_username, 6)
    return prep_msg








