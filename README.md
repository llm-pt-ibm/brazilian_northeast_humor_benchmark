# HuNeBR - Brazilian Northeast Humor Benchmark

Code used to create a benchmark to evaluate LLMs regarding the understanding of humor in texts by comedians from Northeastern Brazil.

Below are the instructions for installing the benchmark dependencies, running the predictions and evaluation, unfolding tasks and scenarios.

# Requirements

- Git (https://git-scm.com/downloads)
- Git LFS (https://git-lfs.com/)
- Python 3.10 ou superior (https://www.python.org/downloads/)
- pip instalado (https://pip.pypa.io/en/stable/installation/)

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

Example:

```
models:
  - provider: openai
    model_name: gpt-4
    api_key: 'YOUR_OPENAI_API_KEY'
```

Specifically, the stage of evaluating the task of explaining humorous texts involves a judgment model. This can be configured in the file```config/judge_model_config.yaml```.

## Tasks and scenarios

Run the benchmark using the ```main.py``` script. By default, it executes all scenarios, all tasks, and evaluation.
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

[...]
