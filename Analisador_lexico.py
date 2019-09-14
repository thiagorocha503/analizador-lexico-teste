#-*-coding:utf8;-*-
#qpy:3
#qpy:console



alfabeto=("a","b","c","d","e",
"f","g","h","i","j","k","l","m",
"n","o","p","q","r","s","t","u",
"v","w","x","y","z","A","B","C",
"D","E","F","G","H","I","J","K",
"L","M","N","O","P","Q","R","S",
"T","U","V","W","X","Y","Z","Á",
"À","Ã","Â","É","Ê","Í","Ó","Ô",
"Õ","Ú","á","à","â","ã","é","ê",
"í","ó","ô","õ","ú","ç","ñ","Ñ",
"_")
numeros = ("0","1","2","3","4","5","6","7","8","9")#,".")          
operadores = ("=","+","-","/","*","%","<",">","!")
outros = (",",":",";","#",".")
delimitadores =("(",")","{","}","[","]")
reservadas =("while","for","break",
"continue","case","if","else","int",
"float","str")
marcadores = ("\n","\t")
# Caracter válidos para strings
validos = ("0","1","2","3","4","5","6",
"7","8","9","a","b","c","d","e","f",
"g","h","i","j","k","l","m","n","o",
"p","q","r","s","t","u","v","w","x",
"y","z","A","B","C","D","E","F","G",
"H","I","J","K","L","M","N","O","P",
"Q","R","S","T","U","V","W","X","Y",
"Z","Á","À","Ã","Â","É","Ê","Í","Ó",
"Ô","Õ","Ú","á","à","â","ã","é","ê","í",
"ó","ô","õ","ú","ñ","Ñ","ç","{","}","[",
"]","/","(",")",".","=","+","-","*",
"%","<",">","!","'",":",";"," ","_", #Aspa não é incluída
",","?","`","~","¿","¡","^","!","$",
"#","@","×","÷","€","£","¥","₩","☆",
"♤","♡","◇","♧","°","\t")

#     NUMERAL 
def numeral():
    global i
    global erros
    ponto = 0
    num = ""
    while i < tamanho:
        if (codigo[i] in numeros) or (codigo[i] == "."):
            if codigo[i] == ".": 
                ponto += 1              
                if ponto == 1:# Verifica se ponto é permitido
                    num = num + "." # adiciona o ponto decimal 
                    i += 1
                else:
                    print("Linha %4.d - Erro 01: Ponto decimal a mais:"%linha)
                    print("Numeral: ",num+codigo[i])
                    print(" "*8," "*len(num),"^")# ponteiro de erro
                    erros += 1
                    i += 1# ignora o ponto a mais
                    break             
            else: # Se não,  número.
                num = num + codigo[i]         
                i += 1
        else:    
            # Verifica se caracter é válido         
            if codigo[i] in ('"'," ") or (codigo[i] in (operadores + outros + alfabeto + delimitadores)):             
                break #  Fim do número
            elif codigo[i] == "\n" or codigo[i] == "\t":
                break    
            else:# Caracter inválido
                aux = num+codigo[i] # variável auxiliar 
                print("Linha %4.d - Erro 02:"%linha)
                print("Caracter inválido: ",aux)         	
                print(" "*17," "*len(aux),"^")# ponteiro de erro
                erros += 1 
                i += 1 # pula o erro
                break   
            
    if  ponto == 0:
        return int(num)
    else:
        return float(num) 
#      VARIÁVEIS/PALAVRAS-RESERVADAS
def constante():
    global i
    global erros
    const = ""
    while True:
        if i < tamanho:
            if codigo[i] in (alfabeto + numeros):
                const = const + codigo[i]
                i += 1
            else:
                if codigo[i] == '"' or codigo[i] == ".":
                    break
                elif codigo[i] in (marcadores + delimitadores):
                    break
                elif codigo[i] in (outros + operadores):
                    break
                elif codigo[i] == " ":
                    i += 1 # pula espaço
                    break                   
                else: # caracter inválido
                    const = const + codigo[i]
                    print("Linha %4.d - Erro 03: caracter invalido"%linha)
                    print(const)
                    print(" "*(len(const)-1),"^")
                    erros += 1
                    i += 1                          
        else:
            break
    return const
#  Palavras reservadas
def reservada(Id):#
    if string in resevarda:
        return True
    else:
        return False
#    OPERADORES
def operador():
    global i
    global erros
    simbolo = codigo[i]   
    i += 1 # 
    if i < tamanho:# Se não chegou ao fim do codigo
        if codigo[i] == " ":# Se for espaços, avance.
            pula_espaços()
        else:    
            if i < tamanho:    
                next_lexema = codigo[i]#  próximo lexema valido            
                if simbolo == "!":# "!" Não pode está desacompanhado de "="
                    if next_lexema == "=":
                        simbolo = "!="
                        i += 1
                    else:
                        aux = simbolo+next_lexema
                        print("Linha %4.d - Erro 04: operador invalido: %s"%(linha,aux))
                        print(" "*41,"^")
                        erros += 1
                else:  
                    if next_lexema in operadores:              
                        if simbolo in ("+","-","/","*") and next_lexema == "=":
                            simbolo = simbolo + next_lexema
                            i +=1
                        elif simbolo == "=" and next_lexema == "=":
                            simbolo = "=="
                            i += 1
                        elif simbolo in (">","<") and next_lexema == "=":
                            simbolo = simbolo + next_lexema
                            i += 1                  
                        else:
                            simbolo = simbolo + next_lexema  
                            print("Linha %4.d - Erro 05: operador invalido: %s"%(linha,simbolo))                    
                            print(" "*41,"^")
                            i += 1
                            erros += 1
    return simbolo
#
#        STRING
#
def string():
    global i
    global erros
    string = '"'
    i += 1#pula aspas iniciais
    if i < tamanho:
        while True:
            if codigo[i] in validos:
                string = string + codigo[i] 
                i += 1        
            elif codigo[i] == '"':
                i += 1 # pula aspa final
                break
            elif codigo[i] == "\n":
                print("Linha %4.d - Erro 06: String com quebra de linha"%linha)
                print(string)
                print(" "*len(string),"^")
                i += 1
                erros += 1
                break
            else:
                string = string + codigo[i]
                print("Linha %4.d - Erro 07: Caracter inválido"%linha)
                print(string)
                print(" "*(len(string)-1),"^")
                i += 1 # próximo carácter
                erros += 1  
            if i >= tamanho:
                print("Linha %4.d - Erro 08: Aspas não fechada:"%linha)
                print(string)
                print(" "*(len(string)-1),"^")               
                erros += 1
                break
    else:#Caso fim da lista apos aspa inicial
        print("Linha %4.d - Erro 09: aspas não fechada"%linha)
        print(string)
        print(" "*(len(string)-1),"^")
    string = string + '"'    
    return string
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
    global i
    # Verifica  que tipo de token se trata
    if n in numeros: # números inteiros/reais 
        token = numeral()
    elif n == '"':# cadeia de caracteres
        token = string()
    elif n in alfabeto: # Identificadores/ palavras chaves              
        token = constante()
    elif n in operadores: # operadores aritméticos/relacionais
        token = operador()
    elif n in outros: # Outros símbolos válidos
        token = codigo[i]
        i += 1
    elif n in delimitadores:# Delimitadores
        token = codigo[i]
        i += 1 
    elif n == "\n":
        token = "《n》"
        #print("marcador: quebrar de linha "
        i += 1
    elif n == "\t":
        token = "《t》"
        #print("marcador: tabulação ")
        i += 1
    else:
        token = codigo[i]
        print("linha %4.d - Erro 10: Carácter invalido: %s"%(linha,token))       
        erros += 1
        i += 1
    return token

def pula_espaços():
    global i
    global space 
    if i < tamanho:
        while codigo[i] == " ":
            space += 1
            i += 1
            if i >= tamanho:
                break
    else:
        print("Fim")   

#     Entrada por arquivo
space = 0 # Qtd de espaços 
analise =[] #Lista que armazena os tokens
arquivo = open("/sdcard/qpython/codigo.txt")
line = arquivo.readline()
total_erros = 0# Erros de todas as linha do código
linha = 0 # linha do código
print()
while line != "":
    linha += 1
    codigo = list(line)
    tamanho = len(codigo)
    erros = 0 # Erros de uma linha do código 
    i = 0 # indice da lista
    while i < tamanho:
        if codigo[i] == " ":
            pula_espaços()    
        token = next_token(codigo[i])          
        total_erros += erros
        analise.append(token)# Adiciona o token
        if erros > 0:# Pule para próxima linha de código       
            break       
    line = arquivo.readline()
if total_erros == 0:    
    print("==================================")
    print("   Analise concluída sem erros  ")
    print("==================================")
    for x in analise:
        print(">>>",x)
    print("Total de erros: ",total_erros)   
else:
    print()
    print("Total de erros: ",total_erros)   