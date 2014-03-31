#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2014-03-24 17:30:08'
__licence__	= 'GPL licence'

from aomp.puppet_config.models import Node_config_message
from aomp.cmdb.models import Server_game_group
def puppet_global_url(request):
    all_gamegroup = Server_game_group.objects.all()
    all_puppetserver = Node_config_message.objects.all()
    context = {'all_gamegroup':all_gamegroup,'all_puppetserver':all_puppetserver}
    return context
