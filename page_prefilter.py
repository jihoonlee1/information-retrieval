import database
import instructions
import openai
import re


def main():
	client = openai.OpenAI()
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT page, content FROM pdf_page_content WHERE pdf_id = ?", (0, ))
		for page, content in cur.fetchall():
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
				max_tokens=50
			)
			response = response.choices[0].message.content
			cur.execute("INSERT INTO pdf_page_prefilter_temp VALUES(?,?,?)", (0, page, response))
			con.commit()


if __name__ == "__main__":
	main()