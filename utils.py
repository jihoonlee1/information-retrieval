import database
import pdf2image
import PyPDF2
import base64


def get_activity_str(name):
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT description, inclusions, exclusions FROM activities WHERE name = ?", (name, ))
		description, inclusions, exclusions = cur.fetchone()
		if not inclusions:
			inclusions = "None"
		if not exclusions:
			exclusions = "None"
		activity = f"""
Activity Name: {name}

Activity Scope: {description}

Activity Inclusions:
{inclusions}

Activity Exclusions:
{exclusions}"""
		return activity.strip()


def _pdf_to_images(pdf_name):
	pages = pdf2image.convert_from_path(f"{pdf_name}/{pdf_name}.pdf")
	for page_index, page in enumerate(pages):
		page_index = page_index + 1
		print(f"PDF to image: {page_index}")
		page.save(f"{pdf_name}/{page_index}.jpg", "JPEG")


def _pdf_images_to_raw_text(pdf_name):
	with database.connect() as con:
		cur = con.cursor()
		reader = PyPDF2.PdfReader(f"{pdf_name}/{pdf_name}.pdf")
		for index, page in enumerate(reader.pages):
			index = index + 1
			print(f"Image raw text to database: {index}")
			text = page.extract_text().strip()
			cur.execute("INSERT OR IGNORE INTO pdf_page_content VALUES(?,?,?)", (pdf_name, index, text))
		con.commit()


def prepare_pdf_data(pdf_name):
	_pdf_to_images(pdf_name)
	_pdf_images_to_raw_text(pdf_name)


def base64_encoded_image(image_path):
	with open(image_path, "rb") as f:
		return base64.b64encode(f.read()).decode("utf-8")


def get_relevant_pages(pdf_name, key):
	result = []
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT page FROM pdf_page_prefilter WHERE pdf_name = ? AND key = ?", (pdf_name, key))
		for page, in cur.fetchall():
			result.append(page)
	return result
