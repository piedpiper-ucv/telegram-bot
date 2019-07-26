import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import urllib.request

def Send(email,password,_from,to,subject,body,url,name):
    fromaddr = email
    toaddr = to
    msg = MIMEMultipart()
    msg['From'] = _from
    msg['To'] = to
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'plain'))

    response =  urllib.request.urlopen(url)
    data = response.read()

    parte = MIMEBase('application', 'octet-stream')
    parte.set_payload(data)
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', "attachment;filename= %s" % name)
    msg.attach(parte)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    texto = msg.as_string()  

    try:
        server.sendmail(fromaddr, toaddr, texto)
    except smtplib.SMTPException:
        print ("El correo no pudo ser enviado" + "\n")
        server.close()
        return 'error'
 
    return 'ok'
    server.close()