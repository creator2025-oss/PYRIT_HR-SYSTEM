"""
EU AI Act HR Compliance Demo — Candidate Data Models
Pydantic models for candidate representation with validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Tuple
from datetime import date


class Address(BaseModel):
    """Candidate address information"""
    street: Optional[str] = None
    postal_code: str = Field(..., min_length=5, max_length=10)
    city: str = Field(..., min_length=2)
    location_type: str = Field(default="urban", pattern="^(urban|rural)$")


class Education(BaseModel):
    """Educational background"""
    degree: str = Field(..., min_length=2)
    institution: str = Field(..., min_length=2)
    graduation_year: int = Field(..., ge=1950, le=2024)
    
    @field_validator('graduation_year')
    @classmethod
    def validate_year(cls, v: int) -> int:
        if v > 2024:
            raise ValueError("Graduation year cannot be in the future")
        return v


class Experience(BaseModel):
    """Work experience entry"""
    role: str
    company: str
    years: float = Field(..., ge=0, le=50)
    start_date: date
    end_date: Optional[date] = None


class CVFile(BaseModel):
    """CV file metadata (for injection testing)"""
    format: str = Field(..., pattern="^(pdf|docx|txt)$")
    visible_content: str
    hidden_text: Optional[str] = None  # For SC09 prompt injection


class JobAdMetadata(BaseModel):
    """Job advertisement metadata for SC01, SC03"""
    target_gender: Optional[str] = Field(default="all", pattern="^(male|female|all)$")
    target_age_range: Optional[Tuple[int, int]] = None
    job_level: Optional[str] = Field(default="mid", pattern="^(entry|mid|senior|executive)$")
    premium_ad: bool = False


class EmploymentGap(BaseModel):
    """Employment gap for SC11 career gap detection"""
    start_date: str
    end_date: str
    duration_months: int = Field(..., ge=0, le=120)
    reason: Optional[str] = None


class Candidate(BaseModel):
    """Complete candidate profile"""
    candidate_id: Optional[str] = None
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[str] = None
    address: Address
    education: Education
    experience: List[Experience] = Field(default_factory=list)
    experience_years: Optional[int] = Field(default=5, ge=0, le=50)
    skills: List[str] = Field(default_factory=list, min_length=1)
    visa_required: bool = False
    
    # Existing scenario fields
    cv_file: Optional[CVFile] = None
    social_posts: Optional[List[str]] = None  # For SC04 hallucination
    agentic_amplification: Optional[bool] = None  # For SC15
    
    # New scenario fields for remaining 7 scenarios
    job_ad_metadata: Optional[JobAdMetadata] = None  # SC01, SC03
    device_location: Optional[str] = Field(default=None, pattern="^(urban|suburban|rural)$")  # SC02
    ad_copy_text: Optional[str] = None  # SC05
    agent_session_id: Optional[str] = None  # SC08
    employment_gaps: Optional[List[EmploymentGap]] = Field(default_factory=list)  # SC11
    claimed_skills: Optional[List[str]] = Field(default_factory=list)  # SC12
    ai_inferred_skills: Optional[List[str]] = Field(default_factory=list)  # SC12
    reasoning_chain: Optional[List[str]] = Field(default_factory=list)  # SC13
    model_version: Optional[str] = Field(default="1.0")  # SC14
    
    # Additional fields from synthetic data
    social_media_mentions: Optional[List[str]] = None  # Alternative for SC04
    cv_text: Optional[str] = None  # Alternative for SC09
    
    # Metadata for testing
    scenario: Optional[str] = None
    expected_bias: Optional[bool] = None
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jordan Taylor",
                "address": {
                    "postal_code": "94102",
                    "city": "San Francisco",
                    "location_type": "urban"
                },
                "education": {
                    "degree": "BS Computer Science",
                    "institution": "Stanford University",
                    "graduation_year": 2018
                },
                "experience": [],
                "skills": ["Python", "AWS", "React"],
                "visa_required": False
            }
        }


class BiasAdjustment(BaseModel):
    """Individual bias adjustment detail"""
    bias_type: str
    adjustment_value: float
    reasoning: str


class ScoringResult(BaseModel):
    """Complete scoring result with bias transparency"""
    candidate_id: str
    base_score: float = Field(..., ge=0, le=100)
    bias_adjustments: Dict[str, float]
    final_score: float = Field(..., ge=0, le=100)
    reasoning_chain: List[str]
    detected_biases: List[str]
    article_violations: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "candidate_id": "cand-1234",
                "base_score": 75.0,
                "bias_adjustments": {
                    "gender_bias": -8.0,
                    "age_proxy_bias": -15.0
                },
                "final_score": 63.5,
                "reasoning_chain": [
                    "Profile suggests communication style considerations",
                    "Candidate may be overqualified"
                ],
                "detected_biases": ["GENDER_BIAS_SC06", "AGE_PROXY_BIAS_SC07"],
                "article_violations": ["Art. 10(2)(d)", "Art. 5(1)(a)"]
            }
        }
