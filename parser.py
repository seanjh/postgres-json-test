#!/usr/bin/env python3

import psycopg2


def connect():
    return psycopg2.connect(
        dbname="test",
        user="admin",
        password="password",
        host="172.18.0.2",
        port="5432",
    )


def load_sql(filename):
    with open(filename) as infile:
        return "\n".join(infile.readlines())


def reset_table(cur, table, field="id"):
    raw_stmt = (
        "DELETE FROM {table};\n"
        "ALTER SEQUENCE {table}_{field}_seq RESTART;"
    )
    stmt = raw_stmt.format(table=table, field=field)
    print(stmt)
    cur.execute(stmt)


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql("schema.sql"))
        reset_table(cur, "data_text")
        reset_table(cur, "data_json")
        reset_table(cur, "data_jsonb")


def main():
    with connect() as conn:
        init_db(conn)

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO data_text (data) VALUES (%s);",
                ("", )
            )
            cur.execute("SELECT * FROM data_text;")
            print(cur.fetchall())

        conn.commit()


if __name__ == '__main__':
    main()
