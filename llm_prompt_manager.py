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

Abaixo estão duas explicações sobre um determinado conteúdo:

Explicação 1:  
{annotated_explanation}

Explicação 2:  
{model_explanation}

A Explicação 1 deve ser considerada uma representação correta do conteúdo.

Sua tarefa é avaliar se a Explicação 2 demonstra que houve uma compreensão correta do conteúdo, com base na comparação com a Explicação 1.

Considere:
- Se a Explicação 2 capta os mesmos conceitos centrais (mesmo com palavras diferentes ou com mais detalhes).
- Se ela acrescenta apenas informações compatíveis, sem distorções ou interpretações incorretas.
- Se há omissões importantes ou mal-entendidos.

Use a seguinte escala de concordância com a Explicação 1 (de 1 a 5):

1. Totalmente discordante – A Explicação 2 demonstra uma compreensão incorreta ou muito diferente do conteúdo.  
2. Parcialmente discordante – Há elementos corretos, mas também erros ou desvios conceituais.  
3. Neutra / Mista – A Explicação 2 acerta em parte, mas deixa de abordar algo essencial.  
4. Parcialmente concordante – A Explicação 2 cobre os pontos principais, ainda que com alguma imprecisão.  
5. Totalmente concordante – A Explicação 2 reflete com precisão os conceitos apresentados na Explicação 1, mesmo com variações de estilo ou enfoque.

Formato obrigatório da resposta (JSON):
{{
  "nivel_concordancia": "<número entre 1 e 5>",
  "justificativa": "<texto explicando a avaliação>"
}}

Responda apenas com o JSON, sem detalhes adicionais.

'''

        return agreement_level_prompt