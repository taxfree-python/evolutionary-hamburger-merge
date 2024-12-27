import optuna
from optuna.samplers import NSGAIISampler

import buns
import fillings

BUNS = buns.BUNS.keys()
FILLINGS = fillings.FILLINGS.keys()

from calculate_score import evaluate_cost, evaluate_uniqueness
from visualize_result import (
    plot_and_save_with_plt,
)


def objective(trial):
    # ハンバーガー全体の長さ
    n_items = trial.suggest_int("n_items", 3, 10)

    # バンズ
    first_bun = trial.suggest_categorical("bun_first", BUNS)
    last_bun = trial.suggest_categorical("bun_last", BUNS)

    # 中身
    fillings_count = n_items - 2
    filling_choices = [
        trial.suggest_categorical(f"filling_{i}", FILLINGS)
        for i in range(fillings_count)
    ]

    # ハンバーガーを作成
    hamburger_sequence = [first_bun] + filling_choices + [last_bun]

    taste_score = evaluate_cost(hamburger_sequence)
    uniqueness_score = evaluate_uniqueness(hamburger_sequence)

    return taste_score, uniqueness_score


def main():
    seed = 42
    sampler = NSGAIISampler(seed=seed)
    study = optuna.create_study(directions=["minimize", "maximize"], sampler=sampler)
    study.optimize(objective, n_trials=1000)

    pareto_trials = study.best_trials

    sorted_pareto_trials = sorted(
        pareto_trials,
        key=lambda t: (t.values[1], t.values[0]),
    )
    unique_threshold = 13.4
    print("Pareto Front Trials:")
    for t in sorted_pareto_trials:
        print(f"  Scores={t.values}, Params={t.params}") if t.values[
            1
        ] > unique_threshold else None

    print("=" * 10)
    for t in sorted_pareto_trials:
        print(f"Recipes={t.params}") if t.values[1] > unique_threshold else None
    plot_and_save_with_plt(study)


if __name__ == "__main__":
    main()
