from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config.from_object('config')

# 因为view 里面引用了app所以要先放在这
import views

if __name__ == '__main__':
    app.run(debug=True)
