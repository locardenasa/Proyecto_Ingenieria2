from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io
import os

app = Flask(__name__)

# -------------------------------
# CONEXIÓN CORRECTA A MONGO
# -------------------------------

mongo_client = MongoClient("mongodb://inventario_mongo:27017/")
mongo_db = mongo_client["inventario_db"]       # ✔ base REAL
productos_collection = mongo_db["products"]    # ✔ colección REAL


@app.get("/")
def home():
    return {"mensaje": "Microservicio de reportes activo"}


# -------------------------------
# LISTAR PRODUCTOS COMO JSON
# -------------------------------
@app.get("/reporte")
def obtener_reportes():
    data = list(productos_collection.find({}, {"_id": 0}))  # ✔ variable correcta
    return jsonify(data)


# -------------------------------
# ENDPOINT: Generar Reporte de Productos
# -------------------------------
@app.route("/reporte/productos", methods=["GET"])
def reporte_productos():
    formato = request.args.get("formato", "json")
    filtro_nombre = request.args.get("nombre")

    filtro = {}
    if filtro_nombre:
        filtro["nombre"] = {"$regex": filtro_nombre, "$options": "i"}

    productos = list(productos_collection.find(filtro, {"_id": 0}))
    # -------------------------------
    # FORMATO JSON
    # -------------------------------
    if formato == "json":
        return jsonify(productos)

    # -------------------------------
    # FORMATO EXCEL
    # -------------------------------
    elif formato == "excel":
        if not productos:
            return jsonify({"mensaje": "No hay productos para exportar"}), 404

        df = pd.DataFrame(productos)

        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        nombre = f"reporte_productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=nombre,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # -------------------------------
    # FORMATO PDF
    # -------------------------------
    elif formato == "pdf":
        if not productos:
            return jsonify({"mensaje": "No hay productos para exportar"}), 404

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Reporte de Productos", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=11)
        for p in productos:
            linea = (
                f"ID: {p.get('id', '')} "
                f"| Nombre: {p.get('nombre', '')} "
                f"| Cantidad: {p.get('cantidad', '')} "
                f"| Precio: {p.get('precio', '')}"
            )
            pdf.multi_cell(0, 10, linea)
            pdf.ln(2)

        output = io.BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        output.write(pdf_bytes)
        output.seek(0)

        nombre = f"reporte_productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return send_file(
            output,
            as_attachment=True,
            download_name=nombre,
            mimetype="application/pdf"
        )

    else:
        return jsonify({"error": "Formato no soportado"}), 400


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    os.makedirs("reportes", exist_ok=True)
    app.run(host="0.0.0.0", debug=True, port=5002)

