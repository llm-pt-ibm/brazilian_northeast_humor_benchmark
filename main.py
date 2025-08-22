from experiment_runner import ExperimentRunner
from evaluator import Evaluator

exp_runner = ExperimentRunner()

# Zero-shot 
exp_runner.execute(prompting_strategy = 'zero_shot')

# Few-shot
#exp_runner.execute(prompting_strategy = 'few-shot')

evaluator = Evaluator()
evaluator.evaluate_models_predictions()