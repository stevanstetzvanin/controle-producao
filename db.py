import mysql.connector    #Importa a biblioteca para conexao com o mysql

# Stevan Stetz Vanin - UFSCar AUTOMAÇÃO INDUSTRIAL 2020

db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='controle')
cursor = db_connection.cursor()


def entrada():
    estacao = input(" Digite o ID da estação: ")
    if estacao == '1':
        ordem = input(" Digite o nome da ordem de serviço: ")
        cursor.execute(f"INSERT INTO producao (ORDEM_ID, ORDEM_NOME, ENTRADA1) VALUES (null, '{ordem}', current_timestamp())")
    else:
        if ordens('ENTRADA', estacao):
            return
        ordem = input(" Digite o ID da ordem: ")
        cursor.execute(f"UPDATE producao SET ENTRADA2=current_timestamp() WHERE ORDEM_ID={ordem}")
    db_connection.commit()
    print(" Registro realizado com sucesso.")

def ordens(registro, estacao):
    condicao = ''
    if registro == 'SAIDA' and estacao == '2':
        condicao = ' AND ENTRADA2 IS NOT NULL'
    elif registro == 'ENTRADA' and estacao == '2':
        condicao = ' AND SAIDA1 IS NOT NULL'
    cursor.execute(f"SELECT ORDEM_ID, ORDEM_NOME FROM producao WHERE {registro+estacao} IS NULL{condicao}")
    ordens = cursor.fetchall()
    if not ordens:
        print(" Não há ordens.")
        return True
    print("\n  --------------------------------")
    for ordem in ordens:
        print(f"  ID: {ordem[0]} ORDEM: {ordem[1]}")
    print("  --------------------------------\n")

def saida():
    estacao = input(" Digite o ID da estação: ")
    if ordens('SAIDA', estacao):
        return
    ordem = input(" Digite o ID da ordem: ")
    cursor.execute(f"UPDATE producao SET SAIDA{estacao}=current_timestamp() WHERE ORDEM_ID={ordem}")
    db_connection.commit()
    print(" Registro realizado com sucesso.")

def ordens_produzidas():
    cursor.execute("SELECT * FROM producao WHERE SAIDA2 IS NOT NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens produzidas.")
        return
    print("\n  ---------------------------------------")
    for resultado in resultados:
        print(f"  ID: {resultado[0]} ORDEM: {resultado[1]}\n   ENTRADA ESTAÇÃO 1: {resultado[2]}\n   SAÍDA ESTAÇÃO 1: {resultado[3]}\n   ENTRADA ESTAÇÃO 2: {resultado[4]}\n   SAÍDA ESTAÇÃO 2: {resultado[5]}")
        print("  ---------------------------------------\n")


def ordens_em_producao():
    cursor.execute("SELECT * FROM producao WHERE SAIDA2 IS NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens em produção.")
        return
    print("\n  ---------------------------------------")
    for resultado in resultados:
        print(f"  ID: {resultado[0]} ORDEM: {resultado[1]}\n   ENTRADA ESTAÇÃO 1: {resultado[2]}\n   SAÍDA ESTAÇÃO 1: {resultado[3]}\n   ENTRADA ESTAÇÃO 2: {resultado[4]}\n   SAÍDA ESTAÇÃO 2: {resultado[5]}")
        print("  ---------------------------------------\n")

def ordens_na_estacao2():
    cursor.execute("SELECT * FROM producao WHERE SAIDA2 IS NULL AND ENTRADA2 IS NOT NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens em produção na estação 2.")
        return
    print("\n  ---------------------------------------")
    for resultado in resultados:
        print(f"  ID: {resultado[0]} ORDEM: {resultado[1]}\n   ENTRADA ESTAÇÃO 1: {resultado[2]}\n   SAÍDA ESTAÇÃO 1: {resultado[3]}\n   ENTRADA ESTAÇÃO 2: {resultado[4]}\n   SAÍDA ESTAÇÃO 2: {resultado[5]}")
        print("  ---------------------------------------\n")

def tempo_medio_producao():
    pass

def dropall():
    check = input("Tem certeza que deseja APAGAR TODOS os registros? Sim/Não: ")
    if check.lower().strip() == 'sim':
        cursor.execute("DELETE FROM producao")
        db_connection.commit()
        print(" TODOS OS DADOS FORAM APAGADOS.")
    return

cursor.execute("CREATE TABLE IF NOT EXISTS producao (ORDEM_ID INTEGER PRIMARY KEY AUTO_INCREMENT, ORDEM_NOME VARCHAR(20) NOT NULL, ENTRADA1 DATETIME, SAIDA1 DATETIME, ENTRADA2 DATETIME, SAIDA2 DATETIME)")
while True:
    opt = input("\n1 - Cadastrar ordem de entrada\n2 - Cadastrar ordem de saída\n3 - Consultar ordens produzidas\n4 - Consultar ordens em produção\n5 - Consultar ordens em produção na estação 2\n6 - Verificar o tempo médio de produção\n7 - Finalizar\n8 - DELETAR TUDO\n Digite a opção desejada: ")
    if opt == '7':
        break
    elif opt == '1':
        entrada()   
    elif opt == '2':
        saida()
    elif opt == '3':
        ordens_produzidas()
    elif opt == '4':
        ordens_em_producao()
    elif opt == '5':
        ordens_na_estacao2()
    elif opt == '6':
        tempo_medio_producao()
    elif opt == '8':
        dropall()       
    else:
        print(" Opção inválida.")

cursor.close()
db_connection.close()
