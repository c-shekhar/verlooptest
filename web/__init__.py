from flask import Flask

app = Flask(__name__)
app.secret_key = 'You will never guess'

import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.setLevel(logging.ERROR)
logger.addHandler(handler)


from web import server