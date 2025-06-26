from comic_styles_manager import ComicStylesManager

class LLMPromptManager:
    def __init__(self):
        self.comic_styles_manager = ComicStylesManager()

    def get_punchlines_prompt(self, humorous_text):
        punchlines_prompt = f'''Dado o seguinte texto humorístico, identifique todas as punchlines presentes.
Definição de punchline: A punchline é a parte de uma piada que provoca o efeito cômico, sendo responsável pela resolução da piada. Ela ocorre quando o receptor reinterpreta a informação e faz uma conexão inesperada entre as partes do texto, gerando o riso.
Identifique apenas as partes que representam a resolução cômica (punchlines).
Cada punchline deve ser registrada como um item em uma lista.
Não adicione explicações ou trechos irrelevantes.
Forneça a resposta no seguinte formato de lista:
["Primeira punchline identificada",
"Segunda punchline identificada",
"...outras punchlines, se existirem..."]
Texto humorístico: {humorous_text}
Responda apenas no formato de lista.'''
        
        return punchlines_prompt

    def get_comic_styles_prompts(self, humorous_text):
        styles_definitions = self.comic_styles_manager.get_styles_definitions()
        comic_styles_prompts = {
        comic_style:f'''Dado o seguinte texto humorístico, avalie se ele contém o estilo cômico ”{self.comic_styles_manager.get_comic_style_pt_br_translation(comic_style)}”.
Definição de {self.comic_styles_manager.get_comic_style_pt_br_translation(comic_style)}: {style_definition}
Responda com 1 se sim, ou 0 se não.
Texto humorístico: {humorous_text}
Não inclua explicações ou qualquer outro texto além do número.'''
        for comic_style, style_definition in styles_definitions.items()
        }

        return comic_styles_prompts
    
    def get_text_explanation_prompt(self, humorous_text):
        text_explanation_prompt = f'''Explique o motivo do humor presente no seguinte texto. Aponte os elementos que contribuem para seu efeito cômico.
Texto humorístico: {humorous_text}
Responda apenas com a explicação, sem detalhes adicionais.'''

        return text_explanation_prompt

    def get_agreement_level_prompt(self, annotated_explanation, model_explanation):
        agreement_level_prompt = f'''Você é um especialista em análise textual com experiência em comparar explicações conceituais.

Abaixo estão duas explicações sobre o que torna engraçado um texto humorístico:

Explicação 1 (anotação humana):  
{annotated_explanation}

Explicação 2 (modelo):  
{model_explanation}

A Explicação 1 foi escrita por um anotador humano e deve ser considerada uma representação correta do que torna o texto engraçado.  
A Explicação 2 foi gerada por um modelo de linguagem.

Sua tarefa é avaliar se a Explicação 2 demonstra que o modelo compreendeu o que torna o texto engraçado, com base na comparação com a Explicação 1.

Considere:
- Se a Explicação 2 capta os mesmos mecanismos de humor (ainda que com outras palavras).
- Se ela acrescenta apenas detalhes compatíveis, sem distorcer ou introduzir interpretações erradas.
- Se há omissões relevantes ou mal-entendidos.

Use a seguinte escala de concordância com a explicação humana (de 1 a 5):

1. Totalmente discordante – A explicação 2 mostra uma compreensão claramente incorreta ou diferente do que torna o texto engraçado.  
2. Parcialmente discordante – Há elementos corretos, mas com interpretações erradas ou mecanismos diferentes.  
3. Neutra / Mista – A explicação 2 acerta parcialmente, mas falta algo essencial ou inclui ideias irrelevantes.  
4. Parcialmente concordante – A explicação 2 capta o essencial, mas de forma incompleta ou um pouco imprecisa.  
5. Totalmente concordante – A explicação 2 reflete com precisão os mecanismos apontados na explicação 1, mesmo com estilo ou detalhes diferentes.

Formato obrigatório da resposta (JSON):
{
  "nivel_concordancia": <número entre 1 e 5>,
  "justificativa": "<texto explicando a avaliação>"
}

Responda apenas com o JSON, sem detalhes adicionais.
'''
        return agreement_level_prompt