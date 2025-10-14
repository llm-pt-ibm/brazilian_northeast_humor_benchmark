# HuNeBR - Brazilian Northeast Humor Benchmark

HuNeBR is a benchmark to evaluate LLMs regarding the understanding of humor in texts by comedians from Northeastern Brazil.

![Input and output examples.](visualizations/pipeline_example.png)

The HuNeBR benchmark includes three tasks and two prompting scenarios (zero-shot and few-shot). In the zero-shot setup, no examples are provided; in the few-shot setup, two examples are added to the prompt using a fixed seed. For comic style classification, one positive and one negative example are provided per style.

1. <b>Punchline Identification.</b>
The model receives the full humorous text and must return only the punchline segments — the parts that resolve an incongruity and trigger the comic effect — formatted as a structured list without extra commentary.

2. <b>Comic Style Classification.</b>
Based on eight styles (fun, benevolent humor, nonsense, wit, irony, sarcasm, satire, and cynicism), the model is asked whether a specific style is present in the text.
The output is binary: 1 (present) or 0 (absent). Multiple styles may co-occur in a single text.

3. <b>Humor Reasoning (Explanation).</b>
The model must provide a concise explanation of why the text is humorous, identifying the elements that produce the comic effect.
This task assesses the model’s ability to interpret and articulate humor mechanisms rather than merely recognize them.

Below are the instructions for installing the benchmark dependencies, running the predictions and evaluation, unfolding tasks and scenarios.

# Requirements

- Git (https://git-scm.com/downloads)
- Git LFS (https://git-lfs.com/)
- Python 3.10 or higher (https://www.python.org/downloads/)
- pip (https://pip.pypa.io/en/stable/installation/)

With the repository cloned and pip installed, run the command in the terminal:
```sh
pip install -r requirements.txt
```
This will install the benchmark dependencies.

# Running the benchmark

The benchmark offers three main tasks: punchline identification, comic style classification, and humorous text explanation.
Next, we'll walk you through how to configure the models and run the predictions and evaluation.

## Models config

A template file for configuring the models you want to run in the benchmark is at ```config/models_config.yaml```.

The template contains the models we ran in an initial experiment, with the credential fields to be filled in. They are: ``deepseek-r1-0528-qwen3-8b, gemini-2.5-flash, gemma-3-gaia-pt-br-4b-it, gpt-4, granite-3-3-8b-instruct, llama-3-405b-instruct e sabia-3.1.``

Example:

```
models:
  - provider: openai
    model_name: gpt-4
    api_key: 'YOUR_OPENAI_API_KEY'
```

Specifically, the stage of evaluating the task of explaining humorous texts involves a judgment model. This can be configured in the file ```config/judge_model_config.yaml```.

## Tasks and scenarios

Run the benchmark using the ```main.py``` script. By default, it executes all scenarios, all tasks, and evaluation.
It’s important to note that all results are persisted. Thus, if there was a previous execution, the next one will continue exactly from where it stopped.
Below are some examples of how the benchmark can be run via the command line, customizing tasks and scenarios.

Run everything (default)
```sh
python main.py
```

Run everything without evaluation
```sh
python main.py --evaluation false
```

Run only one scenario
```sh
python main.py --scenario zero-shot
```
Run multiple scenarios

```sh
python main.py --scenario zero-shot few-shot
```
Run only one task

```sh
python main.py --tasks punchlines
```
Run multiple tasks

```sh
python main.py --tasks punchlines comic_styles texts_explanation
```
Run specific scenario and tasks together

```sh
python main.py --scenario few-shot --tasks punchlines texts_explanation
```

# Saving results

At the end of each run, prediction results are saved as JSON files in folders specific to each model, scenario, and task. For example:
```sh
predictions/
├── few-shot
│   ├── deepseek-r1-0528-qwen3-8b
│   │   ├── comic_styles_predictions.json
│   │   ├── punchlines_predictions.json
│   │   └── texts_explanations_predictions.json
```

Model evaluation results are also saved in JSON format, but divided into three types: aggregated metrics for each task for each model; individual metrics for each model's response to prompts; and saving of the judge model's evaluation responses, to persist previously generated responses. For example:

```sh
evaluation/
├── few-shot
│   ├── aggregate_metrics.json
│   ├── individual_metrics.json
│   └── texts_explanations_evaluation_results.json
```

