list:
	docker container ls -a
build:
	docker build -t devapptest .
run:
	docker run -p 4200:4200 --rm newapp1
prodrun:
	docker run -v "/var/www/PDF:/app/pub/estimate_reports" -p 4200:4200 --rm -d tsappnew
