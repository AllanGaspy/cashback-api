from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Lógica de cálculo
def calcular_cashback(valor, cupom, cliente_vip):
    desconto = valor * (cupom / 100)
    valor_final = valor - desconto

    # Segurança extra (nunca negativo)
    if valor_final < 0:
        valor_final = 0

    CASHBACK_BASE_PERCENTUAL = 0.05
    cashback_base = valor_final * CASHBACK_BASE_PERCENTUAL

    BONUS_VIP_PERCENTUAL = 0.10
    bonus_vip = cashback_base * BONUS_VIP_PERCENTUAL if cliente_vip else 0
    cashback = cashback_base + bonus_vip

    if valor_final > 500:
        cashback *= 2

    return round(cashback, 2)

# Testar se API está funcionando
@app.route("/")
def home():
    return "API OK"

# Rota da API  
@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.json

    valor = data.get("valor")
    cupom = data.get("cupom", 0)
    tipo = data.get("tipo_cliente", "").upper()

    # Validação do valor
    try:
        valor = float(valor)
        if valor <= 0:
            raise ValueError
    except:
        return jsonify({"erro": "Valor deve ser um número maior que 0"}), 400

    # Validação do cupom
    try:
        cupom = float(cupom)
        if cupom < 0 or cupom > 100:
            raise ValueError
    except:
        return jsonify({"erro": "Cupom deve estar entre 0 e 100"}), 400

    # Validação do tipo de cliente
    if tipo not in ["VIP", "REGULAR"]:
        return jsonify({"erro": "tipo_cliente deve ser VIP ou REGULAR"}), 400

    cliente_vip = tipo == "VIP"

    cashback = calcular_cashback(valor, cupom, cliente_vip)

    ip = request.remote_addr

    # Conexão com o banco
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Salvar consulta
    cur.execute(
        "INSERT INTO consultas (ip, tipo_cliente, valor, cashback) VALUES (%s, %s, %s, %s)",
        (ip, tipo, valor, cashback)
    )
    conn.commit()

    # Buscar histórico
    cur.execute(
        "SELECT tipo_cliente, valor, cashback FROM consultas WHERE ip = %s",
        (ip,)
    )
    historico = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "cashback": cashback,
        "historico": historico
    })

# Rodar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)