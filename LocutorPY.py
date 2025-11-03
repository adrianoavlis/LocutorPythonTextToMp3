import sys
import traceback
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)  # Permite requisições cross-origin

# Servir o arquivo index.html
@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texto não fornecido'}), 400

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
        # Criar o arquivo de áudio
        tts = gTTS(text=text, lang='pt-br', slow=False)
        output_file = "Locucao.mp3"
        tts.save(output_file)
        
        # Enviar o arquivo
        return send_file(
            output_file,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="Locucao.mp3"
        )

    except Exception as e:
        print("Erro durante a geração do arquivo MP3:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Verificando dependências...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
        print("Dependências instaladas com sucesso.")
    except Exception as e:
        print("Erro ao instalar dependências:", e)
        print("Por favor, instale manualmente:")
        print(f"    {sys.executable} -m pip install flask flask-cors")
        sys.exit(1)

    # Iniciar o servidor
    print("Iniciando servidor na porta 5000...")
    print("Acesse http://localhost:5000 no seu navegador")
    app.run(debug=True)
consolidou-se como um importante indicador social e econômico, permitindo compreender como a renda do trabalhador se relaciona com o acesso aos bens essenciais
de subsistência. Além de refletir as condições de vida, o acompanhamento de seus valores serve como base para políticas públicas e negociações salariais (ALCÂNTARA
et al., 2025a). Este trabalho tem como objetivo geral analisar os preços da cesta básica e propor uma solução tecnológica que facilite o acesso e a interpretação desses dados. A plataforma desenvolvida busca democratizar a informação econômica,
oferecendo um ambiente interativo e acessível para o público em geral.
A origem da cesta básica remonta ao Decreto-Lei nº 399/1938, que definiu um conjunto mínimo de produtos essenciais à subsistência. Posteriormente, a Consolidação das Leis do Trabalho (CLT) incorporou o conceito à legislação trabalhista,
e sua composição passou a ser orientada por critérios nutricionais e econômicos (BRASIL, 1938; CUNHA, 2024). Assim, a cesta básica tornou-se um indicador de referência para o cálculo de benefícios salariais e programas sociais, servindo como
parâmetro de subsistência adotado por órgãos públicos e institutos de pesquisa em todo o país.
O Departamento Intersindical de Estatística e Estudos Socioeconômicos (DIEESE) é responsável pela Pesquisa Nacional da Cesta Básica de Alimentos, conduzida desde 1959 em diversas capitais brasileiras. O estudo coleta mensalmente
preços de produtos essenciais, calcula o custo total da cesta e estima o salário mínimo necessário (DIEESE, 2024). Essa metodologia consolidou o DIEESE como uma das principais fontes de dados socioeconômicos do país, permitindo análises comparativas entre regiões e o acompanhamento da evolução histórica dos preços dos alimentos.
Em um cenário global marcado por crises econômicas, conflitos e mudanças climáticas, o custo dos alimentos tornou-se um indicador de vulnerabilidade social
e econômica. Organismos internacionais, como a FAO e o Banco Mundial, utilizam índices alimentares para mensurar a segurança alimentar e os impactos da
inflação global (FAO, 2023; BANCO MUNDIAL, 2024). Entretanto, no Brasil, as informações sobre preços e poder de compra ainda se apresentam de forma fragmentada e pouco acessível, o que reforça a necessidade de democratizar o acesso a esses
dados e promover maior transparência nas políticas públicas.
Embora o DIEESE e o IBGE disponibilizem relatórios e planilhas sobre preços e inflação, esses dados estão frequentemente dispersos em formatos técnicos e
pouco intuitivos. A ausência de uma plataforma integrada dificulta a compreensão e o uso das informações por cidadãos, jornalistas e pesquisadores (IBGE, 2024). O
problema, portanto, não é apenas tecnológico, mas informacional — faltam acessibilidade e clareza na apresentação dos dados, o que limita seu potencial educativo
e analítico.
Diversos estudos acadêmicos reforçam a relevância da cesta básica como parâmetro socioeconômico e instrumento de análise das desigualdades regionais.
Alcântara, Urraca-Ruiz e Santos (2025) identificam assimetrias no comprometimento do salário mínimo entre as diferentes capitais brasileiras, enquanto Cunha
(2024) destaca fatores locais que influenciam o custo da cesta no município do Rio de Janeiro. Essas pesquisas apontam a necessidade de ferramentas analíticas que
facilitem a exploração de séries históricas e a comparação regional e temporal dos dados.
O presente estudo utiliza informações da Pesquisa Nacional da Cesta Básica de Alimentos do DIEESE como fonte principal, complementadas por indicadores oficiais do IBGE, como o Índice Nacional de Preços ao Consumidor (INPC) e o Índice de Preços ao Consumidor Amplo (IPCA). Os dados são armazenados em um banco de dados relacional (SQL Server) e processados por meio da plataforma KNIME, o que permite calcular métricas como preço médio, variação mensal e tendências de longo prazo. O uso de scraping ético complementa a coleta de informações sobre produtos e mercados, enriquecendo as análises econômicas. Apesar da ampla disponibilidade de dados públicos, a interpretação dos valores da cesta básica permanece restrita a ambientes técnicos e acadêmicos. A falta de visualizações acessíveis e comparações diretas entre cidades, períodos e produtos compromete a disseminação do conhecimento econômico entre a população. O desafio, portanto, está em transformar dados complexos em informações compreensíveis,
interativas e socialmente úteis. Para mitigar essa dificuldade, propõe-se o desenvolvimento da Plataforma Cesta Básica, uma aplicação web voltada à coleta, tratamento e exibição de dados sobre o custo da cesta básica. O sistema apresenta dashboards interativos
que permitem comparar preços, períodos e produtos entre diferentes cidades, de forma intuitiva e visual. A proposta busca aproximar a população dos dados socioeconômicos, ampliando o acesso à informação e fortalecendo o controle social sobre
as condições de vida no país (ALCÂNTARA et al., 2025a; CUNHA, 2024)."""
tts = gTTS(text=texto, lang='pt-br', slow=False)
try:
	print("Iniciando síntese de voz... (pode requerer conexão com a internet)")
	tts.save("Locucao.mp3")
	print("Arquivo 'Locucao.mp3' salvo com sucesso.")
except Exception:
	print("Erro durante a geração do arquivo Locucao.mp3:")
	traceback.print_exc()
	sys.exit(1)
