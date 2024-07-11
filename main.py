from database import SQLite
from entities_ana import *
from utils import *

db = SQLite('demo_ana.db', create=True, renew=True, read_only=False)
db.connect(Base)

db.close()