FROM localhost/myapp

COPY myapp.conf /etc/myapp.conf

EXPOSE 8001

ENTRYPOINT [ "/app/myapp", "--config=/etc/myapp.conf" ]