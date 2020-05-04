# Запуск тестов

Для того, чтобы запустить тесты, нужно выставить правильные
значения в .env файле. Для начала, нужно скопировать заготовку

```sh
cp .env.example .env
```


## Настроить linux:

#### поднять sshd демон на любом не дефолтном порту без выключения selinux и firewalld (0,5 балла)
```sh
# в server-edition fedora (которую я поднял в виртуалке)
# уже был установлен и запущен sshd, поэтому не нужно устанавливать
# и запускать его

# Сначала в конфиге меняем порт 
➜  ~  sudo vim /etc/ssh/sshd_config
# Port = 2222

# 22 не буду удалять, потому что потом захочу вернуть как было
➜  ~  sudo semanage port -a -t ssh_port_t -p tcp 2222

# Перечитываем конфиг
➜  ~  sudo systemctl reload sshd

# Открываем порт в фаерволе
# можно добавить --permanent, если нужно, чтобы
# после --reload сохранились изменения
➜  ~  sudo firewall-cmd --add-port=2222/tcp
```


####поднять nginx демон на любом не дефолтном порту без выключения selinux и firewalld (1,5 балла)

```sh
# установим nginx
➜  ~ sudo dnf install nginx

# Запускаем, проверяем, что запустился
➜  ~ sudo systemctl start nginx.service 
➜  ~ sudo systemctl status nginx.service
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
     Active: active (running) since Mon 2020-05-04 19:54:27 MSK; 3s ago
    Process: 30641 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
    Process: 30642 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
    Process: 30643 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
   Main PID: 30644 (nginx)
      Tasks: 3 (limit: 2326)
     Memory: 3.4M
        CPU: 42ms
     CGroup: /system.slice/nginx.service
             ├─30644 nginx: master process /usr/sbin/nginx
             ├─30645 nginx: worker process
             └─30646 nginx: worker process

May 04 19:54:27 localhost.localdomain systemd[1]: Starting The nginx HTTP and reverse proxy server...
May 04 19:54:27 localhost.localdomain nginx[30642]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
May 04 19:54:27 localhost.localdomain nginx[30642]: nginx: configuration file /etc/nginx/nginx.conf test is successful
May 04 19:54:27 localhost.localdomain systemd[1]: Started The nginx HTTP and reverse proxy server.

# Поменяем порт
➜  ~ sudo vim /etc/nginx/nginx.conf
    ... 
    server {
        listen       8080;
        listen       [::]:8080;
    ...

➜  ~ sudo systemctl reload nginx.service

➜  ~ sudo firewall-cmd --add-port=8080/tcp
success


    # C хостовой тачки можно потестить, что отдается тестовая страничка
    ➜  ~ curl -v http://192.168.122.221:8080

# Все ок, можно все вернуть как было

sudo firewall-cmd --reload 
```