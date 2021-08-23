import sqlite3
data=[]

def makeConnection():
    conn = sqlite3.connect('data.db')
    return conn

def createTable(conn):
    createQuery = '''CREATE TABLE IF NOT EXISTS
    table_stock (ID TEXT PRIMARY KEY, Name TEXT, Colour TEXT, Year TEXT,Qty INTEGER, Last_Added TEXT,Last_Removed TEXT);'''
    conn.execute(createQuery)

def showStock(conn):
    showQuery='''SELECT * from table_stock ORDER BY qty;'''
    cursor = conn.execute(showQuery)
   
    for row in cursor:
          #print('ID = {}, Name = {}, Colour = {}, Year = {}, Qty = {},Last_Added={},Last_Removed={} '.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
          array =[row[0],row[1],row[2],row[3],row[4],row[5],row[6]]
          data.append(array)
    return data
          
def stockPresent(conn,Id):
    presQuery="SELECT COUNT(*) FROM table_stock WHERE ID='{}'".format(Id)
    cursor = conn.execute(presQuery)
    for row in cursor:
       if str(row[0]) == '1': return True
       else: return False

def deleteStock(conn,Id):
    delQuery="DELETE FROM table_stock WHERE ID='{}'".format(Id)
    conn.execute(delQuery)
    conn.commit()
    
def insertNewStock(conn, Id, name, colour, year, qty,last_added,last_removed):
    addQuery='''INSERT INTO table_stock VALUES('{}', '{}', '{}', '{}', {}, '{}', '{}')'''.format(Id, name, colour, year, qty, last_added, last_removed)
    conn.execute(addQuery)
    conn.commit()

def updateStock(conn, Id, addQty):
    updateQuery="UPDATE table_stock SET qty=qty+{} WHERE ID='{}'".format(addQty, Id)
    conn.execute(updateQuery)
    conn.commit()

def addStock(conn, Id, addQty,Last_Added):
    addingQuery="UPDATE table_stock SET qty=qty+{},Last_Added='{}' WHERE ID='{}'".format(addQty,Last_Added, Id)
    conn.execute(addingQuery)
    conn.commit()

def removeStock(conn, Id, addQty,Last_Removed):
    remQuery="UPDATE table_stock SET qty=qty+{},Last_Removed='{}' WHERE ID='{}'".format(addQty,Last_Removed, Id)
    conn.execute(remQuery)
    conn.commit()
    
def updateAllStock(conn,name,colour,year,Id):
    updateallQuery="UPDATE table_stock SET Name = '{}', Colour = '{}', Year = '{}' WHERE ID='{}'".format(name,colour,year,Id)
    conn.execute(updateallQuery)
    conn.commit()
