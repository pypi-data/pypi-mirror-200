from enum import StrEnum

class MediaFields(StrEnum):
    """
    The Tweet will only return media fields if the Tweet contains media and if
    you've also included the expansions=attachments.media_keys query parameter
    in your request.
    """
    duration_ms = "duration_ms"
    height = "height"
    media_key = "media_key"
    preview_image_url = "preview_image_url"
    type = "type"
    url = "url"
    width = "width"
    public_metrics = "public_metrics"
    non_public_metrics = "non_public_metrics"
    organic_metrics = "organic_metrics"
    promoted_metrics = "promoted_metrics"
    alt_text = "alt_text"
    variants = "variants"
