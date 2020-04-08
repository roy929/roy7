import requests
import time
import socket

# host = 'DESKTOP-03A6E0A'
# host_name = 'DESKTOP-EVCG5AF'  # COMPUTER 2
# host_name = input("enter host name, flask_server prints it in run\r\n"
#                   "if flask runs on this PC type 'localhost'")
host = 'localhost'
host_ip = socket.gethostbyname(host)
flask_port = 5000
flask_url = f'http://{host_ip}:{flask_port}'


def print_info():
    # print(f'host_name = {host_name}')
    print(f'server ip = {host_ip}')
    print(f'server port = {flask_port}')


print_info()


# if call not rejected returns True
def not_rejected(src, dst):
    data = {'src': src, 'dst': dst}
    r = requests.get(flask_url + '/check', data=data)
    return r.json()


def user_lists():
    r = requests.get(flask_url + '/user_list')
    return r.json()  # r.status_code


# returns ip or 0 if user doesnt exist
def get_user_ip(name):
    data = {'name': name}
    r = requests.get(flask_url + '/get_ip', data=data)
    return r.json()  # r.status_code


def login(name, pas):
    data = {'name': name, 'password': pas}
    r = requests.get(flask_url + '/login', data=data)
    if r.json() == 'True':
        return True
    return False


def register(name, pas):
    data = {'name': name, 'password': pas}
    r = requests.post(flask_url + '/register', data=data)
    if r.json() == 'True':
        return True
    return False


# post calling
def call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'calling', 'dst': dst_name}
    r = requests.post(flask_url + '/call', data=new_call)
    # print(r.json())  # r.status_code
    if r.json() == 'True':
        return True
    return False


# change to calling to call
def accept(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'call', 'dst': dst_name}
    r = requests.put(flask_url + '/accept', data=new_call)
    return r.json()
    # print(r.json())  # r.status_code


def look_for_call(dst_name):
    check_call = {'operation': 'calling', 'dst': dst_name}
    r = requests.get(flask_url + '/check', data=check_call)
    return r.json()  # src name || ""


def get_src_name(dst_name):
    name = look_for_call(dst_name)
    if name:
        return name


# check if call accepted or if call still alive
def is_in_chat(name):
    data = {'name': name}
    r = requests.get(flask_url + '/check', data=data)
    return r.json()


# when calling
def stop_calling(name):
    msg = {'name': name, 'operation': 'calling'}
    r = requests.delete(flask_url + "/stop_call", data=msg)
    return r.json()  # r.status_code


# when in chat
def stop_chat(name):
    check_call = {'name': name, 'operation': 'call'}
    r = requests.delete(flask_url + "/stop_call", data=check_call)
    return r.json()  # r.status_code


if __name__ == '__main__':
    my_name = 'kkk'
    print(*user_lists(), sep='\n')
    while True:
        if look_for_call(my_name):
            break
    user = get_src_name(my_name)
    print(user)
    accept(my_name, user)

    time.sleep(7)
    stop_chat(my_name)
