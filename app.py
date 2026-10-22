import tkinter as tk
from tkinter import ttk, messagebox

# --- PALETA DE COLORES BASE ---
COLOR_BG = "#f1f5f9"          # Fondo general gris muy claro
COLOR_CARD = "#ffffff"        # Fondo blanco puro
COLOR_TEXT = "#0f172a"        # Texto principal oscuro
COLOR_TEXT_MUTED = "#475569"  # Texto secundario gris
COLOR_ACCENT = "#2563eb"      # Azul vibrante principal
COLOR_SUCCESS = "#059669"     # Verde esmeralda
COLOR_BORDER = "#cbd5e1"      # Bordes suaves

# --- COLORES EXCLUSIVOS POR FASE DEL CICLO DE INSTRUCCIÓN ---
COLOR_FETCH = "#f59e0b"       # Ámbar / Naranja (FETCH)
COLOR_DECODE = "#2563eb"      # Azul Cobalto (DECODE)
COLOR_EXECUTE = "#7c3aed"     # Púrpura (EXECUTE)
COLOR_STORE = "#059669"       # Verde Esmeralda (STORE)

def aplicar_estilos_claros():
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TNotebook", background=COLOR_BG, borderwidth=0)
    estilo.configure("TNotebook.Tab", background="#e2e8f0", foreground=COLOR_TEXT, padding=[14, 8], font=("Segoe UI", 10, "bold"))
    estilo.map("TNotebook.Tab", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#ffffff")])
    estilo.configure("Treeview", background="#ffffff", foreground=COLOR_TEXT, rowheight=28, fieldbackground="#ffffff", font=("Segoe UI", 10))
    estilo.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", "#000000")])
    estilo.configure("Treeview.Heading", background="#e2e8f0", foreground=COLOR_TEXT, font=("Segoe UI", 10, "bold"))

# --- PESTAÑA 1: CONVERSOR UNIFICADO ---
def procesar_conversor_unificado():
    tipo = combo_conv.get()
    valor = entrada_conv.get().strip()
    
    if not valor:
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa un valor para convertir.")
        return
        
    for item in tabla_conv.get_children():
        tabla_conv.delete(item)
        
    if "Decimal a Binario" in tipo:
        elementos = [("Número", int(valor))] if valor.isdigit() else [(c, ord(c)) for c in valor]
        for etiqueta, decimal in elementos:
            temp, pasos, bin_str = decimal, [], ""
            if temp == 0:
                pasos.append((0, 2, 0, 0))
                bin_str = "0"
            else:
                while temp > 0:
                    pasos.append((temp, 2, temp // 2, temp % 2))
                    bin_str = str(temp % 2) + bin_str
                    temp //= 2
            ancho = max(8, (len(bin_str) + 3) // 4 * 4)
            bin_completo = bin_str.zfill(ancho)
            nombre = f"Dec: {decimal}" if etiqueta == "Número" else f"ASCII '{etiqueta}'"
            id_p = tabla_conv.insert("", "end", values=(nombre, decimal, "Conversión Div/2", bin_completo), open=True)
            for i, (div, dis, coc, res) in enumerate(pasos):
                tabla_conv.insert(id_p, "end", values=(f"Paso {i+1}: {div} ÷ {dis}", f"Cociente: {coc}", f"Residuo: {res}", ""))
    else:
        if not all(c in '01' for c in valor):
            messagebox.showerror("Error", "Ingresa una cadena binaria válida (0s y 1s).")
            return
        decimal_total = int(valor, 2)
        id_p = tabla_conv.insert("", "end", values=(f"Bin: {valor}", f"Total: {decimal_total}", "Suma Posicional", "-"), open=True)
        for i, bit in enumerate(reversed(valor)):
            val_pos = 2 ** i
            tabla_conv.insert(id_p, "end", values=(f"Bit '{bit}' pos 2^{i}", f"+ {int(bit) * val_pos}", f"{bit} × {val_pos}", f"Posición {i}"))

# --- PESTAÑA 2: CALCULADORA BINARIA VISUAL ---
def calcular_binario_completo(operacion):
    b1 = entrada_op1.get().strip()
    b2 = entrada_op2.get().strip() if operacion != "NOT" else "0"
    
    if not b1 or not all(c in '01' for c in b1) or (operacion != "NOT" and (not b2 or not all(c in '01' for c in b2))):
        messagebox.showerror("Error", "Ingresa cadenas binarias válidas (0s y 1s).")
        return
        
    d1 = int(b1, 2)
    d2 = int(b2, 2) if operacion != "NOT" else 0
    res_dec = 0
    
    if operacion == "+": res_dec = d1 + d2
    elif operacion == "-": res_dec = max(0, d1 - d2)
    elif operacion == "×": res_dec = d1 * d2
    elif operacion == "÷":
        if d2 == 0:
            messagebox.showerror("Error", "No se puede dividir entre cero.")
            return
        res_dec = d1 // d2
    elif operacion == "AND": res_dec = d1 & d2
    elif operacion == "OR": res_dec = d1 | d2
    elif operacion == "NOT": res_dec = ((1 << len(b1)) - 1) ^ d1

    res_bin = bin(res_dec)[2:]
    lbl_res_bin.config(text=f"Resultado Binario: {res_bin}")
    lbl_res_dec.config(text=f"Resultado Decimal: {res_dec}")
    
    txt_proceso.delete("1.0", tk.END)
    txt_proceso.insert(tk.END, f"📐 ESTRUCTURA VISUAL DE LA OPERACIÓN ({operacion})\n")
    txt_proceso.insert(tk.END, f"─────────────────────────────────────────────────────────────\n")
    
    # 1. DIVISIÓN TRADICIONAL ESTILO PIZARRA CON COMILLAS DE SEPARACIÓN Y SUBRAYADOS
    if operacion == "÷":
        cociente_bin = bin(d1 // d2)[2:]
        residuo_dec = d1 % d2
        residuo_bin = bin(residuo_dec)[2:]
        
        txt_proceso.insert(tk.END, f"  Num A (Dividendo): {b1}  (Decimal: {d1})\n")
        txt_proceso.insert(tk.END, f"  Num B (Divisor)  : {b2}  (Decimal: {d2})\n\n")
        
        # Generar dividendo con marcadores de comilla (') en las posiciones de separación
        bits_div = list(b1)
        marcas = [""] * len(b1)
        
        # Algoritmo de rastreo de restas y marcas
        curr_val = 0
        pasos_resta = []
        indices_marcados = set()
        
        for i, bit in enumerate(b1):
            curr_val = (curr_val << 1) | int(bit)
            if curr_val >= d2:
                indices_marcados.add(i)
                pasos_resta.append((i, curr_val, curr_val - d2))
                curr_val -= d2
                
        # Construir primera línea con comillas (ej: 1'0 1 0'1'0')
        linea_div_marcada = ""
        for idx, bit in enumerate(b1):
            linea_div_marcada += bit + ("'" if idx in indices_marcados else " ")
            
        dis_len = len(b2)
        txt_proceso.insert(tk.END, f"       {linea_div_marcada}  │ {b2}\n")
        txt_proceso.insert(tk.END, f"       {' ' * len(linea_div_marcada)}  ├─{'─' * max(dis_len, len(cociente_bin))}\n")
        txt_proceso.insert(tk.END, f"       {' ' * len(linea_div_marcada)}  │ {cociente_bin}\n\n")
        
        # Desarrollo paso a paso con las restas e índices alineados
        curr_val = 0
        curr_str = ""
        
        for i, bit in enumerate(b1):
            curr_str += bit
            curr_val = (curr_val << 1) | int(bit)
            
            if curr_val >= d2:
                pos_indent = i * 2 - (dis_len * 2 - 2)
                espacios = " " * (pos_indent + 7)
                
                # Subrayado previo a la resta
                txt_proceso.insert(tk.END, f"{espacios}  {'─' * (dis_len * 2)}\n")
                txt_proceso.insert(tk.END, f"{espacios}- { ' '.join(list(b2)) }\n")
                txt_proceso.insert(tk.END, f"{espacios}  {'─' * (dis_len * 2)}\n")
                
                curr_val -= d2
                curr_str = bin(curr_val)[2:] if curr_val > 0 else "0"
                
                if i < len(b1) - 1:
                    sig_bit = b1[i + 1]
                    siguiente_grupo = curr_str + sig_bit if curr_str != "0" else sig_bit
                    offset_res = " " * ((i + 1) * 2 - len(siguiente_grupo) * 2 + 9)
                    txt_proceso.insert(tk.END, f"{offset_res}{' '.join(list(siguiente_grupo))}\n")
        
        espacio_res = " " * (len(b1) * 2 + 5)
        txt_proceso.insert(tk.END, f"\n{espacio_res}{bin(curr_val)[2:]}\n\n")
        txt_proceso.insert(tk.END, f"  ──────────────────────────────────────────────\n")
        txt_proceso.insert(tk.END, f"  = Cociente : {cociente_bin}  (Decimal: {d1 // d2})\n")
        txt_proceso.insert(tk.END, f"  = Residuo  : {residuo_bin}  (Decimal: {residuo_dec})\n")

    # 2. MULTIPLICACIÓN EN BLOQUES DE PRODUCTOS PARCIALES (ALINEACIÓN LIMPIA)
    elif operacion == "×":
        ancho_max = max(len(b1), len(b2), len(res_bin)) + 4
        
        txt_proceso.insert(tk.END, f"       {b1.rjust(ancho_max)}   (Decimal: {d1})\n")
        txt_proceso.insert(tk.END, f"   ×   {b2.rjust(ancho_max)}   (Decimal: {d2})\n")
        txt_proceso.insert(tk.END, f"       {'─'*ancho_max}\n")
        
        for i, bit in enumerate(reversed(b2)):
            if bit == '1':
                parcial = b1 + ('0' * i)
            else:
                parcial = '0' * (len(b1) + i)
            txt_proceso.insert(tk.END, f"       {parcial.rjust(ancho_max)}\n")
            
        txt_proceso.insert(tk.END, f"       {'─'*ancho_max}\n")
        txt_proceso.insert(tk.END, f"   =   {res_bin.rjust(ancho_max)}   (Decimal: {res_dec})\n")

    # 3. OPERADORES LÓGICOS (AND, OR, NOT)
    elif operacion in ["AND", "OR", "NOT"]:
        max_len = max(len(b1), len(b2))
        b1_n = b1.zfill(max_len)
        b2_n = b2.zfill(max_len)
        
        txt_proceso.insert(tk.END, f" Posición |  Bit A  |  Bit B  |  Operación Lógica  | Resultado Bit\n")
        txt_proceso.insert(tk.END, f" ─────────┼─────────┼─────────┼────────────────────┼──────────────\n")
        for idx in range(max_len):
            bit_a, bit_b = b1_n[idx], b2_n[idx]
            bit_res = res_bin.zfill(max_len)[idx]
            pos = max_len - 1 - idx
            op_desc = f"{bit_a} {operacion} {bit_b}" if operacion != "NOT" else f"NOT {bit_a}"
            bit_b_disp = bit_b if operacion != "NOT" else "-"
            txt_proceso.insert(tk.END, f"   2^{pos:<2}    |    {bit_a}    |    {bit_b_disp}    |     {op_desc:<14} |       {bit_res}\n")

    # 4. SUMA Y RESTA ARITMÉTICA
    else:
        max_len = max(len(b1), len(b2), len(res_bin))
        txt_proceso.insert(tk.END, f"       Num A:   {b1.zfill(max_len):>12}   (Decimal: {d1})\n")
        txt_proceso.insert(tk.END, f"   {operacion:>3} Num B:   {b2.zfill(max_len):>12}   (Decimal: {d2})\n")
        txt_proceso.insert(tk.END, f"       ─────────{'─'*max_len}\n")
        txt_proceso.insert(tk.END, f"   = Resultado: {res_bin.zfill(max_len):>12}   (Decimal: {res_dec})\n")

# --- PESTAÑA 3: DASHBOARD VON NEUMANN CON FASES Y COLORES COORDINADOS ---
estado_dash_lat = {"paso": 0, "d1": 0, "d2": 0, "op": "+", "res": 0, "b1": "", "b2": ""}

def seleccionar_op_dash(op):
    op_seleccionada_dash.set(op)
    for o, btn in botones_dash.items():
        if o == op:
            btn.config(bg=COLOR_ACCENT, fg="#ffffff")
        else:
            btn.config(bg="#e2e8f0", fg=COLOR_TEXT)

def inicializar_dashboard_lat():
    global estado_dash_lat
    val_a = entrada_a_dash.get().strip()
    val_b = entrada_b_dash.get().strip()
    op = op_seleccionada_dash.get()

    if not val_a.isdigit() or not val_b.isdigit():
        messagebox.showerror("Error", "Ingresa números decimales válidos para A y B.")
        return

    d1, d2 = int(val_a), int(val_b)
    res = 0

    if op == "+": res = d1 + d2
    elif op == "-": res = max(0, d1 - d2)
    elif op == "×": res = d1 * d2
    elif op == "÷": res = (d1 // d2) if d2 != 0 else 0
    elif op == "AND": res = d1 & d2
    elif op == "OR": res = d1 | d2
    elif op == "NOT": res = 0 if d1 > 0 else 1

    estado_dash_lat = {
        "paso": 1, "d1": d1, "d2": d2, "op": op, "res": res,
        "b1": bin(d1)[2:].zfill(8), "b2": bin(d2)[2:].zfill(8)
    }

    btn_p1.config(state=tk.NORMAL, bg=COLOR_FETCH, fg="#ffffff")
    btn_p2.config(state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff")
    btn_p3.config(state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff")
    btn_p4.config(state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff")

    actualizar_todo_von_neumann(1)

def ejecutar_paso_lat(fase):
    global estado_dash_lat
    estado_dash_lat["paso"] = fase
    actualizar_todo_von_neumann(fase)

    if fase == 1:
        btn_p1.config(bg=COLOR_FETCH, fg="#ffffff")
        btn_p2.config(state=tk.NORMAL, bg=COLOR_DECODE, fg="#ffffff")
    elif fase == 2:
        btn_p2.config(bg=COLOR_DECODE, fg="#ffffff")
        btn_p3.config(state=tk.NORMAL, bg=COLOR_EXECUTE, fg="#ffffff")
    elif fase == 3:
        btn_p3.config(bg=COLOR_EXECUTE, fg="#ffffff")
        btn_p4.config(state=tk.NORMAL, bg=COLOR_STORE, fg="#ffffff")
    elif fase == 4:
        btn_p4.config(bg=COLOR_STORE, fg="#ffffff")

def actualizar_todo_von_neumann(paso):
    colores_fase = {
        1: COLOR_FETCH,     # Naranja Ámbar
        2: COLOR_DECODE,    # Azul Cobalto
        3: COLOR_EXECUTE,   # Púrpura
        4: COLOR_STORE      # Verde Esmeralda
    }
    color_activo = colores_fase.get(paso, COLOR_ACCENT)

    # 1. ACTUALIZAR PANEL LATERAL IZQUIERDO
    canvas_lat.delete("all")
    fases_info = [
        ("1. FETCH", "Búsqueda en RAM", COLOR_FETCH),
        ("2. DECODE", "Decodificación UC", COLOR_DECODE),
        ("3. EXECUTE", "Cálculo en ALU", COLOR_EXECUTE),
        ("4. STORE", "Guardar en AC", COLOR_STORE)
    ]
    
    for i, (nombre, sub, col) in enumerate(fases_info):
        y = 40 + (i * 95)
        es_actual = (paso == i + 1)
        ya_paso = (paso > i + 1)
        
        bg_box = col if es_actual else (col if ya_paso else "#e2e8f0")
        txt_col = "#ffffff" if (es_actual or ya_paso) else COLOR_TEXT
        
        canvas_lat.create_rectangle(15, y, 215, y+70, outline="#94a3b8", width=2 if not es_actual else 3, fill=bg_box)
        canvas_lat.create_text(115, y+25, text=nombre, fill=txt_col, font=("Segoe UI", 10, "bold"))
        canvas_lat.create_text(115, y+48, text=sub, fill=txt_col, font=("Segoe UI", 8))
        
        if i < 3:
            canvas_lat.create_line(115, y+70, 115, y+95, fill=col if ya_paso else "#94a3b8", width=3, arrow=tk.LAST)

    # 2. ACTUALIZAR DIAGRAMA DE COMPONENTES DE CPU
    canvas_cpu.delete("all")
    d1, d2, op, res = estado_dash_lat["d1"], estado_dash_lat["d2"], estado_dash_lat["op"], estado_dash_lat["res"]
    b1, b2 = estado_dash_lat["b1"], estado_dash_lat["b2"]

    c_ram = COLOR_FETCH if paso == 1 else "#1e293b"
    c_pc = COLOR_FETCH if paso == 1 else "#e2e8f0"
    c_ir = COLOR_DECODE if paso in [1, 2] else "#e2e8f0"
    c_alu = COLOR_EXECUTE if paso == 3 else "#f1f5f9"
    c_ac = COLOR_STORE if paso >= 4 else "#e2e8f0"

    # RAM
    canvas_cpu.create_rectangle(500, 20, 630, 310, outline="#334155", width=3, fill=c_ram)
    canvas_cpu.create_text(565, 45, text="MEMORIA RAM", fill="#ffffff", font=("Segoe UI", 10, "bold"))
    canvas_cpu.create_text(565, 95, text=f"[42] OP: {op}", fill="#ffffff" if paso==1 else "#cbd5e1", font=("Consolas", 9, "bold"))
    canvas_cpu.create_text(565, 140, text=f"[43] A: {b1}", fill="#ffffff" if paso==1 else "#cbd5e1", font=("Consolas", 8))
    canvas_cpu.create_text(565, 190, text=f"[44] B: {b2}", fill="#ffffff" if paso==1 else "#cbd5e1", font=("Consolas", 8))

    # Bus RAM -> IR
    f_col1 = COLOR_FETCH if paso >= 1 else "#cbd5e1"
    canvas_cpu.create_line(390, 160, 500, 160, fill=f_col1, width=4, arrow=tk.LAST)
    canvas_cpu.create_text(445, 140, text="1. Bus Fetch", fill=f_col1, font=("Segoe UI", 8, "bold"))

    # PC
    canvas_cpu.create_rectangle(300, 230, 420, 290, outline="#64748b", width=2, fill=c_pc)
    canvas_cpu.create_text(360, 250, text="PC", fill="#ffffff" if paso==1 else COLOR_TEXT, font=("Segoe UI", 9, "bold"))
    canvas_cpu.create_text(360, 272, text="0x0042", fill="#ffffff" if paso==1 else COLOR_TEXT, font=("Consolas", 9, "bold"))

    # IR & UC
    canvas_cpu.create_rectangle(30, 20, 250, 130, outline="#64748b", width=2, fill=c_ir)
    canvas_cpu.create_text(140, 42, text="IR (Registro Instrucción)", fill="#ffffff" if paso in [1,2] else COLOR_TEXT, font=("Segoe UI", 9, "bold"))
    canvas_cpu.create_text(140, 75, text=f"Orden: [{op}]", fill="#ffffff" if paso in [1,2] else COLOR_TEXT, font=("Consolas", 10, "bold"))
    canvas_cpu.create_text(140, 105, text="Unidad de Control (UC)", fill="#ffffff" if paso in [1,2] else COLOR_TEXT, font=("Segoe UI", 8, "bold"))

    # Bus IR -> ALU
    f_col2 = COLOR_DECODE if paso >= 2 else "#cbd5e1"
    canvas_cpu.create_line(140, 130, 140, 175, fill=f_col2, width=4, arrow=tk.LAST)
    canvas_cpu.create_text(180, 150, text="2. Operandos", fill=f_col2, font=("Segoe UI", 8, "bold"))

    # ALU
    canvas_cpu.create_polygon(30, 175, 290, 175, 250, 260, 70, 260, outline="#6d28d9", width=2, fill=c_alu)
    canvas_cpu.create_text(160, 192, text="ALU (Procesamiento)", fill="#ffffff" if paso==3 else COLOR_TEXT, font=("Segoe UI", 9, "bold"))
    alu_txt = f"{d1} {op} {d2}" if paso >= 3 else "Esperando..."
    canvas_cpu.create_text(160, 228, text=alu_txt, fill="#ffffff" if paso==3 else COLOR_TEXT, font=("Consolas", 10, "bold"))

    # Bus ALU -> AC
    f_col3 = COLOR_EXECUTE if paso >= 3 else "#cbd5e1"
    canvas_cpu.create_line(160, 260, 160, 300, fill=f_col3, width=4, arrow=tk.LAST)
    canvas_cpu.create_text(200, 280, text="3. Resultado", fill=f_col3, font=("Segoe UI", 8, "bold"))

    # AC
    canvas_cpu.create_rectangle(90, 300, 230, 370, outline="#047857", width=2, fill=c_ac)
    canvas_cpu.create_text(160, 320, text="AC (Acumulador)", fill="#ffffff" if paso>=4 else COLOR_TEXT, font=("Segoe UI", 9, "bold"))
    ac_val = str(res) if paso >= 4 else "Vacío"
    canvas_cpu.create_text(160, 348, text=ac_val, fill="#ffffff" if paso>=4 else COLOR_TEXT, font=("Consolas", 11, "bold"))

    # Cuadro Informativo Inferior en Vivo
    explicaciones = [
        ("ESTADO INICIAL:", "Configura números A y B, selecciona una operación y presiona 'Inicializar'."),
        ("1. FETCH (BÚSQUEDA - NARANJA):", f"El Contador (PC) apunta a la RAM 0x42. La RAM envía la orden '{op}' y operandos ({d1}, {d2}) al IR."),
        ("2. DECODE (DECODIFICACIÓN - AZUL):", f"La Unidad de Control (UC) interpreta la orden '{op}' y acondiciona los buses de datos."),
        ("3. EXECUTE (EJECUCIÓN - PÚRPURA):", f"La ALU recibe los operandos y efectúa el cálculo exacto de {d1} {op} {d2}."),
        ("4. STORE (ALMACENAMIENTO - VERDE):", f"El resultado final de la operación ({res}) queda registrado en el Acumulador (AC).")
    ]
    tit, desc = explicaciones[paso]
    canvas_cpu.create_rectangle(15, 385, 630, 440, outline=color_activo, width=2, fill="#ffffff")
    canvas_cpu.create_text(25, 402, text=tit, anchor="w", fill=color_activo, font=("Segoe UI", 9, "bold"))
    canvas_cpu.create_text(25, 422, text=desc, anchor="w", fill=COLOR_TEXT, font=("Segoe UI", 9))

# --- CONSTRUCCIÓN DE LA APLICACIÓN PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Suite Educativa Interactiva: Sistemas Numéricos y CPU Pro")
ventana.geometry("1060x860")
ventana.configure(bg=COLOR_BG)

op_seleccionada_dash = tk.StringVar(value="+")

aplicar_estilos_claros()
control_pestañas = ttk.Notebook(ventana)

# ==========================================
# PESTAÑA 1: CONVERSOR UNIFICADO (DEC <-> BIN)
# ==========================================
pest_conv = tk.Frame(control_pestañas, bg=COLOR_BG)
control_pestañas.add(pest_conv, text="Conversor Decimal ⇄ Binario")

f_sup_c = tk.Frame(pest_conv, bg=COLOR_CARD, padx=20, pady=15, highlightthickness=1, highlightbackground=COLOR_BORDER)
f_sup_c.pack(fill="x", padx=15, pady=15)
tk.Label(f_sup_c, text="Conversor Bidireccional (Decimal, Texto ASCII y Binario)", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))

f_sub_c = tk.Frame(f_sup_c, bg=COLOR_CARD)
f_sub_c.pack(fill="x")

combo_conv = ttk.Combobox(f_sub_c, values=["Decimal a Binario / ASCII", "Binario a Decimal"], width=24, state="readonly", font=("Segoe UI", 10))
combo_conv.pack(side="left", padx=(0, 10))
combo_conv.set("Decimal a Binario / ASCII")

entrada_conv = tk.Entry(f_sub_c, bg="#f8fafc", fg=COLOR_TEXT, font=("Segoe UI", 11), bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
entrada_conv.pack(fill="x", side="left", expand=True, ipady=5, padx=(0, 10))

tk.Button(f_sub_c, text="Procesar Conversión", command=procesar_conversor_unificado, bg=COLOR_ACCENT, fg="#ffffff", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5).pack(side="right")

f_inf_c = tk.Frame(pest_conv, bg=COLOR_BG, padx=15, pady=5)
f_inf_c.pack(fill="both", expand=True, padx=5)
tabla_conv = ttk.Treeview(f_inf_c, columns=("C1", "C2", "C3", "C4"), show="tree headings")
tabla_conv.heading("C1", text="Entrada / Paso"); tabla_conv.heading("C2", text="Valor Principal"); tabla_conv.heading("C3", text="Detalle / Operación"); tabla_conv.heading("C4", text="Resultado Final")
tabla_conv.column("#0", width=25, stretch=tk.NO); tabla_conv.column("C1", width=200); tabla_conv.column("C2", width=130, anchor="center"); tabla_conv.column("C3", width=180, anchor="center"); tabla_conv.column("C4", width=150, anchor="center")
sc_c = ttk.Scrollbar(f_inf_c, orient="vertical", command=tabla_conv.yview); tabla_conv.configure(yscrollcommand=sc_c.set)
tabla_conv.pack(side="left", fill="both", expand=True); sc_c.pack(side="right", fill="y")

# ==========================================
# PESTAÑA 2: CALCULADORA BINARIA Y LÓGICA
# ==========================================
pest_calc = tk.Frame(control_pestañas, bg=COLOR_BG)
control_pestañas.add(pest_calc, text="Calculadora Binaria y Lógica")

f_sup_calc = tk.Frame(pest_calc, bg=COLOR_CARD, padx=20, pady=15, highlightthickness=1, highlightbackground=COLOR_BORDER)
f_sup_calc.pack(fill="x", padx=15, pady=15)

f_inputs_calc = tk.Frame(f_sup_calc, bg=COLOR_CARD)
f_inputs_calc.pack(fill="x", pady=5)

tk.Label(f_inputs_calc, text="Binario A:", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=4)
entrada_op1 = tk.Entry(f_inputs_calc, bg="#f8fafc", fg=COLOR_TEXT, font=("Segoe UI", 11), width=26, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
entrada_op1.grid(row=0, column=1, padx=10, pady=4)

tk.Label(f_inputs_calc, text="Binario B:", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=4)
entrada_op2 = tk.Entry(f_inputs_calc, bg="#f8fafc", fg=COLOR_TEXT, font=("Segoe UI", 11), width=26, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
entrada_op2.grid(row=1, column=1, padx=10, pady=4)

f_botones_calc = tk.Frame(f_sup_calc, bg=COLOR_CARD)
f_botones_calc.pack(fill="x", pady=(12, 5))

tk.Label(f_botones_calc, text="Operadores:", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 10))

for op in ["+", "-", "×", "÷", "AND", "OR", "NOT"]:
    btn_col = "#d97706" if op in ["×", "÷"] else ("#7c3aed" if op in ["AND", "OR", "NOT"] else COLOR_ACCENT)
    tk.Button(f_botones_calc, text=op, command=lambda o=op: calcular_binario_completo(o), bg=btn_col, fg="#ffffff", font=("Segoe UI", 10, "bold"), width=6, bd=0, pady=4).pack(side="left", padx=4)

f_inf_calc = tk.Frame(pest_calc, bg=COLOR_CARD, padx=20, pady=15, highlightthickness=1, highlightbackground=COLOR_BORDER)
f_inf_calc.pack(fill="both", expand=True, padx=15, pady=(0, 15))

lbl_res_bin = tk.Label(f_inf_calc, text="Resultado Binario: -", fg="#059669", bg=COLOR_CARD, font=("Segoe UI", 12, "bold"))
lbl_res_bin.pack(anchor="w", pady=2)
lbl_res_dec = tk.Label(f_inf_calc, text="Resultado Decimal: -", fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, font=("Segoe UI", 11))
lbl_res_dec.pack(anchor="w", pady=(0, 10))

txt_proceso = tk.Text(f_inf_calc, bg="#f8fafc", fg=COLOR_TEXT, font=("Consolas", 10), bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER, padx=10, pady=10)
txt_proceso.pack(fill="both", expand=True)

# ==========================================
# PESTAÑA 3: DASHBOARD VON NEUMANN CON FASES Y COLORES COORDINADOS
# ==========================================
pest_lat = tk.Frame(control_pestañas, bg=COLOR_BG)
control_pestañas.add(pest_lat, text="Dashboard CPU con Gráfico Lateral")

f_head_lat = tk.Frame(pest_lat, bg=COLOR_BG, padx=10, pady=5)
f_head_lat.pack(fill="x", padx=10, pady=5)
tk.Label(f_head_lat, text="⚡ SIMULADOR VON NEUMANN CON FASES Y COLORES COORDINADOS", fg=COLOR_ACCENT, bg=COLOR_BG, font=("Segoe UI", 11, "bold")).pack(anchor="w")

# Controles Superiores
f_top_lat = tk.Frame(pest_lat, bg=COLOR_CARD, padx=15, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
f_top_lat.pack(fill="x", padx=15, pady=5)

f_sub_top = tk.Frame(f_top_lat, bg=COLOR_CARD)
f_sub_top.pack(fill="x")

tk.Label(f_sub_top, text="A:", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=2)
entrada_a_dash = tk.Entry(f_sub_top, bg="#f8fafc", fg=COLOR_TEXT, font=("Segoe UI", 10), width=6, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
entrada_a_dash.grid(row=0, column=1, padx=4, pady=2)
entrada_a_dash.insert(0, "6")

tk.Label(f_sub_top, text="B:", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w", padx=4)
entrada_b_dash = tk.Entry(f_sub_top, bg="#f8fafc", fg=COLOR_TEXT, font=("Segoe UI", 10), width=6, bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
entrada_b_dash.grid(row=0, column=3, padx=4, pady=2)
entrada_b_dash.insert(0, "4")

tk.Label(f_sub_top, text="Op:", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w", padx=6)
f_ops_lat = tk.Frame(f_sub_top, bg=COLOR_CARD)
f_ops_lat.grid(row=0, column=5, padx=4)

botones_dash = {}
for op in ["+", "-", "×", "÷", "AND", "OR", "NOT"]:
    btn = tk.Button(f_ops_lat, text=op, command=lambda o=op: seleccionar_op_dash(o), bg=COLOR_ACCENT if op=="+" else "#e2e8f0", fg="#ffffff" if op=="+" else COLOR_TEXT, font=("Segoe UI", 8, "bold"), width=3, bd=0, pady=2)
    btn.pack(side="left", padx=1)
    botones_dash[op] = btn

tk.Button(f_sub_top, text="▶ Inicializar", command=inicializar_dashboard_lat, bg=COLOR_SUCCESS, fg="#ffffff", font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=3).grid(row=0, column=6, padx=8)

# Botones de Fase con Colores Identificables
f_fases_lat = tk.Frame(f_top_lat, bg=COLOR_CARD)
f_fases_lat.pack(fill="x", pady=(6, 0))

btn_p1 = tk.Button(f_fases_lat, text="1. FETCH", command=lambda: ejecutar_paso_lat(1), state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff", font=("Segoe UI", 8, "bold"), width=12, bd=0, pady=3)
btn_p1.pack(side="left", padx=3)
btn_p2 = tk.Button(f_fases_lat, text="2. DECODE", command=lambda: ejecutar_paso_lat(2), state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff", font=("Segoe UI", 8, "bold"), width=12, bd=0, pady=3)
btn_p2.pack(side="left", padx=3)
btn_p3 = tk.Button(f_fases_lat, text="3. EXECUTE", command=lambda: ejecutar_paso_lat(3), state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff", font=("Segoe UI", 8, "bold"), width=12, bd=0, pady=3)
btn_p3.pack(side="left", padx=3)
btn_p4 = tk.Button(f_fases_lat, text="4. STORE", command=lambda: ejecutar_paso_lat(4), state=tk.DISABLED, bg="#cbd5e1", fg="#ffffff", font=("Segoe UI", 8, "bold"), width=12, bd=0, pady=3)
btn_p4.pack(side="left", padx=3)

# Contenedores Gráficos Izquierda (Procesos) y Derecha (CPU)
f_vis_lat = tk.Frame(pest_lat, bg=COLOR_BG)
f_vis_lat.pack(fill="both", expand=True, padx=15, pady=5)

# Panel Gráfico Izquierdo
f_lat_left = tk.Frame(f_vis_lat, bg=COLOR_CARD, padx=5, pady=5, highlightthickness=1, highlightbackground=COLOR_BORDER)
f_lat_left.pack(side="left", fill="y", padx=(0, 8))
tk.Label(f_lat_left, text="Progreso de Procesos", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="n", pady=2)
canvas_lat = tk.Canvas(f_lat_left, bg="#ffffff", width=230, height=450, highlightthickness=0)
canvas_lat.pack()

# Panel Gráfico Derecho (CPU)
f_lat_right = tk.Frame(f_vis_lat, bg=COLOR_CARD, padx=5, pady=5, highlightthickness=1, highlightbackground=COLOR_BORDER)
f_lat_right.pack(side="right", fill="both", expand=True)
tk.Label(f_lat_right, text="Diagrama de Componentes de la CPU", fg=COLOR_TEXT, bg=COLOR_CARD, font=("Segoe UI", 9, "bold")).pack(anchor="n", pady=2)
canvas_cpu = tk.Canvas(f_lat_right, bg="#ffffff", height=450, highlightthickness=0)
canvas_cpu.pack(fill="both", expand=True)

# Estado inicial
actualizar_todo_von_neumann(0)

control_pestañas.pack(expand=1, fill="both")
ventana.mainloop()
