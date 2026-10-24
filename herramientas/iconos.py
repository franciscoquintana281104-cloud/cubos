# Genera los iconos de la app: tres cubos y un hueco, como el tablero.
# Uso: python3 herramientas/iconos.py   (escribe los PNG en la carpeta de la app)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
S = 1024  # se dibuja grande y se reduce para que los bordes salgan suaves

CREMA, NEGRO, NARANJA, AMARILLO = (230, 226, 216), (29, 29, 27), (255, 91, 26), (245, 196, 0)


def icono(margen_seguro=0.0):
    img = Image.new("RGB", (S, S), CREMA)
    sombra = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    capa = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ds, dc = ImageDraw.Draw(sombra), ImageDraw.Draw(capa)

    m = S * (0.17 + margen_seguro)          # margen exterior
    hueco = S * 0.045                        # separación entre cubos
    lado = (S - 2 * m - hueco) / 2
    radio = lado * 0.2

    def caja(col, fil):
        x, y = m + col * (lado + hueco), m + fil * (lado + hueco)
        return [x, y, x + lado, y + lado]

    for (col, fil), color in {(0, 0): NEGRO, (1, 0): NARANJA, (0, 1): AMARILLO}.items():
        x0, y0, x1, y1 = caja(col, fil)
        ds.rounded_rectangle([x0, y0 + S * 0.018, x1, y1 + S * 0.018], radio, fill=(0, 0, 0, 70))
        dc.rounded_rectangle([x0, y0, x1, y1], radio, fill=color)

    # Esfera de reloj en el cubo negro
    x0, y0, x1, y1 = caja(0, 0)
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, lado * 0.3
    g = S * 0.011  # medio grosor de las agujas, con puntas redondas
    for px, py in [(cx, cy - r), (cx + r * 0.7, cy + r * 0.25)]:
        dc.line([cx, cy, px, py], fill=(247, 245, 240), width=int(2 * g))
        dc.ellipse([px - g, py - g, px + g, py + g], fill=(247, 245, 240))
    dc.ellipse([cx - S * .018, cy - S * .018, cx + S * .018, cy + S * .018], fill=AMARILLO)

    # Hueco libre: una cruz de rejilla
    x0, y0, x1, y1 = caja(1, 1)
    cx, cy, b = (x0 + x1) / 2, (y0 + y1) / 2, lado * 0.09
    gris = (29, 29, 27, 90)
    dc.line([cx - b, cy, cx + b, cy], fill=gris, width=int(S * 0.012))
    dc.line([cx, cy - b, cx, cy + b], fill=gris, width=int(S * 0.012))

    img.paste(sombra.filter(ImageFilter.GaussianBlur(S * 0.012)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(S * 0.012)))
    img.paste(capa, (0, 0), capa)
    return img


normal, mascara = icono(), icono(margen_seguro=0.06)
for tam in (180, 192, 512):
    normal.resize((tam, tam), Image.LANCZOS).save(RAIZ / f"icono-{tam}.png", optimize=True)
mascara.resize((512, 512), Image.LANCZOS).save(RAIZ / "icono-mascara-512.png", optimize=True)
print("iconos listos")
