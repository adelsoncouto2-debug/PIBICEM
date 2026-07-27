import sympy as sp
from typing import List, Dict

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