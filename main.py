# ============================================================
# Interpretador da linguagem MMRLang
# Projeto AV2 - Compiladores
# ============================================================

import ast
import operator
from pathlib import Path


class ErroMMR(Exception):
    """Erro personalizado da linguagem MMRLang."""

    def __init__(self, mensagem, linha=None):
        self.mensagem = mensagem
        self.linha = linha

        if linha is not None:
            super().__init__(f"[Linha {linha}] {mensagem}")
        else:
            super().__init__(mensagem)


class InterpretadorMMR:
    def __init__(self):
        self.variaveis = {}

        self.operadores_binarios = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
        }

        self.operadores_comparacao = {
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
            ast.Gt: operator.gt,
            ast.GtE: operator.ge,
            ast.Lt: operator.lt,
            ast.LtE: operator.le,
        }

    # ------------------------------------------------------------
    # Limpeza de código
    # ------------------------------------------------------------

    def limpar_linha(self, linha):
        """
        Remove espaços extras, comentários e ponto e vírgula final.
        """

        linha = linha.strip()

        if "//" in linha:
            linha = linha.split("//", 1)[0].strip()

        if "#" in linha:
            linha = linha.split("#", 1)[0].strip()

        if linha.endswith(";"):
            linha = linha[:-1].strip()

        return linha

    # ------------------------------------------------------------
    # Avaliação de expressões
    # ------------------------------------------------------------

    def avaliar_expressao(self, expressao, numero_linha=None):
        """
        Avalia números, textos, variáveis e expressões matemáticas.
        """

        expressao = expressao.strip()

        if not expressao:
            raise ErroMMR("Expressão vazia.", numero_linha)

        try:
            arvore = ast.parse(expressao, mode="eval")
            return self._avaliar_no(arvore.body, numero_linha)

        except ErroMMR:
            raise

        except Exception:
            raise ErroMMR(
                f"Não foi possível entender a expressão: {expressao}",
                numero_linha
            )

    def _avaliar_no(self, no, numero_linha=None):
        """
        Avalia os nós da árvore sintática com segurança.
        """

        if isinstance(no, ast.Constant):
            return no.value

        if isinstance(no, ast.Name):
            if no.id in self.variaveis:
                return self.variaveis[no.id]

            if no.id == "verdadeiro":
                return True

            if no.id == "falso":
                return False

            raise ErroMMR(
                f"A variável '{no.id}' não foi declarada.",
                numero_linha
            )

        if isinstance(no, ast.BinOp):
            tipo_operador = type(no.op)

            if tipo_operador not in self.operadores_binarios:
                raise ErroMMR("Operador matemático não suportado.", numero_linha)

            esquerda = self._avaliar_no(no.left, numero_linha)
            direita = self._avaliar_no(no.right, numero_linha)

            return self.operadores_binarios[tipo_operador](esquerda, direita)

        if isinstance(no, ast.Compare):
            esquerda = self._avaliar_no(no.left, numero_linha)

            for operador_ast, comparador in zip(no.ops, no.comparators):
                tipo_operador = type(operador_ast)

                if tipo_operador not in self.operadores_comparacao:
                    raise ErroMMR("Operador de comparação não suportado.", numero_linha)

                direita = self._avaliar_no(comparador, numero_linha)

                resultado = self.operadores_comparacao[tipo_operador](
                    esquerda,
                    direita
                )

                if not resultado:
                    return False

                esquerda = direita

            return True

        if isinstance(no, ast.BoolOp):
            valores = [self._avaliar_no(valor, numero_linha) for valor in no.values]

            if isinstance(no.op, ast.And):
                return all(valores)

            if isinstance(no.op, ast.Or):
                return any(valores)

            raise ErroMMR("Operador lógico não suportado.", numero_linha)

        if isinstance(no, ast.UnaryOp):
            valor = self._avaliar_no(no.operand, numero_linha)

            if isinstance(no.op, ast.Not):
                return not valor

            if isinstance(no.op, ast.USub):
                return -valor

            raise ErroMMR("Operador unário não suportado.", numero_linha)

        raise ErroMMR("Expressão inválida para a MMRLang.", numero_linha)

    def preparar_condicao(self, condicao):
        """
        Converte operadores lógicos da MMRLang para Python internamente.
        """

        condicao = condicao.replace(" e ", " and ")
        condicao = condicao.replace(" ou ", " or ")
        condicao = condicao.replace(" nao ", " not ")

        return condicao

    # ------------------------------------------------------------
    # Execução de comandos simples
    # ------------------------------------------------------------

    def executar_linha(self, linha, numero_linha=None):
        linha = self.limpar_linha(linha)

        if not linha:
            return

        if linha.startswith("falaai"):
            self.comando_falaai(linha, numero_linha)

        elif linha.startswith("guarda"):
            self.comando_guarda(linha, numero_linha)

        else:
            raise ErroMMR(
                f"Comando desconhecido: {linha}",
                numero_linha
            )

    def comando_falaai(self, linha, numero_linha=None):
        """
        Comando de saída da MMRLang.

        Exemplo:
        falaai "Olá, mundo";
        falaai nome;
        falaai idade + 2;
        """

        conteudo = linha.replace("falaai", "", 1).strip()

        if not conteudo:
            raise ErroMMR(
                "O comando 'falaai' precisa receber algum valor.",
                numero_linha
            )

        valor = self.avaliar_expressao(conteudo, numero_linha)
        print(valor)

    def comando_guarda(self, linha, numero_linha=None):
        """
        Comando de criação/alteração de variável.

        Exemplo:
        guarda idade = 18;
        guarda nome = "Maria";
        guarda total = 10 + 5;
        """

        comando = linha.replace("guarda", "", 1).strip()

        if "=" not in comando:
            raise ErroMMR(
                "O comando 'guarda' precisa usar '='.",
                numero_linha
            )

        nome, expressao = comando.split("=", 1)

        nome = nome.strip()
        expressao = expressao.strip()

        if not nome.isidentifier():
            raise ErroMMR(
                f"Nome de variável inválido: {nome}",
                numero_linha
            )

        valor = self.avaliar_expressao(expressao, numero_linha)
        self.variaveis[nome] = valor

    # ------------------------------------------------------------
    # Execução de blocos
    # ------------------------------------------------------------

    def executar_bloco(self, bloco):
        """
        Executa uma lista de linhas do programa.
        """

        i = 0

        while i < len(bloco):
            linha_original, numero_linha = bloco[i]
            linha = self.limpar_linha(linha_original)

            if not linha:
                i += 1
                continue

            if linha.startswith("eai"):
                i = self.executar_if(bloco, i)

            elif linha.startswith("repete"):
                i = self.executar_repete(bloco, i)

            elif linha in ("senaobicho", "fimtrem", "acaboupo"):
                raise ErroMMR(
                    f"'{linha}' apareceu fora de um bloco válido.",
                    numero_linha
                )

            else:
                self.executar_linha(linha, numero_linha)

            i += 1

    def executar_if(self, bloco, indice):
        """
        Executa estrutura condicional.

        Exemplo:
        eai idade >= 18
            falaai "Maior de idade";
        senaobicho
            falaai "Menor de idade";
        fimtrem
        """

        linha_original, numero_linha = bloco[indice]
        linha = self.limpar_linha(linha_original)

        condicao = linha.replace("eai", "", 1).strip()

        if not condicao:
            raise ErroMMR(
                "A estrutura 'eai' precisa de uma condição.",
                numero_linha
            )

        bloco_if = []
        bloco_else = []
        dentro_else = False

        indice += 1

        while indice < len(bloco):
            linha_atual, linha_atual_numero = bloco[indice]
            limpa = self.limpar_linha(linha_atual)

            if limpa == "senaobicho":
                dentro_else = True
                indice += 1
                continue

            if limpa == "fimtrem":
                condicao_python = self.preparar_condicao(condicao)
                resultado = self.avaliar_expressao(condicao_python, numero_linha)

                if resultado:
                    self.executar_bloco(bloco_if)
                else:
                    self.executar_bloco(bloco_else)

                return indice

            if dentro_else:
                bloco_else.append((linha_atual, linha_atual_numero))
            else:
                bloco_if.append((linha_atual, linha_atual_numero))

            indice += 1

        raise ErroMMR(
            "Bloco 'eai' não foi finalizado com 'fimtrem'.",
            numero_linha
        )

    def executar_repete(self, bloco, indice):
        """
        Executa repetição simples.

        Exemplo:
        repete 3
            falaai "MMR em execução";
        acaboupo
        """

        linha_original, numero_linha = bloco[indice]
        linha = self.limpar_linha(linha_original)

        quantidade_texto = linha.replace("repete", "", 1).strip()

        if not quantidade_texto:
            raise ErroMMR(
                "O comando 'repete' precisa de uma quantidade.",
                numero_linha
            )

        quantidade = self.avaliar_expressao(quantidade_texto, numero_linha)

        if not isinstance(quantidade, int):
            raise ErroMMR(
                "A quantidade do 'repete' precisa ser um número inteiro.",
                numero_linha
            )

        if quantidade < 0:
            raise ErroMMR(
                "A quantidade do 'repete' não pode ser negativa.",
                numero_linha
            )

        bloco_repeticao = []

        indice += 1

        while indice < len(bloco):
            linha_atual, linha_atual_numero = bloco[indice]
            limpa = self.limpar_linha(linha_atual)

            if limpa == "acaboupo":
                for _ in range(quantidade):
                    self.executar_bloco(bloco_repeticao)

                return indice

            bloco_repeticao.append((linha_atual, linha_atual_numero))
            indice += 1

        raise ErroMMR(
            "Bloco 'repete' não foi finalizado com 'acaboupo'.",
            numero_linha
        )

    # ------------------------------------------------------------
    # Interpretação do arquivo
    # ------------------------------------------------------------

    def interpretar(self, arquivo):
        caminho = Path(arquivo)

        if not caminho.exists():
            raise ErroMMR(f"O arquivo '{arquivo}' não foi encontrado.")

        if caminho.suffix != ".mmr":
            raise ErroMMR(
                "A MMRLang utiliza arquivos com a extensão '.mmr'."
            )

        with open(caminho, "r", encoding="utf-8") as f:
            linhas = [
                (linha.rstrip(), numero)
                for numero, linha in enumerate(f, start=1)
            ]

        print("====================================")
        print(" Interpretador MMRLang iniciado")
        print("====================================\n")

        self.executar_bloco(linhas)

        print("\n====================================")
        print(" Programa MMR finalizado com sucesso")
        print("====================================")


def main():
    interpretador = InterpretadorMMR()

    arquivo = input("Arquivo MMR: ").strip()

    try:
        interpretador.interpretar(arquivo)

    except ErroMMR as erro:
        print("\nErro MMR:")
        print(erro)

    except ZeroDivisionError:
        print("\nErro MMR:")
        print("Divisão por zero não é permitida.")

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")

    except Exception as erro:
        print("\nErro inesperado:")
        print(erro)


if __name__ == "__main__":
    main()