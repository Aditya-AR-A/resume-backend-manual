from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

# ============================================================================
# BASE MODELS & COMMON SCHEMAS
# ============================================================================

class APIResponse(BaseModel):
    """Base model for API responses"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    meta: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Metadata for paginated responses"""
    total_count: int
    limit: int
    offset: int
    has_more: bool


class FilterOptions(BaseModel):
    """Options for filtering data"""
    field: Optional[str] = None
    value: Optional[Union[str, int, float, bool]] = None
    operation: Optional[str] = "="  # e.g., '=', '!=', '>', '<', 'in'
    skills: Optional[List[str]] = None
    featured: Optional[bool] = None
    category: Optional[str] = None
    status: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class CacheHeaders(BaseModel):
    """Model for cache-related headers"""
    cache_control: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None

# ============================================================================
# DATA MODELS - STRUCTURED SCHEMAS
# ============================================================================

# ---------- Profile ----------
class ProfileImage(BaseModel):
    src: str
    alt: str


class SocialLinks(BaseModel):
    email: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None


class PortfolioProfile(BaseModel):
    profileImage: ProfileImage
    name: str
    title: str
    about: str
    socialLinks: SocialLinks

# ---------- Experience ----------
class Links(BaseModel):
    company: Optional[str] = None
    project: Optional[str] = None


class ExperienceData(BaseModel):
    id: str
    title: str
    company: str
    companyLogo: Optional[str] = None
    position: str
    location: str
    startDate: str
    endDate: Optional[str] = None
    isCurrent: bool
    description: str
    responsibilities: List[str]
    skills: List[str]
    projectIds: Optional[List[str]] = None
    links: Optional[Links] = None
    featured: bool


class ExperienceList(BaseModel):
    __root__: List[ExperienceData]

# ---------- Projects ----------
class ModelMetrics(BaseModel):
    accuracy: Optional[str] = None
    mse: Optional[str] = None
    f1Score: Optional[str] = None
    inferenceTime: Optional[str] = None


class ModelInfo(BaseModel):
    type: str
    framework: Optional[str] = None
    architecture: Optional[str] = None
    base: Optional[str] = None
    metrics: Optional[ModelMetrics] = None


class ProjectLinks(BaseModel):
    github: Optional[str] = None
    live: Optional[str] = None
    notebook: Optional[str] = None
    marketplace: Optional[str] = None


class Demo(BaseModel):
    type: Optional[str] = None
    embedCode: Optional[str] = None


class Deployment(BaseModel):
    type: str
    platform: str
    status: str


class Research(BaseModel):
    notebook: Optional[str] = None


class ProjectData(BaseModel):
    id: str
    name: str
    type: str
    description: str
    shortDescription: str
    thumbnail: Optional[str] = None
    category: str
    featured: bool
    startDate: str
    status: str
    skills: List[str]
    links: Optional[ProjectLinks] = None
    demo: Optional[Demo] = None
    model: Optional[ModelInfo] = None
    research: Optional[Research] = None
    deployment: Optional[Deployment] = None


class ProjectList(BaseModel):
    __root__: List[ProjectData]

# ---------- Certifications ----------
class CertificationData(BaseModel):
    name: str
    file: Optional[str] = None
    snapshot: Optional[str] = None
    provider: str
    field: str
    skills: List[str]
    issueDate: Optional[str] = None
    expiryDate: Optional[str] = None
    credentialId: Optional[str] = None
    credentialUrl: Optional[str] = None
    description: str
    featured: bool = False

# ============================================================================
# HEALTH & STATUS MODELS
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    uptime: Optional[float] = None


class AIStatusResponse(BaseModel):
    """AI system status response"""
    status: str
    components: Dict[str, str]
    providers: Dict[str, bool]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# ERROR MODELS
# ============================================================================

class ErrorDetail(BaseModel):
    """Error detail model"""
    field: str
    message: str
    error_code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standardized error response"""
    success: bool = False
    error: str
    error_code: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

# ============================================================================
# PAGINATED RESPONSES
# ============================================================================

class PaginatedProjectsResponse(BaseModel):
    data: List[ProjectData]
    pagination: PaginationMeta
    filters: Optional[FilterOptions] = None


class PaginatedJobsResponse(BaseModel):
    data: List[ExperienceData]
    pagination: PaginationMeta
    filters: Optional[FilterOptions] = None


class PaginatedCertificatesResponse(BaseModel):
    data: List[CertificationData]
    pagination: PaginationMeta
    filters: Optional[FilterOptions] = None

# ============================================================================
# LLM / AI SYSTEM MODELS
# ============================================================================

# ---------- Provider ----------
class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    LOCAL = "local"


class LLMConfig(BaseModel):
    provider: LLMProvider
    api_key: Optional[str] = None
    model: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0)
    base_url: Optional[str] = None
    timeout: int = Field(default=30, gt=0)


class ProviderInfo(BaseModel):
    provider: LLMProvider
    model: str
    endpoint: Optional[str] = None
    version: Optional[str] = None
    latency: Optional[float] = None
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

# ---------- Input ----------
class LLMRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# ---------- Classification ----------
class MessageType(str, Enum):
    QUESTION = "question"
    COMMAND = "command"
    SEARCH = "search"
    CONVERSATION = "conversation"
    UNKNOWN = "unknown"


class MessageClassification(BaseModel):
    type: MessageType
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    entities: Optional[Dict[str, Any]] = None

# ---------- Response ----------
class ContentType(str, Enum):
    TEXT = "text"
    CARD = "card"
    MIXED = "mixed"


class LLMResponse(BaseModel):
    content_type: ContentType
    content: Any
    confidence: float
    provider_info: ProviderInfo
    suggestions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    processing_time: float

# ============================================================================
# CONFIGURATION
# ============================================================================

class AppConfig(BaseModel):
    name: str = "Resume Backend API"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


class DatabaseConfig(BaseModel):
    url: str = "sqlite:///./resume.db"
    pool_size: int = 10
    max_overflow: int = 20


class CacheConfig(BaseModel):
    enabled: bool = True
    ttl: int = 3600
    max_size: int = 1000


class AIConfig(BaseModel):
    primary_provider: LLMProvider = LLMProvider.OPENAI
    providers: Dict[LLMProvider, LLMConfig]
    enable_caching: bool = True
    cache_ttl: int = 3600
    max_retries: int = 3
    timeout: int = 30


class Settings(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    cache: CacheConfig
    ai: AIConfig
