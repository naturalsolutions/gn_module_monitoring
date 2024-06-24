"""add id_individual col t_observations

Revision ID: 2894b3c03c66
Revises: 6a15625a0f4a
Create Date: 2023-11-21 11:06:04.284038

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import column


# revision identifiers, used by Alembic.
revision = "2894b3c03c66"
down_revision = "7fbcdd93626a"
branch_labels = None
depends_on = "84f40d008640"  # t_individuals (geonature)

monitorings_schema = "gn_monitoring"
table = "t_observations"
column_name = "id_individual"
foreign_schema = monitorings_schema
foreign_table = "t_individuals"
foreign_key = column_name

constraint_name = f"check_{table}_cd_nom_or_id_individual_not_null"
cd_nom_column_name = "cd_nom"


def upgrade():
    op.add_column(
        table,
        sa.Column(
            column_name,
            sa.Integer(),
            sa.ForeignKey(
                f"{foreign_schema}.{foreign_table}.{foreign_key}",
                name=f"fk_{table}_{column_name}",
                onupdate="CASCADE",
            ),
        ),
        schema=monitorings_schema,
    )
    op.alter_column(
        table_name=table, column_name=cd_nom_column_name, nullable=True, schema=monitorings_schema
    )
    op.create_check_constraint(
        table_name=table,
        constraint_name=constraint_name,
        condition=sa.or_(column(cd_nom_column_name).isnot(None), column(column_name).isnot(None)),
        schema=monitorings_schema,
    )


def downgrade():
    op.execute(
        """
        UPDATE gn_monitoring.t_observations SET cd_nom = ind.cd_nom
        FROM gn_monitoring.t_individuals ind 
        WHERE ind.id_individual = gn_monitoring.t_observations.id_individual;
    """
    )
    op.drop_column(table_name=table, column_name=column_name, schema=monitorings_schema)
    op.alter_column(
        table_name=table, column_name=cd_nom_column_name, nullable=False, schema=monitorings_schema
    )
    # constraint automatically dropped with drop_column above
