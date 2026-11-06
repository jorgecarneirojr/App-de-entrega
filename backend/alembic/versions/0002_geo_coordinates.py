"""add coordinates and restaurant address

Revision ID: 0002_geo_coordinates
Revises: 0001_initial
Create Date: 2026-11-06
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_geo_coordinates"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("addresses", sa.Column("latitude", sa.Numeric(10, 7), nullable=True))
    op.add_column("addresses", sa.Column("longitude", sa.Numeric(10, 7), nullable=True))
    op.add_column("restaurants", sa.Column("address", sa.String(length=255), nullable=True))
    op.add_column("restaurants", sa.Column("latitude", sa.Numeric(10, 7), nullable=True))
    op.add_column("restaurants", sa.Column("longitude", sa.Numeric(10, 7), nullable=True))


def downgrade() -> None:
    op.drop_column("restaurants", "longitude")
    op.drop_column("restaurants", "latitude")
    op.drop_column("restaurants", "address")
    op.drop_column("addresses", "longitude")
    op.drop_column("addresses", "latitude")
