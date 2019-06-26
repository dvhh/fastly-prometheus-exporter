'''
HTTP Endpoint to serve `metrics.txt` on `/metrics`
'''
from os.path import getmtime
from time import time

from flask import Flask, send_file, request, make_response


app = Flask(__name__)


@app.route('/status')
def get_status():
    '''
    App status
    '''
    current = time()
    for file in ('metrics.txt', 'metrics.txt.gz'):
        assert (current - getmtime(file)) < 30, 'outdated '+file
    return 'OK'


@app.route('/metrics')
def serve_metrics():
    '''
    Route to serve metrics.txt
    '''
    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' not in accept_encoding.lower():
        return send_file("metrics.txt")
    response = make_response(send_file("metrics.txt.gz"))
    response.headers['Content-Encoding'] = 'gzip'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
