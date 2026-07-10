from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import re

ENDPOINT = "https://anand-elangovan-9821-resource.services.ai.azure.com/api/projects/anand-elangovan-9821"


def clean_response(text: str) -> str:
    import re

    text = re.sub(r"【[^】]*】", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def ask_agent(question: str) -> str:

    with AIProjectClient(
        endpoint=ENDPOINT,
        credential=DefaultAzureCredential(),
        allow_preview=True,
    ) as project_client:

        openai_client = project_client.get_openai_client(
            agent_name="Pet-Proof-Flooring-Advisor"
        )

        response = openai_client.responses.create(
            input=f"""
        Return ONLY raw JSON.

        Do not use markdown.
        Do not use code blocks.
        Do not use ```json.

        Format:

        {{
          "recommendations": [...]
        }}

        Question:
        {question}
        """
        )
        print(response.output_text)
        # cleaned =   clean_response(response.output_text)

        cleaned = clean_response(response.output_text)

        # print("RAW:")
        # print(response.output_text)
        #
        # print("CLEANED:")
        # print(cleaned)

        return cleaned

