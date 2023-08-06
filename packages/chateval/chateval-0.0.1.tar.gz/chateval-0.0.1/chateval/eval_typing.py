from __future__ import annotations

from dataclasses import dataclass


@dataclass
class APIModel:
    content: str


@dataclass
class MetricModel:
    content: str


@dataclass
class PredictionModel:
    content: list[str]
