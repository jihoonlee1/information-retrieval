import database
import instructions
import openai
import re

# $25.46
# $24.16

def main():
	client = openai.OpenAI()
	messages = instructions.messages_template()
	contents = []
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT page FROM pdf_page_prefilter WHERE key = ?", ("operational_expenditure", ))
		for idx, (page,) in enumerate(cur.fetchall()):
			messages[1]["content"].append({
				"type": "image_url",
				"image_url": {
					"url": f"https://jihoonlee1.github.io/{page}.png"
				}
			})
			cur.execute("SELECT content FROM pdf_page_content WHERE page = ?", (page, ))
			content, = cur.fetchone()
			contents.append(f"IMAGE{idx+1}:\n{content}")
	instruction = instructions.operational_expenditure_total(contents)
	messages[1]["content"].append({
		"type": "text",
		"text": instruction
	})
	response = client.chat.completions.create(
		model="gpt-4-vision-preview",
		messages=messages,
		max_tokens=3200
	)


def parse():
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT pdf_id, key, response FROM pdf_total_temp")
		for pdf_id, key, response in cur.fetchall():
			response = re.findall(r"\[(.+?)\]", response)[0]
			image_index, amount = response.split(";")
			image_index= int(image_index.replace("IMAGE", "").strip())
			amount = int(re.sub(r"^[0-9]", "", amount).strip())
			cur.execute("INSERT INTO pdf_total VALUES(?,?,?,?)", (pdf_id, key, -1, amount))
		con.commit()


if __name__ == "__main__":
	main()