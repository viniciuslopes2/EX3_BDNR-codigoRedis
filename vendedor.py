from mymongo import db

col = db.vendedor

def create_vendedor():
    nome = input("Nome: ")
    cpf_cnpj = input("CPF/CNPJ: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

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

    vendedor = {
        "nome": nome,
        "cpf_cnpj": cpf_cnpj,
        "email": email,
        "senha": senha,
        "enderecos": enderecos
    }

    x = col.insert_one(vendedor)
    print("Inserido:", x.inserted_id)

def read_vendedor(nome=""):
    nome = nome or input("Nome (vazio para todos): ")
    if len(nome):
        docs = col.find({"nome": nome})
    else:
        docs = col.find().sort("nome")
    for d in docs:
        print(d)

def update_vendedor(nome):
    vendedor = col.find_one({"nome": nome})
    if vendedor is None:
        print("Nao encontrado")
        return

    print(vendedor)

    nome = input("Novo nome: ")
    if len(nome):
        vendedor["nome"] = nome

    cpf_cnpj = input("Novo CPF/CNPJ: ")
    if len(cpf_cnpj):
        vendedor["cpf_cnpj"] = cpf_cnpj

    email = input("Novo e-mail: ")
    if len(email):
        vendedor["email"] = email

    r = col.update_one({"_id": vendedor["_id"]}, {"$set": vendedor})
    print("Alterados:", r.modified_count)

def delete_vendedor(nome):
    r = col.delete_one({"nome": nome})
    print("Deletados:", r.deleted_count)