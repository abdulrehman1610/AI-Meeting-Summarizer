# Changelog

## [2026-05-15]

### Fixed
- Fixed `KeyError: 'choices'` in `modules/llm_processor.py` when handling OpenRouter API responses.
  - **Issue:** The code expected a successful response containing a `"choices"` key. If OpenRouter returned an error (e.g., due to an invalid model name or API key issues), the returned JSON contained an `"error"` key instead, causing the app to crash.
  - **Fix:** Added error handling to check for the `"choices"` key before accessing it. If missing, the error message from the API is logged and returned gracefully to the UI.
- Added safety checks for JSON parsing to handle cases where the model returns response text wrapped in markdown code blocks (e.g., ` ```json ... ``` `).
- Fixed an issue where the model name `qwen/qwen3-4b:free` caused a `404 No endpoints found` error from OpenRouter, as the model does not exist.
  - **Fix:** Updated the model in `modules/llm_processor.py` to a valid and capable free model: `qwen/qwen-2.5-7b-instruct:free`.
- Fixed a `JSON Parsing Error` caused by the AI model generating malformed JSON.
  - **Issue:** The model (`qwen-2.5-coder-32b-instruct`) left the value for the `"deadline"` key empty (e.g., `"deadline": \n }`) instead of setting it to `null`, which broke Python's `json.loads`.
  - **Fix:** Added `"response_format": {"type": "json_object"}` to the OpenRouter payload to strictly enforce valid JSON generation by the model.
- Improved LLM summarization quality in `modules/llm_processor.py`.
  - **Issue:** The model was sometimes lazily repeating the full transcript in the summary field instead of distilling key points.
  - **Fix:** Rewrote the prompt with strict "CRITICAL" instructions forbidding the model from just transcribing the input, and guiding it to focus on key insights and actionable items.
- Fixed `JSON Parsing Error` when handling OpenRouter API responses.
  - **Issue:** The `qwen/qwen-2.5-coder-32b-instruct` model was prepending conversational filler text (e.g., "Here is the summary in JSON format: \n ```json...") to its output. The previous parsing logic (`text.startswith("```json")`) was too strict and failed to clean up the string, causing `json.loads` to crash.
  - **Fix:** Implemented a robust Regular Expression (`regex`) approach in `modules/llm_processor.py` to extract the JSON block regardless of surrounding conversational text.
- Fixed persistent `JSON Parsing Error` where the model still generated trailing empty values (e.g., `"deadline": \n }`) despite instructions.
  - **Issue:** Even with JSON object format enforced, the model occasionally left values empty before a closing brace or comma.
  - **Fix:** Added a regex substitution `re.sub(r':\s*(?=[,}])', ': null', text)` in `modules/llm_processor.py` to auto-fill empty values with `null` before parsing.
- Fixed hardcoded UI text in `app.py`.
  - **Issue:** The loading spinner text was hardcoded to say "via Ollama..." even when OpenRouter was selected.
  - **Fix:** Updated the spinner text to dynamically display the active backend name using f-string interpolation.
- Fixed UI results disappearing on interaction (e.g., clicking "Send Email").
  - **Issue:** Streamlit reruns the script on interaction. Since processing results were only generated inside the "Process Meeting" button block, they disappeared when other widgets (like the email button) were clicked.
  - **Fix:** Refactored `app.py` to store results in `st.session_state` so they persist across reruns. Added logic to reset state when a new file is uploaded.

### Added
- Implemented Phase 5: Bonus Feature (Email Module).
  - **Feature:** Added the ability to send the meeting summary and action items via email directly from the app.
  - **Details:** Created `modules/email_dispatcher.py` to handle SMTP email sending and updated `app.py` with an email input field and "Send Email" button. Added default SMTP server and port configurations to `.env`.
