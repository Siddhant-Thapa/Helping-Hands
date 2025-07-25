"""removed what added first

Revision ID: 21ed199c1359
Revises: 19b7466db06c
Create Date: 2025-07-16 23:15:40.185259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21ed199c1359'
down_revision = '19b7466db06c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('slots', schema=None) as batch_op:
        batch_op.drop_column('is_cancelled')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('slots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_cancelled', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
