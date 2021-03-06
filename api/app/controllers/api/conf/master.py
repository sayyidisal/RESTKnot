from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app.libs import utils
from app.models import model as db
import os
from app.middlewares.auth import login_required



class MasterData(Resource):
    @login_required
    def get(self):
        command = utils.get_command(request.path)
        command = "cs_"+command
        try:
            results = db.get_all(command)
            obj_userdata = list()
            for i in results :
                data = {
                    "id_master": str(i['id_master']),
                    "nm_slave": i['nm_master'],
                    "ip_master": i['ip_master'],
                    "port": i['port']
                }
                obj_userdata.append(data)
        except Exception:
            results = None
        else:
            return response(200, data=obj_userdata)

    @login_required
    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        command = "cs_"+command
        init_data = cmd.parser(json_req,command)
        respons = dict()
        if init_data['action'] == 'insert':
            table = init_data['data'][0]['table']
            fields = init_data['data'][0]['fields']
            try:
                result = db.insert(table,fields)
            except Exception as e:
                respons = {
                "status" : False,
                "error"	 : str(e)
                }
            else:
                respons = {
                "status": True,
                "messages": "Fine!",
                "id": result
                }
            finally:
                return response(200,data=fields,message=respons)

        if init_data['action'] == 'where':
            obj_userdata = list()
            table = ""
            fields = ""
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
                for a in tags:
                    if tags[a] is not None:
                        fields = a
            try:
                result = db.get_by_id(table,fields,tags[fields])

            except Exception as e:
                respons = {
                "status" : False,
                "messages": str(e)
                }
            else:
                for i in result:
                    data = {
                    "id_master": str(i['id_master']),
                    "nm_master": i['nm_master'],
                    "ip_master": str(i['ip_master']),
                    "port":	str(i['port'])
                    }
                    obj_userdata.append(data)
                respons = {
                "status": True,
                "messages": "Success"
                }
            finally:
                return response(200,data=obj_userdata, message=respons)

        if init_data['action'] == 'remove':
            table = ""
            tags = dict()
            fields = ""
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
            fields = str(list(tags.keys())[0])
            if not isinstance(tags[fields],str) :
                tags[fields] = str(tags[fields])
            try:
                result = db.delete(table,fields,tags[fields])
            except Exception as e:
                respons = {
                "status": False,
                "messages": str(e)
                }
            else:
                respons = {
                "status": result,
                "messages": "data is removed"
                }
            finally:
                return response(200,data=tags,message=respons)

class MasterNotify(Resource):
    @login_required
    def get(self):
        command = utils.get_command(request.path)
        command = "cs_"+command
        try:
            results = db.get_all(command)
            obj_userdata = list()
            for i in results :
                data = {
                "id_master": str(i['id_master']),
                "id_notify_master": str(i['id_notify_master']),
                "id_zone": str(i['id_zone'])
                }
                obj_userdata.append(data)
        except Exception:
            results = None
        else:
            return response(200, data=obj_userdata)
  
    @login_required
    def post(self):

        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        command = "cs_"+command
        init_data = cmd.parser(json_req,command)
        respons = dict()

        if init_data['action'] == 'insert':
            table = init_data['data'][0]['table']
            fields = init_data['data'][0]['fields']
            try:
                result = db.insert(table,fields)
            except Exception as e:
                respons = {
                "status" : False,
                "error"	 : str(e)
                }
            else:
                respons = {
                "status": True,
                "messages": "Fine!",
                "id": result
                }
            finally:
                return response(200,data=fields,message=respons)

        if init_data['action'] == 'where':
            obj_userdata = list()
            table = ""
            fields = ""
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
                for a in tags:
                    if tags[a] is not None:
                        fields = a
            try:
               result = db.get_by_id(table,fields,tags[fields])

            except Exception as e:
                respons = {
                "status" : False,
                "messages": str(e)
                }
            else:
                for i in result:
                    data = {
                    "id_master": str(i['id_master']),
                    "id_notify_master": str(i['id_notify_master']),
                    "id_zone": str(i['id_zone'])
                    }
                    obj_userdata.append(data)
                respons = {
                "status": True,
                "messages": "Success"
                }
            finally:
                return response(200,data=obj_userdata, message=respons)

        if init_data['action'] == 'remove':
            table = ""
            tags = dict()
            fields = ""
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
            fields = str(list(tags.keys())[0])
            try:
                result = db.delete(table,fields,tags[fields])
            except Exception as e:
                respons = {
                "status": False,
                "messages": str(e)
                }
            else:
                respons = {
                "status": result,
                "messages": "data is removed"
                }
            finally:
                return response(200,data=tags,message=respons)


class MasterACL(Resource):
    @login_required
    def get(self):
        command = utils.get_command(request.path)
        command = "cs_"+command
        try:
            results = db.get_all(command)
            obj_userdata = list()
            for i in results :
                data = {
                    "id_master": i['id_master'],
                    "id_acl_master": i['id_acl_master'],
                    "id_zone": i['id_zone']
                }
                obj_userdata.append(data)
        except Exception:
            results = None
        else:
            return response(200, data=obj_userdata)


    @login_required  
    def post(self):

        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        command = "cs_"+command
        init_data = cmd.parser(json_req,command)
        respons = dict()

        if init_data['action'] == 'insert':
            table = init_data['data'][0]['table']
            fields = init_data['data'][0]['fields']
            try:
                result = db.insert(table,fields)
            except Exception as e:
                respons = {
                "status" : False,
                "error"	 : str(e)
                }
            else:
                respons = {
                "status": True,
                "messages": "Fine!",
                "id": result
                }
            finally:
                return response(200,data=fields,message=respons)

        if init_data['action'] == 'where':
            obj_userdata = list()
            table = ""
            fields = ""
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
                for a in tags:
                    if tags[a] is not None:
                        fields = a
            try:
                result = db.get_by_id(table,fields,tags[fields])

            except Exception as e:
                respons = {
                "status" : False,
                "messages": str(e)
                }
            else:
                for i in result:
                    data = {
                    "id_master": str(i['id_master']),
                    "id_acl_master": str(i['id_acl_master']),
                    "id_zone": str(i['id_zone'])
                    }
                    obj_userdata.append(data)
                respons = {
                "status": True,
                "messages": "Success"
                }
            finally:
                return response(200,data=obj_userdata, message=respons)

        if init_data['action'] == 'remove':
            table = ""
            tags = dict()
            fields = ""
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
            fields = str(list(tags.keys())[0])
            try:
                esult = db.delete(table,fields,tags[fields])
            except Exception as e:
                respons = {
                "status": False,
                "messages": str(e)
                }
            else:
                respons = {
                "status": result,
                "messages": "data is removed"
                }
            finally:
                return response(200,data=tags,message=respons)