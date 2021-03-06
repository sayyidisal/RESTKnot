import yaml, os,hashlib
from app import root_dir
from datetime import datetime
import json, requests

def timeset():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()

def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            listdir.append(os.path.join(root, file))
    return listdir

def repoknot():
    abs_path = root_dir
    repo_file = "{}/static/templates/knot.yml".format(abs_path)
    return yaml_parser(repo_file)

def repodata():
    abs_path = root_dir
    repo_file = "{}/static/templates/endpoint.yml".format(abs_path)
    return yaml_parser(repo_file)

def repodefault():
    abs_path = root_dir
    repo_file = "{}/static/templates/default.yml".format(abs_path)
    return yaml_parser(repo_file)

def get_command(req):
    command = req.split("/")
    command = command[2]
    return command

def get_tag():
    return hashlib.md5(str(timeset()).encode('utf-8')).hexdigest()

# def tag_measurement(data):
#     for i in data:
#         measurement = i['measurement']
#         tags = i['tags']
#     return measurement, tags

def send_http(url, data, headers=None):
    json_data = json.dumps(data)
    send = requests.post(url, data=json_data, headers=headers)
    respons = send.json()
    try:
        data = json.loads(respons['data'])
    except Exception as e:
        print(e)
        print(url)
        print(respons)
        raise
    else:
        respons['data'] = data
    return respons

def change_state(field, field_value, state):
    data_state = {
        "where":{
            field : str(field_value)
        },
        "data":{
            "state" : str(state)
        }
    }
    return data_state