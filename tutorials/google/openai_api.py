import openai

from google.auth import default
import google.auth.transport.requests

import openai

import vertexai

from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Tool,
    ToolConfig,
)


def google_auth():

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())
    # Note: the credential lives for 1 hour by default (https://cloud.google.com/docs/authentication/token-types#at-lifetime); after expiration, it must be refreshed.

    ##############################
    # Choose one of the following:
    ##############################

    # If you are calling a Gemini model, set the ENDPOINT_ID variable to use openapi.
    ENDPOINT_ID = "openapi"

    # If you are calling a self-deployed model from Model Garden, set the
    # ENDPOINT_ID variable and set the client's base URL to use your endpoint.
    # ENDPOINT_ID = "YOUR_ENDPOINT_ID"

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/{ENDPOINT_ID}",
        api_key=credentials.token,
    )

def chat_completions():

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    )

    print(response)


def streaming_api():

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
        stream=True,
    )
    for chunk in response:
        print(chunk)


def self_deploy_model_chat():

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"
    # model_id = "gemma-2-9b-it"
    # endpoint_id = "YOUR_ENDPOINT_ID"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/{endpoint_id}",
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    )
    print(response)


def self_deployed_model_stream():

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # location = "us-central1"
    # model_id = "gemma-2-9b-it"
    # endpoint_id = "YOUR_ENDPOINT_ID"

    # Programmatically get an access token
    credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())

    # OpenAI Client
    client = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/{endpoint_id}",
        api_key=credentials.token,
    )

    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
        stream=True,
    )
    for chunk in response:
        print(chunk)


def function_calling():

    # TODO(developer): Update & uncomment below line
    # PROJECT_ID = "your-project-id"

    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location="us-central1")

    # Specify a function declaration and parameters for an API request
    get_product_sku_func = FunctionDeclaration(
        name="get_product_sku",
        description="Get the available inventory for a Google products, e.g: Pixel phones, Pixel Watches, Google Home etc",
        # Function parameters are specified in JSON schema format
        parameters={
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "Product name"}
            },
        },
    )

    # Specify another function declaration and parameters for an API request
    get_store_location_func = FunctionDeclaration(
        name="get_store_location",
        description="Get the location of the closest store",
        # Function parameters are specified in JSON schema format
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Location"}},
        },
    )

    # Define a tool that includes the above functions
    retail_tool = Tool(
        function_declarations=[
            get_product_sku_func,
            get_store_location_func,
        ],
    )

    # Define a tool config for the above functions
    retail_tool_config = ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            # ANY mode forces the model to predict a function call
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            # List of functions that can be returned when the mode is ANY.
            # If the list is empty, any declared function can be returned.
            allowed_function_names=["get_product_sku"],
        )
    )

    model = GenerativeModel(
        model_name="gemini-1.5-flash-002",
        tools=[retail_tool],
        tool_config=retail_tool_config,
    )
    response = model.generate_content(
        "Do you have the Pixel 8 Pro 128GB in stock?",
    )

    print(response.candidates[0].function_calls)
    # Example response:
    # [
    # name: "get_product_sku"
    # args {
    #   fields { key: "product_name" value { string_value: "Pixel 8 Pro 128GB" }}
    #   }
    # ]
