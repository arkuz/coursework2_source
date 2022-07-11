import logging
from flask import Flask

from skyprogram.views import skyprogram_blueprint

logging.basicConfig(filename="log/log.log",
                    level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] - %(name)s -'
                           ' (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(skyprogram_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
