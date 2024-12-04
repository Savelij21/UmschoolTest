from sqlalchemy import Table, MetaData, Column, BigInteger, String

metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('tg_id', BigInteger, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
)
