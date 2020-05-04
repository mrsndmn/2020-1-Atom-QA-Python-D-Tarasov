import threading

from flask import Flask, abort, request

app = Flask(__name__)

users = {'1': {'name': 'Ilya', 'surname': 'Kirillov', 'nick': 'root'}}
host = '127.0.0.1'
port = 5000

def run_mock():
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()

# контроллер, который будет для тестов данные сохранять в словарь
@app.route('/user/<user_id>', methods=['POST'])
def set_user_by_id(user_id: int):
    users[str(user_id)] = request.get_json()
    return None

# получаем пользователя по id
@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    user = users.get(str(user_id), None)
    if user:
        print(user)
        return user
    else:
        abort(404)

    return


# устанавливаем пользователю ник
# пусть, у нас несколько пользователей могут иметь один ник))
@app.route('/nick/<user_id>', methods=['POST'])
def set_nick_to_user_by_id(user_id: int):
    user = users.get(str(user_id), None)
    if user:
        print(user)
        return user
        user['nick'] = request.get_json()['nick']
    else:
        abort(404)
    return

@app.route('/shutdown')
def shutdown():
    shutdown_mock()


if __name__ == '__main__':
    run_mock()