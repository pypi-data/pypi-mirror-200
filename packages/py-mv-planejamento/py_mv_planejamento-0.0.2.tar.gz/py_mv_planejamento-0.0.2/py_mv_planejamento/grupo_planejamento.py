import pymssql
from utils import mssql_exec

mssql = dict


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
