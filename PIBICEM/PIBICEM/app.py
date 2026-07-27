import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Any

class InputValidator:
    @staticmethod
    def validate_expression(expr_str: str) -> Tuple[bool, Any]:
        try:
            expr = sp.sympify(expr_str, strict=False)
            return True, expr
        except (sp.SympifyError, TypeError, ValueError):
            return False, None

    @staticmethod
    def validate_center_and_order(a_str: str, n_str: str) -> Tuple[bool, Any, int]:
        try:
            a_val = sp.sympify(a_str)
            n_val = int(n_str)
            if n_val < 0:
                return False, None, -1
            return True, a_val, n_val
        except Exception:
            return False, None, -1

class MathParser:
    def __init__(self):
        self.x = sp.Symbol('x')
        
    def parse(self, expr_str: str) -> sp.Expr:
        is_valid, expr = InputValidator.validate_expression(expr_str)
        if not is_valid:
            raise ValueError(f"Expressão inválida: {expr_str}")
        return expr

class DerivativeEngine:
    def __init__(self, expr: sp.Expr, var: sp.Symbol):
        self.expr = expr
        self.var = var
        
    def calculate_all(self, order: int) -> List[sp.Expr]:
        derivatives = [self.expr]
        current_expr = self.expr
        for _ in range(order):
            current_expr = sp.diff(current_expr, self.var)
            derivatives.append(current_expr)
        return derivatives

class TaylorBuilder:
    def __init__(self, derivatives: List[sp.Expr], var: sp.Symbol, center: sp.Expr):
        self.derivatives = derivatives
        self.var = var
        self.center = center
        
    def evaluate_at_center(self) -> List[sp.Expr]:
        evaluations = []
        for deriv in self.derivatives:
            val = deriv.subs(self.var, self.center)
            evaluations.append(val)
        return evaluations

    def build_terms(self, evaluations: List[sp.Expr]) -> List[Dict]:
        terms = []
        for n, val in enumerate(evaluations):
            factorial_n = sp.factorial(n)
            poly_part = (self.var - self.center)**n
            term_expr = (val / factorial_n) * poly_part
            terms.append({
                'n': n,
                'f_n_a': val,
                'fact': factorial_n,
                'poly': poly_part,
                'term': term_expr
            })
        return terms

class SymPyValidator:
    @staticmethod
    def simplify_expression(expr: sp.Expr) -> sp.Expr:
        return sp.simplify(expr)
        
    @staticmethod
    def compare_derivative(poly: sp.Expr, var: sp.Symbol) -> Tuple[sp.Expr, sp.Expr, bool]:
        manual_diff = sp.diff(poly, var)
        sympy_diff = sp.diff(sp.simplify(poly), var)
        return manual_diff, sympy_diff, sp.simplify(manual_diff - sympy_diff) == 0

    @staticmethod
    def validate_with_series(original_func: sp.Expr, var: sp.Symbol, center: sp.Expr, order: int, manual_poly: sp.Expr) -> bool:
        sympy_series = sp.series(original_func, var, center, order + 1).removeO()
        diff = sp.simplify(manual_poly - sympy_series)
        return diff == 0

st.set_page_config(
    page_title="Análise de Série de Taylor",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">Análise de Série de Taylor</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("Configurações")
    
    expr_input = st.text_input("Função f(x):", value="sin(x)")
    center_input = st.text_input("Ponto de expansão (a):", value="0")
    order_input = st.text_input("Ordem da aproximação (n):", value="5")
    
    range_val = st.slider("Intervalo de visualização (faixa do gráfico):", min_value=1.0, max_value=20.0, value=5.0, step=0.5)

with col2:
    is_valid_expr, parsed_expr = InputValidator.validate_expression(expr_input)
    is_valid_params, center_val, order_val = InputValidator.validate_center_and_order(center_input, order_input)
    
    if not is_valid_expr:
        st.error("Erro: Expressão matemática inválida.")
    elif not is_valid_params:
        st.error("Erro: Parâmetros de centro ou ordem inválidos.")
    else:
        try:
            parser = MathParser()
            var = parser.x
            
            engine = DerivativeEngine(parsed_expr, var)
            derivatives = engine.calculate_all(order_val)
            
            builder = TaylorBuilder(derivatives, var, center_val)
            evaluations = builder.evaluate_at_center()
            terms = builder.build_terms(evaluations)
            
            manual_poly = sum(t['term'] for t in terms)
            manual_poly_simplified = SymPyValidator.simplify_expression(manual_poly)
            
            is_correct = SymPyValidator.validate_with_series(parsed_expr, var, center_val, order_val, manual_poly)
            
            st.subheader("Resultados Analíticos")
            st.markdown("**Função Original f(x):**")
            st.latex(sp.latex(parsed_expr))
            
            st.markdown("**Polinômio de Taylor Calculado:**")
            st.latex(sp.latex(manual_poly_simplified))
            
            if is_correct:
                st.success("Polinômio validado com sucesso através do SymPy.")
            else:
                st.warning("Aviso: Houve divergência entre o polinômio calculado e o validador do SymPy.")
                
            f_lambdify = sp.lambdify(var, parsed_expr, modules=['numpy', 'math'])
            p_lambdify = sp.lambdify(var, manual_poly_simplified, modules=['numpy', 'math'])
            
            c = float(center_val.evalf())
            x_vals = np.linspace(c - range_val, c + range_val, 400)
            
            try:
                y_func = f_lambdify(x_vals)
                if isinstance(y_func, (int, float)):
                    y_func = np.full_like(x_vals, y_func)
            except Exception:
                y_func = np.array([float(parsed_expr.subs(var, x_val)) for x_val in x_vals])
                
            try:
                y_poly = p_lambdify(x_vals)
                if isinstance(y_poly, (int, float)):
                    y_poly = np.full_like(x_vals, y_poly)
            except Exception:
                y_poly = np.array([float(manual_poly_simplified.subs(var, x_val)) for x_val in x_vals])
                
            error_abs = np.abs(y_func - y_poly)
            error_rel = np.where(y_func != 0, error_abs / np.abs(y_func), 0)
            
            fig, axs = plt.subplots(2, 2, figsize=(10, 7))
            
            axs[0, 0].plot(x_vals, y_func, label='Original f(x)', color='blue')
            axs[0, 0].plot(x_vals, y_poly, label='Taylor T(x)', color='orange', linestyle='--')
            axs[0, 0].axvline(c, color='gray', linestyle=':', label='Centro (a)')
            axs[0, 0].set_title('Função vs Polinômio')
            axs[0, 0].legend()
            axs[0, 0].grid(True)
            
            zoom_range = range_val * 0.2
            x_zoom = np.linspace(c - zoom_range, c + zoom_range, 100)
            try:
                y_func_zoom = f_lambdify(x_zoom)
                if isinstance(y_func_zoom, (int, float)):
                    y_func_zoom = np.full_like(x_zoom, y_func_zoom)
                y_poly_zoom = p_lambdify(x_zoom)
                if isinstance(y_poly_zoom, (int, float)):
                    y_poly_zoom = np.full_like(x_zoom, y_poly_zoom)
            except Exception:
                y_func_zoom = [float(parsed_expr.subs(var, x_val)) for x_val in x_zoom]
                y_poly_zoom = [float(manual_poly_simplified.subs(var, x_val)) for x_val in x_zoom]
                
            axs[0, 1].plot(x_zoom, y_func_zoom, label='f(x)')
            axs[0, 1].plot(x_zoom, y_poly_zoom, label='T(x)', linestyle='--')
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
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Ocorreu um erro no processamento matemático: {str(e)}")
