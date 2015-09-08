#!/bin/sh

#--------------------------------------
#   winsys
#--------------------------------------
export DISPLAY=:0.0
WINSYS_DEBUG=$1/winsys
E17_HOME=/home/app
/bin/mkdir -p ${WINSYS_DEBUG}
/usr/bin/xinfo -p 2> ${WINSYS_DEBUG}/ping.log
/usr/bin/xinfo -xwd_topvwins ${WINSYS_DEBUG}
/bin/cp -af /opt/var/log/keygrab_status.txt ${WINSYS_DEBUG}
/usr/bin/xinfo -topvwins 2> ${WINSYS_DEBUG}/xinfo_topvwins.txt
/usr/bin/xdbg clist > ${WINSYS_DEBUG}/xdbg_clist.log 2>&1
/usr/bin/xdbg drmevent_pending > ${WINSYS_DEBUG}/drmevent_pending.log 2>&1
/usr/bin/xberc drmmode_dump > ${WINSYS_DEBUG}/drmmode_dump.log
/usr/bin/find /var/log/ -name "*Xorg*" -exec /bin/cp {} ${WINSYS_DEBUG}/ \;
/usr/bin/xprop -root -f _E_LOG 8s -set _E_LOG ${E17_HOME}/e.log
/bin/cat ${E17_HOME}/e.log > ${WINSYS_DEBUG}/e.log
/usr/bin/border_win_info -p ALL -f ${E17_HOME}/e_illume2.log
/bin/cat ${E17_HOME}/e_illume2.log > ${WINSYS_DEBUG}/e_illume2.log
/usr/bin/e_comp_util -l DUMP_INFO -f ${E17_HOME}/e_comp.log
/bin/cat ${E17_HOME}/e_comp.log > ${WINSYS_DEBUG}/e_comp.log
/bin/cat ${E17_HOME}/e_comp.log_move > ${WINSYS_DEBUG}/e_comp.log_move
/bin/rm ${E17_HOME}/e.log
/bin/rm ${E17_HOME}/e_comp.log
/bin/rm ${E17_HOME}/e_comp.log_move
/bin/rm ${E17_HOME}/e_illume2.log
