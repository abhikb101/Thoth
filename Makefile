build: 
	docker build -t chatgptslackbot .

deploy: build
	docker run --name chatgptslackbot --env-file ./vendorlabs.env -p 4000:4000 chatgptslackbot

delete:
	docker stop chatgptslackbot
	docker rm chatgptslackbot

dev: delete
	make deploy
