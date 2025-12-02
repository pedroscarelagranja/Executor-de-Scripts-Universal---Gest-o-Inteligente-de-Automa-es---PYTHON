import subprocess
import os
import time
import glob

class ExecutorDeScripts:
    def __init__(self):
        self.scripts_encontrados = []
        
    def procurar_scripts(self):
        """Procura automaticamente por scripts na pasta"""
        padroes = ['*.py', '*.js', '*.bat', '*.exe']
        
        for padrao in padroes:
            for arquivo in glob.glob(padrao):
                # Ignora o próprio arquivo executor
                if arquivo != os.path.basename(__file__):
                    self.scripts_encontrados.append(arquivo)
        
        return self.scripts_encontrados
    
    def mostrar_menu(self):
        """Mostra menu interativo"""
        scripts = self.procurar_scripts()
        
        if not scripts:
            print("Nenhum script encontrado na pasta atual!")
            return
        
        print("\n" + " EXECUTOR DE SCRIPTS - MENU".center(50, "="))
        print("Scripts encontrados automaticamente:")
        
        for i, script in enumerate(scripts, 1):
            print(f"  {i}. {script}")
        
        print("\nOpções:")
        print("  0. Executar TODOS os scripts")
        print("  [número]. Executar script específico")
        print("  s. Sair")
    
    def executar_script(self, caminho_script):
        """Executa um script individual"""
        print(f"\n Executando: {caminho_script}")
        
        if not os.path.exists(caminho_script):
            print("Arquivo não encontrado!")
            return False
        
        try:
            # Determina comando baseado na extensão
            if caminho_script.endswith('.py'):
                comando = ['python', caminho_script]
            elif caminho_script.endswith('.js'):
                comando = ['node', caminho_script]
            elif caminho_script.endswith('.bat'):
                comando = [caminho_script]
            elif caminho_script.endswith('.exe'):
                comando = [caminho_script]
            else:
                comando = [caminho_script]
            
            inicio = time.time()
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=30
            )
            tempo = time.time() - inicio
            
            if resultado.returncode == 0:
                print(f" Sucesso! ({tempo:.2f}s)")
                if resultado.stdout.strip():
                    print(f"📤 Saída: {resultado.stdout.strip()}")
                return True
            else:
                print(f"Erro! ({tempo:.2f}s)")
                if resultado.stderr.strip():
                    print(f"💥 Erro: {resultado.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print(" Timeout - Script muito lento!")
            return False
        except Exception as e:
            print(f" Erro: {e}")
            return False
    
    def executar_todos(self):
        """Executa todos os scripts encontrados"""
        scripts = self.procurar_scripts()
        
        if not scripts:
            print(" Nenhum script para executar!")
            return
        
        print(f"\n Executando {len(scripts)} scripts...")
        sucessos = 0
        
        for script in scripts:
            if self.executar_script(script):
                sucessos += 1
            time.sleep(1)  # Pausa entre scripts
        
        print(f"\n Resumo: {sucessos}/{len(scripts)} executados com sucesso!")
    
    def iniciar(self):
        """Inicia o menu interativo"""
        while True:
            self.mostrar_menu()
            escolha = input("\n Sua escolha: ").strip().lower()
            
            if escolha == 's':
                print(" Até mais!")
                break
            elif escolha == '0':
                self.executar_todos()
            elif escolha.isdigit():
                idx = int(escolha) - 1
                scripts = self.procurar_scripts()
                if 0 <= idx < len(scripts):
                    self.executar_script(scripts[idx])
                else:
                    print(" Opção inválida!")
            else:
                print(" Comando não reconhecido!")
            
            input("\n Pressione Enter para continuar...")

# USO RÁPIDO (sem menu)
def executar_rapido():
    """Versão rápida sem menu - só editar a lista e executar"""
    scripts_personalizados = [
        "script1.py",
        "programa.js", 
        "backup.bat"
    ]
    
    executor = ExecutorDeScripts()
    
    for script in scripts_personalizados:
        executor.executar_script(script)

if __name__ == "__main__":
    executor = ExecutorDeScripts()
    executor.iniciar()
