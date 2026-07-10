import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class TaylorPlotter:
    """Gera visualizações gráficas da aproximação de Taylor."""
    
    @staticmethod
    def plot(func: sp.Expr, poly: sp.Expr, var: sp.Symbol, center: float, range_val: float = 5.0):
        f_lambdify = sp.lambdify(var, func, modules=['numpy', 'math'])
        p_lambdify = sp.lambdify(var, poly, modules=['numpy', 'math'])
        
        c = float(center)
        x_vals = np.linspace(c - range_val, c + range_val, 400)
        
        try:
            y_func = f_lambdify(x_vals)
            y_poly = p_lambdify(x_vals)
        except Exception:
            y_func = np.array([float(func.subs(var, x)) for x in x_vals])
            y_poly = np.array([float(poly.subs(var, x)) for x in x_vals])
            
        error_abs = np.abs(y_func - y_poly)
        error_rel = np.where(y_func != 0, error_abs / np.abs(y_func), 0)

        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Análise da Série de Taylor', fontsize=16)

        axs[0, 0].plot(x_vals, y_func, label='Original f(x)', color='blue')
        axs[0, 0].plot(x_vals, y_poly, label='Taylor T(x)', color='orange', linestyle='--')
        axs[0, 0].axvline(c, color='gray', linestyle=':', label='Centro (a)')
        axs[0, 0].set_title('Função vs Polinômio')
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        zoom_range = range_val * 0.2
        x_zoom = np.linspace(c - zoom_range, c + zoom_range, 100)
        try:
            axs[0, 1].plot(x_zoom, f_lambdify(x_zoom), label='f(x)')
            axs[0, 1].plot(x_zoom, p_lambdify(x_zoom), label='T(x)', linestyle='--')
        except Exception:
            axs[0, 1].plot(x_zoom, [float(func.subs(var, x)) for x in x_zoom], label='f(x)')
            axs[0, 1].plot(x_zoom, [float(poly.subs(var, x)) for x in x_zoom], label='T(x)', linestyle='--')
        axs[0, 1].set_title('Zoom próximo ao Centro')
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        axs[1, 0].plot(x_vals, error_abs, color='red')
        axs[1, 0].set_title('Erro Absoluto |f(x) - T(x)|')
        axs[1, 0].grid(True)

        axs[1, 1].plot(x_vals, error_rel, color='purple')
        axs[1, 1].set_title('Erro Relativo')
        axs[1, 1].grid(True)

        plt.tight_layout()
        plt.show()