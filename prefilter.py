import database
import openai
import re
import sentence_transformers


def ask():
	client = openai.OpenAI()
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT pdf_id, page, content FROM pdf_page_content")
		for pdf_id, page, content in cur.fetchall():
			print(page)
			cur.execute("SELECT 1 FROM pdf_page_prefilter_temp WHERE pdf_id = ? AND page = ?", (pdf_id, page))
			if cur.fetchone() is not None:
				continue
			instruction = f"""
Content:
{content}

Instructions:
1. Identify all the business activities in the given content.
2. For each business activity, find their monetary contribution amount (e.g., $150,123).
3. For each business activity, determine their contribution type using the three available keys:
	- `revenue`: if the business activity contributed to revenue (turnover)
	- `capital_expenditure`: if the business activity contributed to capital expenditure (CapEx)
	- `operational_expenditure`: if the business activity contributed to operational expenditure (OpEx)
4. Output the result as the following format:
`[Business Activity Name; Monetary Contribution Amount; Contribution Type]`

Output Examples:
[Acquisition and Ownership of Buildings; $512,1512.12; revenue]
[Composting of Bio-Waste; $693,612; capital_expenditure]
[Restoration of Wetlands; $51,123; operational_expenditure]
[Conservation Forest; $99,123; revenue]
[Production of Electricity from Wind Power; $5,123,552; revenue]
[Apparel Manufacturer; $683,125,111; capital_expenditure]
[Manufacture of Pesticides and Fertilizers; $123,555; capital_expenditure]
[Manufacturer of Educational Products and Technologies; $555,123; operational_expenditure]
[Infrastructure Enabling Low Carbon Road Transport and Public Transport; $661,123; operational_expenditure]

Output:""".strip()
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
			cur.execute("INSERT INTO pdf_page_prefilter_temp VALUES(?,?,?)", (pdf_id, page, response))
			con.commit()


def parse():
	model = sentence_transformers.SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
	embeddings = []
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT id, name FROM activities")
		for activity_id, activity_name in cur.fetchall():
			embedding = model.encode(activity_name, convert_to_tensor=True)
			embeddings.append((activity_id, embedding))
		cur.execute("SELECT pdf_id, page, response FROM pdf_page_prefilter_temp")
		for pdf_id, page, response in cur.fetchall():
			response = re.findall(r"\[(.+?)\]", response)
			if not response:
				continue
			for row in response:
				temp = row.split(";")
				if len(temp) != 3:
					continue
				activity_name, amount, contribution_type = row.split(";")
				contribution_type = contribution_type.strip()
				if contribution_type not in ["revenue", "capital_expenditure", "operational_expenditure"]:
					continue
				amount = re.sub(r"[^\d\.]", "", amount).strip()
				if not amount:
					continue
				try:
					amount = int(amount)
				except ValueError:
					continue
				activity_name = activity_name.strip()
				embedding = model.encode(activity_name, convert_to_tensor=True)
				top_similar_activity_id = None
				top_similar_score = 0
				for activity_id, fixed_embedding in embeddings:
					similarity_score = sentence_transformers.util.pytorch_cos_sim(fixed_embedding, embedding)[0].item()
					if similarity_score > top_similar_score:
						top_similar_score = similarity_score
						top_similar_activity_id = activity_id
				cur.execute("SELECT ifnull(max(id)+1, 0) FROM pdf_page_prefilter")
				row_id, = cur.fetchone()
				cur.execute("INSERT INTO pdf_page_prefilter VALUES(?,?,?,?,?,?,?,?)",
					(row_id, pdf_id, page, activity_name, contribution_type, amount, top_similar_activity_id, top_similar_score))
		con.commit()



parse()

