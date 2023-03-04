import psycopg2
from psycopg2.errors import SerializationFailure
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import requests
import json
from utility.notify import notication
#git

app = Flask(__name__)
CORS(app)
# conn = psycopg2.connect('postgres://hardik:iN-6Xm5osjOis_We@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/silent-hare-1420.defaultdb?sslmode=verify-full&sslrootcert=app/cc-ca.crt')
conn = psycopg2.connect('postgresql://raj:rcENwdc-uBys7rMnov6Raw@shadow-amoeba-2449.7s5.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=app/cc-ca.crt')
cur = conn.cursor()
a =cur.execute("use defaultdb")
print(cur)

@app.route("/insertCall",methods=['POST'])
def insertCall():
	values=request.get_json()
	print(values)
	if(not values):
		response={'msg':'data not found'}
		print(response)
		return jsonify(response), 400

	query = "INSERT INTO call_log values"
	for val in values:
		print(val)
		query += "('{num}','{name}','{duration}','{type}','{datetime}'),".format(num=val['number'],name=val['name'],duration=val['duration'],type=val['type'],datetime=val['datetime'])
	query = query[0:-1]
	print(query)
	res = cur.execute(query)
	conn.commit()
	if(not res):
		response={'msg':'success'}
		return jsonify(response), 200
	else:
		response={'msg':'insertion fail'}
		print(response)
		return jsonify(response), 400

@app.route("/login",methods=['POST'])
def login():
	values=request.get_json()
	if(not values):
		response={'msg':'data not found'}
		print(response)
		return jsonify(response), 400

	required=['username','password']
	if not all(key in values for key in required):
		response={'msg':'invalid credentials'}
		print(response)
		return jsonify(response), 400

	query = "SELECT * from Users where username = '{username}'".format(username=values['username'])
	res = cur.execute(query)
	a = cur.fetchone()
	conn.commit()
	if(not res):
		response={'username':a[0],'password':a[1],'email_mobile':a[2],'usertype':a[3]}
		print(response)
		return jsonify(response), 200
	else:
		response={'msg':'insertion fail'}
		print(response)
		return jsonify(response), 400


@app.route("/signup",methods=['POST'])
def signup():
	values=request.get_json()
	if(not values):
		response={'msg':'data not found'}
		print(response)
		return jsonify(response), 400

	required=['username','password','userType','email_mobile']
	if not all(key in values for key in required):
		response={'msg':'invalid credentials'}
		print(response)
		return jsonify(response), 400

	query = "INSERT INTO Users values ('{username}','{password}','{email_mobile}','{userType}');".format(username=values['username'],password=values['password'],email_mobile=values['email_mobile'],userType=values['userType'])
	print(query)
	res = cur.execute(query)
	conn.commit()
	if(not res):
		response={'msg':'success'}
		return jsonify(response), 200
	else:
		response={'msg':'insertion fail'}
		print(response)
		return jsonify(response), 400

@app.route("/getCall",methods=['POST'])
def getCall():
	query = "select num,name,duration,type,datetime from call_log;"
	print(query)
	res = cur.execute(query)
	list_dict = []
	temp_dict = { }
	for record in cur:
		temp_dict['number'] = record[0]
		temp_dict['name'] = record[1]
		temp_dict['duration'] = record[2]
		temp_dict['type'] = record[3]
		temp_dict['datetime'] = record[4]
		temp_dict = { }
		list_dict.append(temp_dict)
	print(list_dict)
	tup = cur.fetchone()
	conn.commit()
	if(not res):
		response = list_dict
		print(response)
		return jsonify(response), 200
	else:
		response={'msg':'insertion fail'}
		print(response)
		return jsonify(response), 400

@app.route("/SendCall",methods=['POST'])
def SendCall():
	values=request.get_json()
	print(values)
	required=['number']
	if not bool(values):
		response = {'message':'less required values'}
		print(response)
		return jsonify(response), 400

	query = "select * from call_log where num = '{num}'".format(num=values)
	print(query)
	res = cur.execute(query)
	call = cur.fetchone()
	print(call)
	conn.commit()
	notication(call)
	if(not res):
		response={'msg':'success'}
		return jsonify(response), 200
	else:
		response={'msg':'insertion fail'}
		print(response)
		return jsonify(response), 400

serverToken = 'AAAAaIC2NFQ:APA91bFUn4sxpJJnaHAECR55PIe4C97lCF3GZGLe7ekq5s44sSN57lhDzWd7QYegi1l0nVk0dA47Cnh37WDRWnRhPavsCKVA7h3yy-lR2sghcNuuM-dqmJttFQEtX8ZWSZBgCeCqz9Al'
deviceToken = 'eGj79qVTS7iRx5X3x-07GQ:APA91bE94E2HTLuJ4hpfRGzKhtDc_W9k6TAPgMDMoyLznFTaxYIQdDUQBIv9dtZ9gu_Zrih0I9pDHtIIPT9WRyrG217uYIZJPz04eLmNFv-JDkz_gq23ID-t0ToHh9ZZDXnhNVBjz2LS'

headers = {
    'Content-Type':'application/json',
    'Authorization':'key='+serverToken
}
def notication(callObj):
    print(callObj)
    body = {
        'notication': {
        'title':'Call Arrived',
        'body':'new Call'
        },
        'to':deviceToken,
        'priority':'high'
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)
    print(response.json)
    '''headers ={
    	'Content-Type':'application/json'
    }
    body = {
    	'0':{
    		'number':callObj['number'],
    		'name':callObj['name'],
    		'duration':callObj['duration']
    		'type':callObj['type']
    		'datetime':callObj['datetime']
    	}
    }
    response = requests.post("http://0.0.0.0/insertCall",headers = headers, data=json.dumps(body))
    print(response.status_code)
    print(response.json)'''