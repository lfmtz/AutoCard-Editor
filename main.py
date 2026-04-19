import streamlit as st
from bs4 import BeautifulSoup, Comment
import re

# 1. CONFIGURACIÓN E INICIALIZACIÓN
st.set_page_config(page_title="Editor Stellantis Pro", page_icon="🛻", layout="wide")

# (Aquí va todo tu bloque de CSS personalizado - Se omite en el ejemplo para brevedad pero debes mantenerlo igual)
# st.markdown(""" <style> ... tu CSS ... </style> """, unsafe_allow_html=True)

if "soup" not in st.session_state:
    st.session_state.soup = None

# 2. BANNER DE TÍTULO (Tu diseño)
st.markdown("""
<div class="editor-banner">
  <div style="font-size:2.4rem; line-height:1;">🛻</div>
  <div>
    <h1>Editor Stellantis</h1>
    <p>Gestión total de cards · HTML en memoria</p>
  </div>
  <span class="badge">Multi-Card v2.5</span>
</div>
""", unsafe_allow_html=True)

# 3. CARGA DE ARCHIVO
archivo = st.file_uploader("Sube tu archivo HTML", type=["html"])

if archivo and st.session_state.soup is None:
    contenido = archivo.read().decode("utf-8")
    st.session_state.soup = BeautifulSoup(contenido, "html.parser")

if st.session_state.soup:
    soup = st.session_state.soup
    
    # 4. OBTENER ESTADO ACTUAL DE LAS CARDS
    def get_cards():
        return soup.find_all("article", class_="card")

    cards_html = get_cards()
    nombres_modelos = [c.find("h2").text.strip() for c in cards_html if c.find("h2")]

    col_izq, col_der = st.columns([1, 1])

    # --- COLUMNA IZQUIERDA: EDICIÓN DE CONTENIDO ---
    with col_izq:
        st.subheader("📝 Editar Unidades")
        modelo_a_editar = st.selectbox("Selecciona vehículo:", nombres_modelos)
        
        card_target = None
        for card in cards_html:
            if card.find("h2") and card.find("h2").text.strip() == modelo_a_editar:
                card_target = card
                break

        if card_target:
            with st.form("form_edicion", clear_on_submit=True):
                st.info(f"Modificando: **{modelo_a_editar}**")
                p1, p2 = st.columns(2)
                with p1:
                    nuevo_precio = st.text_input("Precio Principal")
                    nuevo_id_img = st.text_input("ID Cloudinary (Nombre)")
                    activar_inv = st.checkbox("Activar Inventario Especial")
                with p2:
                    nueva_promo = st.text_area("Promo (Negritas auto)")
                    nuevos_ben = st.text_area("Beneficios (uno por línea)")
                
                # Datos de Inventario
                st.markdown("---")
                inv_mod = st.text_input("Inv: Modelo/Año", "RAM 700 2025")
                inv_col = st.text_input("Inv: Color", "Blanco")
                inv_pre = st.text_input("Inv: Precio Contado", "340,000")

                if st.form_submit_button(f"💾 Guardar {modelo_a_editar}"):
                    # Lógica de Actualización de Texto y Estilos
                    if nuevo_precio:
                        tag = card_target.find(class_='model-price')
                        if tag: tag.string = f"Desde ${nuevo_precio}"
                    
                    if nuevo_id_img:
                        img = card_target.find('img')
                        if img:
                            clean_id = nuevo_id_img.strip()
                            img['src'] = f"https://res.cloudinary.com/dbxa0pozm/image/upload/w_600,q_auto,f_auto/{clean_id}.jpg"
                            img['srcset'] = f"https://res.cloudinary.com/dbxa0pozm/image/upload/w_400,q_auto,f_auto/{clean_id}.jpg 400w, https://res.cloudinary.com/dbxa0pozm/image/upload/w_600,q_auto,f_auto/{clean_id}.jpg 600w"

                    # Resaltado Automático (Strong) en Promo y Beneficios
                    regex_resaltado = r'(\$\d+(?:,\d+)*(?:\.\d+)?|0%|[1-9]\d*%)'
                    estilo_strong = r'<strong style="font-size:1.4em;color:var(--acento);">\1</strong>'

                    if nueva_promo:
                        p_div = card_target.find(class_='promo-main')
                        if p_div:
                            fmt = re.sub(regex_resaltado, estilo_strong, nueva_promo)
                            p_div.clear()
                            p_div.append(BeautifulSoup(f"<span>{fmt}</span>", 'html.parser'))

                    if nuevos_ben:
                        ul_b = card_target.find(class_='benefits-list')
                        if ul_b:
                            ul_b.clear()
                            for b in nuevos_ben.split('\n'):
                                if b.strip():
                                    b_fmt = re.sub(regex_resaltado, estilo_strong, b)
                                    li = soup.new_tag("li")
                                    li.append(BeautifulSoup(b_fmt, 'html.parser'))
                                    ul_b.append(li)

                    if activar_inv:
                        for comment in card_target.find_all(string=lambda text: isinstance(text, Comment)):
                            if "inventario-especial" in comment:
                                inv_s = BeautifulSoup(comment, 'html.parser')
                                det = inv_s.find(class_="inventario-detalle")
                                if det: det.string = f"{inv_mod} · Color: {inv_col}"
                                pre = inv_s.find(class_="inventario-precio")
                                if pre:
                                    pre.clear()
                                    pre.append(f"${inv_pre} ")
                                    pre.append(soup.new_tag("small"))
                                comment.replace_with(inv_s)
                                break
                    st.success("Cambios guardados.")
                    st.rerun()

    # --- COLUMNA DERECHA: GESTIÓN DE ESTRUCTURA ---
    with col_der:
        # AÑADIR
        st.subheader("➕ Añadir Unidad")
        with st.form("form_add"):
            n_nombre = st.text_input("Nombre nueva card")
            if st.form_submit_button("Agregar al final") and n_nombre:
                nueva = BeautifulSoup(str(cards_html[0]), 'html.parser').find('article')
                nueva.find('h2').string = n_nombre
                soup.find(class_='grid-promos').append(nueva)
                st.rerun()

        # MOVER
        st.subheader("↕️ Reordenar")
        m_modelo = st.selectbox("Mover esta card:", nombres_modelos, key="move_sel")
        m_pos = st.number_input("A la posición:", 1, len(nombres_modelos), value=1)
        if st.button("🚀 Reubicar"):
            grid = soup.find(class_="grid-promos")
            arts = [a for a in grid.find_all("article", class_="card", recursive=False)]
            target = next(a for a in arts if a.find("h2").text.strip() == m_modelo)
            target.extract()
            arts_restantes = [a for a in grid.find_all("article", class_="card", recursive=False)]
            idx = m_pos - 1
            if idx <= 0: grid.insert(0, target)
            elif idx >= len(arts_restantes): grid.append(target)
            else: arts_restantes[idx].insert_before(target)
            st.rerun()

        # ELIMINAR
        st.subheader("🗑️ Eliminar")
        e_modelo = st.selectbox("Eliminar:", nombres_modelos, key="del_sel")
        confirm = st.checkbox("Confirmar eliminación")
        if st.button("Borrar permanentemente", disabled=not confirm):
            for c in soup.find_all("article", class_="card"):
                if c.find("h2").text.strip() == e_modelo:
                    c.decompose()
                    st.rerun()

    st.divider()
    # 5. DESCARGA
    html_final = soup.prettify(formatter="html")
    st.download_button("📥 DESCARGAR CATÁLOGO COMPLETO", html_final, "catalogo_final.html", "text/html", use_container_width=True)
    if st.button("♻️ Reiniciar Editor"):
        st.session_state.soup = None
        st.rerun()