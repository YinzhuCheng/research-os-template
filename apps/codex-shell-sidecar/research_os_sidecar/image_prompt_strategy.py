from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ImagePromptGuide:
    category_id: str
    display_name: str
    use_cases: list[str]
    required_focus: list[str]
    prompt_structure: list[str]
    negative_guidance: list[str]
    rewrite_tips: list[str]
    default_size: str = "1024x1024"
    default_quality: str = "high"
    default_format: str = "png"


IMAGE_PROMPT_GUIDES: dict[str, ImagePromptGuide] = {
    "people_avatar": ImagePromptGuide(
        category_id="people_avatar",
        display_name="People and avatars",
        use_cases=["realistic portraits", "anime avatars", "game character portraits", "professional profile images"],
        required_focus=["identity and role", "age range and temperament", "hair, outfit, expression", "camera distance", "lighting"],
        prompt_structure=["subject sentence", "visual details", "pose and expression", "background and lighting", "final usage"],
        negative_guidance=["no extra fingers", "no distorted face", "no text or watermark", "no copyrighted celebrity or character"],
        rewrite_tips=["Prefer one clear subject.", "Specify headshot, bust, half-body, or full-body.", "Add clean silhouette for game use."],
    ),
    "illustration_concept": ImagePromptGuide(
        category_id="illustration_concept",
        display_name="Illustration and concept design",
        use_cases=["book illustration", "poster illustration", "game concept art", "film concept frame"],
        required_focus=["story moment", "subject-environment relationship", "mood", "palette", "detail hierarchy"],
        prompt_structure=["theme", "main subject", "environment", "mood and palette", "rendering quality"],
        negative_guidance=["no vague style-word pileups", "no messy perspective", "no unreadable low-res clutter", "no text"],
        rewrite_tips=["Describe a concrete scene, not only a genre.", "Name foreground, midground, and background.", "Use cinematic but readable composition."],
    ),
    "product_advertising": ImagePromptGuide(
        category_id="product_advertising",
        display_name="Product and advertising",
        use_cases=["e-commerce product render", "packaging concept", "brand key visual", "campaign image"],
        required_focus=["product subject", "selling point", "material", "props", "brand tone"],
        prompt_structure=["product identity", "audience", "composition", "lighting and material", "safe blank space"],
        negative_guidance=["no fake trademark", "no malformed product", "no wrong text", "no cluttered background"],
        rewrite_tips=["Keep the product centered and recognizable.", "Request blank copy space instead of generated text.", "Specify material reflections."],
    ),
    "interior_architecture": ImagePromptGuide(
        category_id="interior_architecture",
        display_name="Interior and architecture",
        use_cases=["home render", "building exterior", "landscape design", "exhibition space"],
        required_focus=["space type", "viewpoint", "materials", "light sources", "functional zones"],
        prompt_structure=["space purpose", "design style", "key materials", "camera position", "realism level"],
        negative_guidance=["no impossible structures", "no floating furniture", "no warped perspective", "no fake dimensions"],
        rewrite_tips=["State view angle and lens feel.", "List 3-5 materials.", "Keep scale and circulation plausible."],
    ),
    "landscape_scene": ImagePromptGuide(
        category_id="landscape_scene",
        display_name="Landscape and scene",
        use_cases=["nature view", "city street", "sci-fi scene", "fantasy world", "game map ambience"],
        required_focus=["location", "time and weather", "foreground/midground/background", "motion", "environmental story"],
        prompt_structure=["scene sentence", "spatial layers", "lighting and weather", "landmarks", "usage and aspect ratio"],
        negative_guidance=["no empty generic scene", "no repeated texture", "no broken horizon", "no text"],
        rewrite_tips=["Use landmarks and atmospheric depth.", "Specify time of day.", "Include environmental storytelling details."],
    ),
    "anime_manga_cartoon": ImagePromptGuide(
        category_id="anime_manga_cartoon",
        display_name="Anime, manga, and cartoon",
        use_cases=["manga panel", "anime character", "chibi figure", "sticker", "original mascot"],
        required_focus=["character silhouette", "stylized proportions", "expression and gesture", "line style", "color-block relation"],
        prompt_structure=["character/action", "style family", "line and coloring", "background", "output usage"],
        negative_guidance=["no photorealistic skin", "no western 3D cartoon look unless requested", "no distorted limbs", "no copyrighted IP"],
        rewrite_tips=["Choose manga panel, anime key art, chibi, or sticker.", "Keep expression readable.", "Avoid direct IP references."],
    ),
    "japanese_anime_style": ImagePromptGuide(
        category_id="japanese_anime_style",
        display_name="Japanese anime style",
        use_cases=["JRPG assets", "visual novel standees", "anime-style game sprites", "VTuber material", "magical girl assets"],
        required_focus=["original design", "clean line art", "polished cel shading", "soft anime lighting", "game asset readability"],
        prompt_structure=[
            "state the original character, prop, tile, or scene and its game purpose",
            "specify Japanese anime production style, crisp line art, polished cel shading, soft gradients, and readable shape language",
            "define hair, costume, pose, palette, outline, and functional details",
            "define asset packaging: single asset, transparent background, large gutters, front view, icon, tile, or standee",
            "finish with quality constraints: high detail, crisp, polished, no text, no logo, no watermark",
        ],
        negative_guidance=[
            "no children's book watercolor look",
            "no western cartoon or 3D render",
            "no photorealistic rendering",
            "no text, logo, signature, or watermark",
            "no direct copy of copyrighted characters, uniforms, emblems, or magical-girl franchise motifs",
        ],
        rewrite_tips=[
            "For game sprites, prefer one asset per image or a clear grid sprite sheet with large gutters.",
            "For transparent assets, explicitly request transparent background and clean alpha-friendly edges.",
            "Use original magical-girl wording instead of naming copyrighted series.",
        ],
        default_size="2048x2048",
    ),
    "game_asset_japanese_anime": ImagePromptGuide(
        category_id="game_asset_japanese_anime",
        display_name="Japanese anime game asset",
        use_cases=[
            "JRPG character sprites",
            "magical-girl movement frames",
            "monster sprites",
            "transparent props",
            "RPG terrain tilesets",
            "HUD icons",
        ],
        required_focus=[
            "asset mode: single transparent asset, reference edit, animation frame set, same-category sheet, or tile/autotile set",
            "game role and exact runtime use",
            "style lock for consistent original Japanese anime magical-fantasy art",
            "clean silhouette and readable 64-128px sprite scale",
            "background and alpha contract",
            "post-generation validation criteria",
        ],
        prompt_structure=[
            "asset identity and role in the magical tower game",
            "Japanese 2D anime/JRPG production style with crisp line art, polished cel shading, controlled highlights, and coherent palette",
            "exact composition: one centered object, walk-cycle grid, regular tileset, or same-category icon sheet",
            "technical packaging: transparent background, PNG/WebP, large gutters, no text, no watermark, no cast shadows outside the asset",
            "consistency anchors: match approved reference character, palette, outline weight, camera angle, and sprite scale",
            "validation sentence: alpha must be present, parts must not touch borders, tiles must stitch cleanly, and sheet cells must be separable",
        ],
        negative_guidance=[
            "no mixed character/terrain/prop collage in one image",
            "no checkerboard baked into pixels unless explicitly requested for preview only",
            "no busy painted background behind cutout assets",
            "no direct copy of copyrighted magical-girl characters, uniforms, brooches, logos, poses, or franchise motifs",
            "no inconsistent chibi/realistic/3D style mixing inside one batch",
            "no unreadable text, watermark, signature, frame border, or UI labels",
        ],
        rewrite_tips=[
            "Heroine consistency: first choose one approved reference, then use edit/reference mode for idle and walk_down/up/left/right frames.",
            "Single assets: generate doors, stairs, keys, monsters, gems, HUD icons, and battle portraits one per transparent PNG.",
            "Sheets: use only same-category terrain/icons/decorations, with a regular grid, large gutters, and clear cell count.",
            "Tiles: request center, edge, corner, and transition tiles and validate with 3x3 or 5x5 stitch previews.",
            "If alpha, style, character identity, slice score, or tileability fails, redraw instead of overfitting the slicer.",
        ],
        default_size="2048x2048",
    ),
    "art_style": ImagePromptGuide(
        category_id="art_style",
        display_name="Art style image",
        use_cases=["oil painting", "watercolor", "cyberpunk poster", "retro poster", "pixel art", "ukiyo-e inspired art"],
        required_focus=["art movement or medium", "surface texture", "palette", "brush or pixel treatment", "composition era"],
        prompt_structure=["subject", "style or medium", "color and stroke", "composition", "forbidden elements"],
        negative_guidance=["no too many conflicting styles", "no low-quality scan look", "no unreadable muddy texture"],
        rewrite_tips=["Pick one dominant medium.", "State texture and palette.", "Avoid mixing incompatible style tags."],
    ),
    "education_infographic": ImagePromptGuide(
        category_id="education_infographic",
        display_name="Education and infographic",
        use_cases=["science illustration", "process diagram", "knowledge card", "teaching image", "technical schematic"],
        required_focus=["topic", "visual hierarchy", "icon relation", "readable whitespace", "text risk"],
        prompt_structure=["knowledge topic", "visual layout", "key objects", "color coding", "no text or placeholder-only text"],
        negative_guidance=["no large unreadable generated text", "no fake data", "no misleading medical or technical details"],
        rewrite_tips=["Ask for clean visual metaphors.", "Avoid actual labels unless post-edited manually.", "Use simple icons and layout blocks."],
    ),
    "image_edit_recreation": ImagePromptGuide(
        category_id="image_edit_recreation",
        display_name="Image editing and recreation",
        use_cases=["background replacement", "outpainting", "local repaint", "style transfer", "sketch to finished art"],
        required_focus=["what to preserve", "what to change", "mask or boundary", "style consistency", "output format"],
        prompt_structure=["input image summary", "preserve list", "change list", "style target", "forbidden changes"],
        negative_guidance=["do not change core identity", "do not break composition", "do not add unrelated objects"],
        rewrite_tips=["Separate preserve/change instructions.", "Mention alpha or transparent background if needed.", "Keep reference-image identity stable."],
    ),
    "social_media": ImagePromptGuide(
        category_id="social_media",
        display_name="Social media content",
        use_cases=["cover image", "article thumbnail", "short-video cover", "event poster", "campaign graphic"],
        required_focus=["platform ratio", "hook", "main subject", "blank space", "strong but clean color"],
        prompt_structure=["platform and use", "hook theme", "subject", "background and color", "copy-space without generated text"],
        negative_guidance=["no complex generated Chinese text", "no overstuffed layout", "no cheap template look"],
        rewrite_tips=["Use clear thumbnail composition.", "Reserve blank space for manual typography.", "Keep high contrast at small size."],
    ),
}


def prompt_guides_payload() -> dict[str, Any]:
    return {
        "schema_version": 3,
        "default_rewrite_model": "kimi/kimi-k2.6",
        "fallback_rewrite_model": "deepseek/deepseek-v4-pro",
        "max_yunwu_prompt_chars": 1000,
        "rewrite_policy": {
            "recommended_flow": [
                "select category",
                "ask Kimi or another multimodal/coding-capable model to rewrite the user intent using the selected guide",
                "validate prompt length <= 1000 characters",
                "call Yunwu image generation or edit endpoint",
                "record original prompt, rewritten prompt, category, model, parameters, and local output path",
            ],
            "required_json_fields": [
                "prompt",
                "negative_prompt",
                "size",
                "quality",
                "format",
                "category_id",
                "asset_mode",
                "role",
                "style_lock",
                "composition",
                "background_policy",
                "consistency_refs",
                "negative_constraints",
                "post_validation",
                "notes",
            ],
            "transparent_asset_tip": "For transparent assets, pass background=transparent as a request parameter and use format=png or webp. Prompt wording alone is not sufficient.",
            "edit_route_tip": "When no reference image exists but a transparent cutout is required, use the LCR transparent-asset edit route: it supplies a blank transparent seed PNG, calls /images/edits with background=transparent, and validates alpha afterwards.",
            "batching_tip": "Treat n>1 as unstable until health-checked; production batches should usually use concurrent n=1 draws with max concurrency 5.",
        },
        "game_asset_policy": {
            "reference_image_mode": "Use for heroine walk cycles, consistent monster families, and style-preserving redraws.",
            "single_asset_mode": "Use for doors, stairs, keys, gems, monsters, HUD icons, and battle portraits.",
            "sheet_mode": "Use only for same-category tilesets, HUD icons, or decorations with a regular grid and large gutters.",
            "tileability_mode": "Terrain prompts must specify center/edge/corner/transition tiles and require a 3x3 or 5x5 stitch preview.",
            "redraw_trigger": "If alpha, style, character consistency, sliceability, or tileability fails, redraw with stricter constraints.",
        },
        "guides": [asdict(guide) for guide in IMAGE_PROMPT_GUIDES.values()],
    }


def get_prompt_guide(category_id: str) -> ImagePromptGuide:
    normalized = str(category_id or "japanese_anime_style").strip()
    return IMAGE_PROMPT_GUIDES.get(normalized) or IMAGE_PROMPT_GUIDES["japanese_anime_style"]


def build_rewrite_instruction(
    *,
    category_id: str,
    user_prompt: str,
    target_style: str = "",
    size: str = "2048x2048",
    quality: str = "high",
    image_format: str = "png",
    transparent_background: bool = False,
    reference_image_mode: bool = False,
) -> dict[str, Any]:
    guide = get_prompt_guide(category_id)
    style = target_style.strip() or guide.display_name
    transparent_line = (
        "- If the asset must be cut out, request transparent background, clean alpha-friendly edges, and no cast shadow outside the object.\n"
        if transparent_background
        else ""
    )
    reference_line = (
        "- If reference images are provided, preserve the useful identity/composition cues but improve clarity and asset usability.\n"
        if reference_image_mode
        else ""
    )
    instruction = f"""You are a senior image prompt director for Yunwu gpt-image-2.
Rewrite the user's request into a production-ready English image prompt.

Hard requirements:
- Return JSON only, no Markdown.
- JSON fields: prompt, negative_prompt, size, quality, format, category_id, asset_mode, role, style_lock, composition, background_policy, consistency_refs, negative_constraints, post_validation, notes.
- prompt must be <= 1000 characters.
- Target style: {style}.
- For game assets, emphasize readable game asset, clean silhouette, crisp line art, polished cel shading.
- For transparent assets, the final tool call must pass background=transparent and format=png or webp; do not rely on the prompt alone.
- Prefer the transparent-asset edit route for sprites/props: it edits a blank transparent seed image with background=transparent.
- Transparent background means every pixel outside the asset silhouette must be alpha=0; it is not white, black, grey, paper, canvas, checkerboard, scenery, floor, or a shadow.
- Choose the right asset mode: single_transparent_asset, reference_edit, animation_frame_set, same_category_sheet, terrain_tileset, scene_concept, or ui_icon.
- For heroine or monster consistency, prefer reference_image_mode and state exactly what identity cues to preserve.
- For terrain, describe center/edge/corner/transition tiles and a 3x3/5x5 stitching validation target.
- For sheets, require regular grid layout, large gutters, no touching objects, and only one asset category per sheet.
- Include post_validation checks for alpha, size, style consistency, character consistency, sliceability, and tileability.
- Do not copy copyrighted characters, logos, franchise uniforms, signatures, or watermarks.
- Do not ask the image model to generate readable UI text.
{transparent_line}{reference_line}
Category guide: {guide.display_name}
Use cases: {"; ".join(guide.use_cases)}
Required focus: {"; ".join(guide.required_focus)}
Recommended structure: {"; ".join(guide.prompt_structure)}
Avoid: {"; ".join(guide.negative_guidance)}
Rewrite tips: {"; ".join(guide.rewrite_tips)}

User request:
{user_prompt}

Suggested parameters: size={size}, quality={quality}, format={image_format}
"""
    return {
        "category_id": guide.category_id,
        "display_name": guide.display_name,
        "instruction": instruction,
        "defaults": {"size": size, "quality": quality, "format": image_format},
        "guide": asdict(guide),
    }
