#!/usr/bin/env python

#import module
import os
import md5

file_md5_dict = {}
delete_file_list=[]

def get_file_md5(file):
    f = open(file).read()
    f_md5 = md5.new(f).hexdigest()
    return f_md5

def delete_same_file(root_dir,file_list):
    for file_name in file_list:
        full_dir_file = root_dir+"/"+file_name
        f_md5 = get_file_md5(full_dir_file)
        if f_md5 in file_md5_dict:
            delete_file_list.append(full_dir_file)
        else:
            file_md5_dict[f_md5] = full_dir_file
    return delete_file_list

def main(dir,only=0):
    if not os.path.exists(dir):
        pass
    else:
        dir_len = len(dir.split("/"))
        for root,f_dir,f_name in os.walk(dir):
            if only >= 0:
                if len(root.split("/")) - dir_len <= only:
                    if len(f_name) == 0:
                        print "This dir %s not have file." %root
                    else:
                        delete_same_file(root,f_name)
                        print "The delete file list %s" %delete_file_list
                        for f in delete_file_list:
                        	os.remove(f)
				print "delete file %s is success" %f
                else:
                    continue


dir = '/data/test'
main(dir,0)
