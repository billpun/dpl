# mac only
# please following this instruction to install eralchemy
# brew install graphviz
# python -m pip install \
#   --global-option=build_ext \
#   --global-option="-I$(brew --prefix graphviz)/include/" \
#   --global-option="-L$(brew --prefix graphviz)/lib/" \
#   pygraphviz
# pip install eralchemy
# change in eralchemy/eralchemy/sqla.py from
#   columns=[column_to_intermediary(col) for col in table.c._data.values()] to 
#   columns=[column_to_intermediary(col) for col in table.c._colset]
import sqlalchemy
from sqlalchemy import MetaData
from eralchemy import render_er

engine = sqlalchemy.create_engine('sqlite:///demo.db', echo=False)
metadata = MetaData()
metadata.reflect(bind=engine)

render_er(metadata, 'schema.png')