"""
Workflow parameter injector
"""

def find_node(workflow, class_type):
    for node in workflow.get("nodes", []):
        if node.get("type") == class_type:
            return node
    return None


def inject_parameters(workflow, parameters):
    """
    Safe parameter injection.
    Only scalar parameters should be injected.
    """

    for node in workflow.get("nodes", []):

        # Prompt nodes
        if node.get("type") == "CLIPTextEncode":
            widgets = node.get("widgets_values", [])
            if widgets and "prompt" in parameters:
                widgets[0] = parameters["prompt"]

        # KSampler
        if node.get("type") == "KSampler":
            widgets = node.get("widgets_values", [])

            # seed
            if len(widgets) > 0 and "seed" in parameters:
                widgets[0] = parameters["seed"]

            # steps
            if len(widgets) > 2 and "steps" in parameters:
                widgets[2] = parameters["steps"]

            # cfg
            if len(widgets) > 3 and "cfg" in parameters:
                widgets[3] = parameters["cfg"]

    return workflow
