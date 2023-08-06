import pymssql
from utils import mssql_exec, mssql_get_list, mssql_get_one

mssql = dict


def get_list(db_config: mssql):
    qry_grupos_planejamento = """
        SELECT CodigoGrupoPlanejamento, Comprador, NomeLinha, NomeGrupo, Ativo, VendaQt_12M, VendaPV_12M, NomeChave
        FROM Compras.VwGrupoPlanejamento
        ORDER BY 2,3,4
        """
    return mssql_get_list(db_config, qry_grupos_planejamento)


def get_one(db_config: mssql, codigo: int):
    qry = """
        SELECT CodigoGrupoPlanejamento, Comprador, NomeLinha, NomeGrupo, Ativo, Detalhes
        FROM Compras.GrupoPlanejamento
        WHERE CodigoGrupoPlanejamento = %d
        """
    params = (codigo,)
    return mssql_get_one(db_config, qry, params)


def create(
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


def update(
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


def delete(db_config: mssql, codigo: int):
    qry_delete = """
      DELETE FROM Compras.GrupoPlanejamento WHERE CodigoGrupoPlanejamento = %d
    """
    params = (codigo,)
    return mssql_exec(db_config, qry_delete, params)
