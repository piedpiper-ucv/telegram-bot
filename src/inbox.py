import sys
import imaplib
import email
import email.header
import datetime

M = imaplib.IMAP4_SSL('imap.gmail.com',993)

class MyIMAP4:
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com',993)

server = MyIMAP4()


def process_mailbox(M,min,max):

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return
    len_unseen = data[0].split()
    len_unseen.reverse()
    inboxlist = []
    infinbox= []
    
    if len(len_unseen) < max:
        max = len(len_unseen)
        min = 0

    for i in range(min,max):
        inboxlist.append(len_unseen[i])

    for num in inboxlist:
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        send = email.header.make_header(email.header.decode_header(msg['From']))
        subject = str(hdr)
        sendby = str(send)
        info = 'From: '+ sendby + '\n\nSubject: '+ subject + '\n\nDate: ' + msg['Date']
        infinbox.append(info)

    return infinbox

def OpenInbox(min,max):
    
    rv, mailboxes = server.imap_server .list()
    if rv == 'OK':
        print("Mailboxes:")
    else:
        return 'ERROR'

    rv, data = server.imap_server .select('INBOX')
    if rv == 'OK':
        print("Processing mailbox...\n")
        inbox = process_mailbox(server.imap_server ,min,max)
        server.imap_server .close()
        return inbox 
        
    else:
        print("ERROR: Unable to open mailbox ", rv)
        return 'ERROR: Unable to open mailbox'


def Authenticator(emailAddress,password):
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
    
    

