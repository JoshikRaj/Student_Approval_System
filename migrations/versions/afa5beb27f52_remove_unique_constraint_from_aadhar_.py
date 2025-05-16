"""Remove unique constraint from aadhar_number

Revision ID: afa5beb27f52
Revises: 4b1a7937d14c
Create Date: 2025-05-16 19:35:49.884200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afa5beb27f52'
down_revision = '4b1a7937d14c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE students_new (
        id INTEGER NOT NULL PRIMARY KEY,
        application_number VARCHAR NOT NULL UNIQUE,
        name VARCHAR,
        school VARCHAR,
        district VARCHAR,
        address VARCHAR,
        stdcode VARCHAR,
        phone_number VARCHAR,
        email VARCHAR,
        aadhar_number VARCHAR,
        parent_annual_income DECIMAL,
        community VARCHAR,
        college VARCHAR,
        degree VARCHAR,
        branch_1 VARCHAR,
        branch_2 VARCHAR,
        branch_3 VARCHAR,
        board VARCHAR(100),
        maths FLOAT,
        physics FLOAT,
        chemistry FLOAT,
        nata FLOAT,
        studybreak INTEGER,
        msc_cutoff FLOAT,
        barch_cutoff FLOAT,
        bdes_cutoff FLOAT,
        twelfth_mark INTEGER,
        markpercentage FLOAT,
        engineering_cutoff FLOAT,
        date_of_application DATE,
        applicationstatus VARCHAR,
        year_of_passing VARCHAR
    );
    """)
    op.execute("""
    INSERT INTO students_new SELECT * FROM students;
    """)
    op.execute("""
    DROP TABLE students;
    """)
    op.execute("""
    ALTER TABLE students_new RENAME TO students;
    """)

def downgrade():
    op.execute("""
    CREATE TABLE students_old (
        id INTEGER NOT NULL PRIMARY KEY,
        application_number VARCHAR NOT NULL UNIQUE,
        name VARCHAR,
        school VARCHAR,
        district VARCHAR,
        address VARCHAR,
        stdcode VARCHAR,
        phone_number VARCHAR,
        email VARCHAR,
        aadhar_number VARCHAR UNIQUE,
        parent_annual_income DECIMAL,
        community VARCHAR,
        college VARCHAR,
        degree VARCHAR,
        branch_1 VARCHAR,
        branch_2 VARCHAR,
        branch_3 VARCHAR,
        board VARCHAR(100),
        maths FLOAT,
        physics FLOAT,
        chemistry FLOAT,
        nata FLOAT,
        studybreak INTEGER,
        msc_cutoff FLOAT,
        barch_cutoff FLOAT,
        bdes_cutoff FLOAT,
        twelfth_mark INTEGER,
        markpercentage FLOAT,
        engineering_cutoff FLOAT,
        date_of_application DATE,
        applicationstatus VARCHAR,
        year_of_passing VARCHAR
    );
    """)
    op.execute("""
    INSERT INTO students_old SELECT * FROM students;
    """)
    op.execute("""
    DROP TABLE students;
    """)
    op.execute("""
    ALTER TABLE students_old RENAME TO students;
    """)