Jenkins я поднял в виртуалке.

# Собираем/подгружаем образы
```
podman load -i myapp.dockerimage
podman tag myapp myapp-base
podman build -t vkapi --file dockerfiles/vkapi/Dockerfile vkapi
podman build -t myapp --file dockerfiles/myapp/Dockerfile dockerfiles/myapp
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
podman run -d --pod qa-project --name myapp myapp

# вкапи. Токен нужно взять из настроек приложения
podman run -d --pod qa-project --name vkapi -e VK_API_TOKEN=$VK_API_TOKEN vkapi
```

После того, как все поднялось, можно проинитить базу
```
podman exec myapp /app/myapp --config=/etc/myapp.conf --setup
```

# Что показалось странным:

* Пароли не стоит хранить в открытом виде. Нужно хэшировать + солить.
* Удаление пользователя методом GET, скорее всего, это должен быть метод DELETE
* В базе для username не стоит not null. Для active и access тоже
* active access должны быть типа bool
* странно, что пользователь может сам себя заблокировать
* странно, что валидация полей пользователя на фронте и через апишку разные
* в логах приложения палятся пароли пользователей
* разныя валидация длинн логинов

# Баги:

* При регистрации пользователя с почтой, на которую уже есть аккаунт, возвращается 500
* Перепутаны коды ответов 210 вместо 201
* можно положить zero-byte в базу. С питончиком это явно не проэксплуатировать, но если бы наш сервис общался с каким-нибдудь сишным сервисом, это могло бы где-то выстрелить
* Местами в апишке нет валидации на максимальную длинну поля
* Пользовавтель может заблокировать сам себя


```
echo -ne 'username=mramirez\x0012312123&password=mramirez&submit=Login' > /tmp/login 
curl 'http://localhost:8001/login' -H 'Content-Type: application/x-www-form-urlencoded' --data-binary '@/tmp/login' -v 1>/dev/null
```
