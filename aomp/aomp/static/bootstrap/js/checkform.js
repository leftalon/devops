



function check_form(thisform) {
    var formlist = document.getElementById(thisform.id);
    if (thisform.id == 'add_server' || thisform.id == 'edit_server') {
         if(document.getElementById("inputserver_id").value.split('.').length != 2) {
             alert("服务器唯一标示不正确,正确格式为:game.s3");
             return false;
         }
             
         if(document.getElementById("inputserver_in_ip").value == '' && document.getElementById("inputserver_out_ip").value == '') {
             alert("内网IP和外网IP至少存在一个,请添加");
             return false;
         }
         var re = /^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)(:\d{1,})?$/g;
         if(document.getElementById("inputserver_in_ip").value != '') {
             if(!re.test(document.getElementById("inputserver_in_ip").value)) {
                 alert("内网IP地址非法,请检查");
                 return false;
             }
         }
         if(document.getElementById("inputserver_out_ip").value != '') {
             if(!re.test(document.getElementById("inputserver_out_ip").value)) {
                 alert("外网IP地址非法,请检查");
                 return false;
             }
         }
         var re = new RegExp("(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)");
         if(document.getElementById("server_start_date").value != "") {
             var start_date = document.getElementById("server_start_date").value;
             var d = start_date.split('-');
             if(start_date.length != 10 || !re.test(start_date) || d.length != 3 || d[0].length != 4 || d[1].length != 2 || d[2].length != 2) { 
                 alert("开始时间不正确,请重新填写");
                 document.getElementById("server_start_date").value = "";
                 return false;
             }
          }
          if (thisform.id == 'edit_server') {
              if(document.getElementById("server_end_date").value != "") {
                  var end_date = document.getElementById("server_end_date").value;
                  var d = end_date.split('-');
                  if(end_date.length != 10 || !re.test(end_date) || d.length != 3 || d[0].length != 4 || d[1].length != 2 || d[2].length != 2) {       
                      alert("开始时间不正确,请重新填写");
                      document.getElementById("server_end_date").value = "";
                      return false;
                  }
              }
          }
     }   
     return true;
}
