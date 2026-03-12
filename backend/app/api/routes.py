from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_db_dep
from app.core.config import settings
from app.core.domain import normalize_domain
from app.core.rate_limit import check_rate_limit
from app.core.security import create_access_token
from app.models.scan import ScanRequest, ScanStatus
from app.schemas.scan import (
    InternalSummaryResponse,
    LoginRequest,
    LoginResponse,
    PublicSummaryResponse,
    ScanCreate,
    ScanResponse,
)
from app.services.scanner.checks import run_scan
from app.services.scoring import compute_score
from app.services.summary import generate_internal_summary, generate_public_summary

router = APIRouter(prefix='/api')


@router.post('/auth/login', response_model=LoginResponse)
def login(payload: LoginRequest):
    if payload.email != settings.admin_email or payload.password != settings.admin_password:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return LoginResponse(access_token=create_access_token(payload.email))


@router.post('/scans', response_model=ScanResponse)
def create_scan(payload: ScanCreate, request: Request, db: Session = Depends(get_db_dep)):
    if not payload.gdpr_consent or not payload.public_info_acknowledgment:
        raise HTTPException(status_code=400, detail='Required consent flags must be accepted.')
    client = request.client.host if request.client else payload.email
    check_rate_limit(client)
    domain = normalize_domain(payload.domain)

    results = run_scan(domain)
    score, status_text, penalties = compute_score(results)
    status = ScanStatus(status_text)
    public_summary = generate_public_summary(domain, score, status.value, penalties)
    internal_summary = generate_internal_summary(domain, score, status.value, penalties, results)

    obj = ScanRequest(
        domain=payload.domain,
        normalized_domain=domain,
        organization_name=payload.organization_name,
        organization_type=payload.organization_type,
        email=payload.email,
        phone=payload.phone,
        gdpr_consent=payload.gdpr_consent,
        public_info_acknowledgment=payload.public_info_acknowledgment,
        request_consultation=payload.request_consultation,
        raw_scan_results=results,
        score=score,
        status=status,
        public_summary=public_summary,
        internal_summary=internal_summary,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get('/scans/{scan_id}', response_model=ScanResponse)
def get_scan(scan_id: int, db: Session = Depends(get_db_dep)):
    obj = db.get(ScanRequest, scan_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Scan not found')
    return obj


@router.get('/scans/{scan_id}/public-summary', response_model=PublicSummaryResponse)
def get_public_summary(scan_id: int, db: Session = Depends(get_db_dep)):
    obj = db.get(ScanRequest, scan_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Scan not found')
    return PublicSummaryResponse(scan_id=scan_id, score=obj.score, status=obj.status.value, summary=obj.public_summary)


@router.get('/scans/{scan_id}/internal-summary', response_model=InternalSummaryResponse)
def get_internal_summary(scan_id: int, db: Session = Depends(get_db_dep), _admin: str = Depends(get_admin_user)):
    obj = db.get(ScanRequest, scan_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Scan not found')
    return InternalSummaryResponse(scan_id=scan_id, score=obj.score, status=obj.status.value, summary=obj.internal_summary)


@router.get('/admin/scans', response_model=list[ScanResponse])
def list_scans(
    status: str | None = None,
    organization_type: str | None = None,
    db: Session = Depends(get_db_dep),
    _admin: str = Depends(get_admin_user),
):
    query = select(ScanRequest)
    if status:
        query = query.where(ScanRequest.status == status)
    if organization_type:
        query = query.where(ScanRequest.organization_type == organization_type)
    return list(db.scalars(query.order_by(ScanRequest.created_at.desc())).all())


@router.get('/admin/scans/{scan_id}', response_model=ScanResponse)
def admin_scan_detail(scan_id: int, db: Session = Depends(get_db_dep), _admin: str = Depends(get_admin_user)):
    obj = db.get(ScanRequest, scan_id)
    if not obj:
        raise HTTPException(status_code=404, detail='Scan not found')
    return obj
