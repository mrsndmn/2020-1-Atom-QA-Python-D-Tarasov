Jenkins я поднял в виртуалке.

# Собираем/подгружаем образы
```
podman load -i myapp.dockerimage
podman build -t vkapi --file dockerfiles/vkapi/Dockerfile vkapi
podman build -t myapp --file dockerfiles/myapp/Dockerfile myapp
```

Создаем под
```
podman pod create --name qa-project -p 3306:3306 -p 8000:8000 -p 8001:8001 -p 8080-8090
```

Запускаем сервисы
```
# mysql
podman run -d --pod qa-project --name qamysql -e MYSQL_DATABASE=technoatom -e MYSQL_USER=test_qa -e MYSQL_PASSWORD=qa_test -e MYSQL_ROOT_PASSWORD=root -v qa-mysql-volume:/var/lib/mysql mysql

# приложение
podman run -d --pod qa-project --name myapp qamyapp

# вкапи. Токен нужно взять из настроек приложения
podman run -d --pod qa-project --name vkapi -e VK_API_TOKEN=$VK_API_TOKEN localhost/qa-vkapi
```

После того, как все поднялось, можно проинитить базу
```
podman exec qamyapp /app/myapp --config=/etc/myapp.conf --setup
```

# Что показалось странным:

* Пароли не стоит хранить в открытом виде. Нужнохэшировать + солить.
* Удаление пользователя методом GET, скорее всего, это должен быть метод DELETE


# TODO распределить по приоритету баги

# Тестирование API

# Баги:

---



#### Expected Behavior:

#### Current Behavior:

#### Possible Solution

#### Steps to Reproduce

1.

### Got