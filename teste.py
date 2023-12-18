import base64
import os
import subprocess

# from root_app import Contracheque
# from root_app.shared.database import SessionLocal
#
# sessao = SessionLocal()
#
# cliente = sessao.query(Contracheque).first()
#
# codigocliente = cliente.imagem_contracheque
# matriculacliente = cliente.matricula
# def decode_code(codigo, matricula, mes, ano):
#     codificado = base64.b64decode(codigo)
#     caminho_local = os.getcwd()
#     print(caminho_local)
#     caminho_da_pasta = f'{caminho_local}/CLIENTES/{matricula}'
#     if not os.path.exists(caminho_da_pasta):
#         os.makedirs(caminho_da_pasta)
#     print(caminho_da_pasta)
#     caminho_do_arquivo = os.path.join(caminho_da_pasta, f'{matricula}.pdf')
#     with open(caminho_do_arquivo, 'wb') as documento:
#         documento.write(codificado)
#
#     subprocess.Popen(['explorer', caminho_da_pasta], shell=True)
#
#
# decode_code(codigocliente, matriculacliente, mes=12, ano=2023)

caminho_local = os.getcwd()
print(caminho_local)
caminho_da_pasta = os.path.join(caminho_local, 'CLIENTES', '19639301')
print(caminho_da_pasta, 'caminho')
if not os.path.exists(caminho_da_pasta):
    os.makedirs(caminho_da_pasta)
print(caminho_da_pasta)
subprocess.Popen(['explorer', caminho_da_pasta], shell=True)
