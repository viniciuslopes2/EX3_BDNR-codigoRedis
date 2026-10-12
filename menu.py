import usuario
import vendedor
import produto
import compra
import favorito
import login
import redis_itens


def menu_redis(email):
    sub = 0
    while sub != 'V':
        if not login.sessao_ativa(email):
            print("Sessão expirada")
            return

        print("1-Mover produtos e favoritos para o Redis")
        print("2-Listar produtos")
        print("3-Inserir produto")
        print("4-Atualizar produto")
        print("5-Apagar produto")
        print("6-Listar favoritos")
        print("7-Inserir favorito")
        print("8-Atualizar favorito")
        print("9-Apagar favorito")
        print("10-Devolver produtos e favoritos para o MongoDB")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            redis_itens.mover_para_redis()

        elif sub == '2':
            redis_itens.listar_produtos()

        elif sub == '3':
            redis_itens.inserir_produto()

        elif sub == '4':
            redis_itens.atualizar_produto()

        elif sub == '5':
            redis_itens.apagar_produto()

        elif sub == '6':
            redis_itens.listar_favoritos()

        elif sub == '7':
            redis_itens.inserir_favorito()

        elif sub == '8':
            redis_itens.atualizar_favorito()

        elif sub == '9':
            redis_itens.apagar_favorito()

        elif sub == '10':
            redis_itens.devolver_para_mongo()


def menu_usuario(email):
    sub = 0
    while sub != 'V':
        if not login.sessao_ativa(email):
            print("Sessão expirada")
            return

        print("1-Inserir usuário")
        print("2-Procurar usuário")
        print("3-Atualizar usuário")
        print("4-Apagar usuário")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            usuario.create_usuario()

        elif sub == '2':
            usuario.read_usuario()

        elif sub == '3':
            nome = input("Nome: ")
            usuario.update_usuario(nome)

        elif sub == '4':
            nome = input("Nome: ")
            sobrenome = input("Sobrenome: ")
            usuario.delete_usuario(nome, sobrenome)


def menu_vendedor(email):
    sub = 0
    while sub != 'V':
        if not login.sessao_ativa(email):
            print("Sessão expirada")
            return
        
        print("1-Inserir vendedor")
        print("2-Procurar vendedor")
        print("3-Atualizar vendedor")
        print("4-Apagar vendedor")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            vendedor.create_vendedor()

        elif sub == '2':
            vendedor.read_vendedor()

        elif sub == '3':
            nome = input("Nome: ")
            vendedor.update_vendedor(nome)

        elif sub == '4':
            nome = input("Nome: ")
            vendedor.delete_vendedor(nome)


def menu_produto(email):
    sub = 0
    while sub != 'V':
        if not login.sessao_ativa(email):
            print("Sessão expirada")
            return

        print("1-Inserir produto")
        print("2-Procurar produto")
        print("3-Atualizar produto")
        print("4-Apagar produto")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            produto.create_produto()

        elif sub == '2':
            produto.read_produto()

        elif sub == '3':
            nome = input("Nome: ")
            produto.update_produto(nome)

        elif sub == '4':
            nome = input("Nome: ")
            produto.delete_produto(nome)


def menu_compra(email):
    sub = 0
    while sub != 'V':
        if not login.sessao_ativa(email):
            print("Sessão expirada")
            return

        print("1-Inserir compra")
        print("2-Procurar compra")
        print("3-Atualizar compra")
        print("4-Apagar compra")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            compra.create_compra()

        elif sub == '2':
            compra.read_compra()

        elif sub == '3':
            id = input("ID: ")
            compra.update_compra(id)

        elif sub == '4':
            id = input("ID: ")
            compra.delete_compra(id)


def menu_favorito(email):
    sub = 0
    while sub != 'V':
        if not login.sessao_ativa(email):
            print("Sessão expirada")
            return

        print("1-Inserir favorito")
        print("2-Procurar favorito")
        print("3-Atualizar favorito")
        print("4-Apagar favorito")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            favorito.create_favorito()

        elif sub == '2':
            favorito.read_favorito()

        elif sub == '3':
            id = input("ID: ")
            favorito.update_favorito(id)

        elif sub == '4':
            id = input("ID: ")
            favorito.delete_favorito(id)

email = None
key = 0
while key != 'S':
    if email is None or not login.sessao_ativa(email):
        print("\n Faça login para continuar")
        email = login.login()
        if email is None:
            key = input("Tentar de novo? (S para sair): ")
            continue

    print("\nSessão expira em", login.tempo_restante(email), "segundos")
    print("1-Usuario")
    print("2-Vendedor")
    print("3-Produto")
    print("4-Compra")
    print("5-Favorito")
    print("6-Redis")
    print("L-Logout")
    print("S-Sair")
    key = input("Acessar coleção: ")

    if key == '1':
        menu_usuario(email)

    elif key == '2':
        menu_vendedor(email)

    elif key == '3':
        menu_produto(email)

    elif key == '4':
        menu_compra(email)

    elif key == '5':
        menu_favorito(email)

    elif key =='6':
        menu_redis(email)

    elif key == 'L':
        login.logout(email)
        email = None

print("Tchau Prof...")