#!/usr/bin/env python

import os
from application.views import app

app.run(host="0.0.0.0", port=int(os.environ['PORT']), debug=True)
