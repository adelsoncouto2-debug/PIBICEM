import sympy as sp
from typing import Tuple

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