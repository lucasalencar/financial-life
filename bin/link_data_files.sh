#!/bin/bash

DEST_FOLDER=$(cat .dest-folder)
DATA_FOLDER="./data"

## Symbolic link for everything that is on $DEST_FOLDER to data
ln -sf "$DEST_FOLDER"/*.csv $DATA_FOLDER
