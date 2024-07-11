import os
import sqlalchemy
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
import time

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(cn, _):
	cursor = cn.cursor()
	cursor.execute('pragma page_size=4096;')
	cursor.execute('pragma journal_mode=WAL;')
	cursor.execute('pragma synchronous=NORMAL;')
	cursor.execute('pragma cache_size=1000000;')
	cursor.execute('pragma temp_size=MEMORY;')
	cursor.execute('pragma mmap_size=30000000000;')
	cursor.close()

class SQLite:

	def __init__(self, db_path, create=False, renew=False, read_only=True):
		self.db_path = db_path
		self.create = create
		self.renew = renew
		self.read_only = read_only
		if renew and os.path.exists(db_path):
			os.remove(db_path)
			for postfix in ['-shm', '-wal']:
				if os.path.exists(db_path + postfix):
					os.remove(db_path + postfix)

	def connect(self, base):
		cnstring = f'sqlite:///{self.db_path}'
		if self.read_only:
			cnstring == '?mode=ro'
		self.engine = sqlalchemy.create_engine(cnstring, echo=False)
		if self.create:
			base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		print(f'successfully connected to {self.db_path}.')

	def create_indexes(self, indexes):
		start_time = time.time()
		for index in indexes:
			index.create(bind=self.engine)
		print(f'finished creating indexes, took {int(time.time() - start_time)}s.')
	
	def optimize(self):
		with self.engine.connect() as cn:
			with cn.execution_options(isolation_level='AUTOCOMMIT'):
				start_time = time.time()
				cn.execute(text('PRAGMA analysis_limit;'))
				cn.execute(text('PRAGMA optimize;'))
				cn.execute(text('VACUUM'))
				print(f'finished optimizing the database, took {int(time.time() - start_time)}s.')
	
	def close(self):
		self.session.close()
		self.engine.dispose()
		print(f'successfully closed {self.db_path}.')