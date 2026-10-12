from mymongo import db
import hashlib

col = db.usuario

def create_usuario():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    email = input("E-mail: ")
    senha = hashlib.sha256(input("Senha: ").encode()).hexdigest()

    enderecos = []
    key = "S"
    while key == "S":
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {
            "rua": rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        enderecos.append(endereco)
        key = input("Outro endereço (S/N)? ").upper()

    usuario = {
        "nome": nome,
        "sobrenome": sobrenome,
        "cpf": cpf,
        "email": email,
        "senha": senha,
        "enderecos": enderecos
    }

    x = col.insert_one(usuario)
    print("Inserido:", x.inserted_id)

def read_usuario(nome=""):
    nome = nome or input("Nome (vazio para todos): ")
    if len(nome):
        docs = col.find({"nome": nome})
    else:
        docs = col.find().sort("nome")
    for d in docs:
        print(d)

def update_usuario(nome):
    usuario = col.find_one({"nome": nome})
    if usuario is None:
        print("Nao encontrado")
        return

    print(usuario)

    nome = input("Novo nome: ")
    if len(nome):
        usuario["nome"] = nome

    sobrenome = input("Novo sobrenome: ")
    if len(sobrenome):
        usuario["sobrenome"] = sobrenome

    cpf = input("Novo CPF: ")
    if len(cpf):
        usuario["cpf"] = cpf

    email = input("Novo e-mail: ")
    if len(email):
        usuario["email"] = email

    r = col.update_one({"_id": usuario["_id"]}, {"$set": usuario})
    print("Alterados:", r.modified_count)

def delete_usuario(nome, sobrenome):
    r = col.delete_one({"nome": nome, "sobrenome": sobrenome})
    print("Deletados:", r.deleted_count)