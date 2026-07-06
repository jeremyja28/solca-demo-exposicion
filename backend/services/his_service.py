import json
import logging
from datetime import date

def obtener_pacientes_his(medico_id: int, fecha: date):
    logging.info("Forzando lectura de datos desde mock data.")
    try:
        with open("backend/data/mock_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [p for p in data["pacientes"] if p["MedicoId"] == medico_id]
    except Exception as e:
        logging.error(f"Error cargando mock data: {e}")
        return []

def obtener_pacientes_his_mensual(medico_id: int, anio: int, mes: int):
    logging.info("Forzando lectura de datos mensuales desde mock data.")
    try:
        with open("backend/data/mock_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [p for p in data["pacientes"] if p["MedicoId"] == medico_id]
    except Exception as e:
        logging.error(f"Error cargando mock data mensual: {e}")
        return []
