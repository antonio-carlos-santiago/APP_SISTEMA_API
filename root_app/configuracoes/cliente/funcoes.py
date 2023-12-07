from root_app import Selecionado, Consulta
from root_app.shared.database import SessionLocal

sessao = SessionLocal()


def buscar_cliente():
    cliente_id = sessao.query(Selecionado).first()
    dados_consula = sessao.query(Consulta).filter_by(id_consulta=cliente_id.id_selecionado_cliente).first()
    return dados_consula
