"""Added column staaf number in model employee 

Revision ID: 5fa2802975b1
Revises: 295401065ea8
Create Date: 2022-08-11 21:36:01.091931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa2802975b1'
down_revision = '295401065ea8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('staff_number', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'employees', ['staff_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employees', type_='unique')
    op.drop_column('employees', 'staff_number')
    # ### end Alembic commands ###