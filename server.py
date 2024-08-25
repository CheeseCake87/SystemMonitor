from flask import Flask, request

app = Flask(__name__)


@app.post('/')
def json_mon():
    data = request.json
    print(data['url'])
    print(data['interval'])
    print(data['uuid'])
    return {'ok': True}


if __name__ == '__main__':
    app.run(debug=True)
