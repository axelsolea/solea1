#!/bin/bash
# Author: Djetic Alexandre
# Date: 07/02/2024
# Modified: 07/02/2024
# Description: this script tests every NAT rule

#debug
set -u

# env var
SERVER="192.168.141.2"
LIST_FILE_NAT="list_nat.txt"
FILE_LOG="test_nat.log"

# this function tests 1 SSH NAT rule
function nat_1_ssh {
    # $1 : take 1 line of $LIST_FILE_NAT
    USER=$(echo "$1" | cut -d ':' -f1)
    PASS=$(echo "$1" | cut -d ':' -f2)
    PORT=$(echo "$1" | cut -d ':' -f3)
    DESC=$(echo "$1" | cut -d ':' -f4)

    if [[ "$PASS" == "None" ]]; then
        sshpass -p "" ssh "$USER"@"$SERVER" -p "$PORT" "hostname; exit" >> "$FILE_LOG"
    else
        sshpass -p "$PASS" ssh "$USER"@"$SERVER" -p "$PORT" "hostname; exit" >> "$FILE_LOG"
    fi
}

echo "----------------- test nat -----------------" > "$FILE_LOG"

while IFS= read -r ligne; do
    ISCOMMENTARY=$(echo "$ligne" | awk '{print $1}')

    #test if it is a commentary
    if [[ ! "$ISCOMMENTARY" == "#" ]]; then
        nat_1_ssh "$ligne"
    fi
done < "$LIST_FILE_NAT"

echo "----------------- test nat finish -----------------" >> "$FILE_LOG"
