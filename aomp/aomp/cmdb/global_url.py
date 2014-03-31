#!/usr/bin/python
# encoding: utf-8
__authors__	= ['left']
__version__	= 1.0
__date__	= '2013-11-14 08:55:13'
__licence__	= 'GPL licence'

from aomp.cmdb.models import Game_name_all,IDC_name_all,Server_type_all,Game_type_name,Server_game_group
def global_url(request):
    all_idc = IDC_name_all.objects.all()
    all_gamename = Game_name_all.objects.all()
    all_servertype = Server_type_all.objects.all()
    all_gametype = Game_type_name.objects.all()
    context = {'all_idc':all_idc,'all_gametype':all_gametype,'all_gamename':all_gamename,'all_servertype':all_servertype}
    return context
