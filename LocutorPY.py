import sys
import traceback
from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
import os
import tempfile
import uuid
from datetime import datetime
import time

app = Flask(__name__, static_folder='assets', static_url_path='/assets')
CORS(app)  # Permite requisições cross-origin

# Configurações
MAX_TEXT_LENGTH = 50000  # Máximo de caracteres permitidos
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'locutor_py')
os.makedirs(TEMP_DIR, exist_ok=True)

# Servir o arquivo index.html
@app.route('/')
def home():
    return send_file('index.html')

def cleanup_old_files():
    """Remove arquivos temporários mais antigos que 1 hora"""
    try:
        current_time = time.time()
        for filename in os.listdir(TEMP_DIR):
            filepath = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(filepath):
                if current_time - os.path.getctime(filepath) > 3600:  # 1 hora
                    os.remove(filepath)
    except Exception as e:
        print(f"Erro ao limpar arquivos temporários: {e}")

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Limpar arquivos antigos antes de processar
        cleanup_old_files()
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Texto não fornecido'}), 400
            
        if len(text) > MAX_TEXT_LENGTH:
            return jsonify({'error': f'Texto muito longo. Máximo de {MAX_TEXT_LENGTH} caracteres.'}), 400

        # Importar gTTS (com tratamento de erro)
        try:
            from gtts import gTTS
        except ImportError:
            print("Módulo 'gtts' não encontrado. Instalando...")
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "gTTS"])
                from gtts import gTTS
            except Exception as e:
                return jsonify({'error': f'Erro ao instalar gTTS: {str(e)}'}), 500
        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f"locucao_{timestamp}_{unique_id}.mp3"
        output_file = os.path.join(TEMP_DIR, output_filename)

        # Criar o arquivo de áudio
        tts = gTTS(text=text, lang='pt-br', slow=False)
        tts.save(output_file)

        # Verificar se o arquivo foi criado
        if not os.path.exists(output_file):
            return jsonify({'error': 'Falha ao gerar arquivo de áudio'}), 500

        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(output_file):
                    os.remove(output_file)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {e}")
            return response
        
        # Enviar o arquivo
        return send_file(
            output_file,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="Locucao.mp3",
            max_age=0  # Evita cache no navegador
        )

    except Exception as e:
        print("Erro durante a geração do arquivo MP3:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def check_environment():
    """Verifica e configura o ambiente"""
    try:
        # Verificar permissões do diretório temporário
        test_file = os.path.join(TEMP_DIR, 'test.txt')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except Exception as e:
            print(f"Erro: Sem permissão para escrever em {TEMP_DIR}")
            print(f"Erro detalhado: {e}")
            return False

        # Verificar dependências
        import subprocess
        for package in ['flask', 'flask-cors', 'gTTS']:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                print(f"Instalando {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
        
    except Exception as e:
        print(f"Erro ao configurar ambiente: {e}")
        print("Por favor, instale manualmente:")
        print(f"    {sys.executable} -m pip install flask flask-cors gTTS")
        return False

if __name__ == '__main__':
    if not check_environment():
        sys.exit(1)

    # Limpar arquivos temporários antigos na inicialização
    cleanup_old_files()
    
    # Configurar endereço e porta
    host = '127.0.0.1'  # Localhost apenas
    port = 5000
    
    print(f"\nIniciando servidor em http://{host}:{port}")
    print("Use Ctrl+C para encerrar o servidor")
    
    try:
        app.run(host=host, port=port, debug=False)  # debug=False em produção
    except Exception as e:
        print(f"\nErro ao iniciar servidor: {e}")
        sys.exit(1)
