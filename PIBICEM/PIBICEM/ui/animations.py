from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from ui.printer import console, UIPrinter
import sympy as sp
import time

class AnimationManager:
    """Gerencia spinners, barras de progresso e atualizações ao vivo."""

    @staticmethod
    def build_series_live(terms: list, var: sp.Symbol):
        current_sum = 0
        
        with Live(console=console, refresh_per_second=4) as live:
            for term_data in terms:
                n = term_data['n']
                term_expr = term_data['term']
                current_sum += term_expr
                
                content = f"Adicionando Termo {n}:\n\n"
                content += f"f^({n})(a) = {UIPrinter.pretty_math(term_data['f_n_a'])}\n"
                content += f"Termo: {UIPrinter.pretty_math(term_expr)}\n"
                content += "-" * 30 + "\n"
                content += f"T_{n}(x) = \n{UIPrinter.pretty_math(current_sum)}"
                
                panel = Panel(content, title=f"[bold yellow]Construindo Soma Parcial T_{n}[/]", border_style="cyan")
                live.update(panel)
                time.sleep(0.8)
                
        return current_sum

    @staticmethod
    def run_with_progress(task_name: str, func, *args, **kwargs):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]{task_name}...", total=100)
            for _ in range(5):
                time.sleep(0.1)
                progress.advance(task, 20)
            
            result = func(*args, **kwargs)
            progress.update(task, completed=100, description=f"[bold green]{task_name} Concluído!")
            return result