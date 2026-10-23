import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Suite Educativa: Sistemas Numéricos y CPU", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PERSONALIZADOS (PALETA SUAVE Y VISUAL) ---
st.markdown("""
    <style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Contenedores / Tarjetas estéticas */
    div.stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    div.stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 6px 6px 0px 0px;
        color: #334155;
        font-weight: 600;
        padding: 10px 20px;
    }
    
    div.stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: white !important;
    }
    
    /* Cajas de código personalizadas */
    pre {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #0f172a !important;
        font-family: 'Consolas', monospace !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Suite Educativa Interactiva: Sistemas Numéricos y CPU Pro")
st.markdown("Herramienta didáctica integral para comprender la conversión numérica, la aritmética binaria paso a paso y la arquitectura interna de un computador.")

# Pestañas principales
pest1, pest2, pest3 = st.tabs([
    "🧮 Conversor Decimal ⇄ Binario", 
    "🔢 Calculadora Binaria y Lógica", 
    "⚙️ Dashboard CPU Von Neumann"
])

# ==========================================
# PESTAÑA 1: CONVERSOR UNIFICADO
# ==========================================
with pest1:
    st.subheader("Conversor Bidireccional (Decimal, Texto ASCII y Binario)")
    tipo_conv = st.selectbox("Selecciona el tipo de conversión", ["Decimal a Binario / ASCII", "Binario a Decimal"], key="conv_tipo")
    valor_conv = st.text_input("Ingresa un valor (número decimal o texto):", "21", key="conv_val")
    
    if st.button("Procesar Conversión", type="primary"):
        if not valor_conv.strip():
            st.warning("Por favor, ingresa un valor.")
        elif "Decimal" in tipo_conv:
            if valor_conv.isdigit():
                dec = int(valor_conv)
                st.success(f"Número Decimal Principal: {dec} ➔ Binario: {bin(dec)[2:]}")
                
                st.markdown("### 📐 Método de Divisiones Sucesivas entre 2 (Paso a Paso)")
                temp = dec
                pasos_data = []
                
                if temp == 0:
                    pasos_data.append({"Dividendo": 0, "Cociente": 0, "Residuo": 0})
                    bin_str = "0"
                else:
                    bin_str = ""
                    while temp > 0:
                        cociente = temp // 2
                        residuo = temp % 2
                        pasos_data.append({"Dividendo": temp, "Cociente": cociente, "Residuo": residuo})
                        bin_str = str(residuo) + bin_str
                        temp //= 2
                        
                desglose_div = f"  Proceso de conversión para el número decimal {dec}:\n\n"
                for idx, p in enumerate(pasos_data):
                    desglose_div += f"    Paso {idx+1}: {p['Dividendo']} ÷ 2  ➔  Cociente = {p['Cociente']}  |  Residuo = {p['Residuo']}\n"
                
                st.code(desglose_div)
                st.info(f"👉 Leyendo los residuos de **abajo hacia arriba**, obtenemos el binario final: **{bin_str}**")
            else:
                st.write("### Conversión de caracteres ASCII:")
                for c in valor_conv:
                    val_asc = ord(c)
                    st.info(f"Carácter '{c}' ➔ ASCII: {val_asc} ➔ Binario: {bin(val_asc)[2:]}")
        else:
            if all(c in '01' for c in valor_conv):
                dec_total = int(valor_conv, 2)
                st.success(f"Binario: {valor_conv} ➔ Decimal: {dec_total}")
            else:
                st.error("Ingresa una cadena binaria válida (solo 0s y 1s).")

# ==========================================
# PESTAÑA 2: CALCULADORA BINARIA Y LÓGICA
# ==========================================
with pest2:
    st.subheader("Calculadora Aritmética y Lógica Binaria (Paso a Paso)")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        b1 = st.text_input("Binario A:", "10101", key="calc_b1")
    with col_i2:
        b2 = st.text_input("Binario B:", "101", key="calc_b2")
        
    op = st.selectbox("Operadores:", ["+", "-", "×", "÷", "AND", "OR", "NOT"], key="calc_op")
    
    if st.button("Calcular Operación Binaria", type="primary"):
        if not b1 or not all(c in '01' for c in b1) or (op != "NOT" and (not b2 or not all(c in '01' for c in b2))):
            st.error("Por favor, ingresa cadenas binarias válidas (0s y 1s).")
        else:
            d1 = int(b1, 2)
            d2 = int(b2, 2) if op != "NOT" else 0
            res_dec = 0
            
            if op == "+": res_dec = d1 + d2
            elif op == "-": res_dec = max(0, d1 - d2)
            elif op == "×": res_dec = d1 * d2
            elif op == "÷":
                if d2 == 0:
                    st.error("No se puede dividir entre cero.")
                    res_dec = None
                else:
                    res_dec = d1 // d2
            elif op == "AND": res_dec = d1 & d2
            elif op == "OR": res_dec = d1 | d2
            elif op == "NOT": res_dec = ((1 << len(b1)) - 1) ^ d1
            
            if res_dec is not None:
                res_bin = bin(res_dec)[2:]
                st.markdown(f"### Resultado Binario: {res_bin}")
                st.markdown(f"**Resultado Decimal:** {res_dec}")
                
                st.markdown(f"#### 📐 DESGLOSE PASO A PASO AL MARGEN ({op})")
                
                # 1. SUMA Y RESTA
                if op in ["+", "-"]:
                    simbolo = "+" if op == "+" else "-"
                    max_l = max(len(b1), len(b2), len(res_bin))
                    st.code(f"""
        Num A:     {b1.zfill(max_l)}   (Decimal: {d1})
    {simbolo}   Num B:     {b2.zfill(max_l)}   (Decimal: {d2})
        ────────────────────────
    =   Resultado: {res_bin.zfill(max_l)}   (Decimal: {res_dec})
                    """)
                
                # 2. MULTIPLICACIÓN
                elif op == "×":
                    ancho = max(len(b1), len(b2), len(res_bin)) + 6
                    lineas_mult = f"        Num A: {b1.rjust(ancho)}   (Decimal: {d1})\n"
                    lineas_mult += f"    ×   Num B: {b2.rjust(ancho)}   (Decimal: {d2})\n"
                    lineas_mult += f"        " + "─" * (ancho + 7) + "\n"
                    
                    for idx, bit in enumerate(reversed(b2)):
                        if bit == '1':
                            parcial = b1 + ('0' * idx)
                        else:
                            parcial = '0' * (len(b1) + idx)
                        line_p = parcial.rjust(ancho)
                        lineas_mult += f"        P.Parcial (si bit={bit}) : {line_p}\n"
                        
                    lineas_mult += f"        " + "─" * (ancho + 7) + "\n"
                    lineas_mult += f"    =   Resultado: {res_bin.rjust(ancho)}   (Decimal: {res_dec})"
                    st.code(lineas_mult)

                # 3. DIVISIÓN
                elif op == "÷" and d2 != 0:
                    cociente_str = bin(d1 // d2)[2:]
                    residuo_dec = d1 % d2
                    
                    desglose_galera = f"        Num A (Dividendo): {b1}   (Decimal: {d1})\n"
                    desglose_galera += f"        Num B (Divisor)  : {b2}   (Decimal: {d2})\n\n"
                    desglose_galera += f"        {b1}  │ {b2}\n"
                    desglose_galera += f"        " + "─"*len(b1) + "  ├" + "─"*len(b2) + "\n"
                    desglose_galera += f"        " + " "*len(b1) + f"  │ {cociente_str}\n\n"
                    desglose_galera += f"        PASO A PASO DE RESTAS PARCIALES:\n"
                    
                    curr_val = 0
                    for i, bit in enumerate(b1):
                        curr_val = (curr_val << 1) | int(bit)
                        if curr_val >= d2:
                            desglose_galera += f"          - Tomamos grupo, restamos {b2} (Dec: {d2}) ➔ Resto parcial: {bin(curr_val - d2)[2:]}\n"
                            curr_val -= d2
                        else:
                            desglose_galera += f"          - Bajamos bit '{bit}' ➔ Valor acumulado: {bin(curr_val)[2:]}\n"
                            
                    desglose_galera += f"\n    = Cociente : {cociente_str}   (Decimal: {d1 // d2})\n"
                    desglose_galera += f"    = Residuo  : {bin(residuo_dec)[2:]}   (Decimal: {residuo_dec})"
                    st.code(desglose_galera)

                # 4. OPERADORES LÓGICOS
                else:
                    max_len = max(len(b1), len(b2))
                    b1_n = b1.zfill(max_len)
                    b2_n = b2.zfill(max_len)
                    tabla_logica = " Posición | Bit A | Bit B | Operación Bit a Bit | Resultado\n"
                    tabla_logica +=" ─────────┼───────┼───────┼─────────────────────┼──────────\n"
                    for idx in range(max_len):
                        ba = b1_n[idx]
                        bb = b2_n[idx] if op != "NOT" else "-"
                        bres = res_bin.zfill(max_len)[idx]
                        pos = max_len - 1 - idx
                        desc = f"{ba} {op} {bb}" if op != "NOT" else f"NOT {ba}"
                        tabla_logica += f"   2^{pos:<2}   |   {ba}   |   {bb}   |     {desc:<15} |     {bres}\n"
                    st.code(tabla_logica)

# ==========================================
# PESTAÑA 3: DASHBOARD VON NEUMANN INTERACTIVO
# ==========================================
with pest3:
    st.subheader("⚙️ Simulador Interactivo CPU Von Neumann")
    
    col_cpu1, col_cpu2 = st.columns(2)
    with col_cpu1:
        val_a = st.number_input("Valor Decimal A", value=6, key="cpu_a")
        val_b = st.number_input("Valor Decimal B", value=4, key="cpu_b")
        op_cpu = st.selectbox("Operación ALU", ["+", "-", "×", "÷"], key="cpu_op")
        
    with col_cpu2:
        st.markdown("### Control de Ciclo de Instrucción")
        if "fase_activa" not in st.session_state:
            st.session_state.fase_activa = 1
            
        fase_opciones = ["1. FETCH (Búsqueda)", "2. DECODE (Decodificación)", "3. EXECUTE (Ejecución ALU)", "4. STORE (Almacenamiento)"]
        fase_seleccionada = st.radio("Avanzar paso a paso:", fase_opciones, index=st.session_state.fase_activa - 1)
        st.session_state.fase_activa = fase_opciones.index(fase_seleccionada) + 1

    st.markdown("---")
    
    if op_cpu == "+": res_cpu = val_a + val_b
    elif op_cpu == "-": res_cpu = max(0, val_a - val_b)
    elif op_cpu == "×": res_cpu = val_a * val_b
    else: res_cpu = (val_a // val_b) if val_b != 0 else 0
    
    b_a = bin(val_a)[2:].zfill(8)
    b_b = bin(val_b)[2:].zfill(8)
    
    fase = st.session_state.fase_activa
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🧠 Estado de los Registros Internos")
        st.code(f"""
  [ PC ] Program Counter : 0x0042
  [MAR ] Memoria Addr    : 0x01FA
  [MDR ] Memoria Data    : OP={op_cpu}, A={val_a}, B={val_b}
  [ IR ] Inst. Register  : EXECUTING_{op_cpu}
  [ALU ] Procesamiento   : {val_a} {op_cpu} {val_b}
  [ AC ] Acumulador      : {res_cpu if fase >= 4 else 'Vacío / En proceso'}
        """)
        
    with col_b:
        st.markdown("#### 🔍 Explicación Interactiva del Momento")
        if fase == 1:
            st.info(f"""
            **Fase 1: FETCH (Búsqueda de la Instrucción en RAM)**
            * El **PC** (Contador de Programa) apunta a la dirección de memoria actual (`0x0042`).
            * El **MAR** carga la dirección y el **MDR** recupera desde la RAM los operandos `A = {b_a}` y `B = {b_b}`.
            * Todo viaja por el Bus de Sistema hacia el **IR** (Registro de Instrucción).
            """)
        elif fase == 2:
            st.warning(f"""
            **Fase 2: DECODE (Decodificación en la Unidad de Control)**
            * La **Unidad de Control (UC)** analiza el código de operación (`{op_cpu}`).
            * Interpreta que se requiere activar los circuitos aritméticos de la **ALU**.
            * Configura los multiplexores internos para rutear los bits de los operandos.
            """)
        elif fase == 3:
            st.error(f"""
            **Fase 3: EXECUTE (Ejecución en la ALU)**
            * La **ALU** (Unidad Aritmética Lógica) realiza el cálculo físico a nivel de compuertas lógicas.
            * Operación en curso: **`{val_a} {op_cpu} {val_b}`**.
            * Resultado temporal obtenido en circuitos internos: **`{res_cpu}`** (Binario: `{bin(res_cpu)[2:]}`).
            """)
        else:
            st.success(f"""
            **Fase 4: STORE (Almacenamiento de Resultados)**
            * El resultado final de la operación (`{res_cpu}`) se escribe y deposita de forma definitiva en el **Acumulador (AC)**.
            * Queda disponible para futuras instrucciones o para ser exportado a memoria RAM o pantalla.
            """)
