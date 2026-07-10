from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
import sympy as sp

custom_theme = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "yellow",
    "error": "bold red",
    "math": "magenta",
})

console = Console(theme=custom_theme)

class UIPrinter:
    """Gerencia a exibição formatada de elementos na tela."""
    
    @staticmethod
    def print_header():
        title = Text("TAYLOR STUDIO", justify="center", style="bold cyan")
        panel = Panel(title, box=box.DOUBLE, padding=(1, 5), expand=False)
        console.print(Align.center(panel))
        console.print()

    @staticmethod
    def pretty_math(expr: sp.Expr) -> str:
        return sp.pretty(expr, use_unicode=True)

    @staticmethod
    def show_derivatives_table(derivatives: list):
        table = Table(title="Derivadas Sucessivas", box=box.ROUNDED, show_header=True)
        table.add_column("Ordem (n)", justify="center", style="cyan")
        table.add_column("Notação", justify="center", style="green")
        table.add_column("Expressão", style="math")

        for i, expr in enumerate(derivatives):
            notation = "f(x)" if i == 0 else f"f" + "'" * i if i <= 3 else f"f^({i})(x)"
            table.add_row(str(i), notation, UIPrinter.pretty_math(expr))
        
        console.print(table)