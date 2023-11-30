import database
import utils
import openai


def main():
	justin = "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"
	client = openai.OpenAI(api_key=justin)
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
	contents = []
	with database.connect() as con:
		cur = con.cursor()
		pages = [204, 205, 206]
		for idx, page in enumerate(pages):
			messages[1]["content"].append({
				"type": "image_url",
				"image_url": {
					"url": f"https://jihoonlee1.github.io/{page}.png"
				}
			})
			cur.execute("SELECT content FROM pdf_page_content WHERE page = ?", (page, ))
			content, = cur.fetchone()
			contents.append(f"IMAGE{idx+1}:\n{content}")
		contents = "\n\n".join(contents)
	question = f"""
Task:
Analyze each of the provided images, find all the relevant business activities that contributed to Acciona's total revenue (turnover).

Instructions:
1. Some relevant activities may have a duplicate name with different contribution amount. You MUST KEEP all (they are not duplicates). Find relevant activities that aligns with the given Activity Scope, and Activity Inclusions.
Activity Scope:
This activity assesses the companies' involvement in the renewal of water collection, treatment, and supply systems for domestic and industrial needs, as defined under NACE Code E36.0.0.2 Renewal of Water Collection, Treatment, and Supply Systems.
Activity Inclusions:
- Companies can be considered involved in this activity if they renew systems and networks which are used for water collection, treatment, and supply systems.
- Companies can renew these systems and networks for using them in their own operations or offer the renewal as a service to another company.
- Renewal refers to the rehabilitation or full-scale refurbishment of a substantial part of a network or the whole system (i.e., due to the degradation or age of the system). It implies no material changes to the volume of flow collected, treated or supplied.
- Analysts should be critical as there is a thin line here; some extension work might be done as part of the renewal process, which is covered under this activity.

2. Remove any business activites found in instruction 1, if they are in the given Activity Exclusions.
Activity Exclusions:
- General maintenance, smaller repairs, upkeeping of water collection, treatment, and supply systems are not intended to be captured here, but under the dedicated activity Construction, Extension and Operation of Water Collection, Treatment and Supply Systems
- The construction of new water collection, treatment and supply systems are not included here, but under the dedicated activity Construction, Extension and Operation of Water Collection, Treatment and Supply Systems
- The extension of water collection, treatment and supply systems are not included here, but under the dedicated activity Construction, Extension and Operation of Water Collection, Treatment and Supply Systems
- The operation of these systems is excluded, but it is covered under the dedicated activity Construction, Extension and Operation of Water Collection, Treatment and Supply Systems
- Wastewater services and treatment (also called reclaimed water/recycled water after treatment) are covered by another activity - Construction, Extension and Operation of Wastewater Collection and Treatment - and are not intended to be captured here.

3. Output the final result as the following format. Do not use numerical shorthand. Some amount may be shortened in the images (e.g., 15mil). Write the full digit form, such as 15123123.
[IMAGE#; Activity name; contribution amount]

Output examples:
Example 1: [NONE] (if no business activities found)
Example 2: [IMAGE3; Conservation Forest; 195029102][IMAGE4; District Heating/Cooling Distribution; 5812931]
Example 3: [IMAGE5; Growing of Non-Perennial Crops; 582915][IMAGE4; Livestock Production; 98125]
Example 4: [IMAGE4; Inland Freight Water Transport​; 392125][IMAGE6; Inland Freight Water Transport; 271892]

The images may be unclear. The textual contents are as follows; marked with IMAGE#:
{contents}
""".strip()
	messages[1]["content"].append({
		"type": "text",
		"text": question
	})
	response = client.chat.completions.create(
		model="gpt-4-vision-preview",
		messages=messages,
		max_tokens=3200
	)
	print(response.choices[0].message.content)


if __name__ == "__main__":
	main()

