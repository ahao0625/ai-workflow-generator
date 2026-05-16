"""
Node capability registry
"""

NODE_CAPABILITIES = {
    "KSampler": {
        "inputs": [
            "model",
            "positive",
            "negative",
            "latent"
        ],
        "outputs": [
            "latent"
        ]
    }
}
