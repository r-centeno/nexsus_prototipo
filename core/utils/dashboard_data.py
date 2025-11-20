from datetime import datetime
from core.utils.extensions import db
from core.models import Atendimento, Procedimento, Organizacao


def obter_dados_dashboard():
    hoje = datetime.today()
    mes = hoje.strftime('%Y-%m')

    # Total de exames e valor total do mês
    total_exames = (
        db.session.query(db.func.sum(Atendimento.quantidade))
        .filter(db.func.strftime('%Y-%m', Atendimento.data_procedimento) == mes)
        .scalar()
    ) or 0

    valor_total = (
        db.session.query(db.func.sum(Atendimento.vlr_procedimento))
        .filter(db.func.strftime('%Y-%m', Atendimento.data_procedimento) == mes)
        .scalar()
    ) or 0

    # Pacientes ativos no mês
    pacientes_ativos = (
        db.session.query(db.func.count(db.func.distinct(Atendimento.id_paciente)))
        .filter(db.func.strftime('%Y-%m', Atendimento.data_procedimento) == mes)
        .scalar()
    ) or 0

    # Dados por grupo de exame
    resultados = (
        db.session.query(
            Organizacao.descricao.label("grupo"),
            db.func.sum(Atendimento.quantidade).label("quantidade"),
            db.func.sum(Atendimento.vlr_procedimento).label("valor")
        )
        .join(Procedimento, Procedimento.id_procedimento == Atendimento.id_procedimento)
        .join(Organizacao, Procedimento.cod_procedimento == Organizacao.codigo)
        .filter(db.func.strftime('%Y-%m', Atendimento.data_procedimento) == mes)
        .group_by(Organizacao.descricao)
        .all()
    )

    grupos = []
    for row in resultados:
        percentual = round((row.quantidade / total_exames) * 100, 2) if total_exames else 0
        grupos.append({
            "grupo": row.grupo,
            "quantidade": int(row.quantidade or 0),
            "valor": float(row.valor or 0),
            "percentual": percentual
        })

    return {
        "total_exames": int(total_exames),
        "valor_total": float(valor_total),
        "pacientes_ativos": int(pacientes_ativos),
        "grupos": grupos
    }
