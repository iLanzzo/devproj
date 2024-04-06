#!/bin/bash

# Get the current user's username
current_user=$(whoami)

# Specify the folder name
folder_name="mysql-db"

# Change the owner of the folder to the current user
sudo chown -R $current_user:users $folder_name

# Delete the folder and all its contents
sudo rm -rf $folder_name

echo "Folder '$folder_name' has been deleted."
