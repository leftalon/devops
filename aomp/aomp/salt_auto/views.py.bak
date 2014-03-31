# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from salt_command import Query_salt_client
def test(request):
    result = {}
    arg_dict = {}
    saltid = "Local"
    hostmsg = "*"
    arg1 = "test.ping"
    arg2 = ''
    if request.method == "POST":
        saltid = request.POST.get("saltid")
        hostmsg = request.POST.get("hostmsg")
        arg1 = request.POST.get("arg1")
        arg2 = request.POST.get("arg2",'')
	arg_dict["saltid"] = saltid
	arg_dict["hostmsg"] = hostmsg
	arg_dict["arg1"] = arg1
	arg_dict["arg2"] = arg2
	result = Query_salt_client(arg_dict)
    print arg2
    return render_to_response("saltproject/frist_page.html",{'result':result,'saltid':saltid,'hostmsg':hostmsg,'arg1':arg1,'arg2':arg2},context_instance=RequestContext(request))
