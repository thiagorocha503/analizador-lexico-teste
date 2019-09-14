# from tkinter import messagebox

alfabeto = ("a", "b", "c", "d", "e", "f", "g", "h",
            "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x",
            "y", "z", "A", "B", "C", "D", "E", "F",
            "G", "H", "I", "J", "K", "L", "M", "N",
            "O", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z", "Á", "À", "Ã", "Â",
            "É", "Ê", "Í", "Ó", "Ô", "Õ", "Ú", "á",
            "à", "â", "ã", "é", "ê", "í", "ó", "ô",
            "õ", "ú", "ç", "ñ", "Ñ", "_")
numeros = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")  # ,".")
operadores = ("=", "+", "-", "/", "*", "%", "<", ">", "!")
outros = (",", ":", ";", "#", ".")
delimitadores = ("(", ")", "{", "}", "[", "]")
reservadas = ("while", "for", "break", "swith",
              "continue", "case", "if", "else", "int",
              "float", "str")
marcadores = ("\n", "\t")
# Caracter válidos para strings
caracterValidosString = numeros + alfabeto + delimitadores + outros + operadores


#     NUMERAL
def numeral():
    global indice
    global erros
    ponto = 0
    num = ""
    while indice < tamanho:
        if (codigo[indice] in numeros) or (codigo[indice] in (".", "-")):
            if codigo[indice] == ".":
                ponto += 1
                if ponto == 1:  # Verifica se ponto é permitido
                    num = num + "."  # adiciona o ponto decimal
                    indice += 1
                else:
                    print("Linha %4.d - Erro 01: Ponto decimal a mais:" % linha)
                    print("Numeral: ", num + codigo[indice])
                    print(" " * 8, " " * len(num), "^")  #gitgi ponteiro de erro
                    erros += 1
                    indice += 1  # ignora o ponto a mais
                    break
            elif codigo[indice] == "-":
                num = num + codigo[indice]# adiciona o sinal
                indice += 1
            else:  # Se não,  número.
                num = num + codigo[indice]
                indice += 1
        else:
            # Verifica se caracter é válido         
            if codigo[indice] in ('"', " ") or (codigo[indice] in (operadores + outros + alfabeto + delimitadores)):
                break  # Fim do número
            elif codigo[indice] == "\n" or codigo[indice] == "\t":
                break
            else:  # Caracter inválido
                aux = num + codigo[indice]  # variável auxiliar
                print("Linha %4.d - Erro 02:" % linha)
                print("Caracter inválido: ", aux)
                print(" " * 17, " " * len(aux), "^")  # ponteiro de erro
                erros += 1
                indice += 1  # pula o erro
                break

    if ponto == 0:
        return int(num)
    else:
        return float(num)
    #      VARIÁVEIS/PALAVRAS-RESERVADAS


def constante():
    global indice
    global erros
    const = ""
    while True:
        if indice < tamanho:
            if codigo[indice] in (alfabeto + numeros):
                const = const + codigo[indice]
                indice += 1
            else:
                if codigo[indice] == '"' or codigo[indice] == ".":
                    break
                elif codigo[indice] in (marcadores + delimitadores):
                    break
                elif codigo[indice] in (outros + operadores):
                    break
                elif codigo[indice] == " ":
                    indice += 1  # pula espaço
                    break
                else:  # caracter inválido
                    const = const + codigo[indice]
                    print("Linha %4.d - Erro 03: caracter invalido" % linha)
                    print(const)
                    print(" " * (len(const) - 2), "^")
                    erros += 1
                    indice += 1
        else:
            break
    return const


#  Palavras reservadas
def reservada(_id):
    if _id in reservadas:
        return True
    else:
        return False


#    OPERADORES
def operador():
    global indice
    global erros
    simbolo = codigo[indice]
    indice += 1  #
    if indice < tamanho:  # Se não chegou ao fim do codigo
        if codigo[indice] == " ":  # Se for espaços, avance.
            pula_espacos()
        else:
            if indice < tamanho:
                next_lexema = codigo[indice]  # próximo lexema válido
                if simbolo == "!":  # "!" Não pode está desacompanhado de "="
                    if next_lexema == "=":
                        simbolo = "!="
                        indice += 1
                    else:
                        aux = simbolo + next_lexema
                        print("Linha %4.d - Erro 04: operador invalido: %s" % (linha, aux))
                        print(" " * 41, "^")
                        erros += 1
                else:
                    if next_lexema in operadores:
                        if simbolo in ("+", "-", "/", "*","%") and next_lexema == "=":
                            simbolo = simbolo + next_lexema
                            indice += 1
                        elif (simbolo == next_lexema == "+") or (simbolo == next_lexema == "-"):
                            simbolo += next_lexema
                            indice += 1
                        elif simbolo == "=" and next_lexema == "=":
                            simbolo = "=="
                            indice += 1
                        elif simbolo in (">", "<") and next_lexema == "=":
                            simbolo = simbolo + next_lexema
                            indice += 1
                        else:
                            simbolo = simbolo + next_lexema
                            print("Linha %4.d - Erro 05: operador invalido: %s" % (linha, simbolo))
                            print(" " * 41, "^")
                            indice += 1
                            erros += 1
    return simbolo


#
#        STRING
#
def string():
    global indice
    global erros
    _string = '"'  # underline para outercope
    indice += 1  # pula aspas iniciais
    if indice < tamanho:
        while True:
            if codigo[indice] in caracterValidosString:
                _string = _string + codigo[indice]
                indice += 1
            elif codigo[indice] == '"':
                indice += 1  # pula aspa final
                break
            elif codigo[indice] == "\n":
                print("Linha %4.d - Erro 06: String com quebra de linha" % linha)
                print(_string)
                print(" " * len(_string), "^")
                indice += 1
                erros += 1
                break
            else:
                _string = _string + codigo[indice]
                print("Linha %4.d - Erro 07: Caracter inválido" % linha)
                print(_string)
                print(" " * (len(_string) - 1), "^")
                indice += 1  # próximo carácter
                erros += 1
            if indice >= tamanho:
                print("Linha %4.d - Erro 08: Aspas não fechada:" % linha)
                print(_string)
                print(" " * (len(_string) - 1), "^")
                erros += 1
                break
    else:  # Caso fim da lista apos aspa inicial
        print("Linha %4.d - Erro 09: aspas não fechada" % linha)
        print(_string)
        print(" " * (len(_string) - 1), "^")
    _string = _string + '"'
    return _string


"""
def marcador():
    global i 
    x = 0
    if codigo[i] =="\n":
        x = "\n"
    elif codigo[i] =="\t":
        x = "\t"
    i+=1
    return x
"""


def next_token(n):
    global erros
    global indice
    # Verifica  que tipo de _token se trata
    if n in numeros:  # números inteiros/reais
        _token = numeral()
    elif n == '"':  # cadeia de caracteres
        _token = string()
    elif n in alfabeto:  # Identificadores/ palavras chaves
        _token = constante()
    elif n in operadores:  # operadores aritméticos/relacionais ou número negativo
        if n == '-' and codigo[indice + 1] in numeros:# verifica se após o o sinal há um núemro
            _token = numeral()  # numero real ou inteiro negativo
        else:
            _token = operador()
    elif n in outros:  # Outros símbolos válidos
        _token = codigo[indice]
        indice += 1
    elif n in delimitadores:  # Delimitadores
        _token = codigo[indice]
        indice += 1
    elif n == "\n":
        _token = "《n》"
        # print("marcador: quebrar de linha "
        indice += 1
    elif n == "\t":
        _token = "《t》"
        # print("marcador: tabulação ")
        indice += 1
    else:
        _token = codigo[indice]
        print("linha %4.d - Erro 10: Carácter invalido: %s" % (linha, _token))
        erros += 1
        indice += 1
    return _token


def pula_espacos():
    global indice
    global space
    if indice < tamanho:
        while codigo[indice] == " ":
            space += 1
            indice += 1
            if indice >= tamanho:
                break
    else:
        print("Fim")

    #     Entrada por arquivo

def abreArquivo(nome = "codigo.txt"):
    try:
        _arquivo = open(nome)
        return _arquivo
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado!")
        return None
    except Exception as ex:
        print("Erro: ", str(ex))
        return None

space = 0  # Quantidade de espaços total
analise = []  # Lista que armazena os tokens
arquivo = abreArquivo()
if arquivo is not None:
    line = arquivo.readline()
    total_erros = 0  # Erros de todas as linha do código
    linha = 0  # linha atual de analize do código
    print()
    print("==================================")
    print("      Resultado da análise        ")
    print("==================================")
    print()
    while line != "":
        linha += 1
        codigo = list(line)
        tamanho = len(codigo)
        erros = 0  # Erros de uma linha do código
        indice = 0  # indice da lista
        while indice < tamanho:
            if codigo[indice] == " ":
                pula_espacos()
            token = next_token(codigo[indice])
            total_erros += erros
            analise.append(token)  # Adiciona o token
            if erros > 0:  # Pule para próxima linha de código
                break
        line = arquivo.readline()
    if total_erros == 0:
        for x in analise:
            print(">>>", x)
        print("Nenhum erro lexico encontrado.")
        print("Total de erros: ", total_erros)
    else:
        print()
        print("Total de erros: ", total_erros)
