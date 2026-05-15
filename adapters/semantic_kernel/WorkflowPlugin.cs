// Semantic Kernel Plugin — AI Workflow Generator
// .NET C# Plugin for Microsoft Semantic Kernel
// Install: Add this file to your SK project

using System.ComponentModel;
using Microsoft.SemanticKernel;
using System.Text.Json;

namespace AiWorkflowGenerator;

public class WorkflowPlugin
{
    private readonly Kernel _kernel;

    public WorkflowPlugin(Kernel kernel)
    {
        _kernel = kernel;
    }

    [KernelFunction("generate_workflow")]
    [Description("Generate an AI image/video generation workflow file for the specified platform.")]
    [return: Description("Generated workflow output containing workflow file content, dependencies, and instructions")]
    public async Task<string> GenerateWorkflowAsync(
        [Description("Natural language description of the desired workflow. Include target platform, model, and features.")]
        string description,

        [Description("Target platform: comfyui, a1111, diffusers, replicate, stability, midjourney, dalle")]
        string targetPlatform = "comfyui",

        [Description("Model family: sd15, sdxl, flux, sd3, video")]
        string modelFamily = "sdxl",

        [Description("Pipeline type: txt2img, img2img, inpaint, txt2vid, img2vid")]
        string pipelineType = "txt2img"
    )
    {
        var prompt = BuildGeneratePrompt(description, targetPlatform, modelFamily, pipelineType);

        var result = await _kernel.InvokePromptAsync(prompt);

        return result.ToString();
    }

    [KernelFunction("validate_workflow")]
    [Description("Validate an existing workflow against known compatibility rules.")]
    [return: Description("Structured validation report with issues and warnings")]
    public async Task<string> ValidateWorkflowAsync(
        [Description("The workflow content to validate (JSON/Python/prompt)")]
        string workflowContent,

        [Description("The platform this workflow targets")]
        string targetPlatform = "comfyui"
    )
    {
        var prompt = BuildValidatePrompt(workflowContent, targetPlatform);

        var result = await _kernel.InvokePromptAsync(prompt);

        return result.ToString();
    }

    [KernelFunction("convert_workflow")]
    [Description("Convert a workflow from one platform format to another.")]
    [return: Description("Converted workflow in target platform format")]
    public async Task<string> ConvertWorkflowAsync(
        [Description("The existing workflow content")]
        string sourceWorkflow,

        [Description("Source platform: comfyui, a1111, diffusers, midjourney")]
        string sourcePlatform,

        [Description("Target platform to convert to")]
        string targetPlatform
    )
    {
        var prompt = BuildConvertPrompt(sourceWorkflow, sourcePlatform, targetPlatform);

        var result = await _kernel.InvokePromptAsync(prompt);

        return result.ToString();
    }

    private static string BuildGeneratePrompt(
        string description, string platform, string model, string pipeline)
    {
        return $"""
            You are an AI workflow generator.

            ## User Request
            {description}

            ## Configuration
            - Target Platform: {platform}
            - Model Family: {model}
            - Pipeline Type: {pipeline}

            Follow this process:
            1. Confirm target platform is {platform}
            2. Build IR from the description
            3. Validate against model compatibility rules
            4. Render to {platform} native format
            5. Output: workflow file + dependencies.md + usage notes

            Critical rules:
            - Flux models have NO negative prompt
            - Inpaint must use VAEEncodeForInpaint for ComfyUI
            - LoRA nodes must chain both MODEL and CLIP
            - Every ComfyUI workflow needs SaveImage/PreviewImage terminal node

            Generate the complete workflow now. Output in this JSON wrapper:
            {{
              "workflow": "<workflow file content>",
              "dependencies": "<markdown dependency list>",
              "instructions": "<usage notes>"
            }}
            """;
    }

    private static string BuildValidatePrompt(string content, string platform)
    {
        return $"""
            You are an AI workflow validator.

            ## Validation Target
            Platform: {platform}

            ## Workflow to Validate
            ```
            {content}
            ```

            Apply all known validation rules:
            1. R01: Flux no negative prompt (CRITICAL)
            2. R02: SDXL-Turbo low steps (CRITICAL)
            3. R06: Inpaint uses VAEEncodeForInpaint (CRITICAL)
            4. R07: LoRA threads MODEL and CLIP (CRITICAL)
            5. R08: Terminal node present (CRITICAL)
            6. R09: Unique node IDs (CRITICAL)
            7. R10: Type-safe connections (CRITICAL)
            8. R15: Flux KSampler cfg=1 (CRITICAL)
            9. R16: A1111 LoRA syntax (ADVISORY)
            10. R17: A1111 size divisible by 8 (ADVISORY)

            Output a structured JSON validation report:
            {{
              "passed": true/false,
              "critical_issues": [...],
              "advisory_warnings": [...],
              "suggestions": [...]
            }}
            """;
    }

    private static string BuildConvertPrompt(string source, string fromPlatform, string toPlatform)
    {
        return $"""
            You are an AI workflow converter.

            ## Conversion Task
            Convert from {fromPlatform} to {toPlatform}.

            ## Source Workflow
            ```
            {source}
            ```

            Steps:
            1. Parse the {fromPlatform} source to extract IR fields
            2. Validate IR (note any losses from cross-platform mapping)
            3. Render to {toPlatform} native format
            4. Note conversion losses (e.g., structural control lost, LoRA syntax change)

            Output in this JSON wrapper:
            {{
              "workflow": "<converted workflow>",
              "conversion_losses": ["<list of things that could not map perfectly>"],
              "dependencies": "<updated dependencies>",
              "instructions": "<platform-specific loading instructions>"
            }}
            """;
    }
}
