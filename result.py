import database
import csv


def main():
	result = []
	temp = {
		"revenue": {},
		"capital_expenditure": {},
		"operational_expenditure": {}
	}
	with database.connect() as con:
		cur = con.cursor()
		cur.execute("SELECT DISTINCT page FROM pdf_page_prefilter WHERE top_similar_score >= ?", (0.95, ))
		for page, in cur.fetchall():
			cur.execute("SELECT top_similar_activity_id, contribution_type, amount FROM pdf_page_prefilter WHERE page = ? AND top_similar_score >= ?", (page, 0.60))
			for top_similar_activity_id, contribution_type, contribution_amount in cur.fetchall():
				cur.execute("SELECT name FROM activities WHERE id = ?", (top_similar_activity_id, ))
				top_similar_activity_name, = cur.fetchone()
				if top_similar_activity_name not in temp[contribution_type]:
					temp[contribution_type][top_similar_activity_name] = contribution_amount
				else:
					temp[contribution_type][top_similar_activity_name] = temp[contribution_type][top_similar_activity_name] + contribution_amount
		for key, activities in temp.items():
			cur.execute("SELECT amount FROM pdf_key_total WHERE key = ?", (key, ))
			total_amount, = cur.fetchone()
			for activity_name, contribution_amount in activities.items():
				percentage_involvement = (contribution_amount / total_amount) * 100
				result.append([activity_name, key, percentage_involvement, contribution_amount, total_amount])
	with open("result.csv", "w") as f:
		writer = csv.writer(f, delimiter=";")
		writer.writerow(["activity_name", "involvement_type", "percentage_involvement", "absolute_involvement", "involvement_denominator"])
		writer.writerows(result)


if __name__ == "__main__":
	main()


