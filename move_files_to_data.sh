#!/bin/bash

# Other accounts csv exports
mv $HOME/Downloads/Extrato\ outras\ contas*.csv ./data/

# Nubank csv exports
mv $HOME/Downloads/nubank*.csv ./data/

# Spliwise csv exports from mobile app
mv $HOME/Downloads/Splitwise*.csv ./data/

# Remove current splitwise exports only if there is another to move
if [ -f $HOME/Downloads/mozi-e-eu*.csv ]; then
  rm ./data/mozi-e-eu*.csv
fi

# Spliwise csv exports from site
mv $HOME/Downloads/mozi-e-eu*.csv ./data/
