import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import logging

logger = logging.getLogger('emailer')
logger.setLevel(logging.DEBUG)

# MAIL_SERVER = 'smtp.163.com'
# MAIL_SENDER = 'im22ic@163.com'
# MAIL_SENDER_PASSWORD = 'wy123456'

MAIL_SERVER = 'smtp.qq.com'
MAIL_SENDER = 'bbxxone@qq.com'
MAIL_SENDER_PASSWORD = 'crykrvctngpfhafh'

receivers = ['zhaojinhui@nsfocus.com', 'im22ic@163.com', 'redfoxatasleep@gmail.com']
html_template = '''
html = """
<html>  
  <body>  
    <p> 
       Here is the <a href="{link}">link</a> you wanted.
    </p> 
  </body>  
</html>  
"""    
'''

f = open('/Users/zhaojinhui/github/demz/someapp/templates/mail_template_simple_00.html', 'r')
html_template = f.read()
html = html_template.format(**{
    'button_link': 'https://www.runoob.com/python3/python3-smtp.html',
    'button_text': 'download',
    'p1': 'Hi, guy!',
    'p2': 'Thanks for downloading VT samples. Click the button below to download you samples.',
    'p3': '',
    'p4': '',
})

# message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message = MIMEText(html, 'html', 'utf-8')
message['From'] = formataddr(("RedFoxAtAsleep".upper(), "MAIL@RedFoxAtAsleep.COM".upper()))     # 发送者
message['To'] = formataddr(("SOMEone".upper(), "MAIL@Someone.COM".upper()))          # 接收者
message['Subject'] = "Python3 SMTP 邮件测试"
smtpObj = smtplib.SMTP()

try:
    # with smtplib.SMTP() as smtpObj: pass
    smtpObj.connect(MAIL_SERVER)
    smtpObj.login(MAIL_SENDER, MAIL_SENDER_PASSWORD)
    smtpObj.sendmail(MAIL_SENDER, receivers, message.as_string())
    smtpObj.quit()
    logger.info("邮件发送成功")
except smtplib.SMTPException as e:
    logger.info("Error: 无法发送邮件")

