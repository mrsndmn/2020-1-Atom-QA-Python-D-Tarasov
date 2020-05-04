import threading

from flask import Flask, abort, request

app = Flask(__name__)

users = {}
# users = {'1': {'name': 'Ilya', 'surname': 'Kirillov', 'nick': 'root'}}

def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    print('app started')
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()

# контроллер, который будет для тестов данные сохранять в словарь
@app.route('/user/<user_id>', methods=['POST'])
def set_user_by_id(user_id: int):
    if int(user_id) <= 0:
        abort(400)

    users[str(user_id)] = request.get_json()
    return {'status': "ok"}

# получаем пользователя по id
@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id: int):
    if int(user_id) <= 0:
        abort(400)

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
    if int(user_id) <= 0:
        abort(400)

    user = users.get(str(user_id), None)
    if user:
        user['nick'] = request.get_json()['nick']
        return user
    else:
        abort(404)
    return

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_mock()

if __name__ == '__main__':
    run_mock('127.0.0.1', 5000)