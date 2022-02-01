default: service-test-focused

setpath:
	PYTHONPATH=./src pytest

create-report-folder:
	mkdir -p test_acceptance/reports

service-test-happypath:
	pytest -v ./test_acceptance/step_defs/device_service_happy_path.py --capture=no

service-test-focused:
	make create-report-folder
	pytest -v ./test_acceptance/step_defs/device_service_happy_path.py -m "focus" --capture=no --cucumberjson="test_acceptance/reports/report.json"

#.PHONY: service-test-happypath