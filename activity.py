import database
import utils
import openai


zach = "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"
dong = "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"
justin = "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"


def main():
	client = openai.OpenAI(api_key=justin)
	relevant_pages = utils.get_relevant_pages("acciona", "revenue")
	print(relevant_pages)
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


if __name__ == "__main__":
	main()