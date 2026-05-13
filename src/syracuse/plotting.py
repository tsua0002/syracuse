from __future__ import annotations

from pathlib import Path
import subprocess

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image, ImageDraw

from syracuse.core import SequenceStats


def plot_sequence(stats: SequenceStats, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.plot(range(len(stats.sequence)), stats.sequence, marker="o", linewidth=2)
    ax.set_title(f"Syracuse sequence for n = {stats.start}")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.grid(True, alpha=0.3)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_overlay(stats: tuple[SequenceStats, ...], path: Path) -> None:
    if not stats:
        raise ValueError("stats must not be empty")

    path.parent.mkdir(parents=True, exist_ok=True)

    starts = [item.start for item in stats]
    steps = [item.steps for item in stats]
    normalizer = Normalize(vmin=min(steps), vmax=max(steps))
    color_map = plt.colormaps["viridis_r"]

    fig, ax = plt.subplots(figsize=(14, 8), constrained_layout=True)
    for item in stats:
        ax.plot(
            range(len(item.sequence)),
            item.sequence,
            color=color_map(normalizer(item.steps)),
            alpha=0.24,
            linewidth=0.45,
            zorder=1,
        )

    longest = max(stats, key=lambda item: item.steps)
    highest = max(stats, key=lambda item: item.maximum)
    ax.plot(
        range(len(longest.sequence)),
        longest.sequence,
        color="black",
        linewidth=2.4,
        label=f"Longest: n={longest.start}, {longest.steps} steps",
        zorder=3,
    )
    ax.scatter(
        [highest.sequence.index(highest.maximum)],
        [highest.maximum],
        color="black",
        s=30,
        label=f"Highest peak: n={highest.start}, max={highest.maximum}",
        zorder=5,
    )

    scalar_mappable = plt.cm.ScalarMappable(norm=normalizer, cmap=color_map)
    scalar_mappable.set_array([])
    color_bar = fig.colorbar(scalar_mappable, ax=ax)
    color_bar.set_label("Steps to reach 1")

    ax.set_title(f"Syracuse sequences for n = 1..{max(starts)}")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value (log scale)")
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.18)
    ax.legend(loc="upper right")
    fig.savefig(path, dpi=200)
    plt.close(fig)


def plot_overlay_animation(stats: tuple[SequenceStats, ...], path: Path, *, fps: int = 100) -> None:
    if not stats:
        raise ValueError("stats must not be empty")
    if fps < 1:
        raise ValueError("fps must be greater than or equal to 1")

    path.parent.mkdir(parents=True, exist_ok=True)

    ordered_stats = tuple(sorted(stats, key=lambda item: item.start))
    starts = [item.start for item in ordered_stats]
    steps = [item.steps for item in ordered_stats]
    normalizer = Normalize(vmin=min(steps), vmax=max(steps))
    color_map = plt.colormaps["viridis_r"]

    fig = Figure(figsize=(12.8, 7.2), dpi=100)
    FigureCanvasAgg(fig)
    ax = fig.add_axes((0.08, 0.12, 0.76, 0.76))
    color_axis = fig.add_axes((0.88, 0.12, 0.025, 0.76))
    fig.suptitle(f"Syracuse generation for n = 1..{max(starts)}", fontsize=14, y=0.97)

    ax.set_xlim(0, max(item.steps for item in ordered_stats))
    ax.set_ylim(0.8, max(item.maximum for item in ordered_stats) * 1.15)
    ax.set_xlabel("Step")
    ax.set_ylabel("Value (log scale)")
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.16)

    scalar_mappable = plt.cm.ScalarMappable(norm=normalizer, cmap=color_map)
    scalar_mappable.set_array([])
    color_bar = fig.colorbar(scalar_mappable, cax=color_axis)
    color_bar.set_label("Steps to reach 1")

    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    background = Image.frombytes("RGBA", (width, height), bytes(fig.canvas.buffer_rgba())).copy()

    line_points = []
    for item in ordered_stats:
        points = [ax.transData.transform((step, value)) for step, value in enumerate(item.sequence)]
        pixel_points = [(round(x), round(height - y)) for x, y in points]
        color = color_map(normalizer(item.steps))
        rgba = tuple(round(channel * 255) for channel in color[:3]) + (155,)
        line_points.append((item, pixel_points, rgba))

    plt.close(fig)

    if path.suffix.lower() != ".mp4":
        raise ValueError("animation output must use the .mp4 extension")

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-loglevel",
        "error",
        "-an",
        "-vcodec",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "faststart",
        str(path),
    ]

    line_layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    line_draw = ImageDraw.Draw(line_layer, "RGBA")
    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    try:
        if process.stdin is None:
            raise RuntimeError("ffmpeg stdin is unavailable")

        for item, points, rgba in line_points:
            if len(points) > 1:
                line_draw.line(points, fill=rgba, width=1)

            frame = background.copy()
            frame.alpha_composite(line_layer)
            frame_draw = ImageDraw.Draw(frame)
            frame_draw.rectangle((90, 34, 470, 58), fill=(255, 255, 255, 235))
            frame_draw.text(
                (98, 39),
                f"n = {item.start} / {max(starts)} | steps = {item.steps} | max = {item.maximum}",
                fill=(30, 30, 30),
            )
            process.stdin.write(frame.convert("RGB").tobytes())
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait()

    if return_code != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {return_code}")
