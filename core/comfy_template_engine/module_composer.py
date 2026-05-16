"""
Composable workflow module system
"""

def compose(base_workflow, modules):

    workflow = base_workflow.copy()

    workflow.setdefault("modules", [])

    for module in modules:
        workflow["modules"].append(module)

    return workflow
