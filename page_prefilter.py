import database
import utils
import openai


def main():
	zach = "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"
	dong = "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"
	justin = "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"
	client = openai.OpenAI(api_key=justin)
	pdf_name = "acciona"
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT page, content FROM pdf_page_content WHERE pdf_name = ?", (pdf_name, ))
		for page, content in cur.fetchall():
			cur.execute("SELECT 1 FROM pdf_page_prefilter WHERE pdf_name = ? AND page = ?",
				(pdf_name, page))
			if cur.fetchone() is not None:
				continue
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
			print(page)
			base64_encoded_image = utils.base64_encoded_image(f"{pdf_name}/{page}.jpg")
			messages[1]["content"].append({
				"type": "image_url",
				"image_url": {
					"url": f"data:image/jpeg;base64,{base64_encoded_image}"
				}
			})
			question = f"""
Task:
Analyze the given image to determine if it contains a detailed breakdown of financial information with actual monetary values (e.g., $15,123,123) of Acciona's revenue (turnover), capital expenditure (CapEx), or operational expenditure (OpEx).

Instructions:
1. If the image does not contain a detailed breakdown of financial information with actual monetary values (e.g., $15,123,123), respond with "NONE."
2. Otherwise, indicate which values are displayed on the image using the available keywords:
	2.1. revenue
	2.2. capital_expenditure
	2.3. operational_expenditure

Examples:
Example 1: revenue
Example 2: capital_expenditure
Example 3: operational_expenditure
Example 4: revenue, operational_expenditure
Example 5: revenue, capital_expenditure
Example 6: capital_expenditure, operational_expenditure
Example 7: revenue, capital_expenditure, operational_expenditure

If the image is unclear, the textual content is as follows:
{content}
""".strip()
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
			cur.execute("INSERT INTO pdf_page_prefilter VALUES(?,?,?)", (pdf_name, page, response))
			con.commit()



def parse():
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT pdf_name, page, response FROM pdf_page_prefilter_temp")
		for pdf_name, page, response in cur.fetchall():
			if "NONE" in response:
				continue
			keys = response.split(",")
			keys = [item.strip() for item in keys]
			for key in keys:
				cur.execute("INSERT OR IGNORE INTO pdf_page_prefilter VALUES(?,?,?)",
					(pdf_name, page, key))
		con.commit()


if __name__ == "__main__":
	pass