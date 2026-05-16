"""
Workflow template selector
"""

TEMPLATE_MAP = {
    "sdxl": "sdxl_txt2img.json",
    "flux": "flux_txt2img.json"
}

def select_template(model_family):

    return TEMPLATE_MAP.get(
        model_family,
        "sdxl_txt2img.json"
    )
