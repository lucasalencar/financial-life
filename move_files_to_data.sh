#!/bin/bash

DOWNLOAD_FOLDER="$HOME/Downloads"

# Other accounts csv exports
mv $DOWNLOAD_FOLDER/Extrato\ outras\ contas*.csv ./data/

# Nubank csv exports
mv $DOWNLOAD_FOLDER/nubank*.csv ./data/

# Spliwise csv exports from mobile app
mv $DOWNLOAD_FOLDER/Splitwise*.csv ./data/

# Remove current splitwise exports only if there is another to move
if [ -f $DOWNLOAD_FOLDER/mozi-e-eu*.csv ]; then
  rm ./data/mozi-e-eu*.csv
fi

# Spliwise csv exports from site
mv $DOWNLOAD_FOLDER/mozi-e-eu*.csv ./data/
