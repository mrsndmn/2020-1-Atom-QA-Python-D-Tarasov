
# Собираем/подгружаем образы
```
podman load --help -i myapp.dockerimage
podman build -t qa-vkapi --file dockerfiles/vkapi/Dockerfile vkapi
podman build -t myjenkins build --squash dockerfiles/jenkins/Dockerfile
podman build -t qamyapp --file dockerfiles/myapp/Dockerfile
```

Создаем под
```
podman pod create --name qa-project -p 8000-8080
```

Запускаем женкинс
```
podman run -d --pod qa-project --name qajenkins -v jenkins_home:/var/jenkins_home localhost/myjenkins
```

Инитим базу
```

```

Запускаем сервисы
```
# mysql
podman run --pod qa-project --name qamysql -e MYSQL_DATABASE=technoatom -e MYSQL_USER=test_qa -e MYSQL_PASSWORD=qa_test -e MYSQL_ROOT_PASSWORD=root -v qa-mysql-volume:/var/lib/mysql mysql

# приложение
podman run -d --pod qa-project --name qamyapp qamyapp

# вкапи. Токен нужно взять из настроек приложения
run -d --pod qa-project --name qavkapi -e VK_API_TOKEN=$VK_APP_SERVICE_TOKEN localhost/qa-vkapi
```

После того, как все поднялось, можно проинитить базу
```
podman exec qamyapp /app/myapp --config=/etc/myapp.conf --setup
```