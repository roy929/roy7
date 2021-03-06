import requests
import time

host_ip = input('please enter host IP')
flask_port = 5000
flask_url = f'http://{host_ip}:{flask_port}'


# server's ip and port
def print_info():
    print(f'server ip = {host_ip}')
    print(f'server port = {flask_port}')


print_info()


# if call not rejected returns True
def not_rejected(src, dst):
    data = {'src': src, 'dst': dst}
    r = requests.get(flask_url + '/check', data=data)
    return r.json()


# registered users
def user_lists():
    r = requests.get(flask_url + '/user_list')
    return r.json()  # r.status_code


# returns ip or 0 if user doesnt exist
def get_user_ip(name):
    data = {'name': name}
    r = requests.get(flask_url + '/get_ip', data=data)
    return r.json()  # r.status_code


# return true if user exists
def is_user(name):
    if get_user_ip(name):
        return True
    return False


# login
def login(name, password):
    data = {'name': name, 'password': password}
    r = requests.get(flask_url + '/login', data=data)
    if r.json() == 'True':
        return True
    return False


# register
def register(name, password):
    data = {'name': name, 'password': password}
    r = requests.post(flask_url + '/register', data=data)
    print(r.json())
    if r.json() == 'True':
        return True
    return False


# post calling
def call(src, dst):
    new_call = {'src': src, 'operation': 'calling', 'dst': dst}
    r = requests.post(flask_url + '/call', data=new_call)
    # print(r.json())  # r.status_code
    if r.json() == 'True':
        return True
    return False


# change to calling to call
def accept(src, dst):
    new_call = {'src': src, 'operation': 'call', 'dst': dst}
    r = requests.put(flask_url + '/accept', data=new_call)
    return r.json()
    # print(r.json())  # r.status_code


# check if a user is called
def look_for_call(dst):
    check_call = {'operation': 'calling', 'dst': dst}
    r = requests.get(flask_url + '/check', data=check_call)
    return r.json()  # returns src or ""


# returns name of calling user
def get_src_name(dst):
    name = look_for_call(dst)
    if name:
        return name


# check if call accepted or if call still alive
def is_in_chat(name):
    data = {'name': name}
    r = requests.get(flask_url + '/check', data=data)
    return r.json()


# when calling
def stop(name, operation):
    msg = {'name': name, 'operation': operation}
    r = requests.delete(flask_url + "/stop", data=msg)
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
    stop(my_name, 'call')
