show:
	docker container ls -a
build:
	docker build -t devapptest .
run:
	docker run -p 80:4200 --rm devapptest
