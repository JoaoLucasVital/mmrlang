# MMRLang

## Sobre o Projeto

A **MMRLang** é uma linguagem de programação educacional criada para a AV2 da disciplina de **Compiladores**.

O projeto consiste em um **compilador/interpretador simples desenvolvido em Python**, capaz de ler e executar arquivos com extensão `.mmr`.

A linguagem usa comandos próprios em português, tornando o código mais simples de entender e apresentar.

---

## Objetivo

O objetivo do projeto é demonstrar, na prática, conceitos básicos de compiladores e interpretadores, como:

* Leitura de código-fonte;
* Interpretação de comandos;
* Uso de variáveis;
* Estruturas condicionais;
* Estruturas de repetição;
* Tratamento de erros;
* Versionamento no GitHub;
* Documentação em LaTeX.

---

## Principais Características

A MMRLang possui:

* Sintaxe em português;
* Arquivos com extensão `.mmr`;
* Interpretador feito em Python;
* Comandos personalizados;
* Suporte a variáveis;
* Suporte a operações matemáticas;
* Estrutura condicional;
* Estrutura de repetição;
* Mensagens de erro personalizadas;
* Testes separados por arquivos.

---

## Comandos da Linguagem

* `guarda`: cria ou altera uma variável;
* `falaai`: exibe uma mensagem ou valor na tela;
* `eai`: inicia uma condição;
* `senaobicho`: executa caso a condição seja falsa;
* `fimtrem`: finaliza uma condição;
* `repete`: repete um bloco de comandos;
* `acaboupo`: finaliza uma repetição;
* `verdadeiro`: valor lógico verdadeiro;
* `falso`: valor lógico falso;
* `e`: operador lógico E;
* `ou`: operador lógico OU;
* `nao`: operador lógico de negação.

---

## Como o Projeto Funciona

O interpretador recebe um arquivo `.mmr`, lê o conteúdo linha por linha e identifica os comandos da linguagem.

Depois disso, ele executa as instruções, como criar variáveis, mostrar mensagens, verificar condições e repetir blocos de código.

Caso exista algum erro, o programa exibe uma mensagem informando o problema encontrado.

---

## Exemplo de Código

```mmr
guarda nome = "Maria";
guarda idade = 20;
guarda nota = 8;

falaai "Sistema MMR iniciado";
falaai nome;

eai idade >= 18
    falaai "Usuário maior de idade";
senaobicho
    falaai "Usuário menor de idade";
fimtrem

eai nota >= 7
    falaai "Aluno aprovado";
senaobicho
    falaai "Aluno em recuperação";
fimtrem

repete 3
    falaai "Finalizando processamento...";
acaboupo
```

---

## Saída Esperada

```txt
Sistema MMR iniciado
Maria
Usuário maior de idade
Aluno aprovado
Finalizando processamento...
Finalizando processamento...
Finalizando processamento...
```

---

## Estrutura do Projeto

```txt
compilador-av2/
├── main.py
├── testes/
│   ├── programa1.mmr
│   ├── programa2.mmr
│   ├── programa3.mmr
│   ├── programa4.mmr
│   └── programa5.mmr
├── relatorio/
│   └── main.tex
├── README.md
└── .gitignore
```

---

## Como Rodar o Interpretador

Clone o repositório:

```bash
git clone https://github.com/JoaoLucasVital/mmrlang
```

Entre na pasta do projeto:

```bash
cd compilador-av2
```

Execute o interpretador:

```bash
python main.py
```

Depois informe o caminho de um arquivo `.mmr`:

```txt
testes/programa1.mmr
```

---

## Programas de Teste

Os testes ficam na pasta `testes`.

* `programa1.mmr`: variáveis e saída de dados;
* `programa2.mmr`: operações matemáticas;
* `programa3.mmr`: estrutura condicional;
* `programa4.mmr`: estrutura de repetição;
* `programa5.mmr`: programa completo.

---

## Relatório em LaTeX

O relatório do projeto foi feito em **LaTeX**.

Ferramentas utilizadas:

* **MiKTeX**: compilador LaTeX;
* **Texmaker**: editor usado para escrever e compilar o relatório.

O arquivo principal está em:

```txt
relatorio/main.tex
```

Para gerar o PDF, abra o arquivo no Texmaker, selecione **PDFLaTeX** e compile.

---

## Versionamento

O projeto deve ser entregue pelo **GitHub**, com colaboração entre os integrantes.

Exemplos de commits:

```bash
git add .
git commit -m "feat: adiciona interpretador da MMRLang"
git commit -m "test: adiciona programas de teste"
git commit -m "docs: adiciona relatorio em LaTeX"
git push
```

---

## Tratamento de Erros

O interpretador trata erros como:

* Arquivo não encontrado;
* Extensão inválida;
* Comando desconhecido;
* Variável não declarada;
* Nome de variável inválido;
* Condição sem fechamento;
* Repetição sem fechamento;
* Divisão por zero;
* Operador não suportado.

Exemplo:

```mmr
falaai nome;
```

Saída esperada caso a variável não exista:

```txt
Erro MMR:
[Linha 1] A variável 'nome' não foi declarada.
```

---

## Uso de Inteligência Artificial

A inteligência artificial foi utilizada como ferramenta de apoio para:

* Organizar o projeto;
* Criar a sintaxe da linguagem;
* Melhorar o interpretador;
* Criar testes;
* Escrever o README;
* Produzir o relatório em LaTeX.

As sugestões foram analisadas, testadas e adaptadas pela equipe.

---

## Integrantes

| Nome                           | Matrícula | GitHub                            |
| ------------------------------ | --------- | --------------------------------- |
| Adriano Mikhael M L Cavalcante | 01605455  | https://github.com/AdrianoMikhael |
| João Lucas Vital               | 01624753  | https://github.com/JoaoLucasVital |
| Lucas Soares Silva             | 01631745  | https://github.com/lqnhs1         |

---

## Conclusão

A MMRLang demonstra, de forma simples, como uma linguagem pode ser lida, interpretada e executada.

O projeto aplica conceitos de compiladores, como variáveis, condições, repetições, tratamento de erros, documentação técnica e versionamento no GitHub.
