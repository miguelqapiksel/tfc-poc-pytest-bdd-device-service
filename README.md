# activate virtualenv & install dependencies

pip3 install virtualenv

python3 -m virtualenv enviromentbdd

source enviromentbdd/bin/activate

pip3 install -r ./requirements.txt

# Run a given (py) test

pytest -v device_service_happy_path.py --capture=no

Steps to test e2e devices-->Flow
--------------------------------

device service:
.env.local file must have variables (different port)
BASE_URL_DEVICE_USVC & BASE_URL_FLOW_USVC
run 
-bin/console doctrine:database:create 
-bin/console doctrine:migrations:migrate
-symfony server:start --port=8888

flow service: 
.env.local file must have variables (in device the port from running device)
BASE_URL_DEVICE_USVC & BASE_URL_FLOW_USVC

run 
-bin/console doctrine:database:create 
-bin/console doctrine:migrations:migrate
-symfony server:start --port=8888
-bin/console rabbitmq:consumer pubsub (consumer of flow listening to device)

