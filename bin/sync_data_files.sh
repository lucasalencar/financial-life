#!/bin/bash

CURRENT_DIR="$(cd "$(dirname "$0")" && pwd)"

$CURRENT_DIR/backup_data_files.sh
$CURRENT_DIR/link_data_files.sh
