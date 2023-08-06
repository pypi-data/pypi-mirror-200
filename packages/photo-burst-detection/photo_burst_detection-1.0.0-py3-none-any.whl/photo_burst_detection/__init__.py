import logging

from flask import Flask

from photo_burst_detection.scan import Scanner
from photo_burst_detection.conf import config

app = Flask(__name__)

app.config.update(config)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

scanner = Scanner(
    path=app.config.get('PHOTO_BURST_DETECTION_PATH'),
    logger=app.logger,
)

if 1 == 1:
    from photo_burst_detection import auth, views
