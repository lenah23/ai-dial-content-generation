import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'

    bucket_client = DialBucketClient(api_key=API_KEY, endpoint=DIAL_URL)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_stream = BytesIO(image_bytes)

    upload_result = bucket_client.upload_file(
        file_stream=image_stream,
        file_name=file_name,
        mime_type=mime_type_png
    )

    return Attachment(
        title=file_name,
        url=upload_result["url"],
        type=mime_type_png
    )

def start() -> None:
    model_client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gpt-4o"
    )

    attachment = asyncio.run(_put_image())
    print("Attachment:", attachment)

    message = Message(
        role=Role.USER,
        content="What do you see on this picture?",
        custom_content=CustomContent(attachments=[attachment])
    )

    response = model_client.get_completion(messages=[message])
    print("AI response:", response)

start()