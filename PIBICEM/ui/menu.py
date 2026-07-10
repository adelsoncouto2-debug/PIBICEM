import time
from datetime import datetime
from rich.prompt import Prompt, Confirm
from ui.printer import console, UIPrinter
from ui.animations import AnimationManager
from core.parser import MathParser
from core.derivatives import DerivativeEngine
from core.taylor import TaylorBuilder
from core.simplify import SymPyValidator
from core.graphs import TaylorPlotter

class MenuController:
    def __init__(self):
        self.parser = MathParser()
        self.history = []

    def main_loop(self):
        while True:
            console.clear()
            UIPrinter.print_header()
            
            console.print("1 - [cyan]Nova Série de Taylor[/]")
            console.print("2 - [cyan]Histórico[/]")
            console.print("0 - [red]Sair[/]\n")
            
            choice = Prompt.ask("Escolha uma opção", choices=["1", "2", "0"])
            
            if choice == "0":
                console.print("\n[bold green]Obrigado por usar o Taylor Studio. Até logo![/]")
                break
            elif choice == "1":
                self.run_taylor_pipeline()
            elif choice == "2":
                self.show_history()
                
    def run_taylor_pipeline(self):
        console.rule("[bold magenta]Configuração da Série")
        
        expr_str = Prompt.ask("Digite a função f(x) (ex: sin(x), exp(x), ln(x+1))")
        center_str = Prompt.ask("Centro da expansão (a)", default="0")
        order_str = Prompt.ask("Ordem do polinômio (n)", default="4")
        
        start_time = time.time()
        
        try:
            f_expr = self.parser.parse(expr_str)
            a_val = self.parser.parse(center_str)
            order = int(order_str)
            
            console.print(f"\n[success]✓[/] Função interpretada: [math]{UIPrinter.pretty_math(f_expr)}[/]")
            
            engine = DerivativeEngine(f_expr, self.parser.x)
            derivatives = AnimationManager.run_with_progress("Calculando Derivadas", engine.calculate_all, order)
            UIPrinter.show_derivatives_table(derivatives)
            
            builder = TaylorBuilder(derivatives, self.parser.x, a_val)
            evals = builder.evaluate_at_center()
            terms = builder.build_terms(evals)
            
            console.rule("[bold magenta]Construção da Série (Somas Parciais)")
            polynomial = AnimationManager.build_series_live(terms, self.parser.x)
            
            console.rule("[bold magenta]Simplificação")
            simplified_poly = SymPyValidator.simplify_expression(polynomial)
            console.print("[yellow]Antes:[/]\n", UIPrinter.pretty_math(polynomial))
            console.print("\n[green]Depois:[/]\n", UIPrinter.pretty_math(simplified_poly))
            
            console.rule("[bold magenta]Validação de Derivada")
            man_diff, sym_diff, is_diff_equal = SymPyValidator.compare_derivative(simplified_poly, self.parser.x)
            console.print("Derivada do Polinômio Manual:\n", UIPrinter.pretty_math(man_diff))
            if is_diff_equal:
                console.print("\n[bold green]✓ A derivada coincide com o motor simbólico![/]")
            else:
                console.print("\n[bold red]✗ Diferença encontrada na derivada![/]")
                
            console.rule("[bold magenta]Prova Real (Validação SymPy)")
            is_valid = SymPyValidator.validate_with_series(f_expr, self.parser.x, a_val, order, simplified_poly)
            if is_valid:
                console.print("[bold green]✓ A implementação manual coincide EXATAMENTE com sympy.series()[/]")
            else:
                console.print("[bold red]✗ Alerta: O polinômio gerado difere da engine do SymPy.[/]")

            elapsed_time = time.time() - start_time
            
            self.history.append({
                "função": expr_str,
                "ordem": order,
                "centro": center_str,
                "tempo": round(elapsed_time, 4),
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            if Confirm.ask("\nDeseja visualizar os gráficos?"):
                console.print("[cyan]Gerando janela do Matplotlib...[/]")
                TaylorPlotter.plot(f_expr, simplified_poly, self.parser.x, float(a_val))
                
        except Exception as e:
            console.print(f"\n[error]Erro durante a execução: {str(e)}[/]")
            
        Prompt.ask("\n[dim]Pressione Enter para continuar...[/]")

    def show_history(self):
        console.rule("[bold magenta]Histórico de Cálculos")
        if not self.history:
            console.print("[yellow]Nenhum cálculo realizado nesta sessão.[/]")
        else:
            for item in self.history:
                console.print(f"[cyan]{item['data']}[/] | f(x) = {item['função']} | Ordem: {item['ordem']} | Centro: {item['centro']} | Tempo: {item['tempo']}s")
        Prompt.ask("\n[dim]Pressione Enter para voltar...[/]")