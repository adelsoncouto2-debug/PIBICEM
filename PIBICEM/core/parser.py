import sympy as sp
from utils.validator import InputValidator

class MathParser:
    
    def __init__(self):
        self.x = sp.Symbol('x')
        
    def parse(self, expr_str: str) -> sp.Expr:
        is_valid, expr = InputValidator.validate_expression(expr_str)
        if not is_valid:
            raise ValueError(f"Expressão inválida: {expr_str}")
        return expr