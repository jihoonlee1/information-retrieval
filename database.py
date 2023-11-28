import contextlib
import sqlite3


statements = [
"""
CREATE TABLE IF NOT EXISTS activity_base(
	name        TEXT NOT NULL PRIMARY KEY,
	description TEXT NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS activities(
	base_name   TEXT NOT NULL REFERENCES activity_base(name),
	name        TEXT NOT NULL PRIMARY KEY,
	description TEXT NOT NULL,
	inclusions  TEXT NOT NULL,
	exclusions  TEXT NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_page_content(
	pdf_name TEXT    NOT NULL,
	page     INTEGER NOT NULL,
	content  TEXT    NOT NULL,
	PRIMARY KEY(pdf_name, page)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_page_prefilter_temp(
	pdf_name TEXT    NOT NULL,
	page     INTEGER NOT NULL,
	response TEXT    NOT NULL,
	PRIMARY KEY(pdf_name, page)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_page_prefilter(
	pdf_name TEXT    NOT NULL,
	page     INTEGER NOT NULL,
	key      TEXT    NOT NULL,
	PRIMARY KEY(pdf_name, page, key)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_total_temp(
	pdf_name TEXT NOT NULL,
	key      TEXT NOT NULL,
	response TEXT NOT NULL,
	PRIMARY KEY(pdf_name, key, response)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_total(
	pdf_name         TEXT    NOT NULL,
	key              TEXT    NOT NULL,
	found_page_where INTEGER NOT NULL,
	value            REAL    NOT NULL,
	PRIMARY KEY(pdf_name, key)
)
"""
]

def connect(database="database.sqlite", mode="rw"):
	return contextlib.closing(sqlite3.connect(f"file:{database}?mode={mode}", uri=True))


def main():
	with connect(mode="rwc") as con:
		cur = con.cursor()
		for st in statements:
			cur.execute(st)


if __name__ == "__main__":
	main()