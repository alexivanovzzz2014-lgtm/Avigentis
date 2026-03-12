from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class OrganizationType(str, Enum):
    MUNICIPALITY = 'Municipality'
    PUBLIC_INSTITUTION = 'Public institution'
    PUBLIC_SECTOR_ORG = 'Public sector organization'
    CRITICAL_INFRA = 'Critical infrastructure operator'
    OTHER = 'Other'


class ScanStatus(str, Enum):
    HIGH_PRIORITY = 'High priority for expert review'
    MEDIUM = 'Medium readiness'
    BASIC = 'Basic cyber hygiene present'
    GOOD = 'Good public signals, expert verification recommended'


class ScanRequest(Base):
    __tablename__ = 'scan_requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    domain: Mapped[str] = mapped_column(String(255), index=True)
    normalized_domain: Mapped[str] = mapped_column(String(255), index=True)
    organization_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    organization_type: Mapped[OrganizationType] = mapped_column(SqlEnum(OrganizationType), default=OrganizationType.OTHER)
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    gdpr_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    public_info_acknowledgment: Mapped[bool] = mapped_column(Boolean, default=False)
    request_consultation: Mapped[bool] = mapped_column(Boolean, default=False)
    raw_scan_results: Mapped[dict] = mapped_column(JSON, default=dict)
    score: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[ScanStatus] = mapped_column(SqlEnum(ScanStatus), default=ScanStatus.HIGH_PRIORITY)
    public_summary: Mapped[str] = mapped_column(Text, default='')
    internal_summary: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
