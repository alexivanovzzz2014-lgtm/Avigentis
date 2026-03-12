"""create scan_requests

Revision ID: 0001
Revises:
Create Date: 2026-03-12
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'scan_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('domain', sa.String(255), nullable=False),
        sa.Column('normalized_domain', sa.String(255), nullable=False),
        sa.Column('organization_name', sa.String(255), nullable=True),
        sa.Column('organization_type', sa.String(64), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(64), nullable=True),
        sa.Column('gdpr_consent', sa.Boolean(), nullable=False),
        sa.Column('public_info_acknowledgment', sa.Boolean(), nullable=False),
        sa.Column('request_consultation', sa.Boolean(), nullable=False),
        sa.Column('raw_scan_results', sa.JSON(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('status', sa.String(128), nullable=False),
        sa.Column('public_summary', sa.Text(), nullable=False),
        sa.Column('internal_summary', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('scan_requests')
