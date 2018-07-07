#!/bin/bash

# Other accounts csv exports
mv $HOME/Downloads/Outras\ contas*.csv ./data/

# Nubank csv exports
mv $HOME/Downloads/nubank*.csv ./data/

# Spliwise csv exports from mobile app
mv $HOME/Downloads/Splitwise*.csv ./data/

# Remove current splitwise exports
rm ./data/mozi-e-eu*.csv

# Spliwise csv exports from site
mv $HOME/Downloads/mozi-e-eu*.csv ./data/
