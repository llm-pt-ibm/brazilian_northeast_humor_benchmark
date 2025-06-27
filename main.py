from experiment_runner import ExperimentRunner
from evaluator import Evaluator

exp_runner = ExperimentRunner()
exp_runner.execute()

evaluator = Evaluator()
evaluator.evaluate_models_predictions()