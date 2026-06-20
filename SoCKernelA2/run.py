import os
import time
import numpy as np
from IPython.display import clear_output

from env import ProbeEnv
from agent import ProbeAgent

def render_probe_ascii(h, max_h, v, action, wind, step_count, is_jupyter=False):
    """A high-framerate, pure ASCII terminal renderer."""

    if is_jupyter:
        clear_output(wait=True)
    else:
        os.system('clear' if os.name == 'posix' else 'cls')

    term_lines = 40

    if h > 150.0:
        display_max = max_h
        zoom_str = "[ CAMERA: WIDE ANGLE (1000m) ]"
    else:
        display_max = 150.0
        zoom_str = "[ CAMERA: TARGET APPROACH (150m) ]"

    pos = int((h / display_max) * term_lines)
    pos = max(0, min(term_lines, pos))

    wind_strs = ["Calm", "Gusty", "Adrian Gale"]
    thrust_str = "[####] ON " if action == 1 else "[    ] OFF"

    print(
        f" T+{step_count:03d}s | ALT: {h:6.1f}m | "
        f"VEL: {v:7.1f}m/s | THRUST: {thrust_str} | "
        f"WIND: {wind_strs[wind]}"
    )
    print(f" {zoom_str}")
    print("-" * 75)

    for i in range(term_lines, -1, -1):
        if i == pos:
            if action == 1:
                print("                     /\\")
                print("                    |'|'")
                print("                   /WWW\\")
                print("                    ||  <== spin-drive")
            else:
                print("                     /\\")
                print("                    |'|'")
                print("                   /---\\")
                print("                     *")
        else:
            if i % 10 == 0:
                print(
                    f" {int((i / term_lines) * display_max):4d}m "
                    "+--------------------+"
                )
            else:
                print("                     |")

    print(
        "==================== [ TAUMOEBA TARGET ] ===================="
    )

    time.sleep(0.04)

def evaluate():
    agent=ProbeAgent()
    agent.qtable=np.load("q_table.npy")
    agent.epsilon=0.0

    env=ProbeEnv()
    raw_state=env.reset()
    state=agent.discretize_state(raw_state)

    done=False
    total_reward=0
    step_count=0

    print("\n LAUNCHING PROBE INTO ADRIAN...\n")

    while not done:
        action=agent.choose_action(state)

        render_probe_ascii(
            h=env.h,
            max_h=env.drop_height,
            v=env.v,
            action=action,
            wind=env.wind_idx,
            step_count=step_count,
            is_jupyter=False
        )

        raw_next,reward,done=env.step(action)
        next_state=agent.discretize_state(raw_next)

        state=next_state
        total_reward+=reward
        step_count+=1

    print("\n" + "="*50)
    if env.v>=-3.0:
        print("SOFT LANDING! Taumoeba sample secured!")
    else:
        print(f" PROBE CRUSHED! Impact velocity: {env.v:.1f} m/s")
    print(f"Total Reward: {total_reward:.1f}")
    print(f"Steps taken:  {step_count}")
    print("="*50)


if __name__ == "__main__":
    evaluate()