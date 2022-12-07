import socket
import threading
import time

format = 'UTF-8'
ip = '127.0.0.1'
id = 4
portas = [8001, 8002, 8003, 8004, 8005, 8006, 8007]

lider = portas[6]
porta = portas[id]

addrs = (ip, porta)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(addrs)
server_socket.listen()


def mensagem_server(msg, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(addr)
        s.send(msg.encode(format))

        s.close()

        return True

    except:
        return False


def eleicao_lider(id):
    global lider

    processos_maiores = []
    print('\n\t\t################')
    print('\t\t# Nova Eleição #')
    print('\t\t################')

    for porta in portas:
        if porta != portas[id] and porta != lider:
            resposta = mensagem_server(msg=f'ID:{id}, Ping', addr=(ip, porta))
            if resposta == True:
                if porta > portas[id] and porta != lider:
                    processos_maiores.append(porta)

    if len(processos_maiores) == 0:
        print('\nEu sou novo lider')
        lider = portas[id]
    else:
        lider = processos_maiores[-1]

    for i in range(id):
        mensagem_server(msg=f'ID: {id}, Lider Novo:{lider}', addr=(ip, portas[i]))

    print('\n')
    return lider


def verifica_lider(id, addrs):
    global lider
    print(f'Lider: {addrs}')
    while True:
        status = mensagem_server(msg=f'ID:{str(id)}, Ping', addr=(ip, lider))
        if status == False:
            novo_lider = eleicao_lider(id)
            if portas[id] == novo_lider:
                break
            else:
                print(f'O novo Lider é: {(ip, novo_lider)}')
                lider = novo_lider

        else:
            print(f'O Lider {(ip, lider)} ainda está eleito')
        time.sleep(3)


def recebimento(conn, addr):
    global lider
    print(f'Vizinho Conectado: {addr}')
    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        msg = msg.decode(format)
        msg = msg.split(', ')
        # print(msg)
        if msg[1] == 'Lider Novo':
            msg = msg[1]
            msg = msg.split(':')
            lider = msg[1]
            print(f'\nO novo lider é: {(ip, msg[1])}\n')
        else:
            if msg[1] == 'Ping':
                print(f'O Lider {(ip, lider)} ainda está eleito')


def main():
    global lider
    addrs_lider = (ip, lider)
    if lider != porta:
        thread_verificacao = threading.Thread(target=verifica_lider, args=[id, addrs_lider])
        thread_verificacao.start()
    else:
        print('Sou o Atual Lider')
        print(f'Lider: {addrs_lider}')

    while True:
        conn, addr = server_socket.accept()
        tw = threading.Thread(target=recebimento, args=[conn, addr])
        tw.start()


main = threading.Thread(target=main)
main.start()
