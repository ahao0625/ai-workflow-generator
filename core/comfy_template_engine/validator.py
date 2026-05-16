"""
Workflow validator
"""

def validate_workflow(workflow):

    errors = []

    if "nodes" not in workflow:
        errors.append("Missing nodes")

    if "links" not in workflow:
        errors.append("Missing links")

    node_ids = set()

    for node in workflow.get("nodes", []):

        node_id = node.get("id")

        if node_id in node_ids:
            errors.append(f"Duplicate node id: {node_id}")

        node_ids.add(node_id)

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
