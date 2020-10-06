import mysql.connector

# MADE BY Stevan Stetz Vanin - UFSCar AUTOMAÇÃO INDUSTRIAL 2020

def entrada(cursor, db_connection):
    estacao = input(" Digite o ID da estação: ")
    if estacao == '1':
        ordem = input(" Digite o nome da ordem de serviço: ")
        cursor.execute(f"INSERT INTO producao (ORDEM_ID, ORDEM_NOME, ENTRADA1) VALUES (null, '{ordem}', current_timestamp())")
    else:
        if ordens(cursor, 'ENTRADA', estacao):
            return
        ordem = input(" Digite o ID da ordem: ")
        cursor.execute(f"UPDATE producao SET ENTRADA2=current_timestamp() WHERE ORDEM_ID={ordem}")
    db_connection.commit()
    print(" Registro realizado com sucesso.")

def ordens(cursor, registro, estacao):
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

def saida(cursor, db_connection):
    estacao = input(" Digite o ID da estação: ")
    if ordens(cursor, 'SAIDA', estacao):
        return
    ordem = input(" Digite o ID da ordem: ")
    cursor.execute(f"UPDATE producao SET SAIDA{estacao}=current_timestamp() WHERE ORDEM_ID={ordem}")
    db_connection.commit()
    print(" Registro realizado com sucesso.")

def ordens_produzidas(cursor):
    cursor.execute("SELECT * FROM producao WHERE SAIDA2 IS NOT NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens produzidas.")
        return
    print("\n  ---------------------------------------")
    for resultado in resultados:
        print(f"  ID: {resultado[0]} ORDEM: {resultado[1]}\n   ENTRADA ESTAÇÃO 1: {resultado[2]}\n   SAÍDA ESTAÇÃO 1: {resultado[3]}\n   ENTRADA ESTAÇÃO 2: {resultado[4]}\n   SAÍDA ESTAÇÃO 2: {resultado[5]}")
        print("  ---------------------------------------\n")


def ordens_em_producao(cursor):
    cursor.execute("SELECT * FROM producao WHERE SAIDA2 IS NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens em produção.")
        return
    print("\n  ---------------------------------------")
    for resultado in resultados:
        print(f"  ID: {resultado[0]} ORDEM: {resultado[1]}\n   ENTRADA ESTAÇÃO 1: {resultado[2]}\n   SAÍDA ESTAÇÃO 1: {resultado[3]}\n   ENTRADA ESTAÇÃO 2: {resultado[4]}\n   SAÍDA ESTAÇÃO 2: {resultado[5]}")
        print("  ---------------------------------------\n")

def ordens_na_estacao2(cursor):
    cursor.execute("SELECT * FROM producao WHERE SAIDA2 IS NULL AND ENTRADA2 IS NOT NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens em produção na estação 2.")
        return
    print("\n  ---------------------------------------")
    for resultado in resultados:
        print(f"  ID: {resultado[0]} ORDEM: {resultado[1]}\n   ENTRADA ESTAÇÃO 1: {resultado[2]}\n   SAÍDA ESTAÇÃO 1: {resultado[3]}\n   ENTRADA ESTAÇÃO 2: {resultado[4]}\n   SAÍDA ESTAÇÃO 2: {resultado[5]}")
        print("  ---------------------------------------\n")

def tempo_medio_producao(cursor):
    cursor.execute("SELECT TIMESTAMPDIFF(MINUTE, ENTRADA1, SAIDA2) from producao WHERE SAIDA2 IS NOT NULL")
    resultados = cursor.fetchall()
    if not resultados:
        print(" Não há ordens produzidas para o cálculo.")
        return
    media = 0
    for resultado in resultados:
        media += resultado[0]
    print(" O tempo médio de produção é %i minutos." %(media/len(resultados)))

def dropall(cursor, db_connection):
    check = input(" Tem certeza que deseja APAGAR TODOS os registros? Sim/Não: ")
    if check.lower().strip() == 'sim':
        cursor.execute("DELETE FROM producao")
        db_connection.commit()
        print(" TODOS OS REGISTROS FORAM APAGADOS.")
    return

def main(MY_HOST, MY_USER, MY_PASSWORD, MY_DATABASE):

    db_connection = mysql.connector.connect(host=MY_HOST, user=MY_USER, password=MY_PASSWORD, database=MY_DATABASE)
    cursor = db_connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS producao (ORDEM_ID INTEGER PRIMARY KEY AUTO_INCREMENT, ORDEM_NOME VARCHAR(20) NOT NULL, ENTRADA1 DATETIME, SAIDA1 DATETIME, ENTRADA2 DATETIME, SAIDA2 DATETIME)")
    while True:
        opt = input("\n1 - Cadastrar ordem de entrada\n2 - Cadastrar ordem de saída\n3 - Consultar ordens produzidas\n4 - Consultar ordens em produção\n5 - Consultar ordens em produção na estação 2\n6 - Verificar o tempo médio de produção\n7 - SAIR\n8 - APAGAR TODOS OS REGISTROS\n Digite a opção desejada: ")
        if opt == '7':
            break
        elif opt == '1':
            entrada(cursor, db_connection)   
        elif opt == '2':
            saida(cursor, db_connection)
        elif opt == '3':
            ordens_produzidas(cursor)
        elif opt == '4':
            ordens_em_producao(cursor)
        elif opt == '5':
            ordens_na_estacao2(cursor)
        elif opt == '6':
            tempo_medio_producao(cursor)
        elif opt == '8':
            # dropall(cursor, db_connection)
            print(" Opção desabilitada.")
        else:
            print(" Opção inválida.")

    cursor.close()
    db_connection.close()

if __name__ == '__main__':
    main('localhost', 'root', None ,'controle')
