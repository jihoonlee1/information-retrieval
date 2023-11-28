import database
import utils
import openai


def _question(key, contents):
	useinsent = {
		"revenue": [
			"revenue (turnover)",
			"revenue"
		],
		"capital_expenditure": [
			"capital expenditure (CapEx)",
			"capital expenditure"
		],
		"operational_expenditure": [
			"operational expenditure (OpEx)",
			"operational expenditure"
		]
	}
	first, second = useinsent[key]
	question = f"""
Task:
Analyze each of the provided images to determine Acciona's exact total {first}.

Instructions:
1. Identify the most detailed and complete numeric figure for the total {second}, avoiding any shorthand or rounded representations. Report the full extended numerical value of the total. Ensure that the final result you provide is the most comprehensive and unabridged numerical figure available from the given images.
2. Do not use numerical shorthand. Some numbers may be shortened in the images (e.g., 15mil). Write the full digit form, such as 15,123,123.
3. Clearly specify which image provides the final result.

Examples:
Example 1) IMAGE 9: 129,412,99
Example 2) IMAGE 1: 49,000,512
Example 3) IMAGE 3: 52,412,681
Example 4) IMAGE 2: 9,412,231

If the images are unclear, the textual contents are as follows:
{contents}
""".strip()
	return question


def main():
	zach = "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"
	dong = "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"
	justin = "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"
	client = openai.OpenAI(api_key=dong)
	pdf_name = "acciona"
	key = "revenue"
	pages = utils.get_relevant_pages(pdf_name, key)
	contents = []
	messages = [
		{
			"role": "system",
			"content": [
				{
					"type": "text",
					"text": "You are a business analyst."
				}
			]
		},
		{
			"role": "user",
			"content": []
		}
	]
	with database.connect() as con:
		cur = con.cursor()
		for index, page in enumerate(pages):
			index = index + 1
			base64_encoded_image = utils.base64_encoded_image(f"{pdf_name}/{page}.jpg")
			messages[1]["content"].append({
				"type": "image_url",
				"image_url": {
					"url": f"data:image/jpeg;base64,{base64_encoded_image}"
				}
			})
			cur.execute("SELECT content FROM pdf_page_content WHERE pdf_name = ? AND page = ?", (pdf_name, page))
			content, = cur.fetchone()
			contents.append(f"IMAGE {index}:\n{content}")
		contents = "\n\n".join(contents)
		question = _question(key, contents)
		messages[1]["content"].append({
			"type": "text",
			"text": question
		})
		response = client.chat.completions.create(
			model="gpt-4-vision-preview",
			messages=messages,
			max_tokens=50
		)
		response = response.choices[0].message.content
		cur.execute("INSERT INTO pdf_total_temp VALUES(?,?,?)", (pdf_name, key, response))
		con.commit()


def parse():
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT pdf_name, key, response FROM pdf_total_temp")
		for pdf_name, key, response in cur.fetchall():
			image_index, value = response.split(":", 1)
			image_index = image_index.replace("IMAGE", "").strip()
			image_index = int(image_index) - 1
			relevant_pages = utils.get_relevant_pages(pdf_name, key)
			found_page_where = relevant_pages[image_index]
			value = value.replace(",", "").strip()
			value = float(value)
			cur.execute("INSERT INTO pdf_total VALUES(?,?,?,?)",
			   (pdf_name, key, found_page_where, value))
		con.commit()



if __name__ == "__main__":
	parse()
