"""Insert data into products and categories tables

Revision ID: 6c73e26445b1
Revises: 07d2743e44c5
Create Date: ...
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '6c73e26445b1'
down_revision = '0762743e44c5'
branch_labels = None
depends_on = None


def upgrade():

    categories_table = table('categories',
                             column('id', sa.Integer),
                             column('name', sa.String)
                             )

    products_table = table('products',
                           column('name', sa.String),
                           column('price', sa.Float),
                           column('active', sa.Boolean),
                           column('category_id', sa.Integer)
                           )

    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])

    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True},
        {'name': 'Smartphone', 'price': 800.0, 'active': True},
        {'name': 'Novel', 'price': 20.0, 'active': True},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False},
    ])

    op.execute(
        "UPDATE products SET category_id = (SELECT id FROM categories WHERE name = 'Electronics') WHERE name IN ('Laptop', 'Smartphone')")
    op.execute(
        "UPDATE products SET category_id = (SELECT id FROM categories WHERE name = 'Books') WHERE name = 'Novel'")
    op.execute(
        "UPDATE products SET category_id = (SELECT id FROM categories WHERE name = 'Clothing') WHERE name = 'T-Shirt'")


def downgrade():

    op.execute("DELETE FROM products WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt')")

    op.execute("DELETE FROM categories WHERE name IN ('Electronics', 'Books', 'Clothing')")