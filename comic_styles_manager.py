class ComicStylesManager():

    def __init__(self):
        pass

    def get_styles_definitions(self):
        styles_definitions = {
            "fun": "O estilo cômico da diversão é caracterizado pela intenção de propagar um estado de ânimo positivo e fortalecer os laços de camaradagem. Indivíduos que manifestam este estilo são tipicamente percebidos como sociáveis, joviais e agradáveis. No contexto interpessoal, podem empregar provocações leves e brincalhonas com aqueles que possuem maior familiaridade com esse tipo de interação. A autoimagem de pessoas com alta pontuação em diversão frequentemente inclui traços de serem joviais, gostarem de pregar peças inofensivas e de agir de maneira palhaça.",
            "humor": "O humor benevolente centra-se na capacidade de suscitar simpatia e compreensão perante as incongruências inerentes à existência, as falhas do mundo e as imperfeições humanas, incluindo as próprias. Pessoas com este estilo demonstram ser observadoras perspicazes das fragilidades humanas, contudo, abordam-nas com benevolência e tolerância, muitas vezes incluindo-se em suas observações. Há uma compreensão profunda da condição humana, compartilhada de forma jovial e reflexiva. O humor, nesta acepção, reflete uma postura afetuosa e compreensiva para com os outros, aceitando suas limitações. A perspectiva de quem utiliza este estilo reconhece a imperfeição do mundo, mas permite encarar as adversidades com leveza e até mesmo divertimento.",
            "nonsense": "O absurdo é definido como uma forma de diversão intelectual, lúdica e essencialmente alegre, cujo objetivo reside em expor o caráter ridículo da lógica estrita, embora desprovido de um propósito específico. Indivíduos que apreciam o nonsense descrevem-se como brincalhões e bem-humorados. Caracteriza-se por um jogo mental criativo, especialmente no domínio da linguagem, explorando a fronteira entre o sentido e o sem-sentido. Para estes indivíduos, a resolução de incongruências não é primordial; pelo contrário, quanto mais bizarra e ilógica a situação, maior o potencial de divertimento. Este estilo manifesta-se na criação de um universo invertido, na exploração das imperfeições da linguagem e na apreciação de narrativas fantásticas e incomuns.",
            "wit": "A engenhosidade busca iluminar de maneira súbita e perspicaz, frequentemente através de uma reviravolta inesperada que combina ideias de forma original e imediata. A pessoa engenhosa demonstra habilidade no manejo de palavras e pensamentos, podendo, por vezes, apresentar-se insensível ou maliciosa para maximizar o efeito cômico, direcionando-se a um público que aprecie a agudeza e a brevidade. A produção de engenhosidade exige rapidez na leitura de situações e precisão em apontar aspectos não óbvios de maneira engraçada. Indivíduos com esse estilo surpreendem com comentários espirituosos e julgamentos pertinentes, estabelecendo conexões inesperadas entre conceitos. Personalidades com traços de engenhosidade podem ser percebidas como tensas e vaidosas, valorizando um interlocutor capaz de apreciar a sua sagacidade.",
            "irony": "A ironia, no contexto interacional, visa a construção de um sentimento compartilhado de superioridade em relação a terceiros, através da expressão de ideias de forma contrária ao seu significado literal. Diferentemente da mentira, a ironia pressupõe que o interlocutor inteligente será capaz de decifrar a intenção subjacente à mensagem. Indivíduos irônicos buscam a cumplicidade de mentes consideradas perspicazes, simultaneamente ridicularizando aqueles que não captam a sutileza da comunicação. A ironia serve como um mecanismo para distinguir os iniciados dos não iniciados. Observadores externos podem interpretar o uso frequente de ironia como arrogância, superioridade e uma tendência à crítica negativa.",
            "satire": "A sátira, também referida como humor corretivo, compartilha com o sarcasmo e o cinismo a identificação de falhas e uma vertente agressiva. Contudo, distingue-se pela intenção de promover a melhoria e a correção. O satirista busca depreciar o que é considerado inadequado ou insensato, com o objetivo de aperfeiçoar o mundo e os seus semelhantes, tomando um padrão ético como referência para avaliar a realidade. Embora o satirista possa ser crítico, negativo e tenso, a sua crítica fundamenta-se em princípios morais, visando aprimorar a conduta e as mentalidades sem prejudicar as relações interpessoais. A sátira apela a uma mentalidade crítica e é motivada por uma intenção de bondade.",
            "sarcasm": "O sarcasmo tem como propósito primordial infligir dano emocional ao outro. A pessoa sarcástica é caracterizada por traços de hostilidade e desprezo, utilizando a exposição impiedosa de imperfeições e falhas percebidas num mundo considerado corrupto. O público ideal para a manifestação do sarcasmo frequentemente consiste em indivíduos em posição de subordinação ou dependência. Quem pontua alto em sarcasmo tende a se ver como crítico e mordaz ao denunciar o que considera corrupção e maldade, demonstrando propensão ao escárnio e ao prazer pelo infortúnio.",
            "cynicism": "O cinismo direciona-se à desvalorização de valores amplamente aceitos pela sociedade. Indivíduos cínicos exibem uma atitude pessimista e destrutiva, empregando o desencanto e a zombaria para evidenciar as fragilidades do mundo. Embora não se caracterizem pela ausência total de valores morais, os cínicos desprezam normas e conceitos morais convencionais, considerando-os absurdos."
            }
        
        return styles_definitions
    
    def get_comic_styles(self):
        all_comic_styles = self.get_styles_definitions().keys()
        return all_comic_styles
    
    def get_comic_style_pt_br_translation(self, comic_style):
        styles_translations = {
            "fun": "diversão",
            "humor": "humor benevolente",
            "nonsense": "absurdo",
            "wit": "sagacidade",
            "irony": "ironia",
            "satire": "sátira",
            "sarcasm": "sarcasmo",
            "cynicism": "cinismo"
            }
        
        return styles_translations[comic_style]