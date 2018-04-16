import http.client
import json
from flask import Flask, request, make_response,redirect, jsonify 
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import urllib.parse
import http.client
import json
# from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__, static_url_path='')

app.config['SECRET_KEY'] = 'some-secret-key'

CLIENT_ID = '77kxpwre3m9i0m';
REDIRECT_URI = 'http://localhost:5000/auth'
STATE = 'DCEeFWf45A53sdfKef424'
SCOPE ="r_basicprofile,r_emailaddress,rw_company_admin,w_share"
CLIENT_SECRET = '44qvGIDPiLWmgqi9'
FIELDS = ':(id,firstName,headline,lastName,apiStandardProfileRequest,num-connections,picture-url,location,industry,current_share,summary,specialties,positions,public-profile-url)'


def goto_auth():
	params = {'response_type': 'code', 'client_id':CLIENT_ID, 'redirect_uri':REDIRECT_URI, 'state':STATE,'scope':SCOPE}
	url_encoded = urllib.parse.urlencode(params)
	print("URL encoded:{0}".format(url_encoded))
	URI = "https://www.linkedin.com/oauth/v2/authorization?{0}".format(url_encoded)
	print(URI)
	return URI


@app.route("/", methods=['GET'])
def index():
	return app.send_static_file('index.html')

@app.route("/integration")
def integrate_linkedin():
	URI = goto_auth()
	return redirect(URI)

@app.route("/auth")
def auth():
	code = request.args.get("code")
	state = request.args.get("state")
	if state == STATE:
		headers = {"Content-type": "application/x-www-form-urlencoded"}	
		params = urllib.parse.urlencode({'grant_type':'authorization_code', 'code':code, 'redirect_uri': REDIRECT_URI, 'client_id':CLIENT_ID, 'client_secret': CLIENT_SECRET})
		conn = http.client.HTTPSConnection("www.linkedin.com") 
		conn.request("POST","/oauth/v2/accessToken", body=params, headers=headers)
		response = conn.getresponse()
		access_object =json.loads(response.read())
		if "access_token" not in access_object:
			return redirect(goto_auth())

		# return jsonify(access_object)
		conn = http.client.HTTPSConnection('api.linkedin.com')
		headers = {"Authorization":"Bearer {0}".format(access_object["access_token"])}
		conn.request("GET","/v1/people/~{0}?format=json".format(FIELDS), headers=headers)
	
		response = conn.getresponse()
		profile_info = json.loads(response.read())
		return render_template("profile.html", profile_info=profile_info)
	else:
		return redirect(goto_auth)


