#!/bin/bash

SOURCE_FOLDER=$(cat .source-folder)
DEST_FOLDER=$(cat .dest-folder)

DATA_FOLDER="./data"

## Other accounts csv exports
mv $SOURCE_FOLDER/Extrato\ outras\ contas*.csv "$DEST_FOLDER"

## Nubank csv exports
mv $SOURCE_FOLDER/nubank*.csv "$DEST_FOLDER"

## Spliwise csv exports from site
mv $SOURCE_FOLDER/20*mozi-e-eu*.csv "$DEST_FOLDER"
mv $SOURCE_FOLDER/jacas-keter*.csv "$DEST_FOLDER"

## Symbolic link for everything that is on $DEST_FOLDER to data
ln -sf "$DEST_FOLDER"/*.csv $DATA_FOLDER
