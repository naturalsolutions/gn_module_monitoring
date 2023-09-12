"""Add digitiser to t_sites_groups

Revision ID: e2b66850b5ee
Revises: fc90d31c677f
Create Date: 2023-09-11 12:17:17.280948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e2b66850b5ee"
down_revision = "2003e18f248a"
branch_labels = None
depends_on = None

monitorings_schema = "gn_monitoring"
table = "sites_groups"
column = "id_digitiser"

foreign_schema = "utilisateurs"
table_foreign = "t_roles"
foreign_key = "id_role"


def upgrade():
    op.add_column(
        table,
        sa.Column(
            column,
            sa.Integer(),
            sa.ForeignKey(
                f"{foreign_schema}.{table_foreign}.{foreign_key}",
                name="fk_t_sites_groups_id_digitiser",
                onupdate="CASCADE",
            ),
            nullable=False,
        ),
        schema=monitorings_schema,
    )


def downgrade():
    statement = sa.text(
        f"""
        ALTER TABLE {monitorings_schema}.{table} DROP CONSTRAINT fk_t_sites_groups_id_digitiser;
        """
    )
    op.execute(statement)
    op.drop_column(table, column, schema=monitorings_schema)
