from flask import Flask, request

app = Flask(__name__)


@app.post('/')
def json_mon():
    data = request.json
    print(data['system_id'])
    print(data['url'])
    print(data['interval'])
    print(data['windows_uuid'])
    print(data['epoch'])
    return {'ok': True}


if __name__ == '__main__':
    app.run(debug=True)
