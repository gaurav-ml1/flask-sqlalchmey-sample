users = Table('users', metadata,
   Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
   Column('name', String(50)),
   Column('fullname', String(50)),
   Column('nickname', String(50))
)

ins = users.insert().values(name='Gaurav', fullname='Gaurav Kumar')

#str(ins)

#'INSERT INTO users (name, fullname) VALUES (:name, :fullname)'
