import tkinter as tk
from tkinter import ttk, messagebox
# Asegúrate de mantener este import correcto apuntando a tu backend
from sanciones_backend import GestorSanciones, Sancion

class AplicacionSancionesProfesional(tk.Tk):
    # --- PALETA DE COLORES ACADÉMICA ---
    # Usando códigos hexadecimales para mayor precisión
    COLOR_FONDO_APP = "#F3F4F6"      # Gris muy claro, limpio
    COLOR_FONDO_PANEL = "#FFFFFF"    # Blanco puro para los paneles
    COLOR_INSTITUCIONAL = "#002D62"  # Azul Marino Profundo (Colegio Mayor)
    COLOR_ACENTO = "#B59410"         # Dorado Académico
    COLOR_TEXTO = "#1F2937"          # Gris casi negro
    COLOR_TEXTO_LIGERO = "#6B7280"   # Gris medio para descripciones
    COLOR_SANCION = "#991B1B"        # Rojo oscuro (para el botón de acción)

    def __init__(self):
        super().__init__()
        self.title("Sistema Bibliotecario Institucional - Registro de Sanciones")
        # Un tamaño un poco mayor para dar aire a los elementos
        self.geometry("720x550") 
        self.minsize(680, 500)
        self.configure(bg=self.COLOR_FONDO_APP)

        # Inicializar gestor de datos (Backend)
        self.gestor = GestorSanciones()

        # --- CONFIGURACIÓN DE ESTILOS PROFESIONALES (Ttk Styles) ---
        self.style = ttk.Style()
        self.style.theme_use("clam") # Base limpia

        # Estilo para los Paneles (Pestañas)
        self.style.configure("TNotebook", background=self.COLOR_FONDO_APP, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.COLOR_FONDO_APP, 
                             foreground=self.COLOR_TEXTO_LIGERO, padding=(15, 6),
                             font=("Segoe UI", 10))
        # Estilo cuando una pestaña está seleccionada
        self.style.map("TNotebook.Tab", background=[("selected", self.COLOR_FONDO_PANEL)],
                       foreground=[("selected", self.COLOR_INSTITUCIONAL)],
                       font=[("selected", ("Segoe UI", 10, "bold"))])

        # Estilo para los marcos internos (Panels)
        self.style.configure("TFrame", background=self.COLOR_FONDO_PANEL)

        # Estilo para etiquetas generales
        self.style.configure("TLabel", background=self.COLOR_FONDO_PANEL, 
                             foreground=self.COLOR_TEXTO, font=("Segoe UI", 10))
        
        # Estilo para etiquetas de título de sección
        self.style.configure("Subtitulo.TLabel", foreground=self.COLOR_INSTITUCIONAL, 
                             font=("Segoe UI", 13, "bold"))

        # Estilo para las entradas de texto
        self.style.configure("TEntry", fieldbackground=self.COLOR_FONDO_PANEL, 
                             padding=5)

        # Estilo para los botones (usando el color ocre para acento)
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), 
                             background=self.COLOR_ACENTO, foreground="white", padding=(10, 5))
        # Efecto al pasar el mouse por encima
        self.style.map("Accent.TButton", background=[("active", "#997D0E")]) # Un dorado más oscuro

        # Estilo para el botón de Sanción (Rojo académico)
        self.style.configure("Sancion.TButton", font=("Segoe UI", 10, "bold"), 
                             background=self.COLOR_SANCION, foreground="white", padding=(15, 5))
        self.style.map("Sancion.TButton", background=[("active", "#7F1D1D")])

        # Estilo para la Tabla (Treeview)
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                             background="#E5E7EB", foreground=self.COLOR_TEXTO)

        # --- CONSTRUCCIÓN DE LA UI ---
        self._crear_encabezado_institucional()
        
        # Wireframe principal: Panel de Pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Definición de Sub-wireframes (Pestañas)
        self.frame_registro = ttk.Frame(self.notebook, padding=(20, 20))
        self.frame_historial = ttk.Frame(self.notebook, padding=(20, 20))

        self.notebook.add(self.frame_registro, text="  📝 NUEVA SANCIÓN  ")
        self.notebook.add(self.frame_historial, text="  📜 HISTORIAL DE RETRASOS  ")

        # Construir contenido de pestañas
        self._crear_wireframe_registro()
        self._crear_wireframe_historial()
        self._crear_barra_estado()

    def _crear_encabezado_institucional(self):
        """Simula una barra superior institucional."""
        encabezado = tk.Frame(self, bg=self.COLOR_INSTITUCIONAL, height=60)
        encabezado.pack(fill=tk.X)

        # Título de la Institución
        lbl_colegio = tk.Label(encabezado, text="COLEGIO MAYOR INSTITUCIONAL", 
                               bg=self.COLOR_INSTITUCIONAL, foreground="white",
                               font=("Garamond", 18, "bold"))
        lbl_colegio.pack(side=tk.LEFT, padx=25, pady=15)

        # Título del Sistema
        lbl_sistema = tk.Label(encabezado, text="| Sistema Bibliotecario", 
                               bg=self.COLOR_INSTITUCIONAL, foreground="#CBD5E1",
                               font=("Segoe UI", 12))
        lbl_sistema.pack(side=tk.LEFT, padx=(0, 20), pady=18)

    def _crear_wireframe_registro(self):
        """Wireframe para el formulario de ingreso."""
        
        # Marco para agrupar visualmente el formulario (hace que se vea más limpio)
        frame_formulario = tk.LabelFrame(self.frame_registro, text=" Datos de Devolución Tardía ", 
                                         bg=self.COLOR_FONDO_PANEL, fg=self.COLOR_INSTITUCIONAL,
                                         font=("Segoe UI", 11, "bold"), padx=20, pady=20,
                                         relief=tk.GROOVE)
        frame_formulario.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Campos de entrada en un GRID para orden ---
        # Usuario
        ttk.Label(frame_formulario, text="👤  Identificación / Usuario:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 15))
        self.entry_usuario = ttk.Entry(frame_formulario, width=40)
        self.entry_usuario.grid(row=0, column=1, sticky="w", pady=10)

        # Libro
        ttk.Label(frame_formulario, text="📖  Código / Título del Libro:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_libro = ttk.Entry(frame_formulario, width=40)
        self.entry_libro.grid(row=1, column=1, sticky="w", pady=10)

        # Días
        ttk.Label(frame_formulario, text="🗓️  Días Calendario de Retraso:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=10)
        self.entry_dias = ttk.Entry(frame_formulario, width=15)
        self.entry_dias.grid(row=2, column=1, sticky="w", pady=10)

        # Marco para la descripción de la regla de puntos
        frame_info = tk.Frame(frame_formulario, bg="#EFF6FF", padx=15, pady=10, relief=tk.RIDGE)
        frame_info.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(20, 10))
        
        tk.Label(frame_info, text="🛈 Regla de Sanción", bg="#EFF6FF", fg=self.COLOR_INSTITUCIONAL, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(frame_info, text=f"Se descontarán automáticamente {Sancion.PUNTOS_POR_DIA} puntos por cada día de retraso.",
                 bg="#EFF6FF", fg=self.COLOR_TEXTO_LIGERO, font=("Segoe UI", 9)).pack(anchor="w")

        # Botón de acción (centrado)
        btn_guardar = ttk.Button(frame_formulario, text="🔴 REGISTRAR SANCIÓN Y MULTA", 
                                 command=self._procesar_sancion, style="Sancion.TButton")
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=(25, 10))

    def _crear_wireframe_historial(self):
        """Wireframe para la tabla de historial integrada."""
        
        lbl_titulo = ttk.Label(self.frame_historial, text="Registro Histórico de Devoluciones Tardías", 
                               style="Subtitulo.TLabel")
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        # --- Configuración de la Tabla Profesional ---
        # Panel de scroll y tabla
        frame_tabla = tk.Frame(self.frame_historial, bg=self.COLOR_FONDO_PANEL)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("fecha", "usuario", "libro", "dias", "puntos")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

        # Definir encabezados y anchos
        self.tabla.heading("fecha", text="Fecha de Registro")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.heading("libro", text="Código Libro")
        self.tabla.heading("dias", text="Días Retraso")
        self.tabla.heading("puntos", text="Puntos Multados")

        self.tabla.column("fecha", width=140, anchor="center")
        self.tabla.column("usuario", width=130)
        self.tabla.column("libro", width=160)
        self.tabla.column("dias", width=90, anchor="center")
        self.tabla.column("puntos", width=110, anchor="center")

        # Scrollbar integrado
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _crear_barra_estado(self):
        """Barra de estado inferior profesional."""
        self.frame_estado = tk.Frame(self, bg="#E5E7EB", relief=tk.SUNKEN, height=25)
        self.frame_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.lbl_estado = tk.Label(self.frame_estado, text="🔵 Sistema Operativo | Conectado al Backend.", 
                           bg="#E5E7EB", fg=self.COLOR_TEXTO_LIGERO, font=("Segoe UI", 9), anchor="w", padx=5, pady=3)
        self.lbl_estado.pack(side=tk.LEFT, fill=tk.X, padx=10)

    # --- LÓGICA DE CONTROLADOR (No necesita cambios) ---
    def _procesar_sancion(self):
        usuario = self.entry_usuario.get().strip()
        libro = self.entry_libro.get().strip()
        dias = self.entry_dias.get().strip()

        if not usuario or not libro or not dias:
            messagebox.showwarning("Atención Bibliotecario", "Todos los campos de datos son obligatorios para proceder.")
            return

        try:
            # Llamada al Backend
            sancion = self.gestor.registrar_sancion(usuario, libro, int(dias))
            
            # Actualizar Vista
            self._actualizar_tabla(sancion.a_dict())
            self._limpiar_formulario()
            
            # Actualizar Estado
            self.lbl_estado.config(text=f"🟢 Último Registro Exitoso: {usuario} (-{sancion.puntos_descontados} pts)")
            
            # Feedback al usuario
            messagebox.showinfo("Registro Exitoso", 
                               f"Sanción procesada correctamente.\n\n"
                               f"Usuario: {usuario}\n"
                               f"Multa Aplicada: {sancion.puntos_descontados} puntos.")
        
        except ValueError:
            messagebox.showerror("Error de Datos", "Los días de retraso deben ingresarse como un número entero.")

    def _actualizar_tabla(self, datos):
        # Insertar con un toque visual de multas negativas
        self.tabla.insert("", 0, values=(
            datos["fecha"], datos["usuario"], datos["libro"], datos["dias_retraso"], f"-{datos['puntos']}"
        ))

    def _limpiar_formulario(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_libro.delete(0, tk.END)
        self.entry_dias.delete(0, tk.END)
        self.entry_usuario.focus() # Volver el foco al principio

if __name__ == "__main__":
    app = AplicacionSancionesProfesional()
    app.mainloop()