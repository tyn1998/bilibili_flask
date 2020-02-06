from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    print('something with no meaning.')
    print('test.')
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
