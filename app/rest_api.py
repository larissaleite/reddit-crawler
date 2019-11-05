import sqlite_db as db, json
from flask import Flask, jsonify, request

app = Flask (__name__)

def status_400(message):
	return json.dumps({ "status": "400", "message" : message }), 400

@app.route('/api/tags', methods=['GET'])
def get_tags():
    username = request.args.get('username')
    if username == '':
        return status_400("Invalid username")
    return json.dumps(db.get_tags(username))

@app.route('/api/tags', methods=['PUT'])
def put_tags():
    username = request.args.get('username')
    tag = request.args.get('tag')
    if not username or not tag:
        return status_400("Invalid username or tag")
    db.put_tag(username, tag)
    return ""

@app.route('/api/tag_submission', methods=['PUT'])
def put_tag_submission():
    submission_id = request.args.get('submission_id')
    tag_id = request.args.get('tag_id')
    if not submission_id or not tag_id:
        return status_400("Invalid submission or tag")
    db.put_submission_tag(submission_id, tag_id)
    return ""

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
	type = request.args.get('type', None)

	if 'order_by' in request.args:
		order_by = request.args.get('order_by')

		if order_by != 'num_comments' and order_by != 'punctuation':
			return status_400("Invalid value for parameter: order_by. Valid values: num_comments, punctuation")

		return json.dumps(db.get_submissions(type, order_by))
	else:
		return status_400("Parameter required: order_by")

@app.route('/api/users', methods=['GET'])
def get_users():
	if 'order_by' in request.args:
		order_by = request.args.get('order_by')

		if order_by == 'num_comments': return json.dumps(db.get_top_commenters())
		if order_by == 'num_submissions': return json.dumps(db.get_top_submitters())
		if order_by == 'value' : return json.dumps(db.get_most_valued_users())

		return status_400("Invalid value for parameter: order_by. Valid values: num_comments, num_submissions, value")
	else:
		return status_400("Parameter required: order_by")

@app.route('/api/users/<username>/submissions', methods=['GET'])
def get_submissions_by_user(username):
	submissions = db.get_submissions_by_submitter(username)
	return json.dumps(submissions)

@app.route('/api/users/<username>/comments/parent_submission', methods=['GET'])
def get_submissions_commented_by_user(username):
	submissions = db.get_submissions_commented_by_user(username)
	return json.dumps(submissions)

if __name__ == "__main__":
	db.create_schema_db()

	app.run()
