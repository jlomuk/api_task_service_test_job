import sqlalchemy as sq


meta = sq.MetaData()


task = sq.Table(
    'task',
    meta,
    sq.Column('id', sq.Integer, primary_key=True),
    sq.Column('title', sq.String, nullable=False),
    sq.Column('completed', sq.Boolean, default=False),
    sq.Column('user_id', sq.Integer, index=True, nullable=False),
    sq.Column('username', sq.String, nullable=False),
)