#Plotter takes a Tk root object and uses it as a base to spawn Tk Toplevel plot windows.

import tkinter as tk
import pexpect
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plotter():
    def __init__(self, root):
        plt.close() 
        self.root=root
        self.plots={}
        self.canvases={}
 
    def new_plot(self,i):
        t = tk.Toplevel(self.root)
        t.wm_title('Incidence = '+str(i))
        fig = mpl.figure.Figure(figsize=(20,15))
        plot = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=t)
        canvas.get_tk_widget().pack()
        canvas.draw()
        self.plots[i]=plot
        self.canvases[i]=canvas
        
        def on_closing():
            del self.plots[i]
            t.destroy()
        t.protocol("WM_DELETE_WINDOW", on_closing)
        
    def plot_spectrum(self,i,e, data):
        #If we've never plotted spectra at this incidence angle, make a whole new plot.
        if i not in self.plots:
            self.new_plot(i)
        #Next, plot data onto the appropriate plot.
        self.plots[i].plot(data[0],data[1])
        self.canvases[i].draw()
        
    # def load_data(self, file):
    #     print('loading data')
    #     data = np.genfromtxt(file, skip_header=1, dtype=float,delimiter='\t')
    #     wavelengths=[]
    #     #reflectance=[[],[]]
    #     reflectance=[]
    #     for i, d in enumerate(data):
    #         if i==0: wavelengths=np.array(d) #the first column in my .tsv (now first row) was wavelength in nm
    #         else: #the other columns are all reflectance values
    #             d=np.array(d)
    #             reflectance.append(d)
    #             #d2=d/np.max(d) #d2 is normalized reflectance
    #             #reflectance[0].append(d)
    #             #reflectance[1].append(d2)
    #     print('returning data')
    #     print(wavelengths)
    #     print(reflectance)
    #     return wavelengths, reflectance
    #     
    def plot_spectra(self, name, file, caption):
        self.new_plot(name)
        wavelengths, reflectance, labels=self.load_data(file)
        colors=['red','orange','yellow','greenyellow','green','cyan','dodgerblue','purple','magenta','red','orange','yellow','greenyellow','green','cyan','dodgerblue','purple','magenta','red','orange','yellow','greenyellow','green','cyan','dodgerblue','purple']
        for i,spectrum in enumerate(reflectance):
            self.plots[name].plot(wavelengths, spectrum, label=labels[i+1], color=colors[i])
        self.plots[name].set_title(name, fontsize=24)
        self.plots[name].set_ylabel('Relative Reflectance',fontsize=18)
        self.plots[name].set_xlabel('Wavelength (nm)',fontsize=18)
        self.plots[name].tick_params(labelsize=14)
        self.plots[name].legend()
        self.canvases[name].draw()
        
    def load_data(self, file):
        print('loading')
        data = np.genfromtxt(file, names=True, dtype=float,delimiter='\t')
        labels=list(data.dtype.names)
        print(labels)
        data=zip(*data)
        wavelengths=[]
        #reflectance=[[],[]]
        reflectance=[]
        for i, d in enumerate(data):
            if i==0: wavelengths=d #the first column in my .tsv (now first row) was wavelength in nm
            else: #the other columns are all reflectance values
                d=np.array(d)
                reflectance.append(d)
                #d2=d/np.max(d) #d2 is normalized reflectance
                #reflectance[0].append(d)
                #reflectance[1].append(d2)

        return wavelengths, reflectance, labels
            
        
        