#/usr/bin/python
#encoding=utf-8

import time
import MySQLdb
import smtplib
from email.mime.text import MIMEText
 
to_list = ['yunwei@aomp.com', 'chanpinguanli@aomp.com']

this_year = time.strftime("%Y", time.localtime(time.time()))
this_month = time.strftime("%m", time.localtime(time.time()))
this_day = time.strftime("%d", time.localtime(time.time()))
year_month = this_year + u'年' + str(int(this_month)) + u'月'
month_day = str(int(this_month)) + u'月' + str(int(this_day)) + u'日'

pre_info = u"<style>p{padding-left:1em;}h3{height:1em;padding-left:1em;}</style>各位好，" + month_day + u'的工作日报：<br>'
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='aomp',db='aomp',port=3600,charset='utf8')
    cur=conn.cursor()
    count = cur.execute('select * from days_table where months=\''+year_month+'\' and days=\''+month_day+'\'')
    result = cur.fetchall();
    content = ''
    for r in result:
        content += "<h3>" + r[3] + '</h3>' + r[6]
    if content:
        content = pre_info + content
        to = ','.join(to_list)
        mail_host="mail.aomp.com"
        mail_user="zhibanyw"
        mail_pass="123456"
        mail_postfix="aomp.com"
        me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content,'html','utf-8')
        msg['Subject'] = u'胡莱游戏-运维部-资讯日报-' + month_day
        msg['From'] = me
        msg['To'] = to
        try:
            s = smtplib.SMTP()
            s.connect(mail_host)
            s.login(mail_user,mail_pass)
            s.sendmail(me, to_list, msg.as_string())
            s.close()
        except Exception, e:
            print str(e)
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


