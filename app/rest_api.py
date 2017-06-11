import sqlite_db, json
from flask import Flask, jsonify, request

app = Flask (__name__)

def status_400(param):
	return json.dumps({ "status": "400", "message" : "Parameter required: "+param }), 400

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    type = request.args.get('type', None)

    if 'order_by' in request.args:
        order_by = request.args.get('order_by')

        print type
        print order_by

        return json.dumps(sqlite_db.get_submissions(type, order_by))
    else:
        return status_400('order_by')

if __name__ == "__main__":
    app.run()
