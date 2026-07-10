import sympy as sp
from typing import List

class DerivativeEngine:
    """Calcula derivadas sucessivas de uma função."""
    
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