if [[ ( $DESKTOP_SESSION == "/usr/share/xsessions/xfce" ) || ( $DESKTOP_SESSION == "/usr/share/xsessions/mate" ) || ( $DESKTOP_SESSION == "/usr/share/xsessions/budgie-desktop" ) || ( $DESKTOP_SESSION == "/usr/share/xsessions/cinnamon" ) || ( $DESKTOP_SESSION == "/usr/share/xsessions/lxqt" ) || ( $DESKTOP_SESSION == "/usr/share/xsessions/openbox" ) ]]
then
   . /home/mohsen/.conky/conky-startup.sh
fi
exit
