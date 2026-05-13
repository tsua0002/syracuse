from __future__ import annotations

import argparse
from pathlib import Path

from scipy import ndimage

from syracuse.arithmetic import (
    analyze_block_arithmetic,
    export_block_arithmetic_stats,
    plot_block_arithmetic,
    SuffixArithmeticMetrics,
    write_block_arithmetic_report,
)
from syracuse.analysis import (
    build_parity_stats,
    build_density_grid,
    build_normalized_density_grid,
    build_odd_compression_stats,
    export_common_parity_prefixes,
    export_odd_compression_summary,
    export_parity_summary,
    plot_odd_compression_diagnostics,
    plot_parity_diagnostics,
    plot_parity_metric_heatmaps,
    plot_density_heatmap,
    plot_density_resolution_comparison,
    save_density_grid,
    write_odd_compression_report,
    write_parity_heatmap_report,
    write_parity_report,
    write_density_report,
    write_density_resolution_report,
)
from syracuse.cache import (
    SequenceCache,
    build_fixed_normalized_support_mask_from_cache,
    build_normalized_density_grid_from_cache,
)
from syracuse.core import stats_for, stats_for_range
from syracuse.fit import export_fit_report, fit_log_power_law, fit_power_law, load_epsilon_sweep, plot_fit
from syracuse.plotting import plot_overlay, plot_overlay_animation, plot_sequence
from syracuse.reporting import export_summary_csv, evaluate_hypotheses, write_hypothesis_report
from syracuse.support import (
    analyze_dense_supports,
    analyze_block_attachment,
    analyze_alpha_attachment,
    export_alpha_attachment_stats,
    export_block_attachment_stats,
    export_dense_support_stats,
    export_epsilon_sweep_stats,
    plot_dense_support_masks,
    plot_dense_support_thickening,
    plot_block_attachment,
    plot_block_attachment_maps,
    plot_epsilon_sweep,
    plot_alpha_attachment,
    summarize_epsilon_sweep_item,
    write_dense_support_report,
    write_dense_support_resolution_report,
    write_alpha_attachment_report,
    write_block_attachment_report,
    write_epsilon_sweep_report,
)
from syracuse.tda import (
    compute_alpha_persistence,
    compute_density_persistence,
    export_persistence,
    plot_alpha_window,
    plot_persistence_barcode,
    plot_persistence_diagram,
    points_from_mask_window,
    summarize_alpha_window,
    write_alpha_window_report,
    write_tda_report,
    write_tda_resolution_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Syracuse sequence plots, summary tables, and hypothesis checks."
    )
    parser.add_argument("--start", type=int, default=11, help="Start value for the single-sequence plot.")
    parser.add_argument("--limit", type=int, default=1000, help="Inclusive upper bound for the overlay plot.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Directory for generated files.")
    parser.add_argument("--animate", action="store_true", help="Generate a GIF animation of sequences added one by one.")
    parser.add_argument("--animation-fps", type=int, default=100, help="Frames per second for the MP4 animation.")
    parser.add_argument("--heatmap-bins", type=int, default=240, help="Number of bins for the log-value heatmap axis.")
    parser.add_argument(
        "--compare-heatmap-resolutions",
        action="store_true",
        help="Generate heatmaps for several vertical bin resolutions and a comparison plate.",
    )
    parser.add_argument("--tda", action="store_true", help="Run TDA on density heatmaps using cubical complexes.")
    parser.add_argument(
        "--dense-support",
        action="store_true",
        help="Analyse thickened dense supports for the density heatmap.",
    )
    parser.add_argument(
        "--normalized-support",
        action="store_true",
        help="Analyse dense supports on normalized high-resolution grids.",
    )
    parser.add_argument(
        "--normalized-bins",
        type=int,
        nargs="+",
        default=[1000],
        help="Square grid resolutions for normalized support analysis.",
    )
    parser.add_argument(
        "--epsilon-sweep-limits",
        type=int,
        nargs="+",
        help="Run a lightweight normalized epsilon*(N) sweep for the provided limits.",
    )
    parser.add_argument(
        "--epsilon-sweep-bins",
        type=int,
        default=1000,
        help="Square normalized grid resolution used for epsilon sweep.",
    )
    parser.add_argument(
        "--sequence-cache",
        type=Path,
        help="Persistent SQLite cache for Syracuse suffixes, used by epsilon sweep when provided.",
    )
    parser.add_argument(
        "--fit-epsilon-sweep",
        type=Path,
        help="Fit empirical laws to an epsilon sweep CSV and exit.",
    )
    parser.add_argument(
        "--block-attachment-limits",
        type=int,
        nargs="+",
        help="Measure attachment distances for consecutive blocks in a fixed normalized grid.",
    )
    parser.add_argument(
        "--block-attachment-bins",
        type=int,
        default=1000,
        help="Square fixed grid resolution for block attachment analysis.",
    )
    parser.add_argument(
        "--alpha-attachment",
        action="store_true",
        help="Also measure block attachment distances under several fixed d_alpha metrics.",
    )
    parser.add_argument(
        "--alpha-values",
        type=float,
        nargs="+",
        default=[0.25, 0.5, 1.0, 2.0, 4.0],
        help="Alpha values for d_alpha attachment analysis.",
    )
    parser.add_argument(
        "--block-arithmetic",
        action="store_true",
        help="Aggregate arithmetic trajectory metrics for consecutive blocks.",
    )
    parser.add_argument(
        "--alpha-window",
        action="store_true",
        help="Run a local alpha complex validation on a fixed normalized support window.",
    )
    parser.add_argument("--alpha-window-limit", type=int, default=1_000_000)
    parser.add_argument("--alpha-window-bins", type=int, default=1000)
    parser.add_argument("--alpha-window-max-points", type=int, default=5000)
    parser.add_argument("--alpha-window-x", type=float, nargs=2, default=[0.15, 0.55])
    parser.add_argument("--alpha-window-y", type=float, nargs=2, default=[0.25, 0.70])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir

    if args.fit_epsilon_sweep is not None:
        limits, epsilons = load_epsilon_sweep(args.fit_epsilon_sweep)
        fit_results = (fit_power_law(limits, epsilons), fit_log_power_law(limits, epsilons))
        export_fit_report(limits, epsilons, fit_results, output_dir / "epsilon_fit_report.md")
        plot_fit(limits, epsilons, fit_results, output_dir / "epsilon_fit.png")
        print(f"Generated epsilon fit outputs in {output_dir.resolve()}")
        return

    single_stats = stats_for(args.start)
    range_stats = stats_for_range(args.limit)

    plot_sequence(single_stats, output_dir / f"sequence_{args.start}.png")
    plot_overlay(range_stats, output_dir / f"overlay_1_to_{args.limit}.png")
    if args.animate:
        plot_overlay_animation(
            range_stats,
            output_dir / f"animation_1_to_{args.limit}.mp4",
            fps=args.animation_fps,
        )
    density_grid = build_density_grid(range_stats, log_value_bins=args.heatmap_bins)
    save_density_grid(density_grid, output_dir / f"density_1_to_{args.limit}")
    plot_density_heatmap(density_grid, output_dir / f"heatmap_1_to_{args.limit}.png")
    write_density_report(density_grid, output_dir / f"density_report_1_to_{args.limit}.md")
    if args.dense_support:
        dense_support_stats = analyze_dense_supports(density_grid)
        export_dense_support_stats(dense_support_stats, output_dir / f"dense_support_thresholds_1_to_{args.limit}.csv")
        plot_dense_support_masks(density_grid, dense_support_stats, output_dir / f"dense_support_masks_1_to_{args.limit}.png")
        plot_dense_support_thickening(
            dense_support_stats,
            output_dir / f"dense_support_thickening_1_to_{args.limit}.png",
        )
        write_dense_support_report(dense_support_stats, output_dir / f"dense_support_report_1_to_{args.limit}.md")
    if args.normalized_support:
        normalized_support_by_bins = {}
        for bins in args.normalized_bins:
            normalized_grid = build_normalized_density_grid(range_stats, bins=bins)
            normalized_support_stats = analyze_dense_supports(normalized_grid)
            normalized_support_by_bins[bins] = normalized_support_stats
            plot_density_heatmap(
                normalized_grid,
                output_dir / f"normalized_heatmap_1_to_{args.limit}_bins_{bins}.png",
                title=f"Normalized density of Syracuse orbit visits ({bins}x{bins})",
                x_label="Normalized step",
                y_label=r"Normalized $\log_{10}(u_k(n))$",
            )
            export_dense_support_stats(
                normalized_support_stats,
                output_dir / f"normalized_dense_support_thresholds_1_to_{args.limit}_bins_{bins}.csv",
            )
            plot_dense_support_masks(
                normalized_grid,
                normalized_support_stats,
                output_dir / f"normalized_dense_support_masks_1_to_{args.limit}_bins_{bins}.png",
            )
            plot_dense_support_thickening(
                normalized_support_stats,
                output_dir / f"normalized_dense_support_thickening_1_to_{args.limit}_bins_{bins}.png",
            )
            write_dense_support_report(
                normalized_support_stats,
                output_dir / f"normalized_dense_support_report_1_to_{args.limit}_bins_{bins}.md",
            )
        write_dense_support_resolution_report(
            normalized_support_by_bins,
            output_dir / f"normalized_dense_support_resolution_comparison_1_to_{args.limit}.md",
        )
    if args.epsilon_sweep_limits:
        sorted_sweep_limits = sorted(set(args.epsilon_sweep_limits))
        max_sweep_limit = sorted_sweep_limits[-1]
        sweep_stats = []

        if args.sequence_cache is not None:
            cache = SequenceCache(args.sequence_cache)
            try:
                cache.ensure_range(max_sweep_limit)
                for sweep_limit in sorted_sweep_limits:
                    sweep_grid = build_normalized_density_grid_from_cache(
                        cache,
                        limit=sweep_limit,
                        bins=args.epsilon_sweep_bins,
                    )
                    support_stats = analyze_dense_supports(sweep_grid, thresholds=(1,))[0]
                    sweep_stats.append(
                        summarize_epsilon_sweep_item(
                            limit=sweep_limit,
                            bins=args.epsilon_sweep_bins,
                            threshold=1,
                            stats=support_stats,
                        )
                    )
            finally:
                cache.close()
        else:
            sweep_all_stats = stats_for_range(max_sweep_limit)
            for sweep_limit in sorted_sweep_limits:
                sweep_range_stats = sweep_all_stats[:sweep_limit]
                sweep_grid = build_normalized_density_grid(sweep_range_stats, bins=args.epsilon_sweep_bins)
                support_stats = analyze_dense_supports(sweep_grid, thresholds=(1,))[0]
                sweep_stats.append(
                    summarize_epsilon_sweep_item(
                        limit=sweep_limit,
                        bins=args.epsilon_sweep_bins,
                        threshold=1,
                        stats=support_stats,
                    )
                )

        sweep_stats_tuple = tuple(sweep_stats)
        export_epsilon_sweep_stats(
            sweep_stats_tuple,
            output_dir / f"epsilon_sweep_bins_{args.epsilon_sweep_bins}.csv",
        )
        plot_epsilon_sweep(
            sweep_stats_tuple,
            output_dir / f"epsilon_sweep_bins_{args.epsilon_sweep_bins}.png",
        )
        write_epsilon_sweep_report(
            sweep_stats_tuple,
            output_dir / f"epsilon_sweep_bins_{args.epsilon_sweep_bins}.md",
        )
    if args.block_attachment_limits:
        if args.sequence_cache is None:
            raise ValueError("--block-attachment-limits requires --sequence-cache")
        block_limits = sorted(set(args.block_attachment_limits))
        if len(block_limits) < 2:
            raise ValueError("--block-attachment-limits requires at least two limits")
        cache = SequenceCache(args.sequence_cache)
        try:
            max_limit = block_limits[-1]
            cache.ensure_range(max_limit)
            max_step = max(cache.nodes[start].steps for start in range(1, max_limit + 1))
            max_value = max(cache.nodes[start].maximum for start in range(1, max_limit + 1))
            previous_mask = build_fixed_normalized_support_mask_from_cache(
                cache,
                start=1,
                stop=block_limits[0],
                bins=args.block_attachment_bins,
                max_step=max_step,
                max_value=max_value,
            )
            attachment_stats = []
            alpha_attachment_stats = []
            attachment_maps = []
            arithmetic_stats_list: list = [] if args.block_arithmetic else None
            metrics_cache: dict[int, SuffixArithmeticMetrics] | None = (
                {} if args.block_arithmetic else None
            )
            for block_start, block_stop in zip(block_limits[:-1], block_limits[1:], strict=True):
                block_mask = build_fixed_normalized_support_mask_from_cache(
                    cache,
                    start=block_start + 1,
                    stop=block_stop,
                    bins=args.block_attachment_bins,
                    max_step=max_step,
                    max_value=max_value,
                )
                attachment_stats.append(
                    analyze_block_attachment(
                        previous_mask=previous_mask,
                        block_mask=block_mask,
                        start=block_start + 1,
                        stop=block_stop,
                    )
                )
                new_cells = block_mask & ~previous_mask
                distances = ndimage.distance_transform_edt(~previous_mask)
                attachment_maps.append((block_start + 1, block_stop, new_cells, distances))
                if args.alpha_attachment:
                    for alpha in args.alpha_values:
                        alpha_attachment_stats.append(
                            analyze_alpha_attachment(
                                previous_mask=previous_mask,
                                block_mask=block_mask,
                                start=block_start + 1,
                                stop=block_stop,
                                alpha=alpha,
                            )
                        )
                if arithmetic_stats_list is not None and metrics_cache is not None:
                    arithmetic_stats_list.append(
                        analyze_block_arithmetic(
                            cache,
                            start=block_start + 1,
                            stop=block_stop,
                            metrics_cache=metrics_cache,
                        )
                    )
                previous_mask |= block_mask
        finally:
            cache.close()
        attachment_stats_tuple = tuple(attachment_stats)
        export_block_attachment_stats(
            attachment_stats_tuple,
            output_dir / f"block_attachment_bins_{args.block_attachment_bins}.csv",
        )
        plot_block_attachment(
            attachment_stats_tuple,
            output_dir / f"block_attachment_bins_{args.block_attachment_bins}.png",
        )
        plot_block_attachment_maps(
            tuple(attachment_maps),
            output_dir / f"block_attachment_maps_bins_{args.block_attachment_bins}.png",
        )
        write_block_attachment_report(
            attachment_stats_tuple,
            output_dir / f"block_attachment_bins_{args.block_attachment_bins}.md",
        )
        if args.alpha_attachment:
            alpha_attachment_stats_tuple = tuple(alpha_attachment_stats)
            export_alpha_attachment_stats(
                alpha_attachment_stats_tuple,
                output_dir / f"alpha_attachment_bins_{args.block_attachment_bins}.csv",
            )
            plot_alpha_attachment(
                alpha_attachment_stats_tuple,
                output_dir / f"alpha_attachment_bins_{args.block_attachment_bins}.png",
            )
            write_alpha_attachment_report(
                alpha_attachment_stats_tuple,
                output_dir / f"alpha_attachment_bins_{args.block_attachment_bins}.md",
            )
        if args.block_arithmetic:
            if arithmetic_stats_list is None:
                raise RuntimeError("block arithmetic stats were not collected")
            arithmetic_stats = tuple(arithmetic_stats_list)
            export_block_arithmetic_stats(arithmetic_stats, output_dir / "block_arithmetic.csv")
            plot_block_arithmetic(arithmetic_stats, output_dir / "block_arithmetic.png")
            write_block_arithmetic_report(arithmetic_stats, output_dir / "block_arithmetic.md")
    if args.alpha_window:
        if args.sequence_cache is None:
            raise ValueError("--alpha-window requires --sequence-cache")
        cache = SequenceCache(args.sequence_cache)
        try:
            cache.ensure_range(args.alpha_window_limit)
            max_step = max(cache.nodes[start].steps for start in range(1, args.alpha_window_limit + 1))
            max_value = max(cache.nodes[start].maximum for start in range(1, args.alpha_window_limit + 1))
            mask = build_fixed_normalized_support_mask_from_cache(
                cache,
                start=1,
                stop=args.alpha_window_limit,
                bins=args.alpha_window_bins,
                max_step=max_step,
                max_value=max_value,
            )
        finally:
            cache.close()
        points = points_from_mask_window(
            mask,
            x_range=(args.alpha_window_x[0], args.alpha_window_x[1]),
            y_range=(args.alpha_window_y[0], args.alpha_window_y[1]),
            max_points=args.alpha_window_max_points,
        )
        alpha_features = compute_alpha_persistence(points)
        alpha_summary = summarize_alpha_window(points, alpha_features)
        export_persistence(alpha_features, output_dir / "alpha_window_persistence.csv")
        plot_alpha_window(points, output_dir / "alpha_window_points.png")
        plot_persistence_diagram(alpha_features, output_dir / "alpha_window_diagram.png")
        plot_persistence_barcode(alpha_features, output_dir / "alpha_window_barcode.png")
        write_alpha_window_report(alpha_summary, alpha_features, output_dir / "alpha_window_report.md")
    if args.tda:
        persistence_features = compute_density_persistence(density_grid)
        export_persistence(persistence_features, output_dir / f"tda_persistence_1_to_{args.limit}.csv")
        plot_persistence_barcode(persistence_features, output_dir / f"tda_barcode_1_to_{args.limit}.png")
        plot_persistence_diagram(persistence_features, output_dir / f"tda_diagram_1_to_{args.limit}.png")
        write_tda_report(persistence_features, output_dir / f"tda_report_1_to_{args.limit}.md")
    parity_stats = build_parity_stats(range_stats)
    export_parity_summary(parity_stats, output_dir / f"parity_summary_1_to_{args.limit}.csv")
    export_common_parity_prefixes(parity_stats, output_dir / f"parity_prefixes_1_to_{args.limit}.csv")
    plot_parity_diagnostics(parity_stats, output_dir / f"parity_diagnostics_1_to_{args.limit}.png")
    plot_parity_metric_heatmaps(
        range_stats,
        parity_stats,
        output_dir / f"parity_metric_heatmaps_1_to_{args.limit}.png",
        log_value_bins=args.heatmap_bins,
    )
    write_parity_report(parity_stats, output_dir / f"parity_report_1_to_{args.limit}.md")
    write_parity_heatmap_report(parity_stats, output_dir / f"parity_heatmap_report_1_to_{args.limit}.md")
    compression_stats = build_odd_compression_stats(range_stats)
    export_odd_compression_summary(compression_stats, output_dir / f"odd_compression_summary_1_to_{args.limit}.csv")
    plot_odd_compression_diagnostics(
        compression_stats,
        output_dir / f"odd_compression_diagnostics_1_to_{args.limit}.png",
    )
    write_odd_compression_report(
        compression_stats,
        output_dir / f"odd_compression_report_1_to_{args.limit}.md",
    )
    if args.compare_heatmap_resolutions:
        resolution_grids = {
            bins: build_density_grid(range_stats, log_value_bins=bins)
            for bins in (120, 240, 480, 960)
        }
        for bins, grid in resolution_grids.items():
            plot_density_heatmap(grid, output_dir / f"heatmap_1_to_{args.limit}_bins_{bins}.png")
        plot_density_resolution_comparison(
            resolution_grids,
            output_dir / f"heatmap_resolution_comparison_1_to_{args.limit}.png",
        )
        write_density_resolution_report(
            resolution_grids,
            output_dir / f"heatmap_resolution_comparison_1_to_{args.limit}.md",
        )
        if args.tda:
            persistence_by_bins = {
                bins: compute_density_persistence(grid)
                for bins, grid in resolution_grids.items()
            }
            write_tda_resolution_report(
                persistence_by_bins,
                output_dir / f"tda_resolution_comparison_1_to_{args.limit}.md",
            )
        if args.dense_support:
            dense_support_by_bins = {
                bins: analyze_dense_supports(grid)
                for bins, grid in resolution_grids.items()
            }
            write_dense_support_resolution_report(
                dense_support_by_bins,
                output_dir / f"dense_support_resolution_comparison_1_to_{args.limit}.md",
            )
    export_summary_csv(range_stats, output_dir / f"summary_1_to_{args.limit}.csv")
    write_hypothesis_report(evaluate_hypotheses(range_stats), output_dir / f"hypotheses_1_to_{args.limit}.md")

    print(f"Generated outputs in {output_dir.resolve()}")
    print(f"Sequence n={args.start}: {single_stats.steps} steps, maximum={single_stats.maximum}")
