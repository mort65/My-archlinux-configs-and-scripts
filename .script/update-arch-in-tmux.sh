#!/bin/bash

#this script check for archlinux news and if no news found update the system

Args=$@
USERNAME=${SUDO_USER:-$(id -u -n)}
HOMEDIR="/home/$USERNAME"
SUDO=""
if [ $EUID -ne 0 ]; then
    SUDO='/usr/bin/sudo'
fi

# Colors
blue="\033[1;34m"
green="\033[1;32m"
red="\033[1;31m"
bold="\033[1;37m"
reset="\033[0m"

programname="tupdatesystem"
RSSFILE="$HOMEDIR/.archnews"
TMPFILE="$HOMEDIR/.archnewstmp"
Build=""
Install=""
Mirror=""
Refresh=""
AUR=""
Help=""
Sync=""
LoggingOff=""
RSSOff=""
PacOff=""

function usage {
    echo "Usage: $programname [OPTION]"
    echo "A script for updating archlinux"
    echo ""
    echo "  -a, --aur     Refresh and synchronize all normal and aur package databases"
    echo "  -s, --sync    Refresh and synchronize normal package databases"
    echo "  -y, --refresh Force the refresh of all package databases" 
    echo "  -r  --norss   Disable checking for archlinux news" 
    echo "  -p, --nopac   Disable checking for pacnew files" 
    echo "  -i, --install Install a package"
    echo "  -b, --build   Build a package"
    echo "  -l  --nolog   Disable logging"
    echo "  -m, --mirror  Update mirrors"
    echo "  -h, --help    Display help"
    echo ""
    read -p "Press enter to exit..."
    exit 1
}

#testing number of args:
if [ "${#}" -gt 9 ]; then
    echo -e $red"Error:$reset Invalid number of parameters"
    echo ""
    usage
elif [ "${#}" -eq 0 ]; then
    usage
fi

# Test command-line arguments.
if [ -n "$1" ]; then #non-empty
  while [ "$1" != "" ]; do
    PARAM="$1"
    if [[  $PARAM =~ ^--[Ii][Nn][Ss][Tt][Aa][Ll][Ll]$ ]] || [[ $PARAM =~ ^-[Ii]$ ]]; then
	  if [[ $Install == "" ]]; then
        Install="Yes"
	  else
	    echo -e $red"Error:$reset Invalid arguments '${Args}'"
	    echo ""
	    usage
	  fi
    elif [[ $PARAM =~ ^--[Bb][Uu][Ii][Ll][Dd]$ ]] || [[ $PARAM =~ ^-[Bb]$ ]]; then
      if [[ $Build == "" ]]; then
        Build="Yes"
	  else
        echo -e $red"Error:$reset Invalid arguments '${Args}'"
        echo ""
		usage
	  fi 
    elif [[ $PARAM =~ ^--[Mm][Ii][Rr][Rr][Oo][Rr]$ ]] || [[ $PARAM =~ ^-[Mm]$ ]]; then
	  if [[ $Mirror == "" ]]; then
        Mirror="Yes"
	  else
		echo -e $red"Error:$reset Invalid arguments '${Args}'"
		echo ""
		usage
	  fi
    elif [[ $PARAM =~ ^--[Rr][Ee][Ff][Rr][Ee][Ss][Hh]$ ]] || [[ $PARAM =~ ^-[Yy]$ ]]; then
	  if [[ $Refresh == "" ]]; then
        Refresh="Yes"
	  else
		echo -e $red"Error:$reset Invalid arguments '${Args}'"
		echo ""
		usage
	  fi
    elif [[ $PARAM =~ ^--[Aa][Uu][Rr]$ ]] || [[ $PARAM =~ ^-[Aa]$ ]]; then
	  if [[ $AUR == "" ]]; then
        AUR="Yes"
	  else
		echo -e $red"Error:$reset Invalid arguments '${Args}'"
		echo ""
		usage
	  fi
    elif [[ $PARAM =~ ^--[Hh][Ee][Ll][Pp]$ ]] || [[ $PARAM =~ ^-[Hh]$ ]]; then
      if [[ $Help == "" ]]; then
        Help="Yes"
	  else
        echo -e $red"Error:$reset Invalid arguments '${Args}'"
        echo ""
		usage
	  fi
	elif [[ $PARAM =~ ^--[Ss][Yy][Nn][Cc]$ ]] || [[ $PARAM =~ ^-[Ss]$ ]]; then
      if [[ $Sync == "" ]]; then
        Sync="Yes"
	  else
        echo -e $red"Error:$reset Invalid arguments '${Args}'"
        echo ""
		usage
	  fi
	elif [[ $PARAM =~ ^--[Nn][Oo][Ll][Oo][Gg]$ ]] || [[ $PARAM =~ ^-[Ll]$ ]]; then
      if [[ $LoggingOff == "" ]]; then
        LoggingOff="Yes"
	  else
        echo -e $red"Error:$reset Invalid arguments '${Args}'"
        echo ""
		usage
	  fi
	elif [[ $PARAM =~ ^--[Nn][Oo][Rr][Ss][Ss]$ ]] || [[ $PARAM =~ ^-[Rr]$ ]]; then
      if [[ $RSSOff == "" ]]; then
        RSSOff="Yes"
      else
        echo -e $red"Error:$reset Invalid arguments '${Args}'"
        echo ""
        usage
	  fi
    elif [[ $PARAM =~ ^--[Nn][Oo][Pp][Aa][Cc]$ ]] || [[ $PARAM =~ ^-[Pp]$ ]]; then
      if [[ $PacOff == "" ]]; then
        PacOff="Yes"
	  else
        echo -e $red"Error:$reset Invalid arguments '${Args}'"
        echo ""
		usage
	  fi  
    elif [[ $PARAM =~ ^-[AaBbIiLlMmPpRrSsYy][AaBbIiLlMmPpRrSsYy][AaBbIiLlMmPpRrSsYy]?[AaBbIiLlMmPpRrSsYy]?[AaBbIiLlMmPpRrSsYy]?[AaBbIiLlMmPpRrSsYy]?[AaBbIiLlMmPpRrSsYy]?[AaBbIiLlMmPpRrSsYy]?[AaBbIiLlMmPpRrSsYy]?$ ]]; then
	  i=1
	  while (( i++ < ${#PARAM} ))
	  do
   		char=$(expr substr "$PARAM" $i 1)
   		if [[ $char =~ [Mm] ]]; then
			if [[ $Mirror == "" ]]; then
				Mirror="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
                echo ""
		        usage
			fi
   		elif [[ $char =~ [Ii] ]]; then
			if [[ $Install == "" ]]; then
				Install="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
                echo ""
		        usage
			fi
		elif [[ $char =~ [Bb] ]]; then
			if [[ $Build == "" ]]; then
				Build="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
				echo ""
				usage
			fi		
        elif [[ $char =~ [Yy] ]]; then
			if [[ $Refresh == "" ]]; then
				Refresh="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
                echo ""
		        usage
			fi
        elif [[ $char =~ [Aa] ]]; then
			if [[ $AUR == "" ]]; then
				AUR="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
                echo ""
		        usage
			fi
		elif [[ $char =~ [Ss] ]]; then
			if [[ $Sync == "" ]]; then
				Sync="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
				echo ""
				usage
			fi
		elif [[ $char =~ [Ll] ]]; then
			if [[ $LoggingOff == "" ]]; then
				LoggingOff="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
				echo ""
				usage
			fi
		elif [[ $char =~ [Rr] ]]; then
			if [[ $RSSOff == "" ]]; then
				RSSOff="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
				echo ""
				usage
			fi
		elif [[ $char =~ [Pp] ]]; then
			if [[ $PacOff == "" ]]; then
				PacOff="Yes"
			else
				echo -e $red"Error:$reset Invalid arguments '${Args}'"
				echo ""
				usage
			fi		
		else
			echo -e $red"Error:$reset Invalid argument '$PARAM'"
            echo ""
            usage
		fi
	  done
    else
      echo -e $red"Error:$reset Invalid argument '$PARAM'"
      echo ""
      usage
    fi
    shift
  done
fi

if [[ $Help == "Yes" ]]; then
	usage
fi

if [[ $AUR == "Yes" ]]; then
    Sync="Yes"
fi

if [[ $Install == "" ]]; then
	Install="No"
fi

if [[ $Build == "" ]]; then
	Build="No"
fi

if [[ $Mirror == "" ]]; then
	Mirror="No"
fi

if [[ $Refresh == "" ]]; then
	Refresh="No"
fi

if [[ $AUR == "" ]]; then
	AUR="No"
fi

if [[ $Sync == "" ]]; then
	Sync="No"
fi

if [[ $LoggingOff == "" ]]; then
	LoggingOff="No"
fi

if [[ $RSSOff == "" ]]; then
	RSSOff="No"
fi

if [[ $PacOff == "" ]]; then
	PacOff="No"
fi

if [[ $Refresh == "Yes" ]] && [[ $Sync == "No" ]] && [[ $AUR == "No" ]]; then
    usage
fi

if [[ $Build == "No" ]] && [[ $Install == "No" ]] && [[ $Mirror == "No" ]] && [[ $AUR == "No" ]] && [[ $Sync == "No" ]]; then
    usage
fi

if [[ $PacOff == "No" ]]; then
    echo
    echo -e $blue"===>$reset Checking for pacnew files..."
    echo
    if [[ $($SUDO find /etc -regextype posix-extended -regex ".+\.pac(new|save)" 2> /dev/null) ]]; then
        echo -e $red"Error:$reset Pacnew file(s) found! (Use pacdiff to deal with them):"
        echo
        $SUDO find /etc -regextype posix-extended -regex ".+\.pac(new|save)" 2> /dev/null
        echo
        read -p "Press enter to exit..."
        exit 1
    else
        echo 
        echo "No pacnew file found"
    fi
    echo
    echo
fi
if [[ $RSSOff == "No" ]]; then
    [ -f $RSSFILE ] && cat "${RSSFILE}" 2> /dev/null
    /usr/bin/rm -f "${TMPFILE}"
    echo
    echo -e $blue"===>$reset Checking for unread arch linux news..."
    echo
    echo
    echo
    #tac reverses the output
    { /usr/bin/rsstail -n 5 -1 -u https://www.archlinux.org/feeds/news/ | /usr/bin/tac > "${TMPFILE}" ; } || { echo -e $red"Error:$reset Cannot download the rss content" ; read -p "Press enter to exit..." ; exit 1; }
    [[ -s "${TMPFILE}" ]] || { echo -e $red"Error:$reset Cannot download the rss content" ; read -p "Press enter to exit..." ; exit 1; }
    if [ -f $RSSFILE ]; then
        if /usr/bin/cmp -s "$RSSFILE" "$TMPFILE"; then
            rm -f "${TMPFILE}"
            echo "No new rss entry found"
            echo
        else
            echo -e $red" !!!$reset New arch linux news entry found $red!!!$reset"
            echo
            [ -f $TMPFILE ] && cat "${TMPFILE}" 2> /dev/null
            sleep 3		
            /usr/bin/mv -f $TMPFILE $RSSFILE
            { /usr/bin/rsstail -n 5 -1 -l -d -H -u https://www.archlinux.org/feeds/news/ | /usr/bin/less ; } || { echo -e $red"Error:$reset Cannot download the rss content" ; read -p "Press enter to exit..." ; exit 1; }
            exit 0
        fi
    else
        echo -e $red" !!!$reset New arch linux news entry found $red!!!$reset"
        echo
        [ -f $TMPFILE ] && cat "${TMPFILE}"  2> /dev/null
        echo
        sleep 3
        /usr/bin/mv $TMPFILE $RSSFILE
        { /usr/bin/rsstail -n 10 -1 -l -d -H -u https://www.archlinux.org/feeds/news/ | /usr/bin/less ; } || { echo -e $red"Error:$reset Cannot download the rss content" ; read -p "Press enter to exit..." ; exit 1; }
        exit 0
    fi
fi
if [[ $Mirror == "Yes" ]]; then
        echo
        echo -e  $blue"===>$reset Updating mirrorlist..."
        { $SUDO /usr/bin/cp -f /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak ; } || { echo -e $red"Error:$reset Cannot backup mirrorlist" ; read -p "Press enter to exit..." ; exit 1; }
        { $SUDO reflector --save /etc/pacman.d/mirrorlist --country 'United States' --country Canada --country 'United Kingdom' --country Denmark --country Greece --country 'South Korea' --country Japan --country India --country Qatar --country Turkey --country Iran --sort rate --latest 10 --protocol https --protocol ftp --age 6 ; } || { echo -e $red"Error:$reset Cannot update mirrors"; }
fi
if [[ $Install == "Yes" ]] || [[ $Build == "Yes" ]]; then
    if [[ $Build == "Yes" ]]; then
        echo ""
        echo -e $blue"===>$reset Checking PKGBUILD file for error..."
        echo ""
        /usr/bin/namcap PKGBUILD
        echo ""
        read -p "Press enter to continue..."
        echo ""
        echo -e $blue"===>$reset Building the package..."
        echo ""
        { /usr/bin/sudo -u $USERNAME /usr/bin/makepkg -sc ; } || { echo -e $red"Error:$reset Cannot build the package" ; read -p "Press enter to exit..." ; exit 1; }
    fi
    echo ""
    echo -e $blue"===>$reset Checking the build package file for error..."
    echo ""
    /usr/bin/find . -maxdepth 1 -name '*.pkg.tar.xz' -exec /usr/bin/namcap {} \;
    echo ""
    read -p "Press enter to continue..."
    if [[ $Install == "Yes" ]]; then
        echo ""
        echo -e $blue"===>$reset Installing the package..."
        echo ""
        { /usr/bin/find . -maxdepth 1 -name '*.pkg.tar.xz' -exec $SUDO /usr/bin/pacman -U {} \; ; } || { echo -e $red"Error:$reset Cannot install the package" ; read -p "Press enter to exit..." ; exit 1; }
        #{ $SUDO /usr/bin/pacman -U "$(ls *.pkg.tar.xz 2> /dev/null)" ; } || { echo -e $red"Error:$reset Cannot install the package" ; exit 1; }
    fi
fi	
if [[ $Sync == "Yes" ]]; then
    echo
    echo -e $blue"===>$reset Checking for updates..."
    echo
    if [[ $Refresh == "No" ]]; then
        if [[ $AUR == "Yes" ]]; then
            if [ -x /usr/bin/yaourt ]; then
                { /usr/bin/sudo -u $USERNAME /usr/bin/yaourt -Syua ; } || { echo -e $red"Error:$reset Cannot update the system" ; read -p "Press enter to exit..." ; exit 1; }
            else
                echo -e $red"Error:$reset Yaourt not found"
                exit 1
            fi 
        elif [ -x /usr/bin/pacmatic ]; then
            { $SUDO /usr/bin/pacmatic -Syu ; } || { echo -e $red"Error:$reset Cannot update the system" ; exit 1; }
        else
            { $SUDO /usr/bin/pacman -Syu ; } || { echo -e $red"Error:$reset Cannot update the system" ; read -p "Press enter to exit..." ; exit 1; }
        fi
    else
        if [[ $AUR == "Yes" ]]; then
            if [ -x /usr/bin/yaourt ]; then
                { /usr/bin/sudo -u $USERNAME /usr/bin/yaourt -Syyua ; } || { echo -e $red"Error:$reset Cannot update the system" ; read -p "Press enter to exit..." ; exit 1; }
            else
                echo -e $red"Error:$reset Yaourt not found"
                exit 1
            fi
        elif [ -x /usr/bin/pacmatic ]; then
            { $SUDO /usr/bin/pacmatic -Syyu ; } || { echo -e $red"Error:$reset Cannot update the system" ; exit 1; }
        else
            { $SUDO /usr/bin/pacman -Syyu ; } || { echo -e $red"Error:$reset Cannot update the system" ; read -p "Press enter to exit..." ; exit 1; }
        fi
    fi
fi
echo
if [[ $RSSOff == "No" ]]; then
    [ -f $RSSFILE ] && cat "${RSSFILE}" | 2> /dev/null
fi
echo
if [[ $LoggingOff == "No" ]]; then
    echo
    echo -e  $blue"===>$reset Updating log files..."
    echo
    { /usr/bin/bash "$HOMEDIR/bin/logupdates" ; } || { echo -e $red"Error:$reset Cannot update '.number_of_updates.txt' file" ; }
    { /usr/bin/sudo -u $USERNAME /usr/bin/tail --lines=100 /var/log/pacman.log > $HOMEDIR/.updatesystem.log ; } || { echo -e $red"Error:$reset Cannot update '.updatesystem.log' file" ; }
fi
echo
if [[ $RSSOff == "No" ]]; then
    echo
    echo "Latest arch linux news:"
    echo
    [ -f $RSSFILE ] && cat "${RSSFILE}" 2> /dev/null
fi
echo
read -p "Press enter to exit..."
exit 0
