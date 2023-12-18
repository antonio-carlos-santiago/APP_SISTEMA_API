import base64

from root_app import Contracheque
from root_app.configuracoes.contracheques.elementos import buscar_cliente_cc
from root_app.shared.database import SessionLocal

import fitz

sessao = SessionLocal()

cliente = buscar_cliente_cc()
contra_cheques_salvos = sessao.query(Contracheque).filter_by(cpf=cliente.cpf).first()


pdf_data = base64.b64decode(contra_cheques_salvos.imagem_contracheque)


# 2. Salvar o PDF decodificado
with open("output.pdf", "wb") as pdf_file:
    pdf_file.write(pdf_data)

with fitz.open('output.pdf') as pdf_document:
    for page_number in range(pdf_document.page_count):
        # Obtém a página do PDF
        page = pdf_document[page_number]

        # Cria uma imagem a partir da página
        image = page.get_pixmap()

        # Salva a imagem no formato PNG (ou em qualquer formato desejado)
        image.save(f"{page_number + 1}.png")

