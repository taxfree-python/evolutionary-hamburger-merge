import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_all_trials_with_plotly(study):
    # 全ての試行のスコアを取得
    all_trials_costs = [
        trial.values[0] for trial in study.trials if trial.values is not None
    ]
    all_trials_uniqueness = [
        trial.values[1] for trial in study.trials if trial.values is not None
    ]

    # パレートフロントのスコアを取得
    pareto_trials = study.best_trials
    pareto_costs = [t.values[0] for t in pareto_trials]
    pareto_uniqueness = [t.values[1] for t in pareto_trials]

    # 全ての試行をプロット
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=all_trials_costs,
            y=all_trials_uniqueness,
            mode="markers",
            marker=dict(size=6, color="blue", opacity=0.6),
            name="All Trials",
        )
    )

    # パレートフロントを別途プロット
    fig.add_trace(
        go.Scatter(
            x=pareto_costs,
            y=pareto_uniqueness,
            mode="markers",
            marker=dict(size=8, color="red", opacity=1),
            name="Pareto Front",
        )
    )

    # プロットの装飾
    fig.update_layout(
        title="All Trials and Pareto Front",
        xaxis_title="コスト（味のスコア）",
        yaxis_title="独自性スコア",
        font=dict(
            family="Noto Sans JP, Arial, sans-serif",  # 日本語対応フォント
            size=14,
        ),
        legend=dict(title="Legend"),
    )

    # プロット表示
    fig.show()


def plot_trials_animation(study, show_final=True, speed=50):
    """
    Plot trials with an animation.

    Args:
        study: The Optuna study object.
        show_final (bool): If True, display all trials as the initial state.
        speed (int): Duration (in ms) between frames. Lower is faster.
    """
    # 全ての試行を取得
    all_trials = [
        (
            trial.number,
            trial.values[0],
            trial.values[1],
        )  # (trial number, cost, uniqueness)
        for trial in study.trials
        if trial.values is not None
    ]

    # フレームごとにプロットを作成
    frames = []
    for i in range(1, len(all_trials) + 1):
        frame_data = all_trials[:i]  # 試行を1つずつ追加していく
        frame = go.Frame(
            data=[
                go.Scatter(
                    x=[t[1] for t in frame_data],  # cost
                    y=[t[2] for t in frame_data],  # uniqueness
                    mode="markers",
                    marker=dict(size=10, color="blue"),
                )
            ],
            name=f"Frame {i}",
        )
        frames.append(frame)

    # 最初の状態を切り替える
    if show_final:
        initial_x = [t[1] for t in all_trials]
        initial_y = [t[2] for t in all_trials]
        initial_opacity = 0.3  # 最初のプロットを薄く表示
    else:
        initial_x = []
        initial_y = []
        initial_opacity = 1.0  # 最初はまっさらな状態

    # アニメーションプロット
    fig = go.Figure(
        data=[
            go.Scatter(
                x=initial_x,
                y=initial_y,
                mode="markers",
                marker=dict(size=10, color="blue", opacity=initial_opacity),
                name="All Trials (Initial)",
            )
        ],
        layout=go.Layout(
            title="Trials Animation",
            xaxis=dict(title="Cost"),
            yaxis=dict(title="Uniqueness"),
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[
                                None,
                                dict(
                                    frame=dict(duration=speed, redraw=True),  # 再生速度
                                    fromcurrent=True,
                                ),
                            ],
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[
                                [None],
                                dict(
                                    frame=dict(duration=0, redraw=False),
                                    mode="immediate",
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        frames=frames,
    )

    fig.show()


def plot_and_save_with_plt(study, output_path="pareto_results_temp.png"):
    # 全ての試行のスコアを取得
    all_trials = [
        (
            trial.number,
            trial.values[0],
            trial.values[1],
        )  # (trial number, cost, uniqueness)
        for trial in study.trials
        if trial.values is not None
    ]

    # パレートフロントのスコアを取得
    pareto_trials = study.best_trials
    pareto_costs = [t.values[0] for t in pareto_trials]
    pareto_uniqueness = [t.values[1] for t in pareto_trials]

    # プロットを作成
    plt.figure(figsize=(8, 6))

    # 全ての試行をプロット
    all_costs = [t[1] for t in all_trials]  # コスト
    all_uniqueness = [t[2] for t in all_trials]  # ユニークさ
    plt.scatter(all_costs, all_uniqueness, c="blue", label="All Trials", alpha=0.6)

    # パレートフロントを別途プロット
    plt.scatter(
        pareto_costs, pareto_uniqueness, c="red", label="Pareto Front", alpha=1.0
    )

    # プロットの装飾
    plt.title("All Trials and Pareto Front")
    plt.xlabel("Total Cost")
    plt.ylabel("Uniqueness")
    plt.legend()
    plt.grid(True)

    # PNG形式で保存
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Plot saved as {output_path}")

    # プロットを閉じる
    plt.close()
