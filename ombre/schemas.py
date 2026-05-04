""
Ombre Schemas — All data models and validation.

Pure Python dataclasses — no external dependencies.
Compatible with JSON serialization throughout.
"""

import uuid
import time
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


# ─── Billing rates ──────────────────────────────────────────────────────────

DOMAIN_PRICES = {
    "mathematics": 2.0,
    "code":        3.0,
    "science":     8.0,
    "medicine":    15.0,
    "finance":     12.0,
    "logic":       5.0,
    "general":     2.0,
}

CALL_RATES = {
    "trace_retrieval":       0.08,
    "trace_retrieval_bulk":  0.05,   # above 10K
    "custom_generation":     0.50,
    "dataset_build":         0.08,   # per trace in result
    "dataset_pull":          0.08,
    "problem_browse":        0.00,   # free
    "analytics":             0.00,   # free
    "billing_summary":       0.00,   # free
}

PREMIUM_MULTIPLIER   = 3.0   # applied to traces scoring 95+
STANDARD_MULTIPLIER  = 1.0
MONTHLY_MINIMUM      = 5000.0


# ─── Problem ────────────────────────────────────────────────────────────────

@dataclass
class Problem:
    problem_id:     str   = field(default_factory=lambda: str(uuid.uuid4()))
    source:         str   = "manual"
    domain:         str   = "general"
    subdomain:      str   = ""
    difficulty:     int   = 3
    problem_text:   str   = ""
    known_solution: str   = ""
    embedding_json: str   = "[]"
    ingested_at:    float = field(default_factory=time.time)
    status:         str   = "active"
    dedup_hash:     str   = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Reasoning step ─────────────────────────────────────────────────────────

@dataclass
class ReasoningStep:
    step_id:    int
    reasoning:  str
    action:     str
    confidence: float   # 0.0 – 1.0
    result:     str

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Trace ──────────────────────────────────────────────────────────────────

@dataclass
class Trace:
    trace_id:           str   = field(default_factory=lambda: str(uuid.uuid4()))
    problem_id:         str   = ""
    model_source:       str   = ""
    temperature:        float = 0.6
    steps_json:         str   = "[]"
    final_answer:       str   = ""
    answer_correct:     int   = 0      # 0/1
    generation_time_ms: float = 0.0
    token_count:        int   = 0
    t1_score:           float = 0.0
    t2_score:           float = 0.0
    t3_score:           float = 0.0
    t4_score:           float = 0.0
    final_score:        float = 0.0
    quality_tier:       str   = "unvalidated"
    status:             str   = "pending"
    generated_at:       float = field(default_factory=time.time)
    validated_at:       float = 0.0
    domain_price:       float = 2.0

    @property
    def is_premium(self) -> bool:
        return self.final_score >= 95.0

    @property
    def billing_multiplier(self) -> float:
        return PREMIUM_MULTIPLIER if self.is_premium else STANDARD_MULTIPLIER

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Validation result ───────────────────────────────────────────────────────

@dataclass
class ValidationResult:
    trace_id:       str
    t1_score:       float = 0.0
    t2_score:       float = 0.0
    t3_score:       float = 0.0
    t4_score:       float = 0.0
    final_score:    float = 0.0
    passed:         bool  = False
    quality_tier:   str   = "rejected"
    details:        dict  = field(default_factory=dict)

    def compute_final(self):
        """
        Final score = T1×0.20 + T2×0.25 + T3×0.35 + T4×0.20
        Threshold: 85+ = sellable. 95+ = premium (3x billing).
        """
        self.final_score = round(
            self.t1_score * 0.20 +
            self.t2_score * 0.25 +
            self.t3_score * 0.35 +
            self.t4_score * 0.20,
            2
        )
        if self.final_score >= 95:
            self.quality_tier = "premium"
            self.passed = True
        elif self.final_score >= 85:
            self.quality_tier = "standard"
            self.passed = True
        elif self.final_score >= 60:
            self.quality_tier = "review"
            self.passed = False
        else:
            self.quality_tier = "rejected"
            self.passed = False
        return self


# ─── Provenance event ────────────────────────────────────────────────────────

@dataclass
class ProvenanceEvent:
    trace_id:       str
    event_type:     str
    event_data:     dict
    actor:          str   = "system"
    timestamp:      float = field(default_factory=time.time)


# ─── Usage log ───────────────────────────────────────────────────────────────

@dataclass
class UsageLog:
    log_id:             str   = field(default_factory=lambda: str(uuid.uuid4()))
    client_id:          str   = ""
    trace_id:           str   = ""
    call_type:          str   = ""
    rate_applied:       float = 0.0
    premium_multiplier: float = 1.0
    amount_charged:     float = 0.0
    monthly_total:      float = 0.0
    timestamp:          float = field(default_factory=time.time)
    metadata:           dict  = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["metadata_json"] = str(d.pop("metadata", {}))
        return d


# ─── Billing summary ─────────────────────────────────────────────────────────

@dataclass
class BillingSummary:
    client_id:              str
    client_name:            str
    cycle_month:            str
    standard_calls:         int     = 0
    premium_calls:          int     = 0
    custom_generation_jobs: int     = 0
    base_amount:            float   = 0.0
    premium_uplift:         float   = 0.0
    custom_generation_cost: float   = 0.0
    total_usage:            float   = 0.0
    monthly_minimum:        float   = MONTHLY_MINIMUM
    minimum_met:            bool    = False
    amount_due:             float   = 0.0
    projected_month_end:    float   = 0.0

    def compute(self):
        self.total_usage = self.base_amount + self.premium_uplift + self.custom_generation_cost
        self.minimum_met = self.total_usage >= self.monthly_minimum
        self.amount_due  = max(self.total_usage, self.monthly_minimum)
        return self

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Client ──────────────────────────────────────────────────────────────────

@dataclass
class Client:
    client_id:       str   = field(default_factory=lambda: str(uuid.uuid4()))
    name:            str   = ""
    email:           str   = ""
    monthly_minimum: float = MONTHLY_MINIMUM
    created_at:      float = field(default_factory=time.time)
    active:          int   = 1

    def to_dict(self) -> dict:
        return asdict(self)


# ─── Dataset ─────────────────────────────────────────────────────────────────

@dataclass
class Dataset:
    dataset_id:    str   = field(default_factory=lambda: str(uuid.uuid4()))
    client_id:     str   = ""
    name:          str   = ""
    filters_json:  str   = "{}"
    trace_ids_json:str   = "[]"
    trace_count:   int   = 0
    total_cost:    float = 0.0
    created_at:    float = field(default_factory=time.time)
    status:        str   = "building"

    def to_dict(self) -> dict:
        return asdict(self)
