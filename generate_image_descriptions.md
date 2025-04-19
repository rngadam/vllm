### STRICT INSTRUCTION:
Analyze the provided image(s), which are thumbnails extracted from a video sequence at different moments. Perform a thorough visual analysis of **all** provided images to understand the content comprehensively.

### TASKS TO PERFORM:
1.  Based on the analysis of **all** provided images, generate a synthesized `suggested_title` and `detailed_description` for the entire video sequence.
2.  Generate a **single, comprehensive list** of `relevant_keywords`. This list must be derived from the analysis of **all** images and MUST AGGREGATE terms describing:
    * Main visual elements (objects, animals, landmarks, etc.).
    * Detected person types (e.g., 'man', 'woman in suit', 'group of children', 'silhouette').
    * Identified locations or environments (e.g., 'office', 'beach', 'city street at night', 'forest').
    * Detected actions or events (e.g., 'talking', 'running', 'presenting data', 'cooking', 'sunset').
    * Dominant or notable colors (e.g., 'blue', 'vibrant red', 'pastel colors').
    * Any readable text found in the images.
    * Conceptual keywords or themes suggested by the content (e.g., 'technology', 'nature', 'teamwork', 'celebration', 'learning').

### MANDATORY OUTPUT FORMAT:
Your response MUST be only a valid JSON object, strictly adhering to the structure defined below. Do not include any introductory text, explanation, or concluding text outside the JSON object itself.

### REQUIRED JSON STRUCTURE:
Use only the following JSON structure. Fill each key with the most accurate and detailed information possible based on your comprehensive analysis.

{
  "suggested_title": "string | null", // Propose a concise title (max 70 chars) reflecting the OVERALL video content, based on all images.
  "detailed_description": "string | null", // Write an informative description (2-4 sentences) summarizing the entire video, synthesizing findings from all images.
  "relevant_keywords": [
    "string" // Comprehensive list of keywords derived from ALL images. MUST include terms for elements, person types, locations, actions, colors, text, AND concepts/themes. Aim for a rich and diverse list (15-25+ keywords if possible).
  ]
}
