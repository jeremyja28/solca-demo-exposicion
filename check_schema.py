from sqlalchemy import text
from backend.database import _his_engine

def get_columns():
    engine = _his_engine()
    with engine.connect() as conn:
        res = conn.execute(text("SELECT TOP 1 * FROM [dbo].[UsuariosSolcaT]"))
        print(res.keys())

get_columns()
