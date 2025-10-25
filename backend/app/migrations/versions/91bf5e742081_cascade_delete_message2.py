"""cascade_delete_message2

Revision ID: 91bf5e742081
Revises: fb99f841a8ce
Create Date: 2025-10-25 06:17:54.415614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91bf5e742081'
down_revision: Union[str, Sequence[str], None] = 'fb99f841a8ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint('messages_room_id_fkey', 'messages', type_='foreignkey')
    
    op.create_foreign_key(
        'messages_room_id_fkey', 
        'messages', 
        'rooms', 
        ['room_id'], 
        ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('messages_room_id_fkey', 'messages', type_='foreignkey')
    
    op.create_foreign_key(
        'messages_room_id_fkey', 
        'messages', 
        'rooms', 
        ['room_id'], 
        ['id']
        # Без ondelete CASCADE для отката
    )