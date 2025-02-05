from sqlalchemy.ext.automap import automap_base
from app.database import engine

# Auto-mapping tabel dari database yang sudah ada
Base = automap_base()
Base.prepare(engine, reflect=True)

# Ambil model yang sudah ada
SysDataTracker = Base.classes.sys_data_tracker  # Pastikan nama tabel sesuai dengan database
