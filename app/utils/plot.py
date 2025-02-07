import matplotlib.pyplot as plt
import io
import base64
from app.routers.api.sys import get_sys_data_tracker

async def generate_plot(db):
    res = await get_sys_data_tracker(db, sort_by="created_at", order="desc", page=1, size=10)

    data = res.data[::-1]
    labels = [f"{item.created_at.hour}:{item.created_at.minute}" for item in data]
    values = [item.cpu for item in data]

    # Buat Grafik
    fig, ax = plt.subplots()
    ax.stem(labels, values)
    ax.set_title("CPU Usage")

    # Simpan ke memory buffer sebagai PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    # Encode gambar ke Base64
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    plt.close(fig)  # Tutup figure untuk menghemat memori

    return img_base64
