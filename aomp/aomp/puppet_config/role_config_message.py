#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2014-03-23 17:52:07'
__licence__	= 'GPL licence'

#import module
from items_role_include_modules import items_roles_modules

def test1_node_config(node_name,private_ip,public_ip,items_name,group_name):
    global content
    module_temp = ''
    if items_name in items_roles_modules:
        value = items_roles_modules[items_name]
        if group_name in value:
            module_list = value[group_name]
            for module in module_list:
                module_temp += "    include %s\n" %module
    content = '''
node '%s' {
    $self_public_ip = '%s'
    $self_private_ip = '%s'
    $cluster_name = '%s'
    $inner_dns = '123.125.104.88'
%s
    }
'''%(node_name,private_ip,public_ip,node_name,module_temp)
    return content
