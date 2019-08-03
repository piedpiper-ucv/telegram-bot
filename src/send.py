
import smtplib, socket
 
smtpserver = smtplib.SMTP("smtp.gmail.com", 587) #Protocolo para mandar correos

def Send(emailAddress,password,From,To,Subject,Body):
 
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo() #Habilitar en caso de necesitar la version extendida de smtp
        smtpserver.starttls() #Inicia el protocolo de encriptacion
        smtpserver.ehlo()
        print ("Conexion exitosa con Gmail")
        print ("Concectado a Gmail")

        try:
            smtpserver.login(emailAddress,password)
        except smtplib.SMTPException:
            print ("")
            print ("Autenticacion incorrecta" + "\n")
            smtpserver.close()
 
 
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException):
        print ("Fallo en la conexion con Gmail")
        return 'error'
 
 
    
    
    header = "From: "+ From +"\n" + "To: "+ To + "\n" + "Subject: " + Subject + "\n"
    msg = header + "\n" + Body + "\n\n"
    print (msg)
    if To.find(',') != -1:
        To = To.split(',') #Corta en la coma con n cantidad de correos en un arreglo

    try:
        smtpserver.sendmail(From, To, msg)
    except smtplib.SMTPException:
        print ("El correo no pudo ser enviado" + "\n")
        smtpserver.close()
        return 'error'
 
    return 'ok'
    smtpserver.close()
    