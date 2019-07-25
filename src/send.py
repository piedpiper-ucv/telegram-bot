
import smtplib, socket, sys, getpass
 
smtpserver = smtplib.SMTP("smtp.gmail.com", 587)

def Send(emailAddress,password,From,To,Subject,Body):
 
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
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
        To = To.split(',')

    try:
        smtpserver.sendmail(From, To, msg)
    except smtplib.SMTPException:
        print ("El correo no pudo ser enviado" + "\n")
        smtpserver.close()
        return 'error'
 
    return 'ok'
    smtpserver.close()
    