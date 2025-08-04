import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from scipy.stats import norm
import numpy as np
import pandas as pd
import seaborn as sns

# Call option price calc
def call_bsm_calc(S, K, T, r, vol):
    d1 = ((math.log(S/K))+((r+(vol**2/2))*T))/(vol*math.sqrt(T))
    d2 = d1 - (vol*math.sqrt(T))
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    C = (S*Nd1) - (K*(math.e**(-r*T))*Nd2)
    return round(C, 2)

# Put option price calc
def put_bsm_calc(S, K, T, r, vol):
    d1 = ((math.log(S/K))+((r+(vol**2/2))*T))/(vol*math.sqrt(T))
    d2 = d1 - (vol*math.sqrt(T))
    Nd1 = norm.cdf(-d1)
    Nd2 = norm.cdf(-d2)
    P = (K*(math.e**(-r*T))*Nd2) - (S*Nd1)
    return round(P, 2)

# Heatmap generation
def generate_heatmaps():
    try:
        S = float(entry_S.get())
        K = float(entry_K.get())
        T = float(entry_T.get())
        r = float(entry_r.get())
        vol = float(entry_vol.get())
        min_spot = spot_min_slider.get()
        max_spot = spot_max_slider.get()
        min_vol = vol_min_slider.get() / 100.0
        max_vol = vol_max_slider.get() / 100.0

        if min_spot >= max_spot or min_vol >= max_vol:
            messagebox.showerror("Input Error", "Min must be less than Max for both spot price and volatility.")
            return

        call_val = call_bsm_calc(S, K, T, r, vol)
        put_val = put_bsm_calc(S, K, T, r, vol)
        result_var.set(f"Call Option Price: ${call_val}     Put Option Price: ${put_val}")

        spot_prices = np.round(np.linspace(min_spot, max_spot, 10), 2)
        volatilities = np.round(np.linspace(min_vol, max_vol, 10), 2)

        call_data = np.array([[call_bsm_calc(S_loop, K, T, r, vol_loop)
                               for S_loop in spot_prices] for vol_loop in volatilities])
        put_data = np.array([[put_bsm_calc(S_loop, K, T, r, vol_loop)
                              for S_loop in spot_prices] for vol_loop in volatilities])

        call_df = pd.DataFrame(call_data, index=volatilities, columns=spot_prices)
        put_df = pd.DataFrame(put_data, index=volatilities, columns=spot_prices)

        fig, axs = plt.subplots(1, 2, figsize=(12, 3.5))
        plt.tight_layout(pad=1.0)
        sns.heatmap(call_df, annot=True, fmt=".2f", cmap="YlGnBu", ax=axs[0])
        axs[0].set_title("Call Option Prices")
        axs[0].set_xlabel("Spot Price")
        axs[0].set_ylabel("Volatility")

        sns.heatmap(put_df, annot=True, fmt=".2f", cmap="YlOrRd", ax=axs[1])
        axs[1].set_title("Put Option Prices")
        axs[1].set_xlabel("Spot Price")
        axs[1].set_ylabel("Volatility")

        for widget in window.grid_slaves():
            if isinstance(widget, tk.Widget) and hasattr(widget, 'get_tk_widget'):
                widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=8, column=0, columnspan=4, pady=(5,10), sticky="nsew")
        
        window.grid_rowconfigure(8, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1)
        window.grid_columnconfigure(3, weight=1)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical inputs.")


## GUI Config
window = tk.Tk()
window.title("Black-Scholes Call & Put Heatmap Generator")
window.geometry("1400x750")

ttk.Label(window, text="Spot Price (S):").grid(column=0, row=0, sticky=tk.W)
entry_S = ttk.Entry(window)
entry_S.grid(column=1, row=0)

ttk.Label(window, text="Strike Price (K):").grid(column=0, row=1, sticky=tk.W)
entry_K = ttk.Entry(window)
entry_K.grid(column=1, row=1)

ttk.Label(window, text="Time to Maturity (T):").grid(column=0, row=2, sticky=tk.W)
entry_T = ttk.Entry(window)
entry_T.grid(column=1, row=2)

ttk.Label(window, text="Risk-Free Rate (r):").grid(column=0, row=3, sticky=tk.W)
entry_r = ttk.Entry(window)
entry_r.grid(column=1, row=3)

ttk.Label(window, text="Volatility (σ):").grid(column=0, row=4, sticky=tk.W)
entry_vol = ttk.Entry(window)
entry_vol.grid(column=1, row=4)

ttk.Label(window, text="Spot Price Range:").grid(column=2, row=0, sticky=tk.W)
spot_min_slider = tk.Scale(window, from_=10, to=150, orient=tk.HORIZONTAL, label="Min Spot")
spot_min_slider.set(40)
spot_min_slider.grid(column=3, row=0)
spot_max_slider = tk.Scale(window, from_=10, to=150, orient=tk.HORIZONTAL, label="Max Spot")
spot_max_slider.set(60)
spot_max_slider.grid(column=3, row=1)

ttk.Label(window, text="Volatility Range (%):").grid(column=2, row=2, sticky=tk.W)
vol_min_slider = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, label="Min Vol (%)")
vol_min_slider.set(30)
vol_min_slider.grid(column=3, row=2)
vol_max_slider = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL, label="Max Vol (%)")
vol_max_slider.set(40)
vol_max_slider.grid(column=3, row=3)

generate_btn = ttk.Button(window, text="Generate Prices", command=generate_heatmaps)
generate_btn.grid(column=0, row=5, columnspan=4, pady=10)

result_var = tk.StringVar()
ttk.Label(window, textvariable=result_var, font=("Helvetica", 11, "bold")).grid(row=6, column=0, columnspan=4)

window.mainloop()