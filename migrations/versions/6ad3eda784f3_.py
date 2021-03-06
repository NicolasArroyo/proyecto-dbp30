"""empty message

Revision ID: 6ad3eda784f3
Revises: 06c45ae5122f
Create Date: 2022-05-19 21:47:42.712538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ad3eda784f3'
down_revision = '06c45ae5122f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('is_admin', sa.Boolean(), nullable=False))
    op.drop_column('account', 'is_admin_test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('is_admin_test', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('account', 'is_admin')
    # ### end Alembic commands ###