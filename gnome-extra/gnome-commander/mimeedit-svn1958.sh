#!/bin/bash
#
# gnome-file-types-properties - 
# A zenity-script for chosing preferred applications. 
# Written by Magnus Stålnacke (jemamo at telia.com) 
# Version 0.8.4 Nov. 30 2007
#
export LANG=en_US.utf8 

ARGU="$1"
UTMP="/tmp/$(whoami)"
DATA_DIR="$HOME/.local/share/applications"
GDATA_DIR="/usr/share/applications"
G_CACHE="$GDATA_DIR/mimeinfo.cache"
U_CACHE="$DATA_DIR/mimeinfo.cache"
SUBC="/usr/share/mime/subclasses"
U_DEF="$DATA_DIR/defaults.list"
EXT="usercreated.desktop"
NONEW=1

#
# Create dirs in users home if missing. 
#
if [ -e "$DATA_DIR" ]; then :; else mkdir $DATA_DIR;fi
if [ -e "$U_DEF" ] 
then :; 
else 
  echo "[Default Applications]" > $DATA_DIR/defaults.list 
fi

#
# Check how we got started. 
#
function checkarg (){
  if [ -n "$ARGU" ]
  then
    if [ -e "$ARGU" ]
    then
      chkmtpe 
      deflist
    else
      showhelp
    fi
  else
    selfile
    dtfedit
    if [ -n "$DT_FILE" ]
    then
      update
    fi
  fi
}

#
# Mimetype check.
#
function chkmtpe (){
  MTPE=$(gnomevfs-info -s "$ARGU" | grep "MIME type" | sed 's/.*: //')
  echo "The mimetype is: $MTPE"
}

#
# Build a list with registered apps for this mimetype.
#
function deflist (){
  if [ -e "$UTMP.avail" ]; then cleanup;fi
  # Create the list in "$UTMP.avail" to be used by the zenity list-box
  if [ "$NONEW" == 1 ]
  then
   echo "FALSE Add_New_App New" > "$UTMP.avail"
  fi
  # Get all sub-mimetypes, one per row.
  SUB="$(grep -hs "^$MTPE" $SUBC $G_CACHE $U_CACHE | awk -F= '{print $1}' | sed 's/ /\n/g')"
  # Get all .desktopfiles for the above mimetypes
  MTPEs=$(grep -hs "$SUB" $U_CACHE $G_CACHE | sed 's/.*=//g;s/;$//g;s/;/\n/g;')
  if [ -n "$SUB" ]
  then
    for i in $(echo "$MTPEs" | sort -u); do
      echo "FALSE $i $(grep -hs "^Name=" $GDATA_DIR/$i $DATA_DIR/$i | \
      sed 's/Name=//;s/ /_/g')" >> "$UTMP.avail"
    done
  fi
  # Change FALSE to TRUE for the default app. 
  if grep -q "desktop" "$UTMP.avail"
  then
    DEF_APP=$(gnomevfs-info -s "$ARGU" | grep "Default app" | sed 's/.*: //')
    sed -i "s|FALSE $DEF_APP|TRUE $DEF_APP|" "$UTMP.avail"
  fi
  # Show the list
  zenity --height="350" --width="550" --list --radiolist --text \
"The list below show applications that already have an entry for the mimetype: 
$MTPE on your system, meaning they are registered to be able 
to deal with this mimetype. You can choose your preferred default application 
by checking the radiobutton. The script will adjust the mimetype settings in 
your local home directory, thus not changing anything systemwide.

If you wish you can add an application that is not in the list by checking the first 
option in list named Add_New_App 

Please select" \
  --column "Pick" --column ".desktop file" --column "Application" \
  $(cat "$UTMP.avail") > "$UTMP.chosen" 
  retval=$?
  choice=$(cat "$UTMP.chosen")
  if grep -q "$MTPE=$choice" $U_DEF
  then
    retval=2
  fi
  case $retval in
  0)
    DEF_CH=$(grep -s "$choice" "$UTMP.avail" | awk '{print $2}')
    DEF_NME=$(grep -s "$choice" "$UTMP.avail" | awk '{print $3}')
    if [ "$DEF_CH" = Add_New_App ]
    then
      newmime
    fi
    if [ -z "$NOCH" ]
    then
      if grep -q "$MTPE" $U_DEF
      then
        # Set the users chosen default app for the existing mime.
        sed -i "s|$MTPE=.*|$MTPE=$DEF_CH|" $U_DEF
      else
        # If no user default for this mimetype, add it.
         echo "$MTPE=$DEF_CH" >> $U_DEF
      fi
     update
     zenity --info --text "Default application to handle $MTPE is set to $DEF_NME"
    fi;;
  1)
    echo "Cancel pressed.";;
  -1)
    echo "ESC pressed.";;
  2)
    zenity --info --text "Default was not changed.";;
  esac
  cleanup
}

#
# Show an input box for new app to handle the mimetype.
#
function newmime (){
  NEWAPP=$(zenity --entry --text \
"Fill in the Name and command for the application you want to handle the 
mimetype: $MTPE separate them with a colon (:)

Separate Name and Command with a colon. If you omit the command, or 
type something that is not in your path, you will get the chance to 
provide the command with full path by a file chooser dialog.")

  case $? in 
  0)
   if echo "$NEWAPP" | grep -q ":"
   then
     NAME=$(echo "$NEWAPP" | awk -F: '{print $1}')
     CMD=$(echo "$NEWAPP" | awk -F: '{print $2}')
     if [ -n "$NAME" ]
     then
       check
       usercreate
     else
       zenity --error --text "Application name is missing"
       newmime
     fi
   else
     zenity --error --text "Separator missing"
     newmime
   fi
   ;;
  1)
   deflist
   ;;
  -1)
   deflist
   ;;
  esac
  NOCH=yes
}

#
# Check if the command exists in path, if not give the 
# user a filechooser.
#
function check (){
  if which $CMD >&/dev/null
  then
    CMD=`which $CMD`
  else
    CMD=$(zenity --file-selection --filename=/ --title="Chose application")
    if [ -z $CMD ]
    then
      newmime
    fi
  fi
}

#
# Create a new *.desktop file for the added app that can handle 
# the mimetype in question.
#
function usercreate(){
  APP=$(basename "$CMD")
  USER_APP="$DATA_DIR/$APP-$EXT"
  if cat $G_CACHE $U_CACHE | grep "$MTPE" | grep -q "$APP" 
  then
    zenity --error --text "The mime type: $MTPE is alredy assigned to: $APP"
    NOCH=yes
  else
    if [ -e "$USER_APP" ]
    then
      sed -i "s|MimeType=|MimeType=$MTPE;|g" $USER_APP
      update
      zenity --info --text \
      "The mime type: $MTPE is now registered to be handled by: $APP"
    else
      cat <<EOF >$USER_APP 
[Desktop Entry]
Encoding=UTF-8
Name=$NAME
Exec=$CMD
Type=Application
Terminal=false
NoDisplay=true
MimeType=$MTPE;
EOF
    fi
  fi
  if [ -z "$NOCH" ]
  then
    zenity --question --text \
"The created $(basename "$USER_APP") can now be edited manually, to add, remove or change options, do you want to do this now? 

This file should work as is, so you can safely cancel this operation, but advanced users may want to edit options to their liking. But due to a bug this editor cannot handle '%' charachters and replaces them with garbage." 
    VAL=$?
    if [ "$VAL" == 0 ]
    then 
      DT_FILE="$APP"
      dtfedit
      update
    else 
      update
    fi
    zenity --info --text "$APP is now registered to handle: $MTPE"
  fi
  NONEW=2
  deflist
}

#
# Update the users mime chache and set the defaults 
# first from the defaults.list file
#
function update (){
  update-desktop-database $DATA_DIR
  for i in $(sed '/\[.*\]/d' $U_DEF); do
    MTYPE=$(echo "$i" | awk -F= '{print $1}')
    M_FIL=$(echo "$i" | awk -F= '{print $2}')
    if grep -q "$MTYPE" $U_CACHE
    then
     sed -i "\|$MTYPE|s|$M_FIL||;s|$MTYPE=|$i;|;s|;;|;|" $U_CACHE
    else
     echo "$i" >> $U_CACHE
    fi
  done
  # If there are rows with empty mimetypes, delete them.
  sed -i '/.*=$/d' $U_CACHE
}

#
# Give the user a helping hand. 
#
function showhelp (){
echo
echo "Usage: $(basename $0) [ARGUMENT]"
echo '''
  -h, -?, --help  Show this help and exit. 

DESCRIPTION
  This script is dependent on zenity for creating its GUI. It is 
  to be used as a tool for choosing the default application or to 
  run for different type of files (mimetypes). It modifies or add 
  files in "$HOME/.local/share/applications" 

  When passed a valid filename it checks its mimetype as interpreted  
  by gnomevfs, it will show a list of already registered applications 
  able to handle the mimetype in question, the user can change default 
  application in this list. The list also contains an option to add 
  the Name and command of a program that is not registered to be able 
  to open files of the mimetype. After any changes this script will 
  run the update-desktop-database to update the users mime cache. 

  When executed without any argument, the script will list all 
  applications associated with a mimetype. When selecting an item from 
  this list, the user will be able to edit the options for the selected 
  application. The edited file will be saved in the above path and the 
  update-desktop-database is executed.

  When given an invalid argument or any of the options -h -? --help, 
  this text is shown. 
'''
}

#
# Remove tempfiles.
#
function cleanup (){
  rm -f "$UTMP.avail"
  rm -f "$UTMP.chosen"
}

#
# The .desktop file selector
#
function selfile (){
  DT_FILE=$(for i in $GDATA_DIR/*.desktop $DATA_DIR/*.desktop; do
    if grep -q "MimeType" $i 
    then
      BNME=$(basename $i | sed 's/\.desktop//;s/-usercreated//')
      if [ -e $DATA_DIR/$BNME-$EXT ] 
      then 
        i="$DATA_DIR/$BNME-$EXT"
      fi
      CMD=$(grep -m 1 "^Exec" $i | sed "s/^Exec=//")
      NME=$(grep -m 1 "^Name=" $i | sed 's/^Name=//')
      echo "$BNME---$NME---\"$CMD\""
    fi
  done | sort -u | sed 's/---/\n/g' |  zenity --list --width="550" --height="400" \
  --column="Base name" --column="Program name" --column="Program command" \
  --print-column="1" --text "Select item below. 

By selecting an item in this list and klick OK, you will get another window where 
you can edit the file that contains the options of the selected application. The 
edited file will end up in your: $DATA_DIR 

Pressing "Esc", click Cancel or use the window close (X) button will close without 
any changes in this or the following editor window. Be aware that the editor do 
have problems with the (%)percent charachter and may replace it by garbage.")
}

#
# The .desktop file editor
#
function dtfedit (){ 
  USER_DTF="$DT_FILE-$EXT"
  if [ -n "$DT_FILE" ]
  then 
    # Chose to edit users own file if exist
    if [ -e $DATA_DIR/$USER_DTF ]
    then
      TO_EDIT="$DATA_DIR/$USER_DTF"
    else
      TO_EDIT="$GDATA_DIR/$DT_FILE.desktop"
    fi
    cat "$TO_EDIT" | zenity --height="350" --width="550" --text-info --editable \
    --title "Edititng the file: $USER_DTF" > $UTMP.$USER_DTF 
    if [ -s $UTMP.$USER_DTF ]
    then 
      mv $UTMP.$USER_DTF $DATA_DIR/$USER_DTF 
    else 
      rm -f $UTMP.$USER_DTF 
      DT_FILE=""
    fi
  fi
} 

#
# Check if we have zenity installed then start this mess.
#
if which zenity >&/dev/null 
then
 checkarg 
else 
 echo "Error: zenity not found!"
fi

