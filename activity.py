import database
import instructions
import openai


# $24.16


def main():
	client = openai.OpenAI()
	key = "revenue"
	name = "Installation, Maintenance and Repair of Energy Efficiency Equipment​"
	messages = instructions.messages_template()
	contents = []
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT description, inclusions, exclusions FROM activities WHERE name = ?", (name, ))
		description, inclusions, exclusions = cur.fetchone()
		cur.execute("SELECT page FROM pdf_page_prefilter WHERE key = ?", (key, ))
		for idx, (page, ) in enumerate(cur.fetchall()):
			print(page)
			messages[1]["content"].append({
				"type": "image_url",
				"image_url": {
					"url": f"https://jihoonlee1.github.io/{page}.png",
					"detail": "medium"
				}
			})
			cur.execute("SELECT content FROM pdf_page_content WHERE page = ?", (page, ))
			content, = cur.fetchone()
			contents.append(f"IMAGE{idx+1}:\n{content}")
		contents = "\n\n".join(contents)
		instruction = instructions.revenue_activities(description, inclusions, exclusions, contents)
		messages[1]["content"].append({
			"type": "text",
			"text": instruction
		})
		response = client.chat.completions.create(
			model="gpt-4-vision-preview",
			messages=messages,
			max_tokens=3200
		)
		response = response.choices[0].message.content
		print(response)
		#cur.execute("INSERT INTO pdf_key_activity_temp VALUES(?,?,?,?)", (0, key, f"{name}_less_pages", response))
		#con.commit()


if __name__ == "__main__":
	main()