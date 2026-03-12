from app.db.session import SessionLocal
from app.models.scan import ScanRequest, OrganizationType, ScanStatus

sample = ScanRequest(
    domain='example.bg',
    normalized_domain='example.bg',
    organization_name='Sample Municipality',
    organization_type=OrganizationType.MUNICIPALITY,
    email='contact@example.bg',
    gdpr_consent=True,
    public_info_acknowledgment=True,
    raw_scan_results={'note': 'sample'},
    score=72,
    status=ScanStatus.BASIC,
    public_summary='Sample public summary',
    internal_summary='Sample internal summary',
)

with SessionLocal() as db:
    db.add(sample)
    db.commit()

print('Seed inserted')
