# from eloquent import DatabaseManager
# from eloquent import Model

# config = {
#     'mysql': {
#         'driver': 'mysql',
#         'host': 'localhost:33060',
#         # 'port': 33060,
#         'database': 'aauuss',
#         'username': 'homestead',
#         'password': 'secret',
#         # 'charset': 'utf8',
#         'prefix': ''
#     }
# }

# database = DatabaseManager(config)
# database.set_default_connection('mysql')
# Model.set_connection_resolver(database)

# class Source(Model):
#     pass

# database.select('select * from posts')
####
# from eloquent import DatabaseManager, Model

# config = {
#     'mysql': {
#         'driver': 'mysql',
#         'host': 'localhost:33060',
#         'port': 33060,
#         'database': 'aauuss',
#         'user': 'homestead',
#         'passwd': 'secret',
#         'charset': 'utf8',
#         'prefix': ''
#     }
# }


# db = DatabaseManager(config)
# Model.set_connection_resolver(db)
# db.set_default_connection('mysql')

# class Source(Model):
#     pass

# source = Source.all()

from eloquent import DatabaseManager, Model

config = {
    'default': 'mysql',
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'port': 33060,
        'database': 'aauuss',
        'user': 'homestead',
        'password': 'secret',
        'prefix': ''
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)

class Source(Model):
    pass

source = Source.all()

