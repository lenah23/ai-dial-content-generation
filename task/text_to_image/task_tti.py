import asyncio
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


class Size:
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    standard: str = "standard"
    hd: str = "hd"


async def _save_images(attachments: list[Attachment]):
    # 1. Create DIAL bucket client using async context manager
    async with DialBucketClient(base_url=DIAL_URL, api_key=API_KEY) as bucket_client:

        # 2. Iterate through images from attachments, download and save locally
        for attachment in attachments:
            if attachment.type and attachment.type.startswith("image/"):
                image_data = await bucket_client.get_file(attachment.url)

                filename = attachment.title or f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                with open(filename, "wb") as f:
                    f.write(image_data)

                # 3. Print confirmation
                print(f"Image saved locally: {filename}")


def start() -> None:
    # 1. Create DialModelClient
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="dall-e-3",
        api_key=API_KEY,
    )

    # 2. Generate image for "Sunny day on Bali"
    prompt_message = Message(
        role=Role.USER,
        content="Sunny day on Bali",
    )

    # 4. Configure the picture output via custom_fields
    custom_fields = {
        "size": Size.width_rectangle,
        "quality": Quality.hd,
        "style": Style.vivid,
    }

    # 5. Send request to the image generation model
    response = client.get_completion(
        messages=[prompt_message],
        custom_fields=custom_fields,
    )

    # 3. Get attachments via response.custom_content.attachments
    attachments: list[Attachment] = (
        response.custom_content.attachments if response.custom_content else []
    ) or []

    if not attachments:
        print("No attachments returned in the response.")
        return

    asyncio.run(_save_images(attachments))


start()