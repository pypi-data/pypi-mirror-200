from .utils import mssql_exec, mssql_get_list, mssql_get_one

mssql = dict


def get_list(
    db_config: mssql,
    codigo_grupo_planejamento: int,
):
    qry = """
        SELECT CodigoGrupoPlanejamentoProduto
            , CodigoGrupoPlanejamento
            , CodigoDepartamento
            , NomeDepartamento
            , CodigoClassificacao
            , NomeClassificacao
            , GrupoModeloMaterial
            , VendaQt_12M
            , VendaPV_12M
        FROM Compras.VwGrupoPlanejamentoProduto
        WHERE CodigoGrupoPlanejamento = %d
        """
    return mssql_get_list(
        db_config,
        qry,
        (codigo_grupo_planejamento,),
    )


def create(
    db_config: mssql,
    codigo_grupo_planejamento: int,
    codigo_departamento: int,
    codigo_classificacao: int,
    grupo_modelo_material: str,
):
    qry = """
        INSERT INTO Compras.GrupoPlanejamentoProduto 
            (CodigoGrupoPlanejamento, CodigoDepartamento, CodigoClassificacao, GrupoModeloMaterial)
        VALUES (%d, %d, %d, %s)
    """
    params = (
        codigo_grupo_planejamento,
        codigo_departamento,
        codigo_classificacao,
        grupo_modelo_material,
    )
    return mssql_exec(db_config, qry, params)


def delete(db_config: mssql, codigo: int):
    qry = """
      DELETE FROM Compras.GrupoPlanejamentoProduto 
      WHERE CodigoGrupoPlanejamentoProduto = %d
    """
    params = (codigo,)
    return mssql_exec(db_config, qry, params)
