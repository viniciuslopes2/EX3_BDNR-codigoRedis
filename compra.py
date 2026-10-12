from bson.objectid import ObjectId
from bson.errors import InvalidId
from mymongo import db

col = db.compra
col_usuario = db.usuario
col_produto = db.produto


def to_object_id(valor):
    try:
        return ObjectId(valor)
    except InvalidId:
        print("ID inválido")
        return None


def buscar_usuario_por_nome(nome):
    usuario = col_usuario.find_one({"nome": nome})
    if usuario is None:
        print("Usuario nao encontrado")
        return None
    return usuario


def buscar_produto_por_nome(nome):
    produto = col_produto.find_one({"nome": nome})
    if produto is None:
        print("Produto nao encontrado")
        return None
    return produto


def ler_itens():
    itens = []
    key = "S"
    while key == "S":
        nome_produto = input("Nome do produto: ")
        produto = buscar_produto_por_nome(nome_produto)
        if produto is None:
            continue

        quantidade = int(input("Quantidade: "))

        item = {
            "produto_id": produto["_id"],
            "quantidade": quantidade,
            "preco_unitario": produto["preco"]
        }
        itens.append(item)
        key = input("Adicionar outro item (S/N)? ").upper()

    return itens


def calcular_total(itens):
    total = 0
    for item in itens:
        total += item["quantidade"] * item["preco_unitario"]
    return total


def create_compra():
    nome_usuario = input("Nome do usuário: ")
    usuario = buscar_usuario_por_nome(nome_usuario)
    if usuario is None:
        return

    itens = ler_itens()

    compra = {
        "usuario_id": usuario["_id"],
        "itens": itens,
        "valor_total": calcular_total(itens)
    }

    x = col.insert_one(compra)
    print("Inserido:", x.inserted_id)


def read_compra(nome_usuario=""):
    nome_usuario = nome_usuario or input("Nome do usuário (vazio para todos): ")
    if len(nome_usuario):
        usuario = buscar_usuario_por_nome(nome_usuario)
        if usuario is None:
            return
        docs = col.find({"usuario_id": usuario["_id"]})
    else:
        docs = col.find()
    for d in docs:
        print(d)


def update_compra(compra_id):
    compra_id = to_object_id(compra_id)
    if compra_id is None:
        return

    compra = col.find_one({"_id": compra_id})
    if compra is None:
        print("Nao encontrado")
        return

    print(compra)

    key = input("Adicionar novos itens (S/N)? ").upper()
    if key == "S":
        novos_itens = ler_itens()
        compra["itens"].extend(novos_itens)
        compra["valor_total"] = calcular_total(compra["itens"])

    r = col.update_one({"_id": compra["_id"]}, {"$set": compra})
    print("Alterados:", r.modified_count)


def delete_compra(compra_id):
    compra_id = to_object_id(compra_id)
    if compra_id is None:
        return

    r = col.delete_one({"_id": compra_id})
    print("Deletados:", r.deleted_count)