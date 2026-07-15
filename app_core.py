"""Funções de dados compartilhadas pelo dashboard FinTrack Insights."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).with_name("dados_tratados.csv")
MONTH_ORDER = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
REQUIRED_COLUMNS = {
    "cliente_id",
    "idade",
    "profissao",
    "escolaridade",
    "saldo_conta",
    "possui_emprestimo_pessoal",
    "tipo_contato",
    "mes_contato",
    "duracao_contato_seg",
    "resultado_campanha_anterior",
    "aderiu_produto",
}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Carrega a base tratada e valida seu contrato mínimo."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(missing)}")
    if df.empty:
        raise ValueError("A base de dados está vazia.")
    if df["cliente_id"].duplicated().any():
        raise ValueError("cliente_id deve ser único.")
    if not set(df["aderiu_produto"].dropna().unique()).issubset({0, 1}):
        raise ValueError("aderiu_produto deve conter apenas 0 e 1.")

    out = df.copy()
    out["aderiu_label"] = out["aderiu_produto"].map({1: "Sim", 0: "Não"})
    out["emprestimo_label"] = out["possui_emprestimo_pessoal"].map({1: "Sim", 0: "Não"})
    out["mes_contato"] = pd.Categorical(out["mes_contato"], categories=MONTH_ORDER, ordered=True)
    return out


def summarize(df: pd.DataFrame) -> dict[str, float | int]:
    """Calcula os indicadores principais para o recorte filtrado."""
    clientes = int(len(df))
    adesoes = int(df["aderiu_produto"].sum()) if clientes else 0
    return {
        "clientes": clientes,
        "adesoes": adesoes,
        "taxa_adesao": (adesoes / clientes * 100) if clientes else 0.0,
        "saldo_medio": float(df["saldo_conta"].mean()) if clientes else 0.0,
        "taxa_emprestimo": float(df["possui_emprestimo_pessoal"].mean() * 100) if clientes else 0.0,
    }


def segment_summary(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Retorna volume, adesões e taxas por uma dimensão categórica."""
    if dimension not in df.columns:
        raise KeyError(f"Dimensão inexistente: {dimension}")
    result = (
        df.groupby(dimension, observed=True, as_index=False)
        .agg(
            clientes=("cliente_id", "size"),
            adesoes=("aderiu_produto", "sum"),
            taxa_adesao=("aderiu_produto", "mean"),
            saldo_medio=("saldo_conta", "mean"),
        )
    )
    result["taxa_adesao"] *= 100
    return result

