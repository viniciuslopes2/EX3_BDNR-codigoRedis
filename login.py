import hashlib
from mymongo import db
from myredis import con

col = db.usuario

TEMPO_SESSAO = 120

def login():
    email = input("Email: ")
    senha = hashlib.sha256(input("Senha: ").encode()).hexdigest()

    usuario = col.find_one({"email": email, "senha": senha})
    if usuario is None:
        print("Email ou senha incorretos.")
        return None

    chave = "sessao:" + email
    con.set(chave, usuario["nome"])
    con.expire(chave, TEMPO_SESSAO)

    print("Bem-vindo(a),", usuario["nome"])
    return email

def sessao_ativa(email):
    return con.exists("sessao:" + email) == 1

def tempo_restante(email):
    return con.ttl("sessao:" + email)

def logout(email):
    con.delete("sessao:" + email)
    print("Sessão encerrada")