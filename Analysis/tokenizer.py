from repository import lexer
from sintax_analizer import Sintax_Analizer

analizer= Sintax_Analizer()
parser=analizer.parser
class Tokenizer:

    def __init__(self):
        self.parser= parser
        

    def modo_interactivo(self):
        print("--- Compilador Oskar v1.0 (Mariano Gálvez) ---")
        print("Escribe tu código y presiona Enter para analizar.")
        print("Escribe 'salir' para terminar.\n")

        while True:
            try:
                data = input(">> ")
                if data.lower() == 'salir':
                    break
                if not data:
                    continue

                # 2. Mostrar Análisis Léxico (Opcional pero útil para tu tarea)
                print("\n[ANÁLISIS LÉXICO]")
                lexer.input(data)
                # Copiamos los tokens para no consumirlos antes del parser
                for tok in lexer:
                    print(f"Token: {tok.type:<15} | Lexema: {tok.value}")

                # 3. Mostrar Análisis Sintáctico (AST)
                print("\n[ANÁLISIS SINTÁCTICO - Árbol AST]")
                result = parser.parse(data)
                if result:
                    print(result)
                else:
                    print("La sintaxis es correcta, pero no generó un árbol (vacío).")
                print("-" * 40)

            except Exception as e:
                print(f"Error durante el proceso: {e}")

if __name__ == "__main__":
    tokenizer=Tokenizer()
    tokenizer.modo_interactivo()