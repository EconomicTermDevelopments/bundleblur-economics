"""
Bundleblur: computational implementation for behavioral economics analysis.

Bundleblur refers to intentional obfuscation through complex bundling preventing price comparison. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Bundleblur channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "bundle_complexity",  # Bundle complexity captures a distinct economic channel.
    "opaque_fee_share",  # Opaque fee share captures a distinct economic channel.
    "add_on_density",  # Add on density captures a distinct economic channel.
    "comparability_gap",  # Comparability gap captures a distinct economic channel.
    "search_cost",  # Search cost captures a distinct economic channel.
    "cognitive_load",  # Cognitive load captures a distinct economic channel.
    "disclosure_clarity",  # Disclosure clarity mitigates exposure when it is high.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "bundle_complexity",
    "opaque_fee_share",
    "add_on_density",
    "comparability_gap",
    "search_cost",
    "cognitive_load",
    "disclosure_clarity",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "bundle_complexity": 0.18,  # Bundle complexity captures a distinct economic channel.
    "opaque_fee_share": 0.16,  # Opaque fee share captures a distinct economic channel.
    "add_on_density": 0.14,  # Add on density captures a distinct economic channel.
    "comparability_gap": 0.16,  # Comparability gap captures a distinct economic channel.
    "search_cost": 0.14,  # Search cost captures a distinct economic channel.
    "cognitive_load": 0.12,  # Cognitive load captures a distinct economic channel.
    "disclosure_clarity": 0.1,  # Disclosure clarity mitigates exposure when it is high.
}


class BundleblurCalculator:
    """
    Compute Bundleblur index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_bundleblur(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Bundleblur channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["bundleblur_index"] = (
            + self.weights["bundle_complexity"] * out["bundle_complexity_norm"]
            + self.weights["opaque_fee_share"] * out["opaque_fee_share_norm"]
            + self.weights["add_on_density"] * out["add_on_density_norm"]
            + self.weights["comparability_gap"] * out["comparability_gap_norm"]
            + self.weights["search_cost"] * out["search_cost_norm"]
            + self.weights["cognitive_load"] * out["cognitive_load_norm"]
            + self.weights["disclosure_clarity"] * (1.0 - out["disclosure_clarity_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["bundleblur_band"] = pd.cut(
            out["bundleblur_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Bundleblur channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_bundleblur(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("bundleblur_dataset.csv")
    calc = BundleblurCalculator()
    print(calc.calculate_bundleblur(sample)[["bundleblur_index", "bundleblur_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="bundle_complexity", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["bundleblur_index"].mean()))
