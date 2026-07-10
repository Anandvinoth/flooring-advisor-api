from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://anand-elangovan-9821-resource.services.ai.azure.com/api/projects/anand-elangovan-9821"

with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
    allow_preview=True,
) as project_client:

    openai_client = project_client.get_openai_client(
        agent_name="Pet-Proof-Flooring-Advisor"
    )

    response = openai_client.responses.create(
        input="List all PetPremier products available."
    )

    print(response.output_text)