import sys
from ui.menu import MenuController
from ui.printer import console

def main():
    try:
        app = MenuController()
        app.main_loop()
    except KeyboardInterrupt:
        console.print("\n[bold red]Operação cancelada pelo usuário. Saindo...[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Erro Fatal: {str(e)}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main()