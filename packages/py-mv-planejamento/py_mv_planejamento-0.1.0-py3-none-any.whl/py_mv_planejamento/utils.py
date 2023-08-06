import pymssql

mssql = dict


def mssql_exec(db_config: mssql, sql: str, params: tuple = None):
    conn = pymssql.connect(**db_config)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(sql, params)
    conn.commit()
    result = {
        "rowcount": cursor.rowcount,
        "identity": cursor.lastrowid,
    }
    conn.close()
    return result


def mssql_get_list(db_config: mssql, sql: str, params: tuple = None):
    conn = pymssql.connect(**db_config)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result


def mssql_get_one(db_config: mssql, sql: str, params: tuple = None):
    conn = pymssql.connect(**db_config)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(sql, params)
    row = cursor.fetchone()
    conn.close()
    return row
