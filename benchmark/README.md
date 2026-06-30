# Calendar Extraction — Run Instructions

## Purpose

Collect structured extractions from a set of calendar images. Each image is a
calendar week view; have the model read it and record what it sees, image by
image. This benchmark exists both to compare how well models extract calendar
information and to discover the settings and prompts that best support that
ability.

## Isolation (important)

Each image **must** be extracted in its own clean context, with **no information
carried over from any other image**. The same week is shown in every image, so a
shared context would let the model reuse what it read from an easier image to
answer a harder one — which invalidates the results, especially the
perspective-robustness measurement.

Therefore: run **each image in a fresh session**, or dispatch **one sub-agent per
image**. Never process two images in the same conversation/context, and never
let the model see another image, the previous answers, or earlier reasoning.
One image in, one extraction out, then discard the context.

## Instructions

1. Open `prompts/extraction_prompt.md`.
2. Make a working copy of `results/results-template.md` and fill in the run
   metadata at the top — the model identifier, the run date, your **submitter
   tag**, and the exact **server start command** you used — and paste the
   **exact extraction prompt** into its block. See *Model identifier, server
   command and prompt* below.
3. For each image in `images/`, in **filename order**, start a **fresh session**
   (or a **new sub-agent**) and give the model that single image together with
   the extraction prompt. Paste the model's YAML output into the matching
   `## Image <name>` section of your results copy.
4. You do **not** have to do every image in one go — sections you leave empty are
   **skipped**, so a partial file is valid. Keep the metadata block unchanged and
   you can complete it by re-uploading later without double-counting earlier
   images.

Do not change the prompt's intent, do not reorder or relabel events, and do not
add information of your own to the extractions.

## Model identifier, server command and prompt

Identify the model by its **full, unambiguous name**. For Hugging Face models use
the repository path including the lab/tuner and the quantization tag, e.g.
`unsloth/gemma-3-27b-it-qat-GGUF:UD-Q4_K_XL`. Different labs quantize the same
base model differently, so the bare base name is not enough to reproduce a run.

Record the **exact server start command** you used (the `llama-server` / `ollama`
/ `vLLM` command line, or other launcher). One command line documents the quant,
context length and sampling in a single reproducible place; for a hosted / API
model, give the **service URL** instead.

Paste the **exact extraction prompt** you gave the model into the
*Extraction prompt used* block (the shipped prompt if you did not change it).
This is what lets good prompts be identified, compared and reproduced — runs are
grouped by the prompt you actually used, not by a label.

## Custom prompts (if you experiment)

Trying your own extraction prompt is encouraged — finding prompts that help
models read calendars is an explicit goal of this benchmark. Just keep these
principles, or the result stops being meaningful and comparable:

1. **One prompt for every image.** Use the exact same prompt for all images. Do
   not tune it to a particular image, condition or application. A prompt that
   only scores well because it bakes in app-specific quirks (or, worse, expected
   values) is not a real result.
2. **Keep it practical.** Write it the way you would for real, everyday use —
   something a user could drop into an actual workflow or skill — not a
   benchmark-specific contraption.
3. **No leaked data.** The model gets only the image and the prompt. Never put
   any event data, times, titles, counts or hints drawn from the images into the
   prompt; the model must read everything itself.

## Completion

Return the completed results file as described in `../CONTRIBUTING.md` (pull
request or issue), or hand it to the benchmark administrator for evaluation.
