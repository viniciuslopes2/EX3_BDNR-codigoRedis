from bson.objectid import ObjectId
from bson.errors import InvalidId
from mymongo import db

col = db.favorito
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


def create_favorito():
    nome_usuario = input("Nome do usuário: ")
    usuario = buscar_usuario_por_nome(nome_usuario)
    if usuario is None:
        return

    nome_produto = input("Nome do produto: ")
    produto = buscar_produto_por_nome(nome_produto)
    if produto is None:
        return

    favorito = {
        "usuario_id": usuario["_id"],
        "produto_id": produto["_id"]
    }

    x = col.insert_one(favorito)
    print("Inserido:", x.inserted_id)


def read_favorito(nome_usuario=""):
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


def update_favorito(favorito_id):
    favorito_id = to_object_id(favorito_id)
    if favorito_id is None:
        return

    favorito = col.find_one({"_id": favorito_id})
    if favorito is None:
        print("Nao encontrado")
        return

    print(favorito)

    nome_produto = input("Novo nome do produto: ")
    if len(nome_produto):
        produto = buscar_produto_por_nome(nome_produto)
        if produto is None:
            return
        favorito["produto_id"] = produto["_id"]

    r = col.update_one({"_id": favorito["_id"]}, {"$set": favorito})
    print("Alterados:", r.modified_count)


def delete_favorito(favorito_id):
    favorito_id = to_object_id(favorito_id)
    if favorito_id is None:
        return

    r = col.delete_one({"_id": favorito_id})
    print("Deletados:", r.deleted_count)