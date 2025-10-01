Prompts - HuNeBR

### 1. Identificação de Punchlines (Punchlines Identification)

Descrição: Identificar as punchlines de um texto humorístico.
Definição de punchline: É a parte da piada que provoca o efeito cômico, sendo responsável pela resolução da piada. Ocorre quando o receptor faz uma conexão inesperada entre partes do texto, gerando o riso.

Prompt (zero-shot):
```
Dado o seguinte texto humorístico, identifique todas as punchlines presentes.
Definição de punchline: A punchline é a parte de uma piada que provoca o efeito cômico, sendo responsável pela resolução da piada.
Identifique apenas as partes que representam a resolução cômica (punchlines).
Cada punchline deve ser registrada como um item em uma lista.
Não adicione explicações ou trechos irrelevantes.
Forneça a resposta no seguinte formato de lista:
["Primeira punchline identificada",
"Segunda punchline identificada",
"...outras punchlines, se existirem..."]
Texto humorístico: {humorous_text}
Responda apenas no formato de lista.
```

Prompt (few-shot):
```
Dado o seguinte texto humorístico, identifique todas as punchlines presentes.
Definição de punchline: A punchline é a parte de uma piada que provoca o efeito cômico, sendo responsável pela resolução da piada.
Identifique apenas as partes que representam a resolução cômica (punchlines).
Cada punchline deve ser registrada como um item em uma lista.
Não adicione explicações ou trechos irrelevantes.

Forneça a resposta no seguinte formato de lista:
["Primeira punchline identificada",
"Segunda punchline identificada",
"...outras punchlines, se existirem..."]

Aqui estão alguns exemplos de entrada e saída:

Entrada 1: {humor_example_1}  
Saída 1: ["example 1 punchline"]

Entrada 2: {humor_example_2}  
Saída 2: ["example 2 punchline"]

Agora analise o seguinte caso:

Texto humorístico: {humorous_text}

Saída:
```

### 2. Identificação de Estilos Cômicos (Comic Styles Classification)

Descrição: Avaliar se um texto possui determinado estilo cômico.

Prompt (zero-shot)
```
Dado o seguinte texto humorístico, avalie se ele contém o estilo cômico "{style_name}".
Definição de {style_name}: {style_definition}
Responda com 1 se sim, ou 0 se não.
Texto humorístico: {humorous_text}
Não inclua explicações ou qualquer outro texto além do número.
```

Prompt (few-shot)
```
Dado o seguinte texto humorístico, avalie se ele contém o estilo cômico "{style_name}".
Definição de {style_name}: {style_definition}
Responda com 1 se sim, ou 0 se não.
Não inclua explicações ou qualquer outro texto além do número.

Aqui estão alguns exemplos de entrada e saída:

Entrada 1: {humor_example_1}  
Saída 1: {style_example_1}

Entrada 2: {humor_example_2}  
Saída 2: {style_example_2}

Agora analise o seguinte caso:

Texto humorístico: {humorous_text}

Saída:
```

### 3. Explicação do Texto Humorístico (Humor reasoning)

Descrição: Explicar os elementos que tornam um texto humorístico engraçado.

Prompt (zero-shot)
```
Explique o motivo do humor presente no seguinte texto. Aponte os elementos que contribuem para seu efeito cômico.
Texto humorístico: {humorous_text}
Responda apenas com a explicação, sem detalhes adicionais.
```

Prompt (few-shot)
```
Explique o motivo do humor presente no seguinte texto humorístico. Aponte os elementos que contribuem para seu efeito cômico.
Responda apenas com a explicação, sem detalhes adicionais.

Aqui estão alguns exemplos de entrada e saída:

Entrada 1: {humor_example_1}  
Saída 1: {explication_example_1}

Entrada 2: {humor_example_2}  
Saída 2: {explication_example_2}

Agora analise o seguinte caso:

Texto humorístico: {humorous_text}

Saída:
```

### 4. Avaliação de Nível de Concordância (Agreement Level with Judge Model)

Descrição: Avaliar se uma explicação de modelo está de acordo com uma explicação anotada.

```
Você é um especialista em análise textual com experiência em comparar explicações conceituais.

Explicação 1:  
{annotated_explanation}

Explicação 2:  
{model_explanation}

Sua tarefa é avaliar se a Explicação 2 demonstra compreensão correta do conteúdo, com base na Explicação 1.

Use a escala de 1 a 5:
1 - Totalmente discordante
2 - Parcialmente discordante
3 - Neutra / Mista
4 - Parcialmente concordante
5 - Totalmente concordante

Formato obrigatório da resposta (JSON):
{
  "nivel_concordancia": "<number between 1 and 5>",
  "justificativa": "<explanation about the evaluation>"
}

Responda apenas com o JSON, sem detalhes adicionais.
```