#!/bin/bash

SOURCE_FOLDER=$(cat .source-folder)
DEST_FOLDER=$(cat .dest-folder)

## Other accounts csv exports
mv "$SOURCE_FOLDER"/Extrato\ outras\ contas*.csv "$DEST_FOLDER"

## Nubank csv exports
mv "$SOURCE_FOLDER"/nubank*.csv "$DEST_FOLDER"

## Spliwise csv exports from site
mv "$SOURCE_FOLDER"/20*mozi-e-eu*.csv "$DEST_FOLDER"
mv "$SOURCE_FOLDER"/jacas-keter*.csv "$DEST_FOLDER"

## Easynvest exports
mv "$SOURCE_FOLDER"/Exportar_custodia_*.csv "$DEST_FOLDER"
