import streamlit as st
from bs4 import BeautifulSoup, Comment
import re

st.set_page_config(page_title="Editor Stellantis Multi-Card", page_icon="🛻", layout="wide")

# ─────────────────────────────────────────────
# CSS PERSONALIZADO — Tema Stellantis
# Solo afecta la UI del editor, nunca el HTML de salida.
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fuente global ── */
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Fondo principal ── */
.stApp {
    background: #0F0F0F;
    background-image: radial-gradient(ellipse at top left, #1a0a0a 0%, #0F0F0F 60%);
    color: #E8E8E8;
}

/* ── Banner de título ── */
.editor-banner {
    background: linear-gradient(135deg, #B00020 0%, #7a0015 60%, #1a0a0a 100%);
    border-radius: 12px;
    padding: 22px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 4px 32px rgba(176,0,32,0.35);
    border: 1px solid rgba(176,0,32,0.4);
}
.editor-banner h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #fff;
    margin: 0;
    line-height: 1.1;
}
.editor-banner p {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.65);
    margin: 4px 0 0;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.editor-banner .badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.72rem;
    color: #fff;
    white-space: nowrap;
    margin-left: auto;
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ── Subheaders ── */
h2, h3 {
    font-family: 'Barlow Condensed', sans-serif !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #fff !important;
}

/* ── Contenedores / cards del editor ── */
[data-testid="stVerticalBlockBorderWrapper"] > div > div {
    background: #1A1A1A !important;
    border: 1px solid #2e2e2e !important;
    border-top: 3px solid #B00020 !important;
    border-radius: 10px !important;
    padding: 16px !important;
}

/* ── Inputs y textareas ── */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background: #111 !important;
    border: 1px solid #333 !important;
    color: #eee !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: #B00020 !important;
    box-shadow: 0 0 0 2px rgba(176,0,32,0.25) !important;
}

/* ── Labels de inputs ── */
label[data-testid="stWidgetLabel"] p {
    color: #aaa !important;
    font-size: 0.8rem !important;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Selectbox ── */
[data-baseweb="select"] {
    background: #111 !important;
}
[data-baseweb="select"] > div {
    background: #111 !important;
    border-color: #333 !important;
    color: #eee !important;
    border-radius: 6px !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label span {
    color: #ccc !important;
    font-size: 0.88rem;
}

/* ── Botones principales (guardar) ── */
.stButton > button {
    background: linear-gradient(135deg, #B00020, #7a0015) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 7px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    transition: opacity .2s, transform .15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Botón de descarga — verde oscuro para distinguirlo ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1a6b3c, #0f3d22) !important;
    color: #fff !important;
    border-radius: 7px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 12px !important;
    width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover {
    opacity: 0.88 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] section {
    background: #1A1A1A !important;
    border: 2px dashed #333 !important;
    border-radius: 10px !important;
    color: #888 !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #B00020 !important;
    background: #1e1010 !important;
}

/* ── Success / info messages ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left: 4px solid #B00020 !important;
    background: #1e1010 !important;
}

/* ── Divider ── */
hr {
    border-color: #2e2e2e !important;
    margin: 20px 0 !important;
}

/* ── Caption / vista previa ── */
[data-testid="stCaptionContainer"] p {
    color: #888 !important;
    background: #1a1a1a;
    border: 1px solid #2e2e2e;
    border-radius: 5px;
    padding: 6px 10px;
    font-family: 'Courier New', monospace !important;
    font-size: 0.79rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #B00020; border-radius: 3px; }

/* ── Sid­ebar (si se abre) ── */
[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #1e1e1e !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INICIALIZACIÓN ROBUSTA DEL SESSION STATE
# Garantiza que todos los campos existan siempre,
# sin importar cuántas cards se editen en secuencia.
# ─────────────────────────────────────────────
DEFAULTS = {
    "soup": None,
    "nuevo_precio": "",
    "nuevo_id_img": "",
    "nueva_promo": "",
    "nuevos_ben": "",
    "activar_inv": False,
    # ── Inventario especial: 3 campos base + precio ──
    # Se combinan en inventario-detalle del HTML:
    # "<modelo_ano> · Color: <color> · <km>"
    "inv_modelo_ano": "",   # Ej: RAM 700 2025
    "inv_color": "",        # Ej: Blanco Perla
    "inv_km": "",           # Ej: 0 km
    "inv_precio": "",       # Ej: 349,900  → se muestra como $349,900
    # Gestión de cards
    "confirmar_eliminar": False,
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val


def reset_campos_edicion():
    """Limpia los campos de edición sin tocar soup ni otros estados."""
    campos = [
        "nuevo_precio", "nuevo_id_img", "nueva_promo", "nuevos_ben",
        "activar_inv",
        "inv_modelo_ano", "inv_color", "inv_km", "inv_precio",
    ]
    for campo in campos:
        st.session_state[campo] = DEFAULTS[campo]


# ─────────────────────────────────────────────
# TÍTULO PRINCIPAL
# ─────────────────────────────────────────────
# Banner de título personalizado
st.markdown("""
<div class="editor-banner">
  <div style="font-size:2.4rem; line-height:1;">🛻</div>
  <div>
    <h1>Editor Stellantis</h1>
    <p>Gestión total de cards · HTML en memoria</p>
  </div>
  <span class="badge">Multi-Card v2</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 1. CARGA DE ARCHIVO
# ─────────────────────────────────────────────
archivo = st.file_uploader("Sube tu archivo HTML", type=["html"])

if archivo and st.session_state.soup is None:
    contenido = archivo.read().decode("utf-8")
    st.session_state.soup = BeautifulSoup(contenido, "html.parser")

if st.session_state.soup:
    soup = st.session_state.soup

    # Obtener lista actualizada de modelos
    cards_html = soup.find_all("article", class_="card")
    nombres_modelos = [
        card.find("h2").text.strip()
        for card in cards_html
        if card.find("h2")
    ]

    col_izq, col_der = st.columns([1, 1])

    # ─────────────────────────────────────────
    # 2. EDITOR DE CARDS EXISTENTES
    # ─────────────────────────────────────────
    with col_izq:
        st.subheader("📝 Editar Unidades Existentes")

        modelo_a_editar = st.selectbox(
            "Selecciona para editar (se guardará en memoria):",
            nombres_modelos,
            key="selector_modelo",
        )

        card_target = None
        for card in cards_html:
            if card.find("h2") and card.find("h2").text.strip() == modelo_a_editar:
                card_target = card
                break

        if card_target:
            with st.container(border=True):
                # ── Campos de edición general ──────────────────
                nuevo_precio = st.text_input(
                    "Precio Principal",
                    placeholder="Ej: 450,900",
                    key="nuevo_precio",
                )
                nuevo_id_img = st.text_input(
                    "ID Cloudinary",
                    placeholder="nombre_archivo_sin_extension",
                    key="nuevo_id_img",
                )
                nueva_promo = st.text_area(
                    "Promo (Negritas auto con $ y %)",
                    key="nueva_promo",
                )
                nuevos_ben = st.text_area(
                    "Beneficios (uno por línea)",
                    key="nuevos_ben",
                )

                # ── Inventario especial con DICCIONARIO ────────
                # Estructura del bloque HTML real:
                #   <p class="inventario-detalle">RAM 700 AÑO · Color: XXX · 0 km</p>
                #   <p class="inventario-precio">$XXX,XXX <small>precio de contado</small></p>
                activar_inv = st.checkbox(
                    "Activar Inventario Especial",
                    key="activar_inv",
                )

                if activar_inv:
                    st.markdown("**📋 Datos del Inventario Especial**")
                    col_a, col_b = st.columns(2)
                    # Diccionario de campos dinámicos del inventario
                    inv_campos = {
                        "inv_modelo_ano": col_a.text_input(
                            "Modelo / Año",
                            placeholder="Ej: RAM 700 2025",
                            key="inv_modelo_ano",
                        ),
                        "inv_color": col_b.text_input(
                            "Color",
                            placeholder="Ej: Blanco Perla",
                            key="inv_color",
                        ),
                        "inv_km": col_a.text_input(
                            "Kilometraje",
                            placeholder="Ej: 0 km",
                            key="inv_km",
                        ),
                        "inv_precio": col_b.text_input(
                            "Precio de contado",
                            placeholder="Ej: 349,900",
                            key="inv_precio",
                        ),
                    }
                    # Vista previa del texto que se insertará en inventario-detalle
                    _mod = inv_campos["inv_modelo_ano"] or "MODELO AÑO"
                    _col = inv_campos["inv_color"] or "XXX"
                    _km  = inv_campos["inv_km"] or "0 km"
                    st.caption(f"📄 inventario-detalle → `{_mod} · Color: {_col} · {_km}`")

                # ── Botón de guardado ──────────────────────────
                if st.button(f"💾 Guardar cambios de {modelo_a_editar}"):

                    # Precio principal
                    if nuevo_precio:
                        p_tag = card_target.find(class_="model-price")
                        if p_tag:
                            p_tag.string = f"Desde ${nuevo_precio}"

                    # Imagen Cloudinary
                    if nuevo_id_img:
                        img_tag = card_target.find("img")
                        if img_tag:
                            clean_id = nuevo_id_img.split("/")[-1].split(".")[0]
                            img_tag["src"] = (
                                f"https://res.cloudinary.com/dbxa0pozm/image/upload"
                                f"/w_600,q_auto,f_auto/{clean_id}.jpg"
                            )
                            img_tag["srcset"] = (
                                f"https://res.cloudinary.com/dbxa0pozm/image/upload"
                                f"/w_400,q_auto,f_auto/{clean_id}.jpg 400w, "
                                f"https://res.cloudinary.com/dbxa0pozm/image/upload"
                                f"/w_600,q_auto,f_auto/{clean_id}.jpg 600w"
                            )

                    # Promo principal
                    if nueva_promo:
                        p_div = card_target.find(class_="promo-main")
                        if p_div:
                            texto_fmt = re.sub(
                                r"(\$\d+(?:,\d+)*(?:\.\d+)?|0%|[1-9]\d*%)",
                                r'<strong style="font-size:1.4em;color:var(--acento);">\1</strong>',
                                nueva_promo,
                            )
                            p_div.clear()
                            p_div.append(
                                BeautifulSoup(f"<span>{texto_fmt}</span>", "html.parser")
                            )

                    # Beneficios
                    if nuevos_ben:
                        ul_b = card_target.find(class_="benefits-list")
                        if ul_b:
                            ul_b.clear()
                            for b in nuevos_ben.split("\n"):
                                if b.strip():
                                    b_fmt = re.sub(
                                        r"(\$\d+(?:,\d+)*(?:\.\d+)?|0%|[1-9]\d*%)",
                                        r'<strong style="font-size:1.4em;color:var(--acento);">\1</strong>',
                                        b,
                                    )
                                    li = soup.new_tag("li")
                                    li.append(
                                        BeautifulSoup(b_fmt, "html.parser")
                                    )
                                    ul_b.append(li)

                    # ── Inventario especial con diccionario ────
                    if activar_inv:
                        # Paso 1: localizar el comentario que envuelve el bloque
                        # y reemplazarlo con el HTML descomentado.
                        for comment in card_target.find_all(
                            string=lambda text: isinstance(text, Comment)
                        ):
                            if "inventario-especial" in comment:
                                # Extraer el contenido real del comentario
                                html_desencomentado = BeautifulSoup(
                                    str(comment), "html.parser"
                                )
                                comment.replace_with(html_desencomentado)
                                break  # Solo hay un bloque de inventario por card

                        # Paso 2: construir los valores del diccionario
                        # y escribirlos en los tags correctos del HTML real.
                        #
                        # Mapa:  clase CSS real → valor a insertar
                        modelo_ano = inv_campos.get("inv_modelo_ano", "") or "MODELO AÑO"
                        color      = inv_campos.get("inv_color", "")      or "XXX"
                        km         = inv_campos.get("inv_km", "")         or "0 km"
                        precio     = inv_campos.get("inv_precio", "")

                        etiquetas_inv = {
                            # inventario-detalle → cadena combinada (formato del HTML)
                            "inventario-detalle": f"{modelo_ano} · Color: {color} · {km}",
                            # inventario-precio  → precio con símbolo
                            "inventario-precio":  f"${precio}" if precio else "",
                        }

                        for clase_css, valor in etiquetas_inv.items():
                            if valor:
                                tag = card_target.find(class_=clase_css)
                                if tag:
                                    # inventario-precio tiene un <small> anidado;
                                    # solo actualizamos el nodo de texto principal.
                                    if clase_css == "inventario-precio":
                                        # Buscar el primer NavigableString directo
                                        for node in tag.children:
                                            if isinstance(node, str):
                                                node.replace_with(valor + " ")
                                                break
                                    else:
                                        tag.string = valor

                    st.success(f"¡{modelo_a_editar} actualizado en memoria!")
                    # Limpiar campos tras guardar para la próxima edición
                    reset_campos_edicion()
                    st.rerun()

    # ─────────────────────────────────────────
    # 3. AÑADIR NUEVA CARD
    # ─────────────────────────────────────────
    with col_der:
        st.subheader("➕ Añadir Nueva Card")
        with st.container(border=True):
            nuevo_nombre = st.text_input(
                "Nombre del nuevo modelo (Ej: RAM 1500 Limited)",
                key="nuevo_nombre_card",
            )
            if st.button("➕ Insertar nueva tarjeta al final"):
                if nuevo_nombre and cards_html:
                    # Copiamos la primera card como plantilla
                    nueva_card = BeautifulSoup(
                        str(cards_html[0]), "html.parser"
                    ).find("article")
                    nueva_card.find("h2").string = nuevo_nombre
                    # Limpiamos datos genéricos
                    if nueva_card.find(class_="model-price"):
                        nueva_card.find(class_="model-price").string = "Desde $0,000"

                    # Insertar en el grid
                    grid = soup.find(class_="grid-promos")
                    grid.append(nueva_card)
                    st.success(
                        f"Card de {nuevo_nombre} añadida. "
                        "¡Búscala en la lista de arriba para editarla!"
                    )
                    st.rerun()

    st.divider()

    # ─────────────────────────────────────────
    # 4. GESTIÓN DE ORDEN Y ELIMINACIÓN
    # ─────────────────────────────────────────
    st.markdown("""
    <style>
    .orden-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #888;
        margin-bottom: 2px;
    }
    .orden-pill {
        display: inline-block;
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.8rem;
        color: #ccc;
        margin: 2px 3px;
        font-family: 'Inter', sans-serif;
    }
    .orden-pill.activa {
        background: #B00020;
        border-color: #B00020;
        color: #fff;
        font-weight: 600;
    }
    .danger-zone {
        border: 1px solid #8b0000 !important;
        border-top: 3px solid #ff2244 !important;
        background: #1a0a0a !important;
        border-radius: 10px;
        padding: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    col_orden, col_eliminar = st.columns([1, 1])

    # ── Panel: Mover Cards ──────────────────────────────
    with col_orden:
        st.subheader("↕️ Mover Card")
        with st.container(border=True):
            # Volver a leer los nombres (pueden haber cambiado)
            cards_live = soup.find_all("article", class_="card")
            nombres_live = [
                c.find("h2").text.strip() for c in cards_live if c.find("h2")
            ]

            modelo_mover = st.selectbox(
                "Card a mover",
                nombres_live,
                key="sel_mover",
            )

            # Vista previa del orden actual como pills
            pills_html = ""
            for i, nm in enumerate(nombres_live):
                cls = "orden-pill activa" if nm == modelo_mover else "orden-pill"
                pills_html += f'<span class="{cls}">{i+1}. {nm}</span>'
            st.markdown(
                f'<div class="orden-label">Orden actual</div>{pills_html}',
                unsafe_allow_html=True,
            )
            st.write("")

            # Selector de posición destino
            nueva_pos = st.number_input(
                "Mover a la posición (1 es el principio):",
                min_value=1,
                max_value=len(nombres_live),
                value=nombres_live.index(modelo_mover) + 1,
                key="num_posicion"
            )

            if st.button("🚀 Reubicar Card", use_container_width=True):
                grid = soup.find(class_="grid-promos")
                # Obtener solo los <article class="card"> directos del grid
                articulos = [t for t in grid.children 
                             if getattr(t, "name", None) == "article" 
                             and "card" in t.get("class", [])]
                
                # Encontrar la card a mover
                card_a_mover = next(
                    (a for a in articulos if a.find("h2") and a.find("h2").text.strip() == modelo_mover),
                    None
                )

                if card_a_mover:
                    # Extraerla
                    card_a_mover.extract()
                    # Re-obtener la lista de artículos sin la que extrajimos
                    articulos_restantes = [t for t in grid.children 
                                           if getattr(t, "name", None) == "article" 
                                           and "card" in t.get("class", [])]
                    
                    target_idx = nueva_pos - 1
                    
                    if target_idx <= 0:
                        grid.insert(0, card_a_mover)
                    elif target_idx >= len(articulos_restantes):
                        grid.append(card_a_mover)
                    else:
                        # Insertar antes del elemento que ahora ocupa esa posición
                        articulos_restantes[target_idx].insert_before(card_a_mover)
                    
                    st.success(f"✅ '{modelo_mover}' movida a la posición {nueva_pos}.")
                    st.rerun()

    # ── Panel: Eliminar Card ────────────────────────────
    with col_eliminar:
        st.subheader("🗑️ Eliminar Card")
        with st.container(border=True):
            cards_live2 = soup.find_all("article", class_="card")
            nombres_live2 = [
                c.find("h2").text.strip() for c in cards_live2 if c.find("h2")
            ]

            modelo_eliminar = st.selectbox(
                "Card a eliminar",
                nombres_live2,
                key="sel_eliminar",
            )

            st.markdown(
                f'<p style="color:#ff6b6b;font-size:0.82rem;margin:6px 0;">'
                f'⚠️ Esta acción borra <strong>{modelo_eliminar}</strong> del HTML en memoria.'
                f' No se puede deshacer.</p>',
                unsafe_allow_html=True,
            )

            confirmar = st.checkbox(
                f'Confirmo que quiero eliminar "{modelo_eliminar}"',
                key="confirmar_eliminar",
            )

            if st.button(
                "🗑️ Eliminar card",
                key="btn_eliminar",
                disabled=not confirmar,
            ):
                card_a_borrar = None
                for card in soup.find_all("article", class_="card"):
                    if card.find("h2") and card.find("h2").text.strip() == modelo_eliminar:
                        card_a_borrar = card
                        break
                if card_a_borrar:
                    card_a_borrar.decompose()
                    # Limpiar el checkbox de confirmación
                    st.session_state["confirmar_eliminar"] = False
                    st.success(f"✅ '{modelo_eliminar}' eliminada del catálogo.")
                    st.rerun()

    st.divider()

    # ─────────────────────────────────────────
    # 5. DESCARGA FINAL
    # ─────────────────────────────────────────
    st.subheader("Finalizar y Descargar")
    html_final = soup.prettify(formatter="html")
    st.download_button(
        label="📥 DESCARGAR CATÁLOGO COMPLETO (Todas las ediciones)",
        data=html_final,
        file_name="catalogo_stellantis_final.html",
        mime="text/html",
        use_container_width=True,
    )

    if st.button("♻️ Reiniciar editor (Borrar memoria)"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()