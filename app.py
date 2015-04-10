from flask import Flask, redirect, request, jsonify
import requests


app = Flask(__name__)
app.config.from_object('default_settings')
@app.route("/")
def hello():
    return "Hello world!"


@app.route("/no_auth")
def no_auth():
    g = requests.get("https://api.heroku.com/account")
    return g.content

@app.route("/with_auth")
def with_auth():
    client_id = app.config['HEROKU_KEY']
    return redirect("https://id.heroku.com/oauth/authorize?"+
                    "client_id={0}".format(client_id)+
                    "&response_type=code&scope=global"+
                    "&redirect_uri = /oauth_callback")

@app.route("/oauth_callback")
def oauth_callback():
    code = request.args.get("code")
    param = {'code': code, 'client_secret': app.config['HEROKU_SECRET'], 'grant_type': "authorization_code"}
    r = requests.post("https://id.heroku.com/oauth/token", param)
    json = r.json()
    token = json['access_token']
    header = {'Authorization': "Bearer {0}".format(token)}
    g = requests.get("https://api.heroku.com/account", headers=header)
    return g.content

if __name__ == "__main__":
    app.run(port=5001)





