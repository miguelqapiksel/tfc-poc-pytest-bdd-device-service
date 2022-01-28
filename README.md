# activate virtualenv & install dependencies

pip3 install virtualenv

python3 -m virtualenv enviromentbdd

source enviromentbdd/bin/activate

pip3 install -r ./requirements.txt

# Run a given (py) test

pytest -v device_service_happy_path.py --capture=no

Steps to test e2e devices-->Flow
--------------------------------

#device service:
.env.local file must have variables (different port)
BASE_URL_DEVICE_USVC & BASE_URL_FLOW_USVC
run 
-bin/console doctrine:database:create 
-bin/console doctrine:migrations:migrate
-symfony server:start --port=8888

#flow service: 
.env.local file must have variables (in device the port from running device)
BASE_URL_DEVICE_USVC & BASE_URL_FLOW_USVC

run 
-bin/console doctrine:database:create 
-bin/console doctrine:migrations:migrate
-symfony server:start --port=8080
-bin/console rabbitmq:consumer pubsub (consumer of flow listening to device)

# Update list 27/01/2022 of devices accepted or not by flow service

FLOW DEVICES --->|d0e300af-bcb8-4715-becf-d0bf8d87960b|88ea9140-6ff4-11e9-99c8-cbb88253d865|1e9107fc-b894-43cc-b763-d8addaec6df2|Embrionix emFusion|9aefedf0-2573-11e9-8346-139ab5900c6e|c7e227a8-6322-4967-a02a-e95fce6b3c69|64d7b682-7366-44ea-9257-293e7fbe2c2e|
NOT FLOW DEVICES--->|3c4b4030-444c-11e9-803e-b19926510b86||d3797e1c-ba47-4be8-9666-df376eac850e||3ea011b7-4d22-486b-a2d3-43d89a1de4b1||59cb3bf1-d5a1-4b43-9c41-111b6c6249fb||b148e66f-a2d7-4d3b-9366-a3fee13bd690||dabb1b85-e1e1-49d5-b2db-0c44fb1d2dbf||dfc3087e-c7f4-45f6-95b1-b20240d0d5e0||8a728650-f811-11ea-8f5a-2179b51fae40||cbcfd862-4c30-4006-92f1-fbe436217510||3ac39435-ba68-42e1-8541-2de6776cb1cc||f94039d5-a318-4fe4-bbb4-d7f6d0d7a491||1946b9f0-8bed-11e9-bbcc-a598f2dc39d5||3e39202b-9d6d-4ac6-9f12-10fec91a7bbe||5a29bd46-3fdc-4019-b600-875d460a3e2e||ac9626e8-a27e-40ff-9ed9-7c325fdd9f5f||805f041d-1867-47bc-b3de-2dfb0430f684||12e0c14f-f4d7-403a-b8f8-f1e933a8bf7f||25f75cb9-ee4f-4a89-ba16-e791c5b6ef3e||51b9ed0f-44eb-410e-a2b4-dcc549f2b394||67b5cfed-f946-4f52-847b-072949e834aa||0ce96320-a82e-406a-928c-ff928b1cb809||000dd5c8-9ea7-469d-b7f9-1018f33d5bd1||67b306f4-2808-424a-98d0-9953ee8d333d||57d086aa-dfb8-448b-a492-df2cc3f417b7||2037a1bf-2c53-4bb5-bf86-bc50d0cdc7aa||dff29b0f-4549-4b65-b32d-e72f0f1d3daf||c017c818-1918-455b-9ff2-16ac2433fa1b||59450756-8cf3-4ecd-8551-ccc9cb235b2d||9ca7d10b-a6c9-4809-968f-c8ac8042c946||cce55430-5535-48ad-801b-f19963a997ba||774a5b73-8ea5-4997-b3b6-782e760986f5||5360164f-f5c4-4fd7-9ecc-fe775b889edc||0469dd20-bc36-4b83-ab68-8c8878190788||75abbd5a-f35e-4cad-8739-5d15404ed587||0fbf6e71-a7dc-461c-8410-c791d7fbabce||fa8af6cd-516a-434e-a283-97c4a238a75d||0be04bc4-a37a-4014-892f-9f1b7bc5523a||0382ec09-db7b-48a1-8070-7280b00f3b14||3c5967d0-832e-11e9-9df3-d54852b7573d||49012fad-d869-4d9c-b31c-1ead8a8b70ec||5553fbe6-5743-4eb1-8a67-80b3a1ba6dec||83ac0c03-24b6-4338-91fe-c48dc7fbb400||a55a70f4-36ed-4619-85af-ebb66b0d5b33||c344690f-2027-4242-8140-971ed00939f8||eb03eb86-2e1c-4837-8b35-ea866676cb0e||f8c3b0a8-1088-48e3-b1c5-a48b2f020223||379f02ae-13b3-4b7a-887d-1f3c3c34e248||ac27deca-9127-414f-aa3e-899e1b769bc7||d8429c6e-b6da-4733-b404-63f558e3a97a||f84dc6f1-7c8a-425b-a5c9-ef0eb3e449b3||b108b814-7c19-4748-99e5-25968d95e300||a723b1de-bfe1-4b55-ad6c-1584d0e37bab||bae57518-dda8-46b4-ae8f-0d92d2a1ca37||d3ee0510-19c7-4280-bb2a-6ef608891cf6||2b337841-d482-4c53-af30-f45e12402827||f20afa8a-5df9-4a52-b782-b4190e00d09d||
