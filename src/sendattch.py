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
    msg = MIMEMultipart() #Crea un contenedor de mensajes para correo
    msg['From'] = _from
    msg['To'] = to
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'plain')) #Definir el attach para texto plano

    response =  urllib.request.urlopen(url) #Url que retorna telegram donde monta el adjunto
    data = response.read() #Obtiene toda la data del adjunto

    parte = MIMEBase('application', 'octet-stream') #Define el attach para archivos 'base 64'
    parte.set_payload(data) #
    encoders.encode_base64(parte) #Codifica a base64 el adjunto
    parte.add_header('Content-Disposition', "attachment;filename= %s" % name) #Definir al decodificar de correo el contenido del attachment
    msg.attach(parte) #Anexa el archivo al mensaje a enviar

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    texto = msg.as_string()  #Convierte todo lo anterior en "texto" 

    try:
        server.sendmail(fromaddr, toaddr, texto)
    except smtplib.SMTPException:
        print ("El correo no pudo ser enviado" + "\n")
        server.close()
        return 'error'
 
    return 'ok'
    server.close()