import flask
from flask import Flask

app = Flask(__name__)


@app.route('/myip')
def hello():
	return f"<p>{flask.request.environ['HTTP_X_FORWARDED_FOR']}</p>"
app.run(debug=True)