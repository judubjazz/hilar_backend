# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            # self.connection = sqlite3.connect('db/database.db')
            self.connection = sqlite3.connect('/home/ju/JetBrainsProjects/PycharmProjects/hilar/hilar/db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def create_user(self, username, state,salt, hashed_password, first_name, last_name, gender, phone, email):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select MAX(id) from Customer")
        id_customer = cursor.fetchone()[0]
        connection.execute(("insert into WebUser(username,state, salt, hash_password, id_customer)"
                            " values(?, ?, ?, ?, ?)"), (username, state, salt, hashed_password, id_customer))
        connection.commit()
        connection.execute(("insert into Customer(id,first_name, last_name, gender, phone, email)"
                            " values(?, ?, ?, ?, ?, ?)"), (id_customer, first_name, last_name, gender, phone, email))
        connection.commit()

    def get_user_login_info(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hash_password from WebUser where username=?"),
                       (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute(("insert into Sessions(id_session, username) "
                            "values(?, ?)"), (id_session, username))
        connection.commit()

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute("delete from Sessions where id_session=?",
                           (id_session,))
        connection.commit()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute("select username from Sessions where id_session=?",
                       (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def get_trending(self,):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from Product where trending=?",
                       (3,))
        #3 is the highest trending note
        datas = cursor.fetchall()
        if datas is None:
            return None
        else:
            return [(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]) for data in datas]

    def get_query(self,query):
        #if contains query
        query = "'%" + query + "%'"
        commande_sql = "select * from Product where original_title LIKE %s" %query
        cursor = self.get_connection().cursor()
        cursor.execute(commande_sql)
        #3 is the highest trending note
        datas = cursor.fetchall()
        if datas is None:
            return None
        else:
            return [(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]) for data in datas]

    def get_most_watched(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from Product where watched > 6")
        #3 is the highest trending note
        datas = cursor.fetchall()
        if datas is None:
            return None
        else:
            return [(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]) for data in datas]

    def get_recommanded_for_you(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from Product where watched > 6")
        #3 is the highest trending note
        datas = cursor.fetchall()
        if datas is None:
            return None
        else:
            return [(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]) for data in datas]