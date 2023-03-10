from gevent import monkey
monkey.patch_all()

from app import app_run

app = app_run()
