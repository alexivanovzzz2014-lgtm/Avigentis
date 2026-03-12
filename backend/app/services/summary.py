from textwrap import dedent

DISCLAIMER = (
    'Скенерът анализира само публично достъпна информация. Резултатът е предварителен и '
    'не представлява официален одит, правно становище или гаранция за съответствие.'
)

THEMATIC_MAP = {
    'HTTPS not publicly reachable': 'communication security',
    'SSL certificate appears invalid or expired': 'risk management',
    'DMARC record not found': 'communication security',
    'SPF record not found': 'communication security',
    'Privacy policy signal not found': 'governance and policies',
    'Cookie policy signal not found': 'governance and policies',
    'Server technology leakage visible': 'cyber hygiene',
}


def generate_public_summary(domain: str, score: float, status: str, penalties: list[str]) -> str:
    top = penalties[:5] if penalties else ['No major externally visible issues detected during preliminary analysis.']
    affected = sorted({THEMATIC_MAP.get(p, 'cyber hygiene') for p in top})
    return dedent(
        f"""
        Domain: {domain}
        Preliminary readiness status: {status} ({score}/100)

        Top publicly visible indicators:
        - """ + '\n        - '.join(top) + f"""

        Broad affected themes: {', '.join(affected)}.

        Recommended next step: schedule an expert readiness assessment for support for achieving compliance under NIS2 / ЗКС.
        CTA: Request an Avigentis expert audit package.

        Disclaimer: {DISCLAIMER}
        Avigentis is a consultant, not a guarantor of compliance.
        """
    ).strip()


def generate_internal_summary(domain: str, score: float, status: str, penalties: list[str], results: dict) -> str:
    if score <= 30:
        package = 'Full package'
        priority = 'High'
    elif score <= 60:
        package = 'Standard audit'
        priority = 'Medium'
    else:
        package = 'Basic audit'
        priority = 'Normal'

    findings = penalties if penalties else ['Limited risk indicators found from public evidence.']

    return dedent(
        f"""
        Internal analyst summary for {domain}
        Score: {score}/100 | Status: {status}
        Sales priority: {priority}
        Recommended package: {package}

        Findings:
        - """ + '\n        - '.join(findings) + f"""

        Follow-up call notes:
        - Clarify that this is preliminary analysis based on publicly visible indicators.
        - Position Avigentis as support for achieving compliance, not compliance guarantor.
        - Validate governance controls not inferable from external observation.

        Raw scan themes: risk management, communication security, governance and policies, cyber hygiene, incident readiness.
        Disclaimer: {DISCLAIMER}
        """
    ).strip()
