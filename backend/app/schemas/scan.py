from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.scan import OrganizationType, ScanStatus


DISCLAIMER_BG = (
    'Скенерът анализира само публично достъпна информация. '
    'Резултатът е предварителен и не представлява официален одит, '
    'правно становище или гаранция за съответствие.'
)


class ScanCreate(BaseModel):
    domain: str = Field(min_length=3, max_length=255)
    email: EmailStr
    gdpr_consent: bool
    public_info_acknowledgment: bool
    organization_name: str | None = Field(default=None, max_length=255)
    organization_type: OrganizationType = OrganizationType.OTHER
    phone: str | None = Field(default=None, max_length=64)
    request_consultation: bool = False


class ScanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    domain: str
    normalized_domain: str
    organization_name: str | None
    organization_type: OrganizationType
    email: str
    phone: str | None
    request_consultation: bool
    score: float
    status: ScanStatus
    raw_scan_results: dict
    public_summary: str
    internal_summary: str
    created_at: datetime


class PublicSummaryResponse(BaseModel):
    scan_id: int
    score: float
    status: str
    summary: str
    disclaimer: str = DISCLAIMER_BG


class InternalSummaryResponse(BaseModel):
    scan_id: int
    score: float
    status: str
    summary: str
    disclaimer: str = DISCLAIMER_BG


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
