import os
if os.environ["PROD_OR_DEV"] == 'prod':
    from .prod import *
else:
    from .dev import *