### STRICT INSTRUCTION:
Analyze the provided image(s), which are thumbnails extracted from a video sequence at different moments.

### TASKS TO PERFORM:
1.  Perform a thorough and **individual** visual analysis for **each provided image**.
2.  For **each image**, create a JSON object describing its specific visual content and place this object into the `visual_analysis_per_image` array.
3.  Based on the analysis of **all** provided images, generate the synthesized metadata: `suggested_title`, `detailed_description`, `relevant_keywords`, and the `synthesized_content_evaluation` object (which now includes aggregated lists of detected items).

### MANDATORY OUTPUT FORMAT:
Your response MUST be only a valid JSON object, without any introductory text, explanation, or concluding text outside the JSON object itself.

### REQUIRED JSON STRUCTURE:
You must use the following JSON structure. Fill each key with the most accurate and detailed information possible. If information cannot be clearly identified or is not relevant based on the image(s), use `null` for keys expecting a string or an empty array `[]` for keys expecting a list. Do not use newlines in the output.

{
  "suggested_title": "string | null", // Propose a concise title (max 70 chars) reflecting the OVERALL video content, based on all images.
  "detailed_description": "string | null", // Write an informative description (2-4 sentences) summarizing the entire video, synthesizing findings from all images, including key elements and actions observed.
  "relevant_keywords": [
    "string" // List of keywords (8-15+) relevant to the COMPLETE video, derived from all images. Should encompass elements from the aggregated lists below (objects, person types, locations, actions, concepts, themes).
  ],
  "visual_analysis_per_image": [ // <= THIS IS NOW AN ARRAY
    // One JSON object will be generated here FOR EACH provided image.
    // Example for the first image:
    {
      "image_index": 0, // (Optional but recommended) Index of the analyzed image (0, 1, 2...)
      "main_elements": [
        "string" // List objects, animals, or central subjects in THIS image.
      ],
      "person_types": [
        "string" // Describe types of people visible in THIS image (e.g., 'man in shirt', 'silhouette'). Do not identify specific individuals.
      ],
      "location_environment": {
        "type": "string | null", // General location type for THIS image (e.g., 'Indoor', 'Outdoor', 'Office').
        "details": "string | null" // Specific location details for THIS image (e.g., 'Modern conference room', 'Dense forest at dusk').
      },
      "action_event": "string | null", // Main action or event happening in THIS image (e.g., 'Person presenting graph', 'Group discussion').
      "dominant_colors": [
        "string" // List the 3-5 dominant or most striking colors in THIS image.
      ],
      "readable_text_in_image": "string | null" // Transcribe any clearly readable text within THIS image. Use null if none.
    }
    // , { ... analysis for the second image ... },
    // ... etc. for each provided image.
  ],
  "synthesized_content_evaluation": { // <= Synthesis based on ALL images
    "mood_tone": "string | null", // Overall mood or tone perceived from ALL images (e.g., 'Professional', 'Joyful', 'Tense', 'Calm').
    "suggested_category": "string | null", // Most likely category for the COMPLETE video (e.g., 'Tutorial', 'Vlog', 'News', 'Documentary').
    "potential_themes": [
      "string" // List general themes the video might cover, based on ALL images (e.g., 'Technology', 'Teamwork', 'Nature').
    ],
    "all_detected_elements": [ // NEW: Aggregated list
        "string" // Unique list of all main elements detected across ALL images.
    ],
    "all_detected_person_types": [ // NEW: Aggregated list
        "string" // Unique list of all person types detected across ALL images.
    ],
    "all_detected_locations": [ // NEW: Aggregated list
        "string" // Unique list combining all location types and details detected across ALL images.
    ],
    "all_detected_actions": [ // NEW: Aggregated list
        "string" // Unique list of all actions/events detected across ALL images.
    ],
    "all_detected_colors": [ // NEW: Aggregated list
        "string" // Unique list of all dominant colors detected across ALL images.
    ],
    "all_detected_text": [ // NEW: Aggregated list
        "string" // Unique list of all readable text snippets detected across ALL images.
    ]
  }
}
