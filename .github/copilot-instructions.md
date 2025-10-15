# Copilot Instructions for HuNeBR (Brazilian Northeast Humor Benchmark)

## Visão Geral
Este projeto avalia LLMs na compreensão do humor nordestino brasileiro, com três tarefas principais:
- **Identificação de Punchline**: Extrair segmentos que resolvem a incongruência e geram o efeito cômico.
- **Classificação de Estilo Cômico**: Detectar presença de até 8 estilos (fun, benevolent humor, nonsense, wit, irony, sarcasm, satire, cynicism).
- **Explicação do Humor**: Gerar explicação concisa sobre o mecanismo humorístico do texto.

Cenários de execução:
- **Zero-shot**: Sem exemplos no prompt.
- **Few-shot**: Dois exemplos por estilo (um positivo, um negativo).

## Estrutura e Fluxo
- Scripts principais: `main.py` (orquestra execução), `llm_factory.py` (seleção de modelo), `comic_styles_manager.py`, `dataset_loader.py`, `evaluator.py`, `judge_model.py`.
- Configurações de modelos: `config/models_config.yaml` (preencher credenciais), `config/judge_model_config.yaml` (modelo de julgamento).
- Dados: `data/brazilian_ne_annotated_humorous_texts.csv` (textos anotados).
- Resultados: `predictions/` (por modelo/cenário/tarefa), `evaluation/` (métricas agregadas, individuais, respostas do modelo juiz).
- Notebooks: `results_exploration.ipynb`, `qualitative_exploration.ipynb` (exploração dos resultados).

## Convenções e Padrões
- Resultados persistidos em JSON, organizados por modelo/cenário/tarefa.
- Execução é incremental: recomeça do ponto onde parou se já houver resultados.
- Estilos cômicos são binários e podem coexistir.
- Explicações de humor são avaliadas por modelo juiz via Likert (1–5).
- Métricas específicas por tarefa (ex: Dice para punchlines, F1 para estilos, acordo para explicações).

## Comandos Essenciais
- Instalação: `pip install -r requirements.txt`
- Execução padrão: `python main.py`
- Customização:
  - Sem avaliação: `python main.py --evaluation false`
  - Cenário específico: `python main.py --scenario zero-shot`
  - Tarefa específica: `python main.py --tasks punchlines`
  - Múltiplos cenários/tarefas: `python main.py --scenario zero-shot few-shot --tasks punchlines comic_styles`

## Integrações e Dependências
- Suporte a múltiplos provedores LLM (OpenAI, Google, IBM, etc.) via configuração YAML.
- Avaliação de explicações depende de modelo juiz configurado.
- Dados e resultados organizados para facilitar reuso e análise.

## Exemplos de Padrões
- Para adicionar novo modelo, edite `models_config.yaml` e implemente integração em `llm_factory.py`.
- Para nova métrica, modifique `evaluator.py` e atualize notebooks de exploração.
- Para depuração, verifique persistência em `predictions/` e `evaluation/`.

---

> Atualize este documento conforme novas práticas ou padrões surgirem. Dúvidas ou sugestões? Consulte o README ou peça feedback!
