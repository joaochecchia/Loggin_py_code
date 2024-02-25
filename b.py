import smtplib
import email.message
from dotenv import load_dotenv
import os

def enviar_email(user_email, code):  
    corpo_email = f"""
    <p>Aqui está seu código de verificação {str(code)}.</p>
    <p>ele expira em 90 segundos.</p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Codigo de verificação"
    msg['From'] = f'{os.getenv("EMAIL")}'
    msg['To'] = f'{user_email}'
    password = f'{os.getenv("SENHA")}' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
