#!/bin/bash
#add user
function add_user()
{
cat > user.txt << EOF
aaa
bbb
ccc
EOF

for user in `cat user.txt`
do
  id $user
  if [ $? != 0 ];then
	  useradd $user -M -s /sbin/nologin
	  cat /etc/sudoers|grep -v "\#$user"|grep "$user"
	  if [ `echo $?` != 0 ];then
		  echo "$user        ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers
	  fi
  fi
done

}
