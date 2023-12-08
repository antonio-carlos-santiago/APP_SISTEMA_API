def ler_imagem(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        svg_codigo = arquivo.read()
    return svg_codigo
