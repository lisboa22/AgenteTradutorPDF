# Tradutor de PDF Inglês-Português

## Visão Geral

Este sistema oferece uma interface gráfica amigável para traduzir arquivos PDF do inglês para o português. Utiliza a biblioteca `googletrans` para tradução automática, permitindo que usuários carreguem um PDF, visualizem o texto original, traduzam página a página e salvem o resultado em um novo PDF traduzido.

## Objetivo

Facilitar o processo de tradução de documentos PDF em inglês para o português, mantendo o formato original do documento e proporcionando uma experiência simples e eficiente para o usuário.

## Motivação e Escolha da Solução

Durante o desenvolvimento, foram realizados testes com modelos de tradução hospedados no Hugging Face e o LM Studio. Observou-se que:

- Alguns modelos afirmavam traduzir do inglês para o português, mas não realizavam a tradução corretamente.
- Alguns modelos ignoravam espaçamentos, juntando todo o texto em um único bloco, mesmo havendo separação entre linhas ou páginas.
- O LM Studio apresentou limitações relacionadas ao número de tokens suportados por chamada, inviabilizando o uso para arquivos PDF maiores.

Por esses motivos, optou-se pelo uso da api `googletrans`, que possui limitações de até 15.000 caracteres por chamada, mas oferece resultados mais consistentes e compatibilidade com textos segmentados por página.

## Funcionalidades Principais

- **Carregar PDF**: Seleciona um arquivo PDF em inglês para extração do texto.
- **Exibir Texto Original**: Mostra o texto extraído do PDF, separado por páginas.
- **Traduzir Texto**: Envia o texto de cada página para tradução através da `googletrans`.
- **Exibir Texto Traduzido**: Mostra o texto traduzido, também separado por páginas.
- **Salvar PDF Traduzido**: Cria um novo arquivo PDF com o texto traduzido, mantendo o formato paginado.

## APIs e Bibliotecas Utilizadas

- **Tkinter**: Interface gráfica amigável.
- **PyMuPDF (fitz)**: Manipulação e extração de texto dos arquivos PDF.
- **googletrans**: Tradução automática entre inglês e português.
- **threading & asyncio**: Execução da tradução assíncrona sem travar a interface.
- **os**: Manipulação de arquivos e diretórios.

## Estrutura do Código e Funções

### Extração e Criação de PDF

- `extrair_texto_do_pdf(caminho_do_arquivo)`: Extrai o texto de cada página do PDF e retorna uma lista de strings. Em caso de erro, retorna `None`.
- `criar_pdf_traduzido(texto_traduzido, caminho_de_saida)`: Cria um novo PDF com o texto traduzido, uma página para cada string da lista. Retorna `True` em caso de sucesso ou `False` em caso de erro.

### Tradução

- `traduzir_com_googletrans(texto_por_pagina)`: Função assíncrona que recebe uma lista de textos, realiza a tradução de cada página usando a API do Google Translate e retorna uma lista com o texto traduzido.

### Interface Gráfica (`TradutorPDFApp`)

- Inicialização dos componentes gráficos (botões, caixas de texto, labels).
- `carregar_pdf()`: Abre o diálogo para seleção de arquivo PDF, extrai o texto e exibe o conteúdo original.
- `traduzir_texto()`: Inicia a tradução em uma thread separada para não travar a interface.
- `_executar_traducao()`: Executa a corrotina de tradução de forma síncrona dentro da thread.
- `_verificar_traducao_concluida()`: Atualiza a interface após a tradução e exibe o texto traduzido.
- `salvar_pdf_traduzido()`: Salva o texto traduzido em um novo PDF.

### Execução

- O programa inicia a interface gráfica e aguarda ações do usuário.

## Limitações

- O Google Translate possui limite de 15.000 caracteres por chamada, o que pode impactar traduções de PDFs extensos.
- A tradução depende da disponibilidade da API do Google.
- Não há suporte para formatos PDF protegidos ou criptografados.

## Como Usar

1. Execute o programa.
2. Clique em "Carregar PDF em Inglês" e selecione o arquivo desejado.
3. Visualize o texto extraído.
4. Clique em "Traduzir Texto" para iniciar o processo de tradução.
5. Após o término, visualize o texto traduzido.
6. Clique em "Salvar PDF Traduzido" para gerar o novo arquivo.

## Observações sobre testes

- Modelos do Hugging Face e LM Studio foram testados, mas apresentaram problemas de tradução, formatação e limitação de tokens.
- O `googletrans` foi escolhido por apresentar melhor resultado e maior compatibilidade com textos segmentados por páginas.

## Dependências

- Python 3.x
- tkinter
- pymupdf
- googletrans

## Instalação

Instale as dependências via pip:

```bash
pip install pymupdf googletrans==4.0.0-rc1
```

## Licença

Este projeto está disponível sob licença MIT.
