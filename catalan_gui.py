# -*- coding: utf-8 -*-
"""
Números de Catalan: Problema de la Mesa Redonda
GUI Interactivo con Tkinter
"""

import math
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Punto:
    """Representa una persona en la mesa redonda"""
    id: int
    x: float
    y: float


class NumerosCatalan:
    """Clase para calcular números de Catalan"""
    
    @staticmethod
    def calcular_formula_directa(n: int) -> int:
        """Calcula C(n) = (2n)! / ((n+1)! * n!)"""
        return math.comb(2*n, n) // (n + 1)
    
    @staticmethod
    def generar_secuencia(n: int) -> List[int]:
        """Genera los primeros n números de Catalan"""
        return [NumerosCatalan.calcular_formula_directa(i) for i in range(n)]


class MesaRedonda:
    """Genera y maneja mesas redondas con saludos sin cruces"""
    
    def __init__(self, n_personas: int):
        self.n = n_personas
        self.puntos = self._generar_puntos()
    
    def _generar_puntos(self) -> List[Punto]:
        """Genera los puntos distribuidos en círculo"""
        puntos = []
        for i in range(self.n):
            angulo = 2 * math.pi * i / self.n
            x = math.cos(angulo)
            y = math.sin(angulo)
            puntos.append(Punto(id=i, x=x, y=y))
        return puntos
    
    @staticmethod
    def se_cruzan(conexion1: Tuple[int, int], conexion2: Tuple[int, int], 
                  n: int) -> bool:
        """Verifica si dos saludos se cruzan en un círculo"""
        a, b = conexion1
        c, d = conexion2
        
        if a == b or c == d:
            return False
        
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        
        if a == c or a == d or b == c or b == d:
            return False
        
        return (a < c < b < d) or (c < a < d < b)
    
    @staticmethod
    def generar_colores_vibrantes(cantidad: int):
        """Genera colores vibrantes y saturados para los saludos
        
        Retorna una lista de colores RGB en formato (R, G, B) donde cada valor está entre 0 y 1
        """
        # Paleta de colores vibrantes y saturados
        colores_hex = [
            '#FF0000',  # Rojo vivo
            '#0066FF',  # Azul vivo
            '#00BB00',  # Verde vivo
            '#FFDD00',  # Amarillo vivo
            '#FF6600',  # Naranja vivo
            '#BB00FF',  # Púrpura vivo
            '#00DDFF',  # Cian vivo
            '#FF0088',  # Magenta vivo
            '#66FF00',  # Lima vivo
            '#FF4400',  # Naranja-Rojo vivo
            '#0088FF',  # Azul cielo vivo
            '#FF0044',  # Rosa vivo
        ]
        
        # Si necesitamos más colores que los disponibles, repetir con variaciones
        colores_rgb = []
        for i in range(cantidad):
            hex_color = colores_hex[i % len(colores_hex)]
            # Convertir hex a RGB (0-1)
            rgb = tuple(int(hex_color[j:j+2], 16) / 255.0 for j in (1, 3, 5))
            colores_rgb.append(rgb)
        
        return colores_rgb
    
    def generar_todas_configuraciones(self) -> List[List[Tuple[int, int]]]:
        """Genera todas las configuraciones posibles de saludos sin cruces"""
        if self.n % 2 != 0:
            return []
        
        configuraciones = []
        self._backtrack(list(range(self.n)), [], configuraciones)
        return configuraciones
    
    def _backtrack(self, disponibles: List[int], 
                   saludos_actuales: List[Tuple[int, int]], 
                   configuraciones: List):
        """Búsqueda recursiva para encontrar todas las configuraciones"""
        if not disponibles:
            configuraciones.append(saludos_actuales.copy())
            return
        
        primer = disponibles[0]
        resto = disponibles[1:]
        
        for i, segundo in enumerate(resto):
            nuevo_saludo = (min(primer, segundo), max(primer, segundo))
            
            valida = True
            for saludo_existente in saludos_actuales:
                if self.se_cruzan(nuevo_saludo, saludo_existente, self.n):
                    valida = False
                    break
            
            if valida:
                nuevo_disponible = resto[:i] + resto[i+1:]
                saludos_actuales.append(nuevo_saludo)
                self._backtrack(nuevo_disponible, saludos_actuales, configuraciones)
                saludos_actuales.pop()
    
    def crear_figura_pagina(self, saludos_lista: List[List[Tuple[int, int]]], num_pagina: int, total_paginas: int):
        """Crea figura de matplotlib para una página de configuraciones
        
        Cada página muestra máximo 4 configuraciones en 2 columnas x 2 filas
        """
        # Tamaño fijo para cada página
        fig = Figure(figsize=(10, 6), dpi=100)
        
        cols = 2
        filas = 2
        
        for config_idx, saludos in enumerate(saludos_lista):
            ax = fig.add_subplot(filas, cols, config_idx+1)
            
            circulo = plt.Circle((0, 0), 1, fill=False, color='navy', linewidth=3, linestyle='--')
            ax.add_patch(circulo)
            
            xs = [p.x for p in self.puntos]
            ys = [p.y for p in self.puntos]
            # Ajustar tamaño de puntos según cantidad de personas - disminuye gradualmente
            tam_punto = max(180, 400 - (self.n - 4) * 12)
            tam_texto = max(6.5, 12 - (self.n - 4) * 0.25)  # Más grande para mejor legibilidad
            ancho_linea = max(0.8, 2.5 - (self.n - 4) * 0.12)
            
            ax.scatter(xs, ys, s=tam_punto, c='#FF6B6B', zorder=5, edgecolors='darkred', linewidth=2)
            
            for p in self.puntos:
                ax.text(p.x, p.y, str(p.id), 
                       ha='center', va='center', fontsize=tam_texto, fontweight='bold', color='white')
            
            colors = self.generar_colores_vibrantes(len(saludos))
            for saludo_idx, (a, b) in enumerate(saludos):
                pa = self.puntos[a]
                pb = self.puntos[b]
                ax.plot([pa.x, pb.x], [pa.y, pb.y], 
                       color=colors[saludo_idx], linewidth=ancho_linea, alpha=0.9)
            
            ax.set_xlim(-1.6, 1.6)
            ax.set_ylim(-1.6, 1.6)
            ax.set_aspect('equal')
            ax.axis('off')
            
            title = f'Configuración {config_idx+1}\n'
            title += f'Saludos: {", ".join([f"{a}↔{b}" for a, b in saludos])}'
            fontsize_title = 8 if self.n <= 12 else 7
            ax.set_title(title, fontsize=fontsize_title, fontweight='bold', pad=5)
        
        # Título de la página
        fig.suptitle(f'{self.n} Personas - Página {num_pagina}/{total_paginas}',
                     fontsize=12, fontweight='bold', y=0.98)
        
        fig.tight_layout(rect=[0, 0, 1, 0.97])
        return fig


class AplicacionCatalan:
    """Aplicación GUI para números de Catalan"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Números de Catalan - Mesa Redonda")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")
        
        # Título
        titulo = tk.Label(root, text="NÚMEROS DE CATALAN", 
                         font=("Arial", 20, "bold"), 
                         fg="#ecf0f1", bg="#2c3e50")
        titulo.pack(pady=20)
        
        subtitulo = tk.Label(root, text="Problema de la Mesa Redonda", 
                            font=("Arial", 14), 
                            fg="#bdc3c7", bg="#2c3e50")
        subtitulo.pack(pady=5)
        
        # Frame de botones
        frame_botones = tk.Frame(root, bg="#2c3e50")
        frame_botones.pack(pady=30, expand=True)
        
        # Botón 1
        btn1 = tk.Button(frame_botones, text="📊 Ver Secuencia de Catalan",
                        command=self.ver_secuencia,
                        font=("Arial", 12), width=35, height=2,
                        bg="#3498db", fg="white", activebackground="#2980b9")
        btn1.pack(pady=10)
        
        # Botón 2
        btn2 = tk.Button(frame_botones, text="🔵 Mesa Redonda (Ingresar Personas)",
                        command=self.mesa_redonda,
                        font=("Arial", 12), width=35, height=2,
                        bg="#e74c3c", fg="white", activebackground="#c0392b")
        btn2.pack(pady=10)
        
        # Botón 3
        btn3 = tk.Button(frame_botones, text="ℹ️  Explicación",
                        command=self.mostrar_explicacion,
                        font=("Arial", 12), width=35, height=2,
                        bg="#27ae60", fg="white", activebackground="#229954")
        btn3.pack(pady=10)
        
        # Botón 4
        btn4 = tk.Button(frame_botones, text="❌ Salir",
                        command=root.quit,
                        font=("Arial", 12), width=35, height=2,
                        bg="#95a5a6", fg="white", activebackground="#7f8c8d")
        btn4.pack(pady=10)
    
    def ver_secuencia(self):
        """Muestra la secuencia de números de Catalan"""
        dialog_n = simpledialog.askinteger("Secuencia de Catalan", 
                                           "¿Cuántos números deseas ver? (1-20):",
                                           minvalue=1, maxvalue=20)
        
        if dialog_n is None:
            return
        
        catalan = NumerosCatalan()
        secuencia = catalan.generar_secuencia(dialog_n)
        
        # Crear ventana de resultados
        ventana = tk.Toplevel(self.root)
        ventana.title("Números de Catalan")
        ventana.geometry("600x500")
        ventana.configure(bg="#ecf0f1")
        
        # Título
        titulo = tk.Label(ventana, text="NÚMEROS DE CATALAN", 
                         font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        titulo.pack(pady=10)
        
        # Texto con scroll
        frame_texto = tk.Frame(ventana, bg="#ecf0f1")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        texto = scrolledtext.ScrolledText(frame_texto, font=("Courier", 11), 
                                         height=20, width=60, bg="white", fg="#2c3e50")
        texto.pack(fill=tk.BOTH, expand=True)
        
        # Contenido
        contenido = f"Primeros {dialog_n} números de Catalan:\n"
        contenido += "-" * 60 + "\n"
        contenido += f"{'n':>3} | {'C(n)':>15} | {'Significado'}\n"
        contenido += "-" * 60 + "\n"
        
        for i, c in enumerate(secuencia):
            if i == 0:
                sig = "Valor base"
            elif i == 1:
                sig = "1 o 2 personas"
            else:
                sig = f"Saludos sin cruces ({2*i} personas)"
            contenido += f"{i:3d} | {c:15,d} | {sig}\n"
        
        contenido += "-" * 60 + "\n\n"
        contenido += "Fórmula: C(n) = (2n)! / ((n+1)! × n!)\n"
        
        texto.insert(1.0, contenido)
        texto.config(state=tk.DISABLED)
    
    def mesa_redonda(self):
        """Resuelve el problema de la mesa redonda con paginación"""
        dialog_n = simpledialog.askinteger("Mesa Redonda", 
                                           "¿Cuántas personas? (2-24, número PAR):",
                                           minvalue=2, maxvalue=24)
        
        if dialog_n is None:
            return
        
        if dialog_n % 2 != 0:
            messagebox.showerror("Error", "¡El número debe ser PAR!")
            return
        
        # Calcular
        k = dialog_n // 2
        catalan = NumerosCatalan()
        num_catalan = catalan.calcular_formula_directa(k)
        
        mesa = MesaRedonda(dialog_n)
        configuraciones = mesa.generar_todas_configuraciones()
        
        # Crear ventana de resultados
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Mesa Redonda - {dialog_n} Personas")
        ventana.geometry("1200x850")
        ventana.configure(bg="#ecf0f1")
        
        # Título
        titulo = tk.Label(ventana, text=f"MESA REDONDA CON {dialog_n} PERSONAS", 
                         font=("Arial", 13, "bold"), fg="#2c3e50", bg="#ecf0f1")
        titulo.pack(pady=10)
        
        # Frame superior: información
        frame_info = tk.Frame(ventana, bg="#ecf0f1")
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        
        info_text = f"Personas: {dialog_n}  |  Saludos/persona: {k}  |  Formas: C({k}) = {num_catalan:,}  |  Configuraciones: {len(configuraciones)}"
        label_info = tk.Label(frame_info, text=info_text, font=("Arial", 10), 
                             fg="#2c3e50", bg="#ecf0f1")
        label_info.pack()
        
        # Panel divisor movible (PanedWindow) para redimensionar columnas
        paned_window = tk.PanedWindow(ventana, orient=tk.HORIZONTAL, bg="#ecf0f1", sashwidth=8)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Columna izquierda: Texto con scroll
        frame_texto = tk.Frame(paned_window, bg="#ecf0f1")
        paned_window.add(frame_texto, width=300, sticky="nsew")
        
        texto = scrolledtext.ScrolledText(frame_texto, font=("Courier", 9), 
                                         height=30, width=40, bg="white", fg="#2c3e50")
        texto.pack(fill=tk.BOTH, expand=True)
        
        # Contenido texto
        contenido = f"DETALLE DE CONFIGURACIONES:\n"
        contenido += "="*38 + "\n\n"
        
        for idx, saludos in enumerate(configuraciones):
            pares = ", ".join([f"{a}↔{b}" for a, b in saludos])
            contenido += f"{idx+1}. {pares}\n"
        
        if len(configuraciones) == num_catalan:
            contenido += "\n✅ ¡Correcto!\n"
        
        texto.insert(1.0, contenido)
        texto.config(state=tk.DISABLED)
        
        # Columna derecha: Gráficas con pestañas (páginas)
        frame_grafs = tk.Frame(paned_window, bg="white", relief=tk.SUNKEN, bd=1)
        paned_window.add(frame_grafs, sticky="nsew")
        
        # Dividir configuraciones en páginas (máximo 4 por página)
        configs_por_pagina = 4
        num_paginas = (len(configuraciones) + configs_por_pagina - 1) // configs_por_pagina
        
        # Frame para botones de navegación
        frame_nav = tk.Frame(frame_grafs, bg="#ecf0f1", height=40)
        frame_nav.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Label con información de página
        label_pag = tk.Label(frame_nav, text="", font=("Arial", 9), fg="#2c3e50", bg="#ecf0f1")
        label_pag.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Botón Anterior
        btn_anterior = tk.Button(frame_nav, text="◀ Anterior", 
                                 font=("Arial", 10), bg="#3498db", fg="white",
                                 activebackground="#2980b9", width=12)
        btn_anterior.pack(side=tk.LEFT, padx=2)
        
        # Botón Siguiente
        btn_siguiente = tk.Button(frame_nav, text="Siguiente ▶", 
                                  font=("Arial", 10), bg="#3498db", fg="white",
                                  activebackground="#2980b9", width=12)
        btn_siguiente.pack(side=tk.LEFT, padx=2)
        
        # Crear notebook (pestañas)
        notebook = ttk.Notebook(frame_grafs)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Lista para guardar referencias a las pestañas
        tabs = []
        
        # Crear una pestaña por cada página
        for num_pag in range(1, num_paginas + 1):
            # Calcular índices de inicio y fin para esta página
            inicio = (num_pag - 1) * configs_por_pagina
            fin = min(inicio + configs_por_pagina, len(configuraciones))
            
            # Configuraciones de esta página
            configs_pagina = configuraciones[inicio:fin]
            
            # Crear frame para la pestaña con scroll
            frame_tab = tk.Frame(notebook, bg="white")
            notebook.add(frame_tab, text=f"Página {num_pag}")
            tabs.append(frame_tab)
            
            # Frame con scroll para las gráficas y botones
            main_frame = tk.Frame(frame_tab, bg="white")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Canvas con scrollbar
            canvas_scroll = tk.Canvas(main_frame, bg="white", highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas_scroll.yview)
            scroll_frame = tk.Frame(canvas_scroll, bg="white")
            
            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
            )
            
            canvas_scroll.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas_scroll.configure(yscrollcommand=scrollbar.set)
            
            canvas_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Generar figura para esta página
            saludos_con_indice = [(i + inicio + 1, saludos) for i, saludos in enumerate(configs_pagina)]
            
            # Crear la figura y luego agregar botones
            fig = self._crear_figura_pagina_indexada(mesa, saludos_con_indice, num_pag, num_paginas)
            
            # Frame para la figura
            fig_frame = tk.Frame(scroll_frame, bg="white")
            fig_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            
            # Frame para toolbar
            toolbar_frame = tk.Frame(fig_frame, bg="white")
            toolbar_frame.pack(side=tk.TOP, fill=tk.X)
            
            canvas = FigureCanvasTkAgg(fig, master=fig_frame)
            canvas.draw()
            
            # Agregar toolbar de zoom, pan, reset, etc.
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Frame para botones debajo de la figura
            botones_frame = tk.Frame(scroll_frame, bg="white")
            botones_frame.pack(pady=5)
            
            # Crear botones para cada mesa
            for i, (num_config, saludos) in enumerate(saludos_con_indice):
                btn = tk.Button(
                    botones_frame,
                    text=f"👁️ Ver completo (Conf. {num_config})",
                    font=("Arial", 9),
                    bg="#3498db",
                    fg="white",
                    activebackground="#2980b9",
                    command=lambda nc=num_config, s=saludos: self.mostrar_mesa_detalle(mesa, nc, s)
                )
                btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # Función para actualizar botones de navegación
        def actualizar_botones():
            pag_actual = notebook.index(notebook.select()) + 1
            label_pag.config(text=f"Página {pag_actual} de {num_paginas}")
            
            # Desactivar botón Anterior si estamos en página 1
            if pag_actual == 1:
                btn_anterior.config(state=tk.DISABLED, bg="#95a5a6", activebackground="#7f8c8d")
            else:
                btn_anterior.config(state=tk.NORMAL, bg="#3498db", activebackground="#2980b9")
            
            # Desactivar botón Siguiente si estamos en última página
            if pag_actual == num_paginas:
                btn_siguiente.config(state=tk.DISABLED, bg="#95a5a6", activebackground="#7f8c8d")
            else:
                btn_siguiente.config(state=tk.NORMAL, bg="#3498db", activebackground="#2980b9")
        
        # Funciones para los botones
        def ir_anterior():
            pag_actual = notebook.index(notebook.select())
            if pag_actual > 0:
                notebook.select(pag_actual - 1)
                actualizar_botones()
        
        def ir_siguiente():
            pag_actual = notebook.index(notebook.select())
            if pag_actual < num_paginas - 1:
                notebook.select(pag_actual + 1)
                actualizar_botones()
        
        # Asignar comandos a los botones
        btn_anterior.config(command=ir_anterior)
        btn_siguiente.config(command=ir_siguiente)
        
        # Evento cuando cambia la pestaña
        notebook.bind("<<NotebookTabChanged>>", lambda e: actualizar_botones())
        
        # Actualizar botones inicialmente
        actualizar_botones()
    
    def mostrar_mesa_detalle(self, mesa, num_config: int, saludos: List[Tuple[int, int]]):
        """Muestra una configuración en una ventana grande ocupando toda la pantalla"""
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title(f"Configuración {num_config} - {mesa.n} Personas")
        ventana_detalle.geometry("900x850")
        ventana_detalle.configure(bg="#ecf0f1")
        
        # Frame superior con información y botón
        frame_sup = tk.Frame(ventana_detalle, bg="#ecf0f1", height=50)
        frame_sup.pack(fill=tk.X, padx=10, pady=10)
        
        titulo = tk.Label(frame_sup, 
                         text=f"Configuración {num_config} - {mesa.n} Personas",
                         font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        titulo.pack(side=tk.LEFT, expand=True)
        
        btn_volver = tk.Button(frame_sup, text="🔙 Volver",
                              font=("Arial", 11, "bold"), bg="#e74c3c", fg="white",
                              activebackground="#c0392b",
                              command=ventana_detalle.destroy)
        btn_volver.pack(side=tk.RIGHT)
        
        # Frame para la gráfica
        frame_graf = tk.Frame(ventana_detalle, bg="white", relief=tk.SUNKEN, bd=1)
        frame_graf.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear figura grande para una sola configuración
        fig = Figure(figsize=(8, 7), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        
        # Dibujar la mesa
        circulo = plt.Circle((0, 0), 1, fill=False, color='navy', linewidth=4, linestyle='--')
        ax.add_patch(circulo)
        
        xs = [p.x for p in mesa.puntos]
        ys = [p.y for p in mesa.puntos]
        
        # Tamaños grandes para vista detalle
        tam_punto = 600
        tam_texto = 18  # Más grande para vista completa
        ancho_linea = 3.5
        
        ax.scatter(xs, ys, s=tam_punto, c='#FF6B6B', zorder=5, edgecolors='darkred', linewidth=3)
        
        for p in mesa.puntos:
            ax.text(p.x, p.y, str(p.id), 
                   ha='center', va='center', fontsize=tam_texto, fontweight='bold', color='white', zorder=7)
        
        colors = mesa.generar_colores_vibrantes(len(saludos))
        for saludo_idx, (a, b) in enumerate(saludos):
            pa = mesa.puntos[a]
            pb = mesa.puntos[b]
            ax.plot([pa.x, pb.x], [pa.y, pb.y], 
                   color=colors[saludo_idx], linewidth=ancho_linea, alpha=0.9, zorder=3)
        
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.8, 1.8)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Título con detalles
        title_text = f'Configuración {num_config}\n'
        title_text += f'Saludos: {", ".join([f"{a}↔{b}" for a, b in saludos])}'
        fig.suptitle(title_text, fontsize=12, fontweight='bold', y=0.98)
        
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Incrustar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_graf)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Info adicional
        frame_info = tk.Frame(ventana_detalle, bg="#ecf0f1")
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        
        info_text = f"Personas: {mesa.n}  |  Número de saludos: {len(saludos)}"
        label_info = tk.Label(frame_info, text=info_text, font=("Arial", 9, "italic"), 
                             fg="#34495e", bg="#ecf0f1")
        label_info.pack()
    
    def _crear_figura_pagina_indexada(self, mesa, saludos_con_indice: List[Tuple[int, List[Tuple[int, int]]]], num_pag: int, total_pags: int):
        """Crea figura para una página con índices de configuración correctos"""
        fig = Figure(figsize=(10, 6), dpi=100)
        
        cols = 2
        filas = 2
        
        for subcfg_idx, (num_config, saludos) in enumerate(saludos_con_indice):
            ax = fig.add_subplot(filas, cols, subcfg_idx+1)
            
            circulo = plt.Circle((0, 0), 1, fill=False, color='navy', linewidth=3, linestyle='--')
            ax.add_patch(circulo)
            
            xs = [p.x for p in mesa.puntos]
            ys = [p.y for p in mesa.puntos]
            # Ajustar tamaño de puntos según cantidad de personas - disminuye gradualmente
            tam_punto = max(180, 400 - (mesa.n - 4) * 12)
            tam_texto = max(6.5, 12 - (mesa.n - 4) * 0.25)  # Más grande para mejor legibilidad
            ancho_linea = max(0.8, 2.5 - (mesa.n - 4) * 0.12)
            
            ax.scatter(xs, ys, s=tam_punto, c='#FF6B6B', zorder=5, edgecolors='darkred', linewidth=3)
            
            # Dibujar números más grandes y visibles en las personas
            for p in mesa.puntos:
                # Crear texto con contorno para mejor contraste
                ax.text(p.x, p.y, str(p.id), 
                       ha='center', va='center', fontsize=tam_texto, fontweight='bold', 
                       color='white', zorder=6)
            
            colors = mesa.generar_colores_vibrantes(len(saludos))
            for saludo_idx, (a, b) in enumerate(saludos):
                pa = mesa.puntos[a]
                pb = mesa.puntos[b]
                ax.plot([pa.x, pb.x], [pa.y, pb.y], 
                       color=colors[saludo_idx], linewidth=ancho_linea, alpha=0.9)
            
            ax.set_xlim(-1.6, 1.6)
            ax.set_ylim(-1.6, 1.6)
            ax.set_aspect('equal')
            ax.axis('off')
            
            title = f'Configuración {num_config}\n'
            title += f'Saludos: {", ".join([f"{a}↔{b}" for a, b in saludos])}'
            fontsize_title = 8 if mesa.n <= 12 else 7
            ax.set_title(title, fontsize=fontsize_title, fontweight='bold', pad=5)
        
        # Título de la página
        fig.suptitle(f'{mesa.n} Personas - Página {num_pag}/{total_pags}',
                     fontsize=12, fontweight='bold', y=0.98)
        
        fig.tight_layout(rect=[0, 0, 1, 0.97])
        return fig
    
    def mostrar_explicacion(self):
        """Muestra explicación de números de Catalan"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Explicación - Números de Catalan")
        ventana.geometry("800x700")
        ventana.configure(bg="#ecf0f1")
        
        titulo = tk.Label(ventana, text="¿QUÉ SON LOS NÚMEROS DE CATALAN?", 
                         font=("Arial", 13, "bold"), fg="#2c3e50", bg="#ecf0f1")
        titulo.pack(pady=10)
        
        frame_texto = tk.Frame(ventana, bg="#ecf0f1")
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        texto = scrolledtext.ScrolledText(frame_texto, font=("Courier", 10), 
                                         height=30, width=95, bg="white", fg="#2c3e50")
        texto.pack(fill=tk.BOTH, expand=True)
        
        explicacion = """DEFINICIÓN:
Los números de Catalan (C_n) son una secuencia de números naturales
que aparecen en muchos problemas combinatorios:

   C_n = (2n)! / ((n+1)! × n!)

SECUENCIA:
C(0)=1, C(1)=1, C(2)=2, C(3)=5, C(4)=14, C(5)=42, C(6)=132...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EL PROBLEMA DE LA MESA REDONDA:

Si n personas se sientan alrededor de una mesa redonda,
¿DE CUÁNTAS FORMAS PUEDEN SALUDARSE SIN QUE LOS SALUDOS SE CRUCEN?

RESPUESTA: C(n/2) maneras

EJEMPLO CON 4 PERSONAS:
Personas: 0, 1, 2, 3

Forma 1 ✅: Personas 0-1 se saludan, personas 2-3 se saludan
Forma 2 ✅: Personas 0-3 se saludan, personas 1-2 se saludan
Forma 3 ❌: Personas 0-2 y 1-3 se saludan → ¡SE CRUZAN!

Total: 2 formas = C(2) ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APLICACIONES:
• Formas de triangular un polígono
• Expresiones con paréntesis balanceados
• Caminos sin cruzarse en una malla
• Emparejamientos en torneos
• Análisis de genomas en biología
• ¡Y muchas más!

OBSERVACIONES:
• C(n) crece EXPONENCIALMENTE
• C(10) = 16,796
• C(20) = 6,564,120,420 (¡más de 6 mil millones!)
• Aparecen frecuentemente en la naturaleza
• Tienen múltiples interpretaciones equivalentes
"""
        
        texto.insert(1.0, explicacion)
        texto.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = AplicacionCatalan(root)
    root.mainloop()


if __name__ == "__main__":
    main()
