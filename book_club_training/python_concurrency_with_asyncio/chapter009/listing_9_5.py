from flask import Flask, jsonify
import psycopg2
from base import SETTING

app = Flask(__name__)
conn_info = (
    f"dbname={SETTING.POSTGRES_DATABASE_NAME} "
    f"user={SETTING.POSTGRES_USER} "
    f"password={SETTING.POSTGRES_PASSWORD} "
    f"host={SETTING.POSTGRES_HOST}"
)

db = psycopg2.connect(conn_info)


@app.route("/brands")
def brands():
    cur = db.cursor()
    cur.execute("SELECT brand_id, brand_name FROM brand")
    rows = cur.fetchall()
    cur.close()
    return jsonify([{"brand_id": row[0], "brand_name": row[1]} for row in rows])
