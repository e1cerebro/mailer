import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sender   = 'nwachukwu.uchenna.christian@outlook.com'
password = "Heaven111"
to="nwachukwu16@gmail.com"

subject = "the subject"

msg = MIMEMultipart()
msg['From']=sender
msg['To']=to
msg['subject'] = subject


# Add this section if you want to send attachment
filename = 'abc.txt'

attachment = open(filename, 'rb')
part = MIMEBase('application/html', 'octat-stream')
part.set_payload(attachment.read())

encoders.encode_base64(part)

part.add_header('Content-Disposition', "attachment_file; filename ="+filename)
msg.attach(part)
# End of the attachment part


body =  """
This is an e-mail message to be sent in HTML format
<p style=\"color:red\"> This is a paragraph</p>
<b>This is HTML message.</b>
<h1>This is headline.</h1>
"""

msg.attach(MIMEText(body, 'html'))

content = msg.as_string()
server = smtplib.SMTP('smtp-mail.outlook.com:587')

server.starttls()

server.login(sender, password)

try:
   #server.sendmail(sender, to, content)
   print ("Successfully sent email")
except smtplib.SMTPException:
   print ("Error: unable to send email")

server.quit()




def split_email(email_str):
   emails = email_str

   email_list = emails.split(";")
   for email in email_list:
      email_first_part = email.strip()
      print(email_first_part)
      print(get_username(email_first_part))
   return email_list


def get_username(email_add):
   email_user = email_add.split("@")
   email_user = email_user[0]

   if email_user.find("_") != -1:
      return max(email_user.split("_"), key=len)
   elif email_user.find(".") != -1:
      return max(email_user.split("."), key=len)
   else:
      return email_user


def prep_message(message, to_email, to_username):
    # replace the email tag
    prep_msg = message.replace("[email]", to_email, 6)
    # replace the username tag
    prep_msg = prep_msg.replace("[user]", to_username, 6)
    return prep_msg


print(prep_message("Hi [email], how are you doing. Can you call [user] with your phone"))
#split_email('nwachukwu16@gmail.com;tech.nwachukwu16@gmail.com;christianoronaldo_uchenna_nwachukwu16@gmail.com')

