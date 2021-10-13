import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/RRD/'
imgpath = '/home/gonzalo/PycharmProjects/Practica2/Principal/IMG/'
fname = 'trend.rrd'

mailsender = "x19j28@gmail.com"
mailreceip = "x19j28@gmail.com"
# correo profesora: tanibet.escom@gmail.com
mailserver = 'smtp.gmail.com: 587'
password = 'Tiburoncin_5'
# subject = "Un asunto"
def send_alert_attached(subject,nombre): #Recibe el asunto y el nombre del archivo que va a enviar

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imgpath+nombre+".png", 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()