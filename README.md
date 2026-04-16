# API de Cashback

API desenvolvida em Python com Flask para cálculo de cashback, integração com banco PostgreSQL (Supabase) e histórico de consultas por IP.

---

## 🔗 Frontend

Esta API é consumida por uma aplicação frontend desenvolvida em HTML, JavaScript e Tailwind CSS.

Frontend: https://cashback-frontend-vert.vercel.app/

Repositório do frontend: https://github.com/AllanGaspy/cashback-frontend

---

## Tecnologias utilizadas

- Python 3
- Flask
- PostgreSQL (Supabase)
- psycopg2
- Render (deploy)

---

## Regras de negócio

O cálculo de cashback segue as seguintes regras:

- Cashback base: **5% sobre o valor final da compra**
- Cupom de desconto aplicado antes do cálculo
- Cliente VIP recebe **+10% sobre o cashback base**
- Compras acima de R$ 500 recebem **cashback dobrado**
- Todo histórico de consultas é salvo por IP

---

## Endpoint

### POST `/calcular`

Responsável por calcular o cashback e retornar o histórico do usuário.

---

### Exemplo de requisição

```json
{
  "valor": 600,
  "cupom": 20,
  "tipo_cliente": "VIP"
}
```

### Exemplo de resposta

```json
{
  "cashback": 52.8,
  "historico": [
    ["VIP", 600.0, 52.8]
  ]
}
```

### Exemplo de uso (curl)

```bash
curl -X POST https://cashback-api-lrou.onrender.com \
-H "Content-Type: application/json" \
-d '{"valor":600,"cupom":20,"tipo_cliente":"VIP"}'
```

---

## Banco de dados

Tabela: `consultas`

| Campo | Tipo |
|---|---|
| ip | TEXT |
| tipo_cliente | TEXT |
| valor | FLOAT |
| cashback | FLOAT |

---

## Deploy

API hospedada no Render:
https://cashback-api-lrou.onrender.com/

---

## Rodar localmente

```bash
pip install -r requirements.txt
python app.py
```

---

## Autor

Projeto desenvolvido por Allan para desafio técnico de estágio - Nology.