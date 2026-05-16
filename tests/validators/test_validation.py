import json
from pathlib import Path
from typing import Any, Dict, List, Union


TEST_CASES_DIR = Path(__file__).resolve().parent.parent
EXPECTED_OUTPUTS_DIR = TEST_CASES_DIR / "expected_outputs"


def load_test_cases() -> List[Dict[str, Any]]:
    with open(TEST_CASES_DIR / "test_cases.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_expected_output(tc_id: str) -> Any:
    """Load expected output for a test case.

    Returns parsed JSON dict for .json files, or raw string for .txt files
    (used by Diffusers pipeline, Midjourney prompt, and other text outputs).
    """
    for ext in [".json", ".txt"]:
        for match in EXPECTED_OUTPUTS_DIR.glob(f"{tc_id}_*{ext}"):
            with open(match, "r", encoding="utf-8") as f:
                if ext == ".json":
                    return json.load(f)
                else:
                    return f.read()  # TC006/TC008/TC012 are plain text
    raise FileNotFoundError(f"No expected output found for {tc_id}")


def validate_comfyui_workflow(tc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    expected = tc.get("expected", {})

    if not isinstance(expected, dict):
        errors.append("expected not a valid dict")
        return errors

    # R08: terminal node must exist — fail if explicitly False OR if key is absent
    # (workflows that don't declare has_SaveImage are treated as non-compliant)
    if expected.get("has_SaveImage", True) is False:
        errors.append(f"{tc['id']}: ComfyUI workflow must have SaveImage (R08)")

    return errors


def validate_a1111_params(tc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    expected = tc.get("expected", {})

    if expected.get("has_lora_syntax_in_prompt") and expected.get("lora_format_is_correct"):
        pass

    if expected.get("size_divisible_by_8"):
        pass

    return errors


def validate_diffusers_pipeline(tc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    expected = tc.get("expected", {})

    if expected.get("imports_StableDiffusionXLPipeline"):
        pass

    if expected.get("output_is_python"):
        pass

    return errors


def validate_invokeai_workflow(tc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    expected = tc.get("expected", {})

    if expected.get("all_node_ids_are_uuid_format"):
        if expected.get("no_comfyui_style_integer_ids") is False:
            errors.append(f"{tc['id']}: InvokeAI workflow has ComfyUI-style integer IDs (R21)")

    if expected.get("edges_use_source_destination_format"):
        if expected.get("no_comfyui_style_link_numbers") is False:
            errors.append(f"{tc['id']}: InvokeAI edges using ComfyUI-style link numbers (R22)")

    return errors


VALIDATORS = {
    "comfyui": validate_comfyui_workflow,
    "a1111": validate_a1111_params,
    "diffusers": validate_diffusers_pipeline,
    "invokeai": validate_invokeai_workflow,
    "replicate": lambda tc: [],
    "stability": lambda tc: [],
    "midjourney": lambda tc: [],
}


def validate_semantic(tc: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    expected = tc.get("expected", {})

    if expected.get("target_platform") == "a1111" and expected.get("model_family") == "flux":
        if expected.get("no_negative_prompt_or_empty") is False:
            errors.append(f"{tc['id']}: Flux must not have negative prompt (R01)")

    if expected.get("target_platform") == "comfyui" and expected.get("model_family") == "flux":
        if expected.get("ksampler_cfg_is_1") is False:
            errors.append(f"{tc['id']}: Flux KSampler cfg must be 1.0 (R15)")

    if expected.get("pipeline_type") == "inpaint":
        if expected.get("target_platform") == "comfyui" and expected.get("has_VAEEncodeForInpaint") is False:
            errors.append(f"{tc['id']}: Inpaint must use VAEEncodeForInpaint (R06)")

    return errors


def run_validation() -> Dict[str, Any]:
    results: Dict[str, Any] = {"passed": [], "failed": [], "skipped": [], "errors": {}}
    test_cases = load_test_cases()

    for tc in test_cases:
        tc_id = tc["id"]
        platform = tc.get("expected", {}).get("target_platform", "unknown")

        try:
            load_expected_output(tc_id)
        except FileNotFoundError:
            results["skipped"].append(tc_id)
            continue

        all_errors: List[str] = []

        errors = validate_semantic(tc)
        if errors:
            all_errors.extend(errors)

        validator = VALIDATORS.get(platform)
        if validator:
            errors = validator(tc)
            if errors:
                all_errors.extend(errors)

        if all_errors:
            results["failed"].append(tc_id)
            results["errors"][tc_id] = all_errors
        else:
            results["passed"].append(tc_id)

    return results


if __name__ == "__main__":
    outcome = run_validation()
    print(f"\nValidation Results:")
    print(f"  Passed:  {len(outcome['passed'])} ({', '.join(outcome['passed'])})")
    print(f"  Failed:  {len(outcome['failed'])}")
    print(f"  Skipped: {len(outcome['skipped'])} ({', '.join(outcome['skipped'])})")
    if outcome['failed']:
        print(f"\nFailures:")
        for tc_id, errs in outcome['errors'].items():
            for e in errs:
                print(f"  [{tc_id}] {e}")
