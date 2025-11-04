# Locutor Python - Conversor de Texto para Áudio

Aplicação web que converte textos em português para arquivos de áudio MP3 utilizando a biblioteca gTTS (Google Text-to-Speech).

## 🚀 Funcionalidades

- Conversão de texto para áudio em português brasileiro
- Interface web responsiva e moderna
- Suporte a textos longos
- Download automático do arquivo MP3 gerado

## 📋 Pré-requisitos

- Python 3.10 ou superior instalado 
- Biblioteca gTTS instalado
- Conexão com internet (necessária para a conversão e CDNs utilizados)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd [NOME_DO_REPOSITORIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Inicie um servidor local Python:
```bash
python -m http.server 8000
```

2. Abra o navegador e acesse:
```
http://localhost:8000
```

3. Digite ou cole o texto desejado na área de texto
4. Clique em "Converter para Áudio"
5. Aguarde a conversão e o download iniciará automaticamente

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- gTTS (Google Text-to-Speech)
- VOSK (Speech-to-Text)
- Bootstrap 5
- HTML5/CSS3
- JavaScript

## ✒️ Estrutura do Projeto

```
├── README.md           # Documentação do projeto
├── requirements.txt    # Dependências Python
├── LocutorPY.py       # Script Python de conversão
└── index.html         # Interface web responsiva
```

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes

## 🎁 Notas

- O serviço gTTS requer conexão com a internet
- Arquivos muito grandes podem levar mais tempo para processar
- Recomendado usar navegadores modernos para melhor experiência
