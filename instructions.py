def page_prefilter(content):
	question = f"""
Task:
Analyze the given image to determine if it contains financial information of Acciona's revenue (turnover), capital expenditure (CapEx), or operational expenditure (OpEx).

Instructions:
1. Determine if the image contains the amount of total revenue (turnover).
2. Determine if the image contains the name of business activity and its contribution amount towards revenue (turnover).
3. Determine if the image contains the amount of total capital expenditure (CapEx).
4. Determine if the image contains the name of business activity and its contribution amount towards capital expenditure (CapEx).
5. Determine if the image contains the amount of total operational expenditure (OpEx).
6. Determine if the image contains the name of business activity and its contribution amount towards operational expenditure (OpEx).
7. If none of things from instrctions 1~6 is true, respond with [NONE].
8. Otherwise, use the following Available Keys to output the result:
Available Keys:
revenue (if Instruction 1, or Instruction 2 is true)
capital_expenditure (if Instruction 3, or Instruction 4 is true)
operational_expenditure (if Instruction 5, or Instruction 6 is true)

Example outputs:
Example 1: [NONE]
Example 2: [revenue]
Example 3: [capital_expenditure]
Example 4: [operational_expenditure]
Example 5: [revenue, operational_expenditure]
Example 6: [revenue, capital_expenditure]
Example 7: [capital_expenditure, operational_expenditure]
Example 8: [revenue, capital_expenditure, operational_expenditure]

The image may be unclear. The textual content is as follows:
{content}
""".strip()
	return question


def revenue_total(contents):
	question = f"""
Task:
Analyze each of the provided images to determine Acciona's exact total revenue (turnover).

Instructions:
1. Identify the most detailed and complete numeric figure for the total revenue, avoiding any shorthand or rounded representations. Report the full extended numerical value of the total. Ensure that the final result you provide is the most comprehensive and unabridged numerical figure available from the given images.
2. Do not use numerical shorthand. Some numbers may be shortened in the images (e.g., 15mil). Write the full digit form, such as 15123123.
3. Clearly specify which image provides the final result.

Example outputs:
Example 1: [IMAGE 9; 12941299]
Example 2: [IMAGE 1; 49000512]
Example 3: [IMAGE 3; 52412681]
Example 4: [IMAGE 2; 9412231]

The images may be unclear. The textual contents are as follows; marked with IMAGE#:
{contents}
""".strip()
	return question


def capital_expenditure_total(contents):
	question = f"""
Task:
Analyze each of the provided images to determine Acciona's exact total capital expenditure (CapEx).

Instructions:
1. Identify the most detailed and complete numeric figure for the total capital expenditure, avoiding any shorthand or rounded representations. Report the full extended numerical value of the total. Ensure that the final result you provide is the most comprehensive and unabridged numerical figure available from the given images.
2. Do not use numerical shorthand. Some numbers may be shortened in the images (e.g., 15mil). Write the full digit form, such as 15123123.
3. Clearly specify which image provides the final result.

Example outputs:
Example 1: [IMAGE 9; 12941299]
Example 2: [IMAGE 1; 49000512]
Example 3: [IMAGE 3; 52412681]
Example 4: [IMAGE 2; 9412231]

The images may be unclear. The textual contents are as follows; marked with IMAGE#:
{contents}
""".strip()
	return question


def operational_expenditure_total(contents):
	question = f"""
Task:
Analyze each of the provided images to determine Acciona's exact total operational expenditure (OpEx).

Instructions:
1. Identify the most detailed and complete numeric figure for the total operational expenditure, avoiding any shorthand or rounded representations. Report the full extended numerical value of the total. Ensure that the final result you provide is the most comprehensive and unabridged numerical figure available from the given images.
2. Do not use numerical shorthand. Some numbers may be shortened in the images (e.g., 15mil). Write the full digit form, such as 15123123.
3. Clearly specify which image provides the final result.

Example outputs:
Example 1: [IMAGE 9; 12941299]
Example 2: [IMAGE 1; 49000512]
Example 3: [IMAGE 3; 52412681]
Example 4: [IMAGE 2; 9412231]

The images may be unclear. The textual contents are as follows; marked with IMAGE#:
{contents}
""".strip()
	return question


def revenue_activities(activity_description, activity_inclusions, activity_exclusions, contents):
	question = f"""
Task:
Analyze each of the provided images, find all the relevant business activities that contributed to Acciona's total revenue (turnover).

Instructions:
1. Some relevant activities may have a duplicate name with different contribution amount. You MUST KEEP all (they are not duplicates). Find relevant activities that aligns with the given Activity Scope, and Activity Inclusions.
Activity Scope:
{activity_description}
Activity Inclusions:
{activity_inclusions}

2. Remove any business activites found in instruction 1, if they are in the given Activity Exclusions.
Activity Exclusions:
{activity_exclusions}

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
	return question


def capital_expenditure_activities(activity_description, activity_inclusions, activity_exclusions, contents):
	question = f"""
Task:
Analyze each of the provided images, find all the relevant business activities that contributed to Acciona's total capital expenditure (CapEx).

Instructions:
1. Some relevant activities may have a duplicate name with different contribution amount. You MUST KEEP all (they are not duplicates). Find relevant activities that aligns with the given Activity Scope, and Activity Inclusions.
Activity Scope:
{activity_description}
Activity Inclusions:
{activity_inclusions}

2. Remove any business activites found in instruction 1, if they are in the given Activity Exclusions.
Activity Exclusions:
{activity_exclusions}

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
	return question


def operational_expenditure_activities(activity_description, activity_inclusions, activity_exclusions, contents):
	question = f"""
Task:
Analyze each of the provided images, find all the relevant business activities that contributed to Acciona's total operational expenditure (OpEx).

Instructions:
1. Some relevant activities may have a duplicate name with different contribution amount. You MUST KEEP all (they are not duplicates). Find relevant activities that aligns with the given Activity Scope, and Activity Inclusions.
Activity Scope:
{activity_description}
Activity Inclusions:
{activity_inclusions}

2. Remove any business activites found in instruction 1, if they are in the given Activity Exclusions.
Activity Exclusions:
{activity_exclusions}

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
	return question


def messages_template():
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
	return messages