#! /home/xs026388/usr/bin/python
from wsgiref.handlers import CGIHandler
from list import app
CGIHandler().run(app)