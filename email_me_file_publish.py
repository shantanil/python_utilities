#!/usr/bin/python
################################################################################
#
#    This application sends out  the file as attachment email to the recipient
#    
#   
#    Dated: 18-sep-2019 : Sunny Chakraborty
#    Run:
#    python email_me_file.py --send-file mytext.txt --recipient mypasssunny@gmail.com
#
#
#
#
################################################################################

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import argparse
import os.path


class ScriptAbort(Exception):


def abort(err_msg, emit_fail=True):
    if emit_fail is True:
        print "FAILED"
    print >> sys.stderr, err_msg
    raise ScriptAbort

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--send-file', type=str, default=None, help='File name if same dir or path with file name if it has to be emailed ')
    parser.add_argument('--recipient', type=str, default=None, help=' email of the recipient')
    return parser.parse_args()

def validate_response(res, err_msg, is_abort=False):
    if not res.success:
        if is_abort:
            abort(err_msg, emit_fail=False)
        print err_msg
        return False
    return True

def main():

    args = get_args()
    myfile=args.send_file
    email=args.recipient

    if not args.send_file:
        abort('--send-file is required.\nNote: Indicate the full path to the attachment file ', emit_fail=False)

    if not args.recipient:
        abort('--recipient email ID is required.\nNote: Indicate one email id ', emit_fail=False)

    if os.path.exists(myfile):
      process(myfile,email);

    else:
      print ("File {} do not exists -Aborting".format(myfile))
#    print ("Email sent -Done !")



def process(f,e):

  email='mysmtpserver@gmail.com'
  password='mypass'
  send_to_email=e

  myfile=f
  #myfile="uwsgi_07.log"

  msg=MIMEMultipart()
  subject='File {} attached'.format(f)
  body = "Attached is the sent file"
  msg['From']=email
  msg['To']=send_to_email
  msg['Subject']=subject
  msg.attach(MIMEText(body, 'plain'))

  attachment = open(myfile, "rb")
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition','attachment',filename=myfile)
  msg.attach(part)

  server=smtplib.SMTP('smtp.gmail.com',587)
  server.starttls()
  server.login(email, password)
  text=msg.as_string()
  server.sendmail(email,send_to_email, text)
  server.quit()
  print ("Email send -Done!")



if __name__ == '__main__':
    sys.exit(main())


