import contextlib
import sqlite3


statements = [
"""
CREATE TABLE IF NOT EXISTS activity_base(
	id          INTEGER NOT NULL PRIMARY KEY,
	name        TEXT    NOT NULL,
	description TEXT    NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS activities(
	id          INTEGER NOT NULL PRIMARY KEY,
	name        TEXT    NOT NULL,
	description TEXT    NOT NULL,
	inclusions  TEXT    NOT NULL,
	exclusions  TEXT    NOT NULL,
	base_id     INTEGER NOT NULL REFERENCES activity_base(id)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdfs(
	id   INTEGER NOT NULL PRIMARY KEY,
	name TEXT    NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_page_content(
	pdf_id  INTEGER NOT NULL REFERENCES pdfs(id),
	page    INTEGER NOT NULL,
	content TEXT    NOT NULL,
	PRIMARY KEY(pdf_id, page)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_page_prefilter_temp(
	pdf_id   INTEGER NOT NULL,
	page     INTEGER NOT NULL,
	response TEXT    NOT NULL,
	PRIMARY KEY(pdf_id, page)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_page_prefilter(
	id                      INTEGER NOT NULL PRIMARY KEY,
	pdf_id                  INTEGER NOT NULL,
	page                    INTEGER NOT NULL,
	activity_name           TEXT    NOT NULL,
	contribution_type       TEXT    NOT NULL,
	amount                  INTEGER NOT NULL,
	top_similar_activity_id INTEGER NOT NULL,
	top_similar_score       INTEGER NOT NULL
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_key_total_temp(
	pdf_id   INTEGER NOT NULL,
	key      TEXT    NOT NULL,
	response TEXT    NOT NULL,
	PRIMARY KEY(pdf_id, key)
)
""",
"""
CREATE TABLE IF NOT EXISTS pdf_key_total(
	pdf_id INTEGER NOT NULL,
	key    TEXT    NOT NULL,
	amount INTEGER NOT NULL,
	PRIMARY KEY(pdf_id, key)
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