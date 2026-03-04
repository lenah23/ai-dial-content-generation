import base64
from pathlib import Path

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl

def start() -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    # 1. Create DialModelClient
    client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gpt-4o"
    )

    # 2A. Analyze image with base64
    base64_message = ContentedMessage(
        role=Role.USER,
        content=[
            ImgContent(
                type="image_url",
                image_url=ImgUrl(
                    url=f"data:image/png;base64,{base64_image}"
                )
            ),
            TxtContent(
                type="text",
                text="What do you see in this image?"
            )
        ]
    )
    print("Analyzing base64 image...")
    response_base64 = client.get_completion(messages=[base64_message])
    print("Base64 image response:", response_base64)

    # 2B. Analyze image with URL
    url_message = ContentedMessage(
        role=Role.USER,
        content=[
            ImgContent(
                type="image_url",
                image_url=ImgUrl(
                    url="https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"
                )
            ),
            TxtContent(
                type="text",
                text="What do you see in this image?"
            )
        ]
    )
    print("\nAnalyzing image from URL...")
    response_url = client.get_completion(messages=[url_message])
    print("URL image response:", response_url)

start()