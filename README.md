# Black-Scholes Call & Put Heatmap Generator

## Overview
This Python program calculates Call and Put option prices using the Black-Scholes-Merton (BSM) model and visualizes them in heatmap form over a range of spot prices and volatilities.  
The program features an interactive GUI built with `tkinter`, allowing the user to input parameters, set ranges, and view results instantly.
Inspiration taken from this project by Prudhvi Reddy (https://blackschole.streamlit.app/)

## Black-Scholes Formula

The Black-Scholes-Merton model prices European-style options under certain assumptions (log-normal asset price distribution, constant volatility, and no dividends).  

For a Call option price (C):

```math
C = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)
```

For a Put option price (P):

```math
P = K \cdot e^{-rT} \cdot N(-d_2) - S \cdot N(-d_1)
```

Where:

```math
d_1 = \frac{\ln(S/K) + (r + \frac{\sigma^2}{2})T}{\sigma \sqrt{T}}
```

```math
d_2 = d_1 - \sigma \sqrt{T}
```

**Parameters:**
- S = Current stock price
- K = Strike price  
- r = Risk-free rate
- T = Time to expiration
- σ = Volatility
- N(x) = Cumulative standard normal distribution function

---

## How the Program Uses the Formula
- The functions `call_bsm_calc` and `put_bsm_calc` implement the above formulas to compute Call and Put prices respectively.
- Inputs are taken from the GUI fields for:
  - Spot Price (S)
  - Strike Price (K)
  - Time to Maturity (T)
  - Risk-Free Rate (r)
  - Volatility (σ)
- The calculated option prices are rounded to two decimal places for display.

---

## Heatmap Functionality
- The program generates two heatmaps: one for Call prices and one for Put prices.
- Axes:
  - **X-axis:** Spot Price values within a user-defined range.
  - **Y-axis:** Volatility values within a user-defined range.
- Each cell in the heatmap represents the option price for that combination of Spot Price and Volatility, calculated using the Black-Scholes formula.
- Color intensity corresponds to the magnitude of the option price, providing a clear visual representation of how prices change across the parameter space.

---

## Features
- Call and Put price calculation using the Black-Scholes-Merton model.
- Interactive GUI with input fields and sliders for parameter ranges.
- Side-by-side heatmaps for Call and Put prices.
- Error handling for invalid inputs.
- Adjustable spot price and volatility ranges.

---

## Requirements
Install the required libraries:
pip install matplotlib seaborn numpy pandas scipy
