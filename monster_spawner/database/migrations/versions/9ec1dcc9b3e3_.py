"""empty message

Revision ID: 9ec1dcc9b3e3
Revises: fdb32991bc77
Create Date: 2022-01-29 12:17:12.942609

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9ec1dcc9b3e3"
down_revision = "fdb32991bc77"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("mob", sa.Column("hostile", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("mob", "hostile")
    # ### end Alembic commands ###
