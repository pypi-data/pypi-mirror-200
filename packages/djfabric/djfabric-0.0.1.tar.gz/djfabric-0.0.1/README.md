
# Deploy django project with fabric

### Installation
1. Add `djfabric` to `requirements.txt`
`.env` example:
```
DOMAIN=example.com
HOST=123.123.123.123
HOST_PASSWORD=123
PROJECT_NAME=proj
DB_NAME=projdb
DEV_EMAIL=pmaigutyak@gmail.com
CELERY=off
```

```fabfile.py``` example:
```

from djfabric.fab import setup, restart, deploy

setup()

```
