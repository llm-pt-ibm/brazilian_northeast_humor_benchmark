import argparse
from string_utils import StringUtils
from experiment_runner import ExperimentRunner

ALL_TASKS = ["punchlines", "comic_styles", "texts_explanation"]
ALL_SCENARIOS = ["zero-shot", "few-shot"]

def main():
    parser = argparse.ArgumentParser(
        description="Run benchmarks on models with different scenarios and tasks."
    )
    parser.add_argument(
        "--scenario",
        nargs="*",
        default=ALL_SCENARIOS,
        help="Scenario(s) to run. Options: zero-shot, few-shot. Default: both."
    )
    parser.add_argument(
        "--tasks",
        nargs="*",
        default=ALL_TASKS,
        help="Task(s) to run. Options: punchlines, comic_styles, texts_explanation. Default: all."
    )
    parser.add_argument(
        "--evaluation",
        type=StringUtils.str2bool,
        default=True,
        help="Whether to run global evaluation after tasks. Default: true. Options: true/false."
    )

    args = parser.parse_args()

    scenarios_to_run = ALL_SCENARIOS if "all" in args.scenario else args.scenario
    tasks_to_run = ALL_TASKS if "all" in args.tasks else args.tasks

    invalid_scenarios = [s for s in scenarios_to_run if s not in ALL_SCENARIOS]
    if invalid_scenarios:
        raise ValueError(f"Invalid scenario(s): {invalid_scenarios}")

    invalid_tasks = [t for t in tasks_to_run if t not in ALL_TASKS]
    if invalid_tasks:
        raise ValueError(f"Invalid task(s): {invalid_tasks}")

    exp_runner = ExperimentRunner()

    for scenario in scenarios_to_run:
        print(f"\n=== Running scenario: {scenario} ===\n")
        exp_runner.execute(prompting_strategy=scenario, tasks=tasks_to_run)

    if args.evaluation:
        from evaluator import Evaluator
        evaluator = Evaluator()
        evaluator.evaluate_all_scenarios()


if __name__ == "__main__":
    main()
