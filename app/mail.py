from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import config
 
def enviar_mail(to_addr, token):
    """ Enviar Email Notification """
    msg = MIMEMultipart()

    message = """
    Para activar su cuenta haga client en el siguiente link:
    http://localhost:5000/v1/activate/{}
    """.format(token)

    msg['From'] = config.EMAIL_ACCOUNT
    msg['To'] = to_addr
    msg['Subject'] = "Subscription"

    msg.attach(MIMEText(message, 'plain'))


    server = smtplib.SMTP(
        config.EMAIL_SERVER,
        config.EMAIL_SERVER_PORT
    )
    
    server.starttls()

    server.login(config.EMAIL_ACCOUNT, config.EMAIL_ACCOUNT_PASSWORD)

    server.sendmail(
        config.EMAIL_ACCOUNT, 
        msg['To'], 
        msg.as_string()
    )

    server.quit()
