import database
import openai
import re


def ask():
	client = openai.OpenAI()
	result = {
		"revenue": [],
		"capital_expenditure": [],
		"operational_expenditure": []
	}
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT DISTINCT page FROM pdf_page_prefilter WHERE top_similar_score >= ?", (0.95, ))
		for page, in cur.fetchall():
			cur.execute("SELECT DISTINCT contribution_type FROM pdf_page_prefilter WHERE page = ?", (page, ))
			for contribution_type, in cur.fetchall():
				result[contribution_type].append(page)
		for contribution_type, pages in result.items():
			print(contribution_type)
			replace_str = {
				"revenue": "revenue (turnover)",
				"capital_expenditure": "capital expenditure (CapEx)",
				"operational_expenditure": "operational expenditure (OpEx)"
			}
			contents = []
			for page in pages:
				cur.execute("SELECT content FROM pdf_page_content WHERE page = ?", (page, ))
				content, = cur.fetchone()
				contents.append(content)
			contents = "\n".join(contents)
			instruction = f"""
	Content:
{content}

Task:
Identify the total {replace_str[contribution_type]} in the given content. Enclose the result with a square bracket.

Output Examples:
[$125,512,151]
[$612,693]
[$81,123,111]

Output:
	""".strip()
			messages = [
				{
					"role": "user",
					"content": instruction
				}
			]
			response = client.chat.completions.create(
				model="gpt-4",
				messages=messages,
				max_tokens=3200
			)
			response = response.choices[0].message.content
			cur.execute("INSERT INTO pdf_key_total_temp VALUES(?,?,?)", (0, contribution_type, response))
			con.commit()


def parse():
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT pdf_id, key, response FROM pdf_key_total_temp")
		for pdf_id, key, response in cur.fetchall():
			response = re.findall(r"\[(.+?)\]", response)[0].strip()
			response = re.sub(r"[^\d\.]", "", response)
			amount = int(response)
			cur.execute("INSERT INTO pdf_key_total VALUES(?,?,?)", (pdf_id, key, amount))
		con.commit()


if __name__ == "__main__":
	parse()