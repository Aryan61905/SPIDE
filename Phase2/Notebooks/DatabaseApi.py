from conncect_db import connect_to_database

conn,cursor = connect_to_database("Main")

def getStats(select_v,table_v,where_v,val,order="DESC",num = 50):
    order_val = select_v if select_v != "*" else where_v

    cursor.execute(f"Select {select_v} from {table_v} where {where_v} = '{val}' ORDER BY {order_val} {order} LIMIT {num}")
    return [cursor.fetchall(),[description[0] for description in cursor.description]]

def getList(select_v,table_v):
    cursor.execute(f"Select Distinct {select_v} from {table_v}")
    return [cursor.fetchall(),[description[0] for description in cursor.description]]


def getOrderedStats(select_v,table_v,val,order="DESC",num = 5):
    cursor.execute(f"SELECT {select_v} FROM {table_v} ORDER BY {val} {order} LIMIT {num}")
    return cursor.fetchall()



def getBoxScoreStats(select_v,table_v,where_v,val,limit,order="ASC"):
    order_val = False
    query = f"SELECT {select_v} FROM {table_v} WHERE "
    while where_v:
        query += where_v.pop(0) + " = " +"'"+val.pop(0)+"'" +" AND "
    query=query[:-5]
    
    if order == "AVG":
        cursor.execute(query)
        return [cursor.fetchall(),[description[0] for description in cursor.description]]
    
    if order_val !=False:
        cursor.execute(query + f" ORDER BY {order_val} {order}")
    else:
        cursor.execute(query + f" ORDER BY Date {order}")
    return [cursor.fetchall(),[description[0] for description in cursor.description]]

def getBoxScoreStatsByDateRange(select_v,table_v,where_v,val,sd,ed,order="ASC"):
    order_val = select_v if select_v != "*" else False
    query = f"SELECT {select_v} FROM {table_v} WHERE "
    while where_v:
        query += where_v.pop(0) + " = " +'"'+val.pop(0)+'"' +" AND "
    query += "Date >= "+sd+ " AND Date <= "+ed
    #query=query[:-5]
    if order_val !=False:
        cursor.execute(query + f" ORDER BY {order_val} {order}")
    else:
        cursor.execute(query + f" ORDER BY Date {order}")
    return [cursor.fetchall(),[description[0] for description in cursor.description]]



   


#print(getBoxScore('Token','202310240DENVSLAL'))