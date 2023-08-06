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


def grupo_insert(
    db_config: mssql,
    comprador: str,
    nome_linha: str,
    nome_grupo: str,
    detalhes: str,
    ativo: int,
):
    qry_insert = """
      INSERT INTO Compras.GrupoPlanejamento (Comprador, NomeLinha, NomeGrupo, Detalhes, Ativo)
      VALUES (%s, %s, %s, %s, %d)
    """
    params = (comprador, nome_linha, nome_grupo, detalhes, ativo)
    return mssql_exec(db_config, qry_insert, params)


def grupo_update(
    db_config: mssql,
    codigo: int,
    comprador: str,
    nome_linha: str,
    nome_grupo: str,
    detalhes: str,
    ativo: int,
):
    qry_update = """
        UPDATE Compras.GrupoPlanejamento
        SET 
            Comprador = %s
            , NomeLinha = %s
            , NomeGrupo = %s
            , Detalhes = %s
            , Ativo = %d
        WHERE CodigoGrupoPlanejamento = %d
        """
    params = (comprador, nome_linha, nome_grupo, detalhes, ativo, codigo)
    return mssql_exec(db_config, qry_update, params)


def grupo_delete(db_config: mssql, codigo: int):
    qry_delete = """
      DELETE FROM Compras.GrupoPlanejamento WHERE CodigoGrupoPlanejamento = %d
    """
    params = (codigo,)
    return mssql_exec(db_config, qry_delete, params)
