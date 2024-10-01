git pull
docker build -t django-server .
docker run -p 8000:8000 -d --name django-server django-server
