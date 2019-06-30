import connect


class TestConnect():


    def test_query(self):
        database = 'wallet.db'
        connection = connect.Database()
        connection.open_connect(database)
