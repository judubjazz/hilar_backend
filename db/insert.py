import sqlite3
import os

#
# class Blob:
#     """Automatically encode a binary string."""
#     def __init__(self, s):
#         self.s = s
#
#     def _quote(self):
#         return "'%s'" % sqlite3.encode(self.s)
path = '/home/ju/JetBrainsProjects/PycharmProjects/hilar/hilar/src/data/beige2_hat.jpeg'
with open(path, 'rb') as f:
  backDrop=sqlite3.Binary(f.read())

id=1
original_title="beige2 hat"
overview ='look at a beige hat'
vote_average=1
category = 'hat'
trending = 1
watched=1
connection = sqlite3.connect("/home/ju/JetBrainsProjects/PycharmProjects/hilar/hilar/db/database.db")

cursor = connection.cursor()
cursor.execute('insert into Product (id, original_title, overview,vote_average,backDrop, category, trending, watched) '
               'values (?,?,?,?,?,?,?,?)', (id, original_title, overview, vote_average,backDrop, category, trending, watched))

connection.commit()


