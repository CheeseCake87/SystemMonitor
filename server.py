from flask import Flask, request

app = Flask(__name__)

REGISTERED_SYSTEMS = [
    "WIN-1",
    "WIN-2",
    "WIN-3",
    "WIN-4",
    "MAC-1",
    "LINUX-1"
]


@app.post('/')
def json_mon():
    data = request.json

    action = data.get('action')

    if action == 'check_url':
        return '', 202

    if action == 'check_system_id':

        print("Check System ID:", data['system_id'])

        print(REGISTERED_SYSTEMS)

        if data['system_id'] in REGISTERED_SYSTEMS:
            print("System ID exists")
            return '', 200

        print("System ID does not exist")
        return '', 204

    if action == 'send_stats':
        print(data['system_id'])
        print(data['url'])
        print(data['interval'])
        print(data['epoch'])
        return '', 200

    return '', 400


if __name__ == '__main__':
    app.run(debug=True)
