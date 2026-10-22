import streamlit as st

st.set_page_config(page_title="Suite Educativa: Sistemas Numéricos y CPU", layout="wide")

st.title("⚡ Suite Educativa Interactiva: Sistemas Numéricos y CPU Pro")

# Pestañas principales
pest1, pest2, pest3 = st.tabs([
    "Conversor Decimal ⇄ Binario", 
    "Calculadora Binaria y Lógica", 
    "Dashboard CPU Von Neumann"
])

# ==========================================
# PESTAÑA 1: CONVERSOR UNIFICADO
# ==========================================
with pest1:
    st.header("Conversor Bidireccional (Decimal, Texto ASCII y Binario)")
    tipo_conv = st.selectbox("Selecciona el tipo de conversión", ["Decimal a Binario / ASCII", "Binario a Decimal"], key="conv_tipo")
    valor_conv = st.text_input("Ingresa un valor:", "21", key="conv_val")
    
    if st.button("Procesar Conversión"):
        if not valor_conv.strip():
            st.warning("Por favor, ingresa un valor.")
        elif "Decimal" in tipo_conv:
            if valor_conv.isdigit():
                dec = int(valor_conv)
                st.success(f"Número Decimal: {dec} ➔ Binario: {bin(dec)[2:]}")
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
    st.header("Calculadora Aritmética y Lógica Binaria")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        b1 = st.text_input("Binario A (Dividendo / Operando 1):", "101010", key="calc_b1")
    with col_i2:
        b2 = st.text_input("Binario B (Divisor / Operando 2):", "110", key="calc_b2")
        
    op = st.selectbox("Selecciona la operación:", ["+", "-", "×", "÷", "AND", "OR", "NOT"], key="calc_op")
    
    if st.button("Calcular Operación Binaria"):
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
                st.metric("Resultado Decimal", res_dec)
                st.code(f"Resultado Binario: {res_bin}")
                
                st.markdown("### 📐 Estructura Visual del Proceso:")
                if op == "÷" and d2 != 0:
                    # Simulación visual estilo galera
                    indices_marcados = set()
                    curr_val = 0
                    for i, bit in enumerate(b1):
                        curr_val = (curr_val << 1) | int(bit)
                        if curr_val >= d2:
                            indices_marcados.add(i)
                            curr_val -= d2
                    
                    linea_div = "".join([bit + ("'" if i in indices_marcados else " ") for i, bit in enumerate(b1)])
                    st.code(f"""
  {linea_div}  │ {b2}
  {'─' * len(linea_div)}  ├─{'─' * len(b2)}
  {' ' * len(linea_div)}  │ {res_bin}

  * Decimal Inicial (A): {d1}
  * Decimal Divisor (B): {d2}
  * Cociente Decimal: {d1 // d2}
  * Residuo Decimal: {d1 % d2}
                    """)
                elif op == "×":
                    st.code(f"""
        {b1.rjust(12)}   (Decimal: {d1})
    ×   {b2.rjust(12)}   (Decimal: {d2})
        ──────────────
    =   {res_bin.rjust(12)}   (Decimal: {res_dec})
                    """)
                else:
                    st.code(f"Operación lógica/aritmética completada exitosamente entre {b1} y {b2}.")

# ==========================================
# PESTAÑA 3: DASHBOARD VON NEUMANN
# ==========================================
with pest3:
    st.header("⚡ Simulador CPU Von Neumann con Fases")
    
    col_cpu1, col_cpu2 = st.columns(2)
    with col_cpu1:
        val_a = st.number_input("Valor Decimal A", value=6, key="cpu_a")
        val_b = st.number_input("Valor Decimal B", value=4, key="cpu_b")
        op_cpu = st.selectbox("Operación ALU", ["+", "-", "×", "÷"], key="cpu_op")
        
    with col_cpu2:
        st.markdown("### Ciclo de Instrucción")
        fase_cpu = st.radio("Selecciona la fase activa:", [
            "1. FETCH (Búsqueda en RAM - Ámbar)",
            "2. DECODE (Decodificación UC - Azul)",
            "3. EXECUTE (Cálculo en ALU - Púrpura)",
            "4. STORE (Almacenamiento AC - Verde)"
        ])
        
    st.markdown("---")
    
    # Cálculo en vivo
    if op_cpu == "+": res_cpu = val_a + val_b
    elif op_cpu == "-": res_cpu = max(0, val_a - val_b)
    elif op_cpu == "×": res_cpu = val_a * val_b
    else: res_cpu = (val_a // val_b) if val_b != 0 else 0
    
    b_a_bin = bin(val_a)[2:].zfill(8)
    b_b_bin = bin(val_b)[2:].zfill(8)
    
    if fase_cpu.startswith("1"):
        st.info(f"**[FETCH]** El Contador de Programa (PC) apunta a la celda 0x42 de la RAM. La RAM envía la orden `{op_cpu}` y los operandos A=`{b_a_bin}`, B=`{b_b_bin}` hacia el Registro de Instrucción (IR).")
    elif fase_cpu.startswith("2"):
        st.info(f"**[DECODE]** La Unidad de Control (UC) decodifica la instrucción `{op_cpu}` y prepara los buses internos de datos hacia la ALU.")
    elif fase_cpu.startswith("3"):
        st.info(f"**[EXECUTE]** La ALU procesa la operación aritmética: `{val_a} {op_cpu} {val_b}` obteniendo el resultado temporal `{res_cpu}`.")
    else:
        st.success(f"**[STORE]** El resultado final `{res_cpu}` (Binario: `{bin(res_cpu)[2:]}`) se guarda de forma permanente en el Acumulador (AC).")
