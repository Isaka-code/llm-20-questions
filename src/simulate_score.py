import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from typing import Any


def generate_random_movements(num_circles: int, num_turns: int) -> list[np.ndarray]:
    """
    Generate random movements.

    Args:
        num_circles (int): Number of circles
        num_turns (int): Number of turns

    Returns:
        list[np.ndarray]: Positions of each circle for each turn
    """
    initial_positions = np.zeros(num_circles)
    movements = np.random.choice([-1, 1], size=(num_turns, num_circles))
    positions = [initial_positions]

    for turn in range(num_turns):
        new_positions = positions[-1] + movements[turn]
        positions.append(new_positions)

    return positions


def update(
    frame: int,
    scat: Any,
    positions: list[np.ndarray],
    turn_text: Any,
    top_score_text: Any,
    top_score_count_text: Any,
) -> tuple:
    """
    Update the animation frame.

    Args:
        frame (int): Current frame number
        scat (Any): Scatter plot object
        positions (list[np.ndarray]): Positions of each circle for each turn
        turn_text (Any): Text object for displaying the turn number
        top_score_text (Any): Text object for displaying the top score
        top_score_count_text (Any): Text object for displaying the count of the top score

    Returns:
        tuple: Updated objects
    """
    scat.set_offsets(np.c_[range(len(positions[0])), positions[frame]])
    turn_text.set_text(f"Turn: {frame}")

    top_score = np.max(positions[frame])
    top_score_count = np.sum(positions[frame] == top_score)

    top_score_text.set_text(f"Top Score: {top_score}")
    top_score_count_text.set_text(f"Top Score Count: {top_score_count}")

    return scat, turn_text, top_score_text, top_score_count_text


def animate_circles(num_circles: int, num_turns: int) -> None:
    """
    Display the random movement of circles as an animation.

    Args:
        num_circles (int): Number of circles
        num_turns (int): Number of turns
    """
    positions = generate_random_movements(num_circles, num_turns)

    fig, ax = plt.subplots()
    scat = ax.scatter(range(num_circles), positions[0])

    ax.set_xlabel("Circle Index")
    ax.set_ylabel("Position")
    ax.set_title("Random Movement Simulation of Circles")
    ax.set_ylim(-num_turns, num_turns)

    turn_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    top_score_text = ax.text(0.02, 0.90, "", transform=ax.transAxes)
    top_score_count_text = ax.text(0.02, 0.85, "", transform=ax.transAxes)

    ani = FuncAnimation(
        fig,
        update,
        frames=range(num_turns + 1),
        fargs=(scat, positions, turn_text, top_score_text, top_score_count_text),
        interval=500,
        blit=True,
    )

    plt.show()


if __name__ == "__main__":
    animate_circles(num_circles=2000, num_turns=20)
