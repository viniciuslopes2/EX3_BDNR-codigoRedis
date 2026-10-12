from bson.objectid import ObjectId
from bson.errors import InvalidId
from mymongo import db
from myredis import con

col_produto = db.produto
col_favorito = db.favorito
col_usuario = db.usuario
col_vendedor = db.vendedor


def mover_produtos():
    produtos = list(col_produto.find())
    for p in produtos:
        chave = "produto:" + str(p["_id"])
        con.hset(chave, mapping={
            "nome": p.get("nome", ""),
            "descricao": p.get("descricao", ""),
            "preco": p.get("preco", 0),
            "quantidade": p.get("quantidade", 0),
            "vendedor_id": str(p.get("vendedor_id", ""))
        })
        col_produto.delete_one({"_id": p["_id"]})
    print("Produtos movidos para o Redis:", len(produtos))


def mover_favoritos():
    favoritos = list(col_favorito.find())
    for f in favoritos:
        chave = "favorito:" + str(f["_id"])
        con.hset(chave, mapping={
            "usuario_id": str(f.get("usuario_id", "")),
            "produto_id": str(f.get("produto_id", ""))
        })
        col_favorito.delete_one({"_id": f["_id"]})
    print("Favoritos movidos para o Redis:", len(favoritos))


def mover_para_redis():
    mover_produtos()
    mover_favoritos()


def listar_produtos():
    for chave in con.scan_iter("produto:*"):
        print(chave, con.hgetall(chave))


def inserir_produto():
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))

    vendedor = col_vendedor.find_one({"nome": input("Nome do vendedor: ")})
    if vendedor is None:
        print("Vendedor nao encontrado")
        return

    chave = "produto:" + str(ObjectId())
    con.hset(chave, mapping={
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "quantidade": quantidade,
        "vendedor_id": str(vendedor["_id"])
    })
    print("Inserido:", chave)


def atualizar_produto():
    chave = "produto:" + input("ID do produto: ")
    if not con.exists(chave):
        print("Nao encontrado")
        return

    print(con.hgetall(chave))

    nome = input("Novo nome: ")
    if len(nome):
        con.hset(chave, "nome", nome)

    descricao = input("Nova descrição: ")
    if len(descricao):
        con.hset(chave, "descricao", descricao)

    preco = input("Novo preço: ")
    if len(preco):
        con.hset(chave, "preco", float(preco))

    quantidade = input("Nova quantidade: ")
    if len(quantidade):
        con.hset(chave, "quantidade", int(quantidade))

    print("Alterado:", con.hgetall(chave))


def apagar_produto():
    id = input("ID do produto: ")
    print("Deletados:", con.delete("produto:" + id))

    for chave in list(con.scan_iter("favorito:*")):
        if con.hget(chave, "produto_id") == id:
            con.delete(chave)
            print("Favorito apagado junto:", chave)


def buscar_produto_redis(nome):
    for chave in con.scan_iter("produto:*"):
        if con.hget(chave, "nome") == nome:
            return chave
    print("Produto nao encontrado")
    return None


def listar_favoritos():
    for chave in con.scan_iter("favorito:*"):
        print(chave, con.hgetall(chave))


def inserir_favorito():
    usuario = col_usuario.find_one({"nome": input("Nome do usuário: ")})
    if usuario is None:
        print("Usuario nao encontrado")
        return

    chave_produto = buscar_produto_redis(input("Nome do produto: "))
    if chave_produto is None:
        return

    chave = "favorito:" + str(ObjectId())
    con.hset(chave, mapping={
        "usuario_id": str(usuario["_id"]),
        "produto_id": chave_produto.split(":")[1]
    })
    print("Inserido:", chave)


def atualizar_favorito():
    chave = "favorito:" + input("ID do favorito: ")
    if not con.exists(chave):
        print("Nao encontrado")
        return

    print(con.hgetall(chave))

    nome_produto = input("Novo nome do produto: ")
    if len(nome_produto):
        chave_produto = buscar_produto_redis(nome_produto)
        if chave_produto is None:
            return
        con.hset(chave, "produto_id", chave_produto.split(":")[1])

    print("Alterado:", con.hgetall(chave))


def apagar_favorito():
    chave = "favorito:" + input("ID do favorito: ")
    print("Deletados:", con.delete(chave))


def to_object_id(valor):
    try:
        return ObjectId(valor)
    except InvalidId:
        return valor


def devolver_produtos():
    chaves = list(con.scan_iter("produto:*"))
    for chave in chaves:
        dados = con.hgetall(chave)
        produto = {
            "_id": ObjectId(chave.split(":")[1]),
            "nome": dados["nome"],
            "descricao": dados["descricao"],
            "preco": float(dados["preco"]),
            "quantidade": int(dados["quantidade"]),
            "vendedor_id": to_object_id(dados["vendedor_id"])
        }
        col_produto.replace_one({"_id": produto["_id"]}, produto, upsert=True)
        con.delete(chave)
    print("Produtos devolvidos para o MongoDB:", len(chaves))


def devolver_favoritos():
    chaves = list(con.scan_iter("favorito:*"))
    for chave in chaves:
        dados = con.hgetall(chave)
        favorito = {
            "_id": ObjectId(chave.split(":")[1]),
            "usuario_id": to_object_id(dados["usuario_id"]),
            "produto_id": to_object_id(dados["produto_id"])
        }
        col_favorito.replace_one({"_id": favorito["_id"]}, favorito, upsert=True)
        con.delete(chave)
    print("Favoritos devolvidos para o MongoDB:", len(chaves))


def devolver_para_mongo():
    devolver_produtos()
    devolver_favoritos()