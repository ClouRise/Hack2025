from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '9e8baf62e543'
down_revision = '86e836b81237'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Удаляем все foreign key constraints
    op.drop_constraint('users_room_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('messages_room_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_user_id_fkey', 'messages', type_='foreignkey')
    
    # 2. Меняем тип primary key колонок
    op.execute('ALTER TABLE rooms ALTER COLUMN id TYPE UUID USING id::uuid')
    op.execute('ALTER TABLE users ALTER COLUMN id TYPE UUID USING id::uuid')
    
    # 3. Меняем тип foreign key колонок
    op.execute('''
        ALTER TABLE users ALTER COLUMN room_id TYPE UUID 
        USING CASE 
            WHEN room_id IS NULL THEN NULL 
            ELSE room_id::uuid 
        END
    ''')
    
    op.execute('ALTER TABLE messages ALTER COLUMN room_id TYPE UUID USING room_id::uuid')
    op.execute('ALTER TABLE messages ALTER COLUMN user_id TYPE UUID USING user_id::uuid')
    
    # 4. Восстанавливаем foreign key constraints
    op.create_foreign_key('users_room_id_fkey', 'users', 'rooms', ['room_id'], ['id'])
    op.create_foreign_key('messages_room_id_fkey', 'messages', 'rooms', ['room_id'], ['id'])
    op.create_foreign_key('messages_user_id_fkey', 'messages', 'users', ['user_id'], ['id'])


def downgrade():
    # 1. Удаляем foreign key constraints
    op.drop_constraint('users_room_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('messages_room_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('messages_user_id_fkey', 'messages', type_='foreignkey')
    
    # 2. Возвращаем обратно к VARCHAR
    op.execute('ALTER TABLE rooms ALTER COLUMN id TYPE VARCHAR USING id::varchar')
    op.execute('ALTER TABLE users ALTER COLUMN id TYPE VARCHAR USING id::varchar')
    
    op.execute('''
        ALTER TABLE users ALTER COLUMN room_id TYPE VARCHAR 
        USING CASE 
            WHEN room_id IS NULL THEN NULL 
            ELSE room_id::varchar 
        END
    ''')
    
    op.execute('ALTER TABLE messages ALTER COLUMN room_id TYPE VARCHAR USING room_id::varchar')
    op.execute('ALTER TABLE messages ALTER COLUMN user_id TYPE VARCHAR USING user_id::varchar')
    
    # 3. Восстанавливаем foreign key constraints
    op.create_foreign_key('users_room_id_fkey', 'users', 'rooms', ['room_id'], ['id'])
    op.create_foreign_key('messages_room_id_fkey', 'messages', 'rooms', ['room_id'], ['id'])
    op.create_foreign_key('messages_user_id_fkey', 'messages', 'users', ['user_id'], ['id'])