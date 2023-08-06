import pymssql

mssql = dict


def mssql_exec(db_config: mssql, sql: str, params: tuple):
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
