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
        # TO-DO retornar dicionário com todos os prompts de uma vez
        styles_definitions = self.comic_styles_manager.get_styles_definitions()
        for comic_style, style_definition in styles_definitions.items():
            comic_style_prompt = f'''Dado o seguinte texto humorístico, avalie se ele contém o estilo cômico ”{style_definition}”.
            Definição de {comic_style}: {style_definition}
            Responda com 1 se sim, ou 0 se não.
            Texto: {humorous_text}
            Não inclua explicações ou qualquer outro texto além do número.
            '''

            yield comic_style_prompt
    
    def get_text_explanation_prompt(self, humorous_text):
        text_explanation_prompt = f'''Explique o motivo do humor presente no seguinte texto. Aponte os elementos que contribuem para seu efeito cômico.
        Texto: {humorous_text}
        Responda apenas com a explicação, sem detalhes adicionais.
        '''

        return text_explanation_prompt
