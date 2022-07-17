install:
	pip install -r requirements.txt

start:
	./scripts/start.sh

test:
	pytest

backup:
	./scripts/backup_data_files.sh

link:
	./scripts/link_data_files.sh

sync:
	./scripts/sync_data_files.sh
