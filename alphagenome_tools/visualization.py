"""
Visualization utilities for AlphaGenome results

This module provides convenient functions for visualizing AlphaGenome predictions,
including variant comparisons, batch summaries, and expression heatmaps.
"""

import logging
from pathlib import Path
from typing import List, Optional, Union
import numpy as np

# Visualization imports
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib/seaborn not installed. Install with: pip install matplotlib seaborn")

# AlphaGenome imports
try:
    from alphagenome.visualization import plot_components
    from alphagenome.data import genome
except ImportError:
    plot_components = None
    genome = None

# Pandas
try:
    import pandas as pd
except ImportError:
    pd = None

# Setup logging
logger = logging.getLogger(__name__)

# Set default style
if MATPLOTLIB_AVAILABLE:
    sns.set_style('whitegrid')
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 10


def quick_plot(outputs, figsize=(12, 6), save_path: Optional[Path] = None):
    """
    Generate a quick preview plot of AlphaGenome outputs.

    This is a simplified visualization for quick inspection of results.

    Args:
        outputs: AlphaGenome prediction outputs
        figsize: Figure size (width, height)
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.error("matplotlib not available")
        return None

    fig, ax = plt.subplots(figsize=figsize)

    # This is a placeholder - actual implementation depends on output structure
    # TODO: Implement based on actual AlphaGenome output structure

    ax.text(0.5, 0.5, 'AlphaGenome Output Visualization',
            ha='center', va='center', transform=ax.transAxes, fontsize=14)
    ax.set_xlabel('Genomic Position')
    ax.set_ylabel('Prediction Score')
    ax.set_title('AlphaGenome Prediction Results')

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        logger.info(f"Figure saved to {save_path}")

    return fig


def plot_variant_comparison(
    ref_outputs,
    alt_outputs,
    variant: genome.Variant,
    figsize=(14, 6),
    save_path: Optional[Path] = None,
    title: Optional[str] = None
):
    """
    Create side-by-side comparison of reference and alternate allele predictions.

    Args:
        ref_outputs: Reference allele outputs
        alt_outputs: Alternate allele outputs
        variant: The variant being compared
        figsize: Figure size (width, height)
        save_path: Optional path to save the figure
        title: Optional custom title

    Returns:
        matplotlib Figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.error("matplotlib not available")
        return None

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Plot reference
    # TODO: Implement based on actual AlphaGenome output structure
    ax1.text(0.5, 0.5, f'Reference\n{variant.reference_bases}',
             ha='center', va='center', transform=ax1.transAxes, fontsize=14)
    ax1.set_title('Reference Allele')
    ax1.set_xlabel('Genomic Position')
    ax1.set_ylabel('Prediction Score')

    # Plot alternate
    ax2.text(0.5, 0.5, f'Alternate\n{variant.alternate_bases}',
             ha='center', va='center', transform=ax2.transAxes, fontsize=14, color='red')
    ax2.set_title('Alternate Allele')
    ax2.set_xlabel('Genomic Position')
    ax2.set_ylabel('Prediction Score')

    # Set overall title
    if title is None:
        title = f'Variant Effect: {variant.chromosome}:{variant.position} ' \
                f'{variant.reference_bases}>{variant.alternate_bases}'

    fig.suptitle(title, fontsize=14, y=1.02)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        logger.info(f"Figure saved to {save_path}")

    return fig


def plot_batch_summary(
    results_df: pd.DataFrame,
    metric: str = 'success',
    figsize=(10, 6),
    save_path: Optional[Path] = None
):
    """
    Create summary visualization for batch predictions.

    Args:
        results_df: DataFrame with batch prediction results
        metric: Column name to visualize
        figsize: Figure size (width, height)
        save_path: Optional path to save the figure

    Returns:
        matplotlib Figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.error("matplotlib not available")
        return None

    if pd is None:
        logger.error("pandas not available")
        return None

    fig, ax = plt.subplots(figsize=figsize)

    # Count successes vs failures
    if metric == 'success':
        success_counts = results_df['success'].value_counts()
        colors = ['green' if x else 'red' for x in success_counts.index]
        success_counts.plot(kind='bar', ax=ax, color=colors)
        ax.set_ylabel('Count')
        ax.set_title('Batch Prediction Summary')
        ax.set_xticklabels(['Success', 'Failure'], rotation=0)

        # Add count labels on bars
        for i, (idx, count) in enumerate(success_counts.items()):
            label = 'Success' if idx else 'Failure'
            ax.text(i, count, str(count), ha='center', va='bottom')

    # Chromosome distribution
    elif 'chromosome' in results_df.columns:
        chr_counts = results_df['chromosome'].value_counts().sort_index()
        chr_counts.plot(kind='bar', ax=ax, color='steelblue')
        ax.set_ylabel('Count')
        ax.set_title('Variants by Chromosome')
        ax.set_xlabel('Chromosome')
        plt.xticks(rotation=45)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        logger.info(f"Figure saved to {save_path}")

    return fig


def plot_expression_heatmap(
    data,
    figsize=(12, 8),
    cmap: str = 'viridis',
    save_path: Optional[Path] = None,
    title: str = 'Gene Expression Heatmap'
):
    """
    Create a heatmap visualization of gene expression predictions.

    Args:
        data: Expression data (2D array or DataFrame)
        figsize: Figure size (width, height)
        cmap: Colormap name
        save_path: Optional path to save the figure
        title: Figure title

    Returns:
        matplotlib Figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.error("matplotlib not available")
        return None

    fig, ax = plt.subplots(figsize=figsize)

    # Convert to numpy array if needed
    if hasattr(data, 'values'):
        data = data.values
    elif not isinstance(data, np.ndarray):
        data = np.array(data)

    # Create heatmap
    im = ax.imshow(data, cmap=cmap, aspect='auto')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Expression Level')

    # Set labels
    ax.set_xlabel('Genomic Position')
    ax.set_ylabel('Samples/Genes')
    ax.set_title(title)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        logger.info(f"Figure saved to {save_path}")

    return fig


def plot_tracks_overlaid(
    tracks_data: dict,
    interval,
    figsize=(14, 6),
    save_path: Optional[Path] = None,
    title: Optional[str] = None
):
    """
    Plot multiple genomic tracks overlaid on the same plot.

    Args:
        tracks_data: Dictionary of track data {name: data_array}
        interval: Genomic interval for the plot
        figsize: Figure size (width, height)
        save_path: Optional path to save the figure
        title: Optional custom title

    Returns:
        matplotlib Figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.error("matplotlib not available")
        return None

    fig, ax = plt.subplots(figsize=figsize)

    # Plot each track
    for track_name, track_data in tracks_data.items():
        # Convert to numpy array if needed
        if hasattr(track_data, 'values'):
            y_data = track_data.values
        elif isinstance(track_data, list):
            y_data = np.array(track_data)
        else:
            y_data = track_data

        # Create x-axis (genomic position)
        x_data = np.linspace(interval.start, interval.end, len(y_data))

        # Plot track
        ax.plot(x_data, y_data, label=track_name, linewidth=1.5)

    # Add legend
    ax.legend(loc='best')

    # Set labels and title
    ax.set_xlabel(f'Genomic Position ({interval.chromosome})')
    ax.set_ylabel('Prediction Score')

    if title is None:
        title = f'Genomic Tracks: {interval.chromosome}:{interval.start}-{interval.end}'

    ax.set_title(title)

    # Add grid
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        logger.info(f"Figure saved to {save_path}")

    return fig


def create_multi_panel_figure(
    outputs_list: list,
    titles: Optional[list] = None,
    figsize=(16, 10),
    save_path: Optional[Path] = None,
    main_title: Optional[str] = None
):
    """
    Create a multi-panel figure with multiple plots.

    Useful for creating publication-ready figures with multiple panels.

    Args:
        outputs_list: List of output objects to plot
        titles: Optional list of titles for each panel
        figsize: Overall figure size (width, height)
        save_path: Optional path to save the figure
        main_title: Optional main title for the entire figure

    Returns:
        matplotlib Figure object
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.error("matplotlib not available")
        return None

    n_panels = len(outputs_list)

    # Calculate grid dimensions
    n_cols = min(3, n_panels)
    n_rows = (n_panels + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten axes array for easier iteration
    if n_rows == 1 and n_cols == 1:
        axes = [axes]
    elif n_rows == 1 or n_cols == 1:
        axes = axes.flatten()
    else:
        axes = axes.flatten()

    # Plot each panel
    for i, (outputs, ax) in enumerate(zip(outputs_list, axes)):
        # TODO: Implement actual plotting based on AlphaGenome output structure
        ax.text(0.5, 0.5, f'Panel {i+1}', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)

        if titles and i < len(titles):
            ax.set_title(titles[i])
        else:
            ax.set_title(f'Panel {i+1}')

    # Hide extra axes
    for i in range(n_panels, len(axes)):
        axes[i].set_visible(False)

    # Add main title
    if main_title:
        fig.suptitle(main_title, fontsize=16, y=0.995)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches='tight')
        logger.info(f"Figure saved to {save_path}")

    return fig


def save_figure(fig, filepath: Union[str, Path], formats: List[str] = None):
    """
    Save figure in multiple formats.

    Args:
        fig: matplotlib Figure object
        filepath: Base file path (without extension)
        formats: List of formats to save ('png', 'pdf', 'svg', 'eps')
    """
    if formats is None:
        formats = ['png', 'pdf']

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        output_path = filepath.with_suffix(f'.{fmt}')
        fig.savefig(output_path, bbox_inches='tight', format=fmt)
        logger.info(f"Figure saved to {output_path}")
