#!/usr/bin/env python
#encoding:utf-8

#import module
import MySQLdb
import sys
import os
def main(host='localhost',port=3306,user='root',passwd='edge'):
        try:
                db_connect = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd)
        except Exception,e:
                print e
        cursor = db_connect.cursor()
        db_name = raw_input("input need create db name:")
        index_db = "show databases like \"%s\"" %db_name
        create_db = "create database %s" %db_name
        if cursor.execute('%s'%index_db):
                print "The database %s is exist" %db_name
        else:
                cursor.execute('%s'%create_db)
                print "create %s is auccess" %db_name
        sql_file = raw_input("please input you need import sql file:")
        if os.path.exists(sql_file):
                os.system("mysql -h %s -u %s -p%s -P %s %s < %s"%(host,user,passwd,port,db_name,sql_file))
                print "import sql file success"
        else:
                print "sql file is not found" %sql_file
if __name__ == "__main__":
        main()
