import utils
import database
import openai


zach = "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"
dong = "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"
justin = "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"
client = openai.OpenAI(api_key=justin)


pdf_name = "acciona"
images = utils.get_relevant_images(pdf_name, "revenue")
raw_texts = []
messages = [
	{
		"role": "system",
		"content": [
			{
				"type": "text",
				"text": "You are a business analyst."
			}
		]
	}
]

with database.connect() as con:
	cur = con.cursor()
	for idx, image_index in enumerate(images):
		cur.execute("SELECT raw_text FROM pdf_image_index_raw_text WHERE pdf_name = ? AND image_index = ?", (pdf_name, image_index))
		raw_text, = cur.fetchone()
		raw_texts.append(f"IMAGE {idx}:\n{raw_text}")
		base64_encoded_image = utils.base64_encoded_image(f"{pdf_name}/{image_index}.jpg")
		image_url = {
			"role": "user",
			"content": [
				{
					"type": "image_url",
					"image_url": {
						"url": f"data:image/jpeg;base64,{base64_encoded_image}"
					}
				}
			]
		}
		messages.append(image_url)
	raw_texts = "\n\n".join(raw_texts)
	activity_str = utils.get_activity_str("Infrastructure Enabling Low Carbon Road Transport and Public Transport")
	question = f"""These images are sourced from Acciona's 2022 business report. Your task is to identify all the activities that contributed to total revenue (turnover), and the activity must follow the given Activity Scope, Activity Inclusions, and Activity Exclusions. The activities can be found on multiple images. Here is the activity defintion:
{activity_str}

Here are the raw texts of the images for your reference:
{raw_texts}
"""
	question = {
		"role": "user",
		"content": [
			{
				"type": "text",
				"text": question
			}
		]
	}
	messages.append(question)
	response = client.chat.completions.create(
		model="gpt-4-vision-preview",
		messages=messages,
		max_tokens=3200
	)

	response = response.choices[0].message.content
	print(response)

