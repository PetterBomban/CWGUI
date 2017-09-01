from flask import Flask, flash, render_template, request
from clockwork import clockwork

app = Flask(__name__)
app.secret_key = ('devkey')

def send_msg(key, to, from_name, msg):
    api = clockwork.API(key)

    message = clockwork.SMS(
        to = to,
        message = msg,
        from_name = from_name
    )
    response = api.send(message)
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', response=None, error=None, key_check=False, key=None)
    else:
        key = request.form['key']
        to = request.form['to']
        from_name = request.form['from']
        msg = request.form['msg']
        error = None

        response = send_msg(key, to, from_name, msg)

        if not response.success:
            flash('Failed to send SMS!')
            error = response.error_message
        else:
            flash('Successfully sent sms!\n To: ' + str(to) + '\nMessage: ' + str(msg) + '\nFrom: ' + str(from_name) )

        return render_template('index.html', response=response, error=error, key_check=True, key=key)


if __name__ == '__main__':
    app.run()

