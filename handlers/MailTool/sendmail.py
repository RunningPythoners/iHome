# coding:utf-8
from tornado.web import RequestHandler
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging
import pdb

class SendMailHandler(RequestHandler):
    """send mail"""
    def post(self):
        json_req = self.request.body
        req = json.loads(json_req)
        """
        {
            recevier:
            subject:
            msg:
        }
        """
        recevier = req.get('recevier')
        subject = req.get('subject', 'ihome_subject')
        msg = req.get('msg', 'ihome_msg')
        # check params
        sender = 'ihome@ihome.com'
        receivers = [recevier,]# 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        logging.debug("****************")
        # pdb.set_trace()
        message = MIMEText(msg, 'plain', 'utf-8')
        # message['From'] = Header("bigjeffwang@sina.com", 'utf-8')
        # message['To'] =  Header("receiver_name", 'utf-8')
        # message['Subject'] = Header(subject, 'utf-8')
        message['From'] = "delron.kung@qq.com"
        message['To'] =  "receiver_name"
        message['Subject'] = subject
        try:
            mailClient = smtplib.SMTP_SSL()
            mailClient.connect('smtp.qq.com', 465)
            mailClient.login('delron.kung@qq.com', 'fuetnskqacerbgfh')
            mailClient.sendmail('delron.kung@qq.com', receivers, message.as_string())
        except Exception as e:
            logging.error(e)
            self.write('send mail failed')
            return
        self.write('send mail successed')





