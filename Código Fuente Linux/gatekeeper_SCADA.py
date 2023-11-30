import importlib
from tkinter import PhotoImage
import tkinter.messagebox
import customtkinter as ct
from customtkinter import CTk, CTkFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import mplcyberpunk
import json
import serial
import time
from scipy import stats as st
from uri_template import expand

serial_port = '/dev/ttyUSB0'
baud_rate = 9600

ct.set_appearance_mode('Dark')

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title('Gatekeeper SCADA')
        self.geometry('1720x880')
        self.ser = serial.Serial(serial_port, baud_rate)


        self.frame2 = CTkFrame(self)
        self.frame2.grid(column=2, row=0, sticky='nsew')

        self.frame1 = CTkFrame(self)
        self.frame1.grid(column=3, row=0, sticky='nsew')

        self.columnconfigure([3,3], weight=1)
        self.rowconfigure(0, weight=1)
        
        self.sidebar_frame = ct.CTkFrame(self, width=10, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)
        self.logo_label = ct.CTkLabel(self.sidebar_frame, text="Gatekeeper SCADA", font=ct.CTkFont(size=25, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.mostrargraficas, text="Mostrar gráficas", width=220)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.muestreo_de_alcohol, text="Muestrear Alcohol", width=220)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.muestreo_dioxido_de_carbono, text="Muestrear Dióxido de Carbono", width=220)
        self.sidebar_button_1.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.media, text="Obtener media", width=220)
        self.sidebar_button_1.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.mediana, text="Obtener mediana", width=220)
        self.sidebar_button_1.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.moda, text="Obtener moda", width=220)
        self.sidebar_button_1.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.probabilidad, text="Estudiar probabilidades", width=220)
        self.sidebar_button_1.grid(row=7, column=0, padx=20, pady=10)
        self.sidebar_button_1 = ct.CTkButton(self.sidebar_frame, command=self.exportar_muestreo, text="Exportar datos", width=220)
        self.sidebar_button_1.grid(row=8, column=0, padx=20, pady=10)
        self.appearance_mode_label = ct.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=15, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ct.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event, width=220)
        self.appearance_mode_optionemenu.grid(row=16, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ct.CTkLabel(self.sidebar_frame, text="Escala de Interfaz:", anchor="w")
        self.scaling_label.grid(row=17, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ct.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event, width=220)
        self.scaling_optionemenu.grid(row=18, column=0, padx=20, pady=(10, 20))

    


    def graficas(self):

            try:
                line = self.ser.readline().decode('utf-8')
                data = json.loads(line)
                carbondioxide = data.get("co2", 0)
                alcohol = data.get("alcohol", 0)
                print(data)
                self.fig1, self.ax1 = plt.subplots(dpi=60, facecolor = '#000000')
                self.ax1.set_facecolor('#000000')
                self.ax1.grid(alpha=0.2)
                self.ax1.set_xlabel("Tiempo", color = 'white', family='Cambria', size=25)
                self.ax1.set_ylabel("Porcentaje", color = 'white', family='Cambria', size=25)
                self.ax1.tick_params(color='white', labelcolor='white', length=6, width=2)
                self.ax1.spines['bottom'].set_color('white')
                self.ax1.spines['left'].set_color('white')
                bar1 = self.ax1.bar(["Alcohol (°)"], [alcohol], color=['blue'])
                mplcyberpunk.add_bar_gradient(bars=bar1)                 
                self.fig2, self.ax2 = plt.subplots(dpi=60, facecolor = '#000000')
                self.ax2.set_facecolor('#000000')
                self.ax2.grid(alpha=0.2)
                self.ax2.set_xlabel("Tiempo", color = 'white', family='Cambria', size=25)
                self.ax2.set_ylabel("Cantidad", color = 'white', family='Cambria', size=25)
                self.ax2.tick_params(color='white', labelcolor='white', length=6, width=2)
                self.ax2.spines['bottom'].set_color('white')
                self.ax2.spines['left'].set_color('white')
                bar2 = self.ax2.bar(["Dioxido de Carbono (ppm)"], [carbondioxide], color=['green'])
                mplcyberpunk.add_bar_gradient(bars=bar2)
                
                FigureCanvasTkAgg(self.fig1, master=self.frame1).get_tk_widget().pack(expand=True, fill='both')
                FigureCanvasTkAgg(self.fig2, master=self.frame2).get_tk_widget().pack(expand=True, fill='both')
                
            except json.JSONDecodeError:
                print("Error decoding JSON data")
                self.after(1000, self.graficas)
            except UnicodeDecodeError:
                print("Error decoding serial data")
                self.after(1000, self.graficas)
    
    def realtime_data(self):
        self.textbox = ct.CTkTextbox(self, width=450, height= 1080)
        self.textbox.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
    

    def mostrargraficas(self):
        self.graficas()


    def muestreo_de_alcohol(self):
        self.realtime_data()
        self.textbox.insert(0.0, "Muestreo de Alcohol\n")
        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            alcohol = data.get("alcohol", 0)
            self.textbox.insert("end", f"{alcohol}\n")


    def muestreo_dioxido_de_carbono(self):
        self.realtime_data()
        self.textbox.insert(0.0, "Muestreo de Dióxido de Carbono\n")
        for i in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            carbondioxide = data.get("co2", 0)
            self.textbox.insert("end", f"{carbondioxide}\n")


    def media(self):
        alcoholaverage=[]
        carbondioxideaverage=[]
        self.realtime_data()

        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            alcohol = data.get("alcohol", 0)
            alcoholaverage.append(alcohol)

        self.textbox.insert(0.0, np.mean(alcoholaverage))

        self.textbox.insert(0.0, "\n\nMedia de porcentaje de alcohol\nen un espacio de 120 muestras:\n\n")


        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            carbondioxide = data.get("co2", 0)
            carbondioxideaverage.append(carbondioxide)

        self.textbox.insert(0.0, np.mean(carbondioxideaverage))

        self.textbox.insert(0.0, "\nMedia de partes por millón de dióxido de carbono\nen un espacio de 120 muestras:\n\n")

    def mediana(self):
        alcoholmedian=[]
        carbondioxidemeian=[]
        self.realtime_data()

        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            alcohol = data.get("alcohol", 0)
            alcoholmedian.append(alcohol)

        self.textbox.insert(0.0, np.median(alcoholmedian))

        self.textbox.insert(0.0, "\n\nMediana de porcentaje de alcohol\nen un espacio de 120 muestras:\n\n")

        time.sleep(0.5)

        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            carbondioxide = data.get("co2", 0)
            carbondioxidemeian.append(carbondioxide)
            x=x+1

        self.textbox.insert(0.0, np.median(carbondioxidemeian))

        self.textbox.insert(0.0, "\nMediana de partes por millón de dióxido de carbono\nen un espacio de 120 muestras:\n\n")

    def moda(self):
        alcoholmode=[]
        carbondioxidemode=[]
        self.realtime_data()
        time.sleep(0.10)

        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            alcohol = data.get("alcohol", 0)
            alcoholmode.append(alcohol)
            x=x+1

        self.textbox.insert(0.0, st.mode(alcoholmode))

        self.textbox.insert(0.0, "\nModa de porcentaje de alcohol en un espacio de 120 muestras:\n\n")

        time.sleep(0.5)

        for x in range (120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            carbondioxide = data.get("co2", 0)
            carbondioxidemode.append(carbondioxide)
            x=x+1

        self.textbox.insert(0.0, st.mode(carbondioxidemode))

        self.textbox.insert(0.0, "\nModa de partes por millón de dióxido de carbono en un espacio de 120 muestras:\n\n")

    def probabilidad(self):
        espaciomuestralalcohol = []
        espaciomuestraldioxidodecarbono = []
    
        self.realtime_data()
    
        for _ in range(120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            alcohol = data.get("alcohol", 0)
            espaciomuestralalcohol.append(alcohol)
    
        for _ in range(120):
            line = self.ser.readline().decode('utf-8')
            data = json.loads(line)
            carbondioxide = data.get("co2", 0)
            espaciomuestraldioxidodecarbono.append(carbondioxide)

        prob_alcohol_mayor_32 = np.mean(np.array(espaciomuestralalcohol) <= 32)
        prob_dioxidodecarbono_mayor_38 = np.mean(np.array(espaciomuestraldioxidodecarbono) >= 38)

        self.textbox.insert(0.0,prob_alcohol_mayor_32)

        self.textbox.insert(0.0, "\nProbabilidad de obtener un porcentaje de alcohol menor a 32° en un espacio de 120 muestras:\n\n")
        
        self.textbox.insert(0.0,prob_dioxidodecarbono_mayor_38)

        self.textbox.insert(0.0, "\nProbabilidad de obtener 38 partes por millón de dióxido de carbono en un espacio de 120 muestras:\n\n")



    def exportar_muestreo(self):
        a = np.empty((0, 2))

        for _ in range(120):
            try:
                line = self.ser.readline().decode('utf-8')
                data = json.loads(line)
                carbondioxide = data.get("co2", 0)
                alcohol = data.get("alcohol", 0)
                a = np.append(a, np.array([[carbondioxide, alcohol]]), axis=0)
            except json.JSONDecodeError:
                print("Error al decodificar JSON")

        np.savetxt("espaciomuestral.csv", a, delimiter=",", header="Dioxido de carbono,Alcohol", comments="",fmt='%1.4f')


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ct.set_widget_scaling(new_scaling_float)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)        

        
if __name__ == '__main__':
    app = App()
    app.mainloop()