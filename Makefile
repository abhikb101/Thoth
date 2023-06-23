build: 
	docker build -t chatgptslackbot .

deploy: build
	docker run --name chatgptslackbot --env-file ./.env -p 4000:4000 chatgptslackbot 