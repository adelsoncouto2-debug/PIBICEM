import sympy as sp
from typing import Tuple, Any

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