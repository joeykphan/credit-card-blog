"""new fields in user model

Revision ID: 31801707ac25
Revises: a27f9e9361c1
Create Date: 2023-04-16 20:16:23.448002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31801707ac25'
down_revision = 'a27f9e9361c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')

    # ### end Alembic commands ###
