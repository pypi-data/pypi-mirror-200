from .metrics import PromotedMetrics, NonPublicMetrics, OrganicMetrics, PublicMetrics
from ._variant import Variant

class Media():
    def __init__(self, media_key: str, type: str, url: str = None, duration_ms: int = None, height: int = None, non_public_metrics: NonPublicMetrics = None, organic_metrics: OrganicMetrics = None, preview_image_url: str = None, promoted_metrics: PromotedMetrics = None, public_metrics: PublicMetrics = None, width: int = None, alt_text: str = None, variants: list[Variant] = None, ) -> None:
        self.media_key = media_key
        self.type = type
        self.url = url
        self.duration_ms = duration_ms
        self.height = height
        self.non_public_metrics = non_public_metrics
        self.organic_metrics = organic_metrics
        self.preview_image_url = preview_image_url
        self.promoted_metrics = promoted_metrics
        self.public_metrics = public_metrics
        self.width = width
        self.alt_text = alt_text
        self.variants = variants
    
    def __str__(self) -> str:
        str_representation = {
            "Type": self.type,
            "Desc": self.alt_text,
            "Size": f"{self.width}x{self.height}px" if self.width != None and self.height != None else None,
            "Views": self.public_metrics.view_count if self.public_metrics != None else None,
            "URL": self.url
        }
        clean_str = []
        for key, val in str_representation.items():
            if val != None:
                clean_str.append(f"{key}: {val}")
        return ' / '.join(clean_str)
