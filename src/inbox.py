import sys
import imaplib
import email
import email.header
import datetime

class MyIMAP4:
    #Se instancio la coneccion al puerto de gmail
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com',993)

server = MyIMAP4()


def process_mailbox(M,min,max):
    
    rv, data = M.search(None, "ALL") #Obtengo todos los correos de la carpeta seleccionada anteriormente
    if rv != 'OK':
        print("No messages found!")
        return
    len_unseen = data[0].split() #Separo los codigos de los correos en un arreglo de tamaño n (cantidad de correos)
    len_unseen.reverse() #Lo invierto para obtener los mas recientes de primero
    inboxlist = []
    infinbox= []
    
    if len(len_unseen) < max: #Reducir el for para cuando hay menos correos de los 10 iniciales
        max = len(len_unseen)
        min = 0

    for i in range(min,max):
        inboxlist.append(len_unseen[i]) #Pegar los 10 correos de la iteracion i

    for num in inboxlist:
        rv, data = M.fetch(num, '(RFC822)') #Retorna en formato texo con el "from" "subject" "date"
        if rv != 'OK':
            print("ERROR getting message", num)
            return
        #Declaro las variables de cada correo i a mostrar
        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        send = email.header.make_header(email.header.decode_header(msg['From']))
        #Volvi string para construir el cuadro de texto
        subject = str(hdr)
        sendby = str(send)
        info = 'From: '+ sendby + '\n\nSubject: '+ subject + '\n\nDate: ' + msg['Date']
        infinbox.append(info) #Uno los correos i en modo texto
    #Muestro el cuadro de texto con 10 correos
    return infinbox

def OpenInbox(min,max):
    
    rv, mailboxes = server.imap_server .list()#Seleccionar todas las carpetas
    if rv == 'OK':
        print("Mailboxes:")
    else:
        return 'ERROR'

    rv, data = server.imap_server .select('INBOX')#Selecciono los de la carpeta "inbox"
    if rv == 'OK':
        print("Processing mailbox...\n")
        inbox = process_mailbox(server.imap_server ,min,max)
        server.imap_server .close() #Se debe cerrar siempre
        return inbox 
        
    else:
        print("ERROR: Unable to open mailbox ", rv)
        return 'ERROR: Unable to open mailbox'


def Authenticator(emailAddress,password): #Verifico el email y clave del usuario
    print('entro al login')
    if server.imap_server.state == 'LOGOUT':
        server.imap_server = imaplib.IMAP4_SSL('imap.gmail.com',993)
        try:
            rv, data = server.imap_server.login(emailAddress,password)
            return 'ok'
        except imaplib.IMAP4.error:
            return 'error'
    else:
        try:
            rv, data = server.imap_server.login(emailAddress,password)
            return 'ok'
            
        except imaplib.IMAP4.error:
            return 'error'

def Logout():
    print ("LOGOUT!!! ")
    server.imap_server.logout()
    
    

