#!/bin/bash
# Author: Axel 
# Date: 16/02/2024
# Last edit: 18/03/2024
# Description: Permet de se connecter au serveur samba, créer un dossier, un fichier et de nettoyer

# Environment variables
IP="172.18.0.252"
SHARE="solea_document"
SHARE_DIR="/mnt/smb_share"
USER_SHARE="admin1"
PASS="123"

# Create the directory
mkdir -p "$SHARE_DIR"

# Mount point setup
sudo mount -t cifs "//$IP/$SHARE" "$SHARE_DIR" -o username="$USER_SHARE",password="$PASS"

# Test that the mount is successful
if [ $? -eq 0 ]; then
  echo "Mount point success!"
else
  echo "Mount point failed!"
fi

# Test that the point is writable
mkdir "$SHARE_DIR/test" > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo "Create dir successful!"
  rm -rf "$SHARE_DIR/test"  # Clean up the test directory
else
  echo "Failed to create directory!"
fi

# Test with a user that doesn't exist
mkdir -p "$SHARE_DIR/failed"
sudo mount -t cifs "//$IP/$SHARE" "$SHARE_DIR/failed" -o username="azerty",password="azerty"

# Test that the mount is successful
if [ $? -eq 1 ]; then
  echo "Mount point failed as expected!"
  umount "$SHARE_DIR/failed"  # Clean up the failed mount
else
  echo "Mount point success ... not normal"
  umount "$SHARE_DIR/failed"  # Clean up the unexpected mount
fi
