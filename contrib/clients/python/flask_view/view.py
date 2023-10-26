from flask import Flask, request, jsonify, redirect, render_template
from contrib.clients.python.service import SSOAgent

app = Flask(__name__)
SSO_API_KEY = None
SSO_API_SECRET = None

@app.route("/login")
def login_page():
    sso_authentication_route = SSOAgent(SSO_API_KEY).authentication_route
    return render_template('index.html', sso_authentication_route=sso_authentication_route)


@app.route('/sso/callback/', methods=['GET'])
def sso_callback():
    if request.args.get('state') != 'SUCCESS':
        return jsonify({'state': 'UNVERIFIED'}), 400

    # Replace this with your actual SSO logic, for example using an SSO library
    sso = SSOAgent(SSO_API_KEY, SSO_API_SECRET, token=request.args.get('auth_token'))
    auth = sso.get_user_details()

    if auth is None:
        return jsonify({'state': 'UNVERIFIED'}), 400

    # Handle whatever you want here
    return jsonify({'state': 'VERIFIED'})


if __name__ == '__main__':
    app.run()
