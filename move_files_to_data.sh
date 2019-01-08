#!/bin/bash

DOWNLOAD_FOLDER="$HOME/Downloads"

# Other accounts csv exports
mv $DOWNLOAD_FOLDER/Extrato\ outras\ contas*.csv ./data/

# Nubank csv exports
mv $DOWNLOAD_FOLDER/nubank*.csv ./data/

# Spliwise csv exports from mobile app
mv $DOWNLOAD_FOLDER/Splitwise*.csv ./data/

# Spliwise csv exports from site
mv $DOWNLOAD_FOLDER/20*mozi-e-eu*.csv ./data/
