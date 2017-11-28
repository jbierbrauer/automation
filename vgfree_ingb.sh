#!/bin/sh
#
# Usage: ./vgfree_inpct.sh -w <warn> -c <crit>
#
# ## Description:
#
# This plugin finds all LVM logical volume groups, checks their used space, and 
# compares against the supplied thresholds.
#
# ## Output: 
#
# The plugin prints "ok" or either "warning" or "critical" if the corresponing 
# threshold is reached, followed by the used space info for the offending volumes groups.
#
# Exit Codes
# 0 OK
# 1 Warning
# 2 Critical
# 3 Unknown  Invalid command line arguments or could not determine used space
#
# Example: check_lvm -w 30 -c 20
#
# OK                                  (exit code 0)
# WARNING - vg01=16.4g von 40.0g frei (exit code 1)
# CRITICAL - vg00=12.0 von 40.0g frei (exit code 2)


PROGNAME=`basename $0`
VERSION="0.4"
AUTHOR="(c) 2017 "

# Exit codes
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4

print_version() {
    echo "$PROGNAME $VERSION $AUTHOR"
}

print_usage() {
    echo "Usage: $PROGNAME [-h|-V] | -w nnn -c nnn"; echo ""
    echo "  -h, --help"; echo "          print the help message and exit"
    echo "  -V, --version"; echo "          print version and exit"
    echo "  -w nn, --warning=nn"; echo "          warning threshold in GB(=1000MB) of space free"
    echo "  -c nn, --critical=nn"; echo "          critical threshold in GB(=1000MB) of space free"
    echo "---------------------------------------------"
    echo "Example: $PROGNAME -c 20 -w 30 "
    echo "Description: Gives a Warning when any of the Volume Groups have less than 30GB free Space available and an Alert when any of the Volume Groups has less then 20GB of free Space available"




}

print_help() {
    print_version
    echo ""
    echo "Plugin for Nagios check free space of all volume groups"
    echo ""
    print_usage
    echo ""
}


# Make sure the correct number of command line
# arguments have been supplied

if [[ ! `echo "$*" |grep -E "(-[hVwc]\>|--(help|version|warning|critical)=)"` ]]; then
    print_usage
    exit $STATE_UNKNOWN
fi

# Grab the command line arguments

thresh_warn=""
thresh_crit=""
exitstatus=$STATE_WARNING #default
while test -n "$1"; do
    case "$1" in
        --help)
            print_help
            exit $STATE_OK
            ;;
        -h)
            print_help
            exit $STATE_OK
            ;;
        --version)
            print_version
            exit $STATE_OK
            ;;
        -V)
            print_version
            exit $STATE_OK
            ;;
        --warning=*)
            thresh_warn=`echo $1 | awk -F = '{print $2}'`
            if [[ `expr match "$thresh_warn" '\([0-9]*\)'` != $thresh_warn ]] || [ -z $thresh_warn ]; then
                echo "Warning value must be a number greater than zero"
                exit $STATE_UNKNOWN
            fi
            ;;
        -w)
            thresh_warn=$2
            if [[ `expr match "$thresh_warn" '\([0-9]*\)'` != $thresh_warn ]] || [ -z $thresh_warn ]; then
                echo "Warning value must be a number greater than zero"
                exit $STATE_UNKNOWN
            fi
            shift
            ;;
        --critical=*)
            thresh_crit=`echo $1 | awk -F = '{print $2}'`
            if [[ `expr match "$thresh_crit" '\([0-9]\+\)'` != $thresh_crit ]] || [ -z $thresh_crit ]; then
                echo "Critical value must be a number greater than zero (--critical)"
                exit $STATE_UNKNOWN
            fi
            ;;
        -c)
            thresh_crit=$2
            if [[ `expr match "$thresh_crit" '\([0-9]\+\)'` != $thresh_crit ]] || [ -z $thresh_crit ]; then
                echo "Critical value must be a number greater than zero (-c)"
                exit $STATE_UNKNOWN
            fi
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            print_usage
            exit $STATE_UNKNOWN
            ;;
    esac
    shift
done

#echo "Warn: ${thresh_warn}"
#echo "Crit: ${thresh_crit}"



i=0
for vg in `vgs --noheadings --nosuffix --units b --separator " " --options vg_name`; do
#   echo /home/aqdejbi/nagios-plugin/bin/check_vg_free -c ${thresh_crit}% -w ${thresh_warn}% $vg   
   /home/aqdejbi/nagios-plugin/bin/check_vg_free -c ${thresh_crit}000 -w ${thresh_warn}000 $vg
   erg[i]=$?
   vgname[i]=$vg
#   echo ${erg[i]}
   if [[ "${erg[i]}" -eq "2" ]]; then
      critflag=1
#      echo "Kritisch"
   elif [[ "${erg[i]}" -eq "1" ]]; then
      warnflag=1
#      echo "Warnung"
   fi
   i=$i+1
done
vganzahl=${#vgname[@]}

for ((x=0; x<${vganzahl};x++));
do
  if [[ ${erg[x]} -gt "0"  ]]; then     
#     echo "${vgname[x]} = ${erg[x]}";
     curmsg=`vgs --noheadings ${vgname[x]} | awk '{print "="$7 " von "$6" frei. "}' `
     msgs=${msgs}${vgname[x]}${curmsg}
  fi
done

if [ $critflag ]; then
    mesg="CRITICAL -"
    exitstatus=$STATE_CRITICAL
elif [ $warnflag ]; then
    mesg="WARNING -"
    exitstatus=$STATE_WARNING
else
    mesg="OK"
    exitstatus=$STATE_OK
fi

echo "$mesg $msgs"
exit $exitstatus

