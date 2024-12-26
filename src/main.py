import optuna
from optuna.samplers import NSGAIISampler

import buns
import fillings

BUNS = buns.BUNS.keys()
FILLINGS = fillings.FILLINGS.keys()

from calculate_score import evaluate_cost, evaluate_uniqueness


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
    study = optuna.create_study(
        directions=["minimize", "maximize"], sampler=NSGAIISampler()
    )
    study.optimize(objective, n_trials=100)

    pareto_trials = study.best_trials

    print("Pareto Front Trials:")
    for t in pareto_trials:
        print(f"  Scores={t.values}, Params={t.params}")


if __name__ == "__main__":
    main()
