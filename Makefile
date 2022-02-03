default: service-test-poc

setpath:
	PYTHONPATH=./src pytest

create-report-folder:
	if [ ! -d "/test_acceptance/reports" ]; then \
	  mkdir -p test_acceptance/reports; \
	fi

service-test-happypath:
	make create-report-folder
	pytest -v ./test_acceptance/step_defs/device_service_happy_path.py --capture=no --alluredir=test_acceptance/allure_reports
	allure generate reports --clean

service-test-focused:
	make create-report-folder
	pytest -v ./test_acceptance/step_defs/device_service_happy_path.py -m "focus" --capture=no --alluredir=test_acceptance/allure_reports
	allure generate reports --clean

service-test-poc:
	make create-report-folder
	pytest -v ./test_acceptance/step_defs/test_integration_test_device_create_flow.py -m "poc" --capture=no --alluredir=test_acceptance/allure_reports
	allure generate test_acceptance/allure_reports --clean -o test_acceptance/reports

#.PHONY: service-test-happypath