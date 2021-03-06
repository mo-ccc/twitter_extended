"""Initial

Revision ID: 1b2f89225efc
Revises: 
Create Date: 2020-12-16 11:46:11.735630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b2f89225efc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('screen_name', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('emotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tweets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=280), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('source_device', sa.String(), nullable=True),
    sa.Column('in_reply_to_tweet_id', sa.Integer(), nullable=True),
    sa.Column('conversation_id', sa.Integer(), nullable=True),
    sa.Column('possibly_sensitive', sa.Boolean(), nullable=True),
    sa.Column('filter_level', sa.Enum('NONE', 'LOW', 'MEDIUM', name='filterlevel'), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['conversation_id'], ['tweets.id'], ),
    sa.ForeignKeyConstraint(['in_reply_to_tweet_id'], ['tweets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favourite_emotes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('emote_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['emote_id'], ['emotes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'emote_id')
    )
    op.create_table('tweet_emote_joint',
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.Column('emote_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['emote_id'], ['emotes.id'], ),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ),
    sa.PrimaryKeyConstraint('tweet_id', 'emote_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet_emote_joint')
    op.drop_table('favourite_emotes')
    op.drop_table('tweets')
    op.drop_table('emotes')
    op.drop_table('accounts')
    op.drop_table('users')
    # ### end Alembic commands ###
