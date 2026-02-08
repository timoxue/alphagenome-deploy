"""
Helper functions for AlphaGenome API interactions

This module provides utilities for batch processing, data loading/exporting,
and API quota monitoring.
"""

import os
import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Union
import pandas as pd

# AlphaGenome imports
try:
    from alphagenome.data import genome
    from alphagenome.models import dna_client
    from alphagenome import dna_client as client_module
except ImportError:
    print("Warning: alphagenome package not installed. Install with: pip install alphagenome")
    genome = None
    dna_client = None
    client_module = None

# Try to import tqdm for progress bars
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIMonitor:
    """
    Monitor AlphaGenome API usage and quota.

    Tracks the number of API calls made and provides warnings when approaching limits.
    """

    def __init__(self, limit: int = 1000000, warning_threshold: float = 0.9):
        """
        Initialize API monitor.

        Args:
            limit: Maximum number of API calls allowed (default: 1M for free tier)
            warning_threshold: Fraction of limit at which to warn (default: 0.9)
        """
        self.limit = limit
        self.warning_threshold = warning_threshold
        self.calls = 0
        self.log_file = Path.home() / 'work' / 'api_usage.log'

        # Load previous usage if exists
        self._load_usage()

    def _load_usage(self):
        """Load previous API usage from log file."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    last_line = f.readlines()[-1]
                    if 'Total calls' in last_line:
                        self.calls = int(last_line.split('Total calls:')[1].strip())
            except Exception as e:
                logger.warning(f"Could not load previous usage: {e}")

    def increment(self, count: int = 1):
        """
        Increment API call counter.

        Args:
            count: Number of API calls to add
        """
        self.calls += count
        self._log_usage()

        # Check if approaching limit
        usage_fraction = self.calls / self.limit
        if usage_fraction >= self.warning_threshold:
            logger.warning(
                f"API usage warning: {self.calls:,}/{self.limit:,} calls "
                f"({usage_fraction*100:.1f}%)"
            )

    def _log_usage(self):
        """Log current API usage to file."""
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, 'a') as f:
                f.write(f"{datetime.now().isoformat()} - Total calls: {self.calls}\n")
        except Exception as e:
            logger.error(f"Could not log usage: {e}")

    def get_usage(self) -> Dict[str, int]:
        """
        Get current API usage statistics.

        Returns:
            Dictionary with 'calls', 'limit', 'remaining'
        """
        return {
            'calls': self.calls,
            'limit': self.limit,
            'remaining': self.limit - self.calls
        }

    def __str__(self):
        """String representation of API usage."""
        remaining = self.limit - self.calls
        return f"API Usage: {self.calls:,}/{self.limit:,} calls ({remaining:,} remaining)"


# Global API monitor instance
_api_monitor = None


def monitor_api_quota(limit: int = 1000000, reset: bool = False) -> APIMonitor:
    """
    Get or create the global API monitor instance.

    Args:
        limit: Maximum number of API calls allowed
        reset: If True, reset the counter

    Returns:
        APIMonitor instance
    """
    global _api_monitor
    if _api_monitor is None or reset:
        _api_monitor = APIMonitor(limit=limit)
    return _api_monitor


def load_variants_from_csv(filepath: Union[str, Path]) -> List[genome.Variant]:
    """
    Load variants from a CSV file.

    Expected CSV format:
        chromosome,position,reference_bases,alternate_bases
        chr22,36201698,A,C
        chr22,36201699,G,T

    Args:
        filepath: Path to CSV file

    Returns:
        List of genome.Variant objects
    """
    variants = []
    filepath = Path(filepath)

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variant = genome.Variant(
                chromosome=row['chromosome'],
                position=int(row['position']),
                reference_bases=row['reference_bases'],
                alternate_bases=row['alternate_bases']
            )
            variants.append(variant)

    logger.info(f"Loaded {len(variants)} variants from {filepath}")
    return variants


def load_intervals_from_csv(filepath: Union[str, Path]) -> List[genome.Interval]:
    """
    Load genomic intervals from a CSV file.

    Expected CSV format:
        chromosome,start,end
        chr22,35677410,36725986
        chr21,33000000,34000000

    Args:
        filepath: Path to CSV file

    Returns:
        List of genome.Interval objects
    """
    intervals = []
    filepath = Path(filepath)

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            interval = genome.Interval(
                chromosome=row['chromosome'],
                start=int(row['start']),
                end=int(row['end'])
            )
            intervals.append(interval)

    logger.info(f"Loaded {len(intervals)} intervals from {filepath}")
    return intervals


def batch_predict_variants(
    variants: List[genome.Variant],
    model,
    interval: Optional[genome.Interval] = None,
    ontology_terms: Optional[List[str]] = None,
    requested_outputs=None,
    show_progress: bool = True,
    monitor: bool = True
) -> pd.DataFrame:
    """
    Batch predict variant effects.

    Args:
        variants: List of genome.Variant objects
        model: AlphaGenome model instance (from dna_client.create())
        interval: Genomic interval for predictions (optional)
        ontology_terms: List of ontology terms (e.g., ['UBERON:0001157'])
        requested_outputs: List of output types (e.g., [dna_client.OutputType.RNA_SEQ])
        show_progress: Show progress bar if tqdm is available
        monitor: Track API usage with APIMonitor

    Returns:
        DataFrame with prediction results
    """
    if requested_outputs is None:
        requested_outputs = [client_module.OutputType.RNA_SEQ]

    if ontology_terms is None:
        ontology_terms = []

    results = []
    iterator = tqdm(variants, desc="Predicting variants") if (show_progress and tqdm) else variants

    for variant in iterator:
        try:
            # If interval not provided, create one around the variant
            if interval is None:
                # Create 100kb window around variant
                window_size = 100000
                interval = genome.Interval(
                    chromosome=variant.chromosome,
                    position=max(0, variant.position - window_size // 2),
                    end=variant.position + window_size // 2
                )

            # Run prediction
            outputs = model.predict_variant(
                interval=interval,
                variant=variant,
                ontology_terms=ontology_terms,
                requested_outputs=requested_outputs
            )

            # Store results
            result = {
                'chromosome': variant.chromosome,
                'position': variant.position,
                'reference': variant.reference_bases,
                'alternate': variant.alternate_bases,
                'success': True,
            }

            # Add output-specific data
            if hasattr(outputs, 'reference') and hasattr(outputs, 'alternate'):
                result['has_outputs'] = True
            else:
                result['has_outputs'] = False

            results.append(result)

            # Update API monitor
            if monitor:
                monitor_api_quota().increment()

        except Exception as e:
            logger.error(f"Error predicting variant {variant.chromosome}:{variant.position}: {e}")
            results.append({
                'chromosome': variant.chromosome,
                'position': variant.position,
                'reference': variant.reference_bases,
                'alternate': variant.alternate_bases,
                'success': False,
                'error': str(e)
            })

    df = pd.DataFrame(results)
    logger.info(f"Completed {len(df)} variant predictions ({df['success'].sum()} successful)")

    return df


def batch_predict_sequences(
    intervals: List[genome.Interval],
    model,
    requested_outputs=None,
    show_progress: bool = True,
    monitor: bool = True
) -> pd.DataFrame:
    """
    Batch predict sequence features.

    Args:
        intervals: List of genome.Interval objects
        model: AlphaGenome model instance
        requested_outputs: List of output types
        show_progress: Show progress bar
        monitor: Track API usage

    Returns:
        DataFrame with prediction results
    """
    if requested_outputs is None:
        requested_outputs = [client_module.OutputType.RNA_SEQ]

    results = []
    iterator = tqdm(intervals, desc="Predicting sequences") if (show_progress and tqdm) else intervals

    for interval in iterator:
        try:
            outputs = model.predict_sequence(
                interval=interval,
                requested_outputs=requested_outputs
            )

            result = {
                'chromosome': interval.chromosome,
                'start': interval.start,
                'end': interval.end,
                'length': interval.end - interval.start,
                'success': True,
            }

            results.append(result)

            if monitor:
                monitor_api_quota().increment()

        except Exception as e:
            logger.error(f"Error predicting interval {interval.chromosome}:{interval.start}-{interval.end}: {e}")
            results.append({
                'chromosome': interval.chromosome,
                'start': interval.start,
                'end': interval.end,
                'length': interval.end - interval.start,
                'success': False,
                'error': str(e)
            })

    df = pd.DataFrame(results)
    logger.info(f"Completed {len(df)} sequence predictions ({df['success'].sum()} successful)")

    return df


def create_comparison_table(ref_outputs, alt_outputs) -> pd.DataFrame:
    """
    Create a comparison table between reference and alternate predictions.

    Args:
        ref_outputs: Reference allele outputs
        alt_outputs: Alternate allele outputs

    Returns:
        DataFrame with comparison metrics
    """
    # This is a placeholder - actual implementation depends on output structure
    data = {
        'metric': [],
        'reference': [],
        'alternate': [],
        'difference': []
    }

    # Extract comparison metrics from outputs
    # TODO: Implement based on actual AlphaGenome output structure

    return pd.DataFrame(data)


def save_results(
    outputs,
    prefix: str,
    output_dir: Union[str, Path] = None,
    formats: List[str] = None
) -> Path:
    """
    Save results to multiple formats.

    Args:
        outputs: AlphaGenome outputs object
        prefix: Filename prefix
        output_dir: Output directory (default: ~/work/results)
        formats: List of formats to save ('csv', 'excel', 'json', 'pickle')

    Returns:
        Path to output directory
    """
    if formats is None:
        formats = ['csv']

    if output_dir is None:
        output_dir = Path.home() / 'work' / 'results'
    else:
        output_dir = Path(output_dir)

    # Create timestamped directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_dir = output_dir / f'{prefix}_{timestamp}'
    result_dir.mkdir(parents=True, exist_ok=True)

    # Save in different formats
    if 'csv' in formats:
        export_to_csv(outputs, result_dir / f'{prefix}.csv')

    if 'excel' in formats:
        export_to_excel(outputs, result_dir / f'{prefix}.xlsx')

    if 'json' in formats:
        import json
        with open(result_dir / f'{prefix}.json', 'w') as f:
            # TODO: Convert outputs to JSON-serializable format
            json.dump({}, f)

    logger.info(f"Results saved to {result_dir}")
    return result_dir


def export_to_csv(data, filepath: Union[str, Path]):
    """
    Export data to CSV format.

    Args:
        data: Data to export (DataFrame, dict, or AlphaGenome outputs)
        filepath: Output file path
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, pd.DataFrame):
        data.to_csv(filepath, index=False)
    elif isinstance(data, dict):
        pd.DataFrame(data).to_csv(filepath, index=False)
    else:
        # Try to convert to DataFrame
        pd.DataFrame(data).to_csv(filepath, index=False)

    logger.info(f"Exported to CSV: {filepath}")


def export_to_excel(data, filepath: Union[str, Path], sheet_name: str = 'Results'):
    """
    Export data to Excel format.

    Args:
        data: Data to export (DataFrame, dict, or multiple DataFrames)
        filepath: Output file path
        sheet_name: Sheet name for single DataFrame
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, pd.DataFrame):
        data.to_excel(filepath, sheet_name=sheet_name, index=False)
    elif isinstance(data, dict):
        with pd.ExcelWriter(filepath) as writer:
            for key, value in data.items():
                pd.DataFrame(value).to_excel(writer, sheet_name=str(key), index=False)
    else:
        pd.DataFrame(data).to_excel(filepath, sheet_name=sheet_name, index=False)

    logger.info(f"Exported to Excel: {filepath}")
