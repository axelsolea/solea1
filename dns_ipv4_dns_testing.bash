#!/bin/bash
# Author: Djetic Alexandre
# Date: 10/01/2024
# Modifed: 17/01/2024
# Description: this script will test a dns using IPv4

# Check if the script is provided with the DNS IP as an argument
if [ $# -ne 1 ]; then
  echo "usage: $0 <dns_ip>"
  exit 1
fi

#file location
list_file=$PWD/list_name.txt
log_file=$PWD/dns_test.log

#property
dns=$1
list_name=$(<"$list_file")

#this function clear the log
function cleanup_log() {
  echo "" >> "$log_file"
}

#this function test a dns resolv
function test_site() {
  nslookup -q=A $1 $2 >> $log_file

  if [ $? -eq 0 ]; then
    echo "INFO: testing $1...success"
  else
    echo "INFO: testing $1...failed"
  fi
}

#empty log file
cleanup_log

echo "NOTIFY: using the list file: $list_file"
echo "NOTIFY: using the log file: $log_file"
echo "NOTIFY: starting..."

#dns request
for name in $list_name
do
  test_site $name $dns
done

echo "NOTIFY: finish...exiting"
exit 0


