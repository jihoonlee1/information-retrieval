import database
import instructions
import openai
import re


# $31.70
# $26.09


def main():
	client = openai.OpenAI()
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT page, content FROM pdf_page_content WHERE pdf_id = ?", (0, ))
		for page, content in cur.fetchall():
			cur.execute("SELECT 1 FROM pdf_page_prefilter_temp WHERE page = ?", (page, ))
			if cur.fetchone() is not None:
				continue
			print(page)
			messages = instructions.messages_template()
			instruction = instructions.page_prefilter(content)
			messages[1]["content"].append({
				"type": "text",
				"text": instruction
			})
			messages[1]["content"].append({
				"type": "image_url",
				"image_url": {
					"url": f"https://jihoonlee1.github.io/{page}.png"
				}
			})
			response = client.chat.completions.create(
				model="gpt-4-vision-preview",
				messages=messages,
				max_tokens=3200
			)
			response = response.choices[0].message.content
			cur.execute("INSERT INTO pdf_page_prefilter_temp VALUES(?,?,?)", (0, page, response))
			con.commit()


def parse():
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT pdf_id, page, response FROM pdf_page_prefilter_temp")
		for pdf_id, page, response in cur.fetchall():
			response = re.findall(r"\[(.+?)\]", response)[0]
			if "NONE" in response:
				continue
			keys = [item.strip() for item in response.split(",")]
			for key in keys:
				cur.execute("INSERT OR IGNORE INTO pdf_page_prefilter VALUES(?,?,?)", (pdf_id, page, key))
		con.commit()


if __name__ == "__main__":
	parse()