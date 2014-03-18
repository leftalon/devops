#!/usr/bin/python
# encoding: utf-8
__authors__ = ['left']
__version__ = 1.0
__date__    = '2014-03-18 10:28:40'
__licence__ = 'GPL licence'

#import modules
import salt.client

def Query_salt_client(args):
    global result
    result = {}
    if args.get("saltid"):
        salt_frist_arg = args["saltid"]
        if salt_frist_arg == "Local":
            salt_frist_arg = salt.client.LocalClient()
            hostmsg = args["hostmsg"]
            arg1 = args["arg1"]
	    if args["arg2"].strip():
            	arg2 = list(args["arg2"].strip().split(","))
                result = salt_frist_arg.cmd(hostmsg,arg1,arg2)
	    else:
		result = salt_frist_arg.cmd(hostmsg,arg1)
    return result

