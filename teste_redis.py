from myredis import con

try:
    con.ping()
    print("Conectado ao Redis!")
except Exception as e:
    print(e)

con.set("vinicius@gmail.com", "Vinicius Silva")
print(con.get("vinicius@gmail.com"))