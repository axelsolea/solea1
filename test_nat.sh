#!/bin/bash
# Author: Djetic Alexandre
# Date: 07/02/2024
# Modified: 07/02/2024
# Description: this script test every nat rule

#debug
set -u

# env var
SERVER="192.168.141.2"
LIST_FILE_NAT="list_nat.txt"
FILE_LOG="test_nat.log"

# this function test 1 ssh nat rule
function nat_1_ssh {
    # $1 : take 1 ligne of $LIST_FILE_NAT
    USER=$(echo "$1" | sed "s/:/ /g" | awk '{print $1}')
    PASS=$(echo "$1" | sed "s/:/ /g" | awk '{print $2}')
    PORT=$(echo "$1" | sed "s/:/ /g" | awk '{print $3}')
    DESC=$(echo "$1" | sed "s/:/ /g" | awk '{print $4}')

    if [[ "$PASS" == "None" ]]; then
        sshpass -p "" ssh "$USER"@"$SERVER" -p "$PORT" "hostname; exit" >> "$FILE_LOG"
    else
        sshpass -p "$PASS" ssh "$USER"@"$SERVER" -p "$PORT" "hostname; exit" >> "$FILE_LOG"
    fi

    return $?
}

echo "----------------- test nat -----------------" > "$FILE_LOG"

for ligne in $(cat "$LIST_FILE_NAT")
do
    ISCOMMENTARY=$(echo "$ligne" | awk '{print $1}')
    
    #test if it is a commentary
    if [[ ! "$ISCOMMENTARY" == "#" ]]; then
        nat_1_ssh "$ligne"
    fi	
done

echo "----------------- test nat finish -----------------" >> "$FILE_LOG"
