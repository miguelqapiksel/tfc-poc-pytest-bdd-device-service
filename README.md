# activate virtualenv & install dependencies

pip3 install virtualenv

python3 -m virtualenv enviromentbdd

source enviromentbdd/bin/activate

pip3 install -r ./requirements.txt

# Run a given (py) test

pytest -v device_service_happy_path.py --capture=no
