"""
Root WSGI Entrypoint for Render / Cloud Deployment
Forwards to backend/app.py so both `gunicorn app:app` and `python backend/app.py` work out of the box.
"""

import os
import sys

BACKEND_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
