# Demo Video Guide

This guide will help you create a 5-10 minute demonstration video showcasing the QA Agent system.

## Pre-Recording Checklist

- [ ] Backend is running (FastAPI)
- [ ] Streamlit UI is running
- [ ] All project assets are in `project_assets/` folder
- [ ] `.env` file is configured with valid API key
- [ ] Screen recording software is ready
- [ ] Browser window is clean and maximized
- [ ] Close unnecessary applications

## Demo Script (8-10 minutes)

### Part 1: Introduction (1 minute)

**Script:**
"Hello! Today I'll demonstrate the Autonomous QA Agent - an intelligent system that generates test cases and Selenium scripts from documentation. This system uses AI and RAG (Retrieval-Augmented Generation) to create comprehensive, documentation-grounded test plans."

**Actions:**
- Show the Streamlit home page
- Briefly explain the 4-step process shown on screen
- Show the dashboard with initial stats (all zeros)

### Part 2: Document Upload (2 minutes)

**Script:**
"First, we'll upload our support documents. For this demo, we have an e-commerce checkout page and its documentation including product specifications, UI/UX guidelines, API endpoints, and test scenarios."

**Actions:**
1. Navigate to "Document Upload" page
2. Show the file upload interface
3. Click "Browse files" and select all files from `project_assets/`:
   - `checkout.html`
   - `product_specs.md`
   - `ui_ux_guide.txt`
   - `api_endpoints.json`
   - `test_scenarios.md`
4. Show the selected files (5 files)
5. Click "Upload Documents" button
6. Wait for success message
7. Show the uploaded files list

**Key Points to Mention:**
- "The system supports multiple formats: MD, TXT, JSON, PDF, and HTML"
- "These documents contain all the business rules and UI specifications"
- "Everything from discount codes to form validation rules is documented"

### Part 3: Build Knowledge Base (2 minutes)

**Script:**
"Now we'll build the knowledge base. The system will process these documents, extract text, create chunks, generate embeddings, and store them in a vector database for semantic search."

**Actions:**
1. Scroll to "Build Knowledge Base" section
2. Read the info box explaining what will happen
3. Click "Build Knowledge Base" button
4. Show the progress/spinner
5. Wait for success message with details:
   - Files processed: 5
   - Chunks created: ~100+
6. Show the updated status in sidebar (green checkmark)
7. Show the Knowledge Base Status section with metrics

**Key Points to Mention:**
- "The system uses ChromaDB for vector storage"
- "Text is chunked with overlap for better context"
- "Sentence transformers generate embeddings"
- "This enables semantic search - finding relevant info by meaning, not just keywords"

### Part 4: Generate Test Cases (2-3 minutes)

**Script:**
"Now let's generate test cases. The AI agent will search the knowledge base for relevant information and create structured, documentation-grounded test cases."

**Actions:**
1. Navigate to "Test Case Generation" page
2. Show the suggested scenarios dropdown
3. Select: "Generate all positive and negative test cases for the discount code feature"
4. Click "Generate Test Cases" button
5. Show the generation progress (30-60 seconds)
6. When complete, scroll through generated test cases
7. Expand 2-3 test cases to show details:
   - TC-001: Valid discount code SAVE15
   - TC-002: Invalid discount code
   - TC-003: Empty discount code
8. Point out key fields:
   - Test ID
   - Feature
   - Test Scenario
   - Test Type (positive/negative)
   - Priority
   - Test Steps
   - Expected Result
   - **Grounded In** (source document)

**Key Points to Mention:**
- "Each test case references its source document - no hallucinations"
- "The system generates both positive and negative test scenarios"
- "Test steps are detailed and actionable"
- "Priority levels help with test execution planning"
- "Notice the 'Grounded In' field - this shows which document provided this information"

**Optional:**
- Show export options (JSON and Markdown download)
- Generate another set with different query

### Part 5: Generate Selenium Script (2-3 minutes)

**Script:**
"Finally, let's convert a test case into an executable Selenium Python script. The agent will analyze the test case, examine the HTML structure, and generate production-ready code."

**Actions:**
1. Navigate to "Script Generation" page
2. Upload `checkout.html` file
3. Show the test case dropdown
4. Select test case: "TC-001: Discount Code - Valid discount code SAVE15"
5. Expand "View Selected Test Case Details" to show the test case
6. Click "Generate Selenium Script" button
7. Show generation progress (30-60 seconds)
8. When complete, scroll through the generated script
9. Point out key elements:
   - Imports (selenium, webdriver_manager, unittest)
   - Class structure (unittest.TestCase)
   - setUp and tearDown methods
   - Test method with detailed steps
   - Explicit waits (WebDriverWait)
   - Assertions
   - Comments explaining each step
10. Show the "How to Run This Script" instructions
11. Click "Download Script" button

**Key Points to Mention:**
- "The script uses actual element IDs and selectors from the HTML"
- "It includes proper waits, not just sleep statements"
- "WebDriver is managed automatically via webdriver-manager"
- "Comprehensive assertions verify the expected behavior"
- "Comments make the code maintainable"
- "The script is production-ready and can run as-is"

**Optional but Impressive:**
- Actually run the script (if time permits and setup is ready)
- Show the browser automation in action
- Show test passing with green output

### Part 6: Dashboard Overview (1 minute)

**Script:**
"Let's look at the dashboard to see an overview of our session."

**Actions:**
1. Navigate to "Dashboard" page
2. Show metrics:
   - Uploaded Files: 5
   - Knowledge Chunks: ~100+
   - Test Cases Generated: 3-5
   - Scripts Generated: 1
3. Show uploaded documents list
4. Show test case summary (by type and priority)
5. Show system information (LLM provider, Vector DB status)

**Key Points to Mention:**
- "The dashboard provides a quick overview of the entire session"
- "You can see what documents are loaded, how many test cases exist"
- "System information shows which LLM provider is being used"

### Part 7: Conclusion (30 seconds)

**Script:**
"This demonstration showed how the Autonomous QA Agent can transform documentation into actionable test cases and executable scripts. The entire process is grounded in your actual documentation, ensuring accuracy and reducing hallucinations. The system supports multiple LLM providers, handles various document formats, and generates production-ready code. Thank you for watching!"

**Actions:**
- Show the home page one final time
- Maybe show the README or project structure briefly
- End recording

## Recording Tips

### Technical Setup
- **Resolution:** 1920x1080 minimum
- **Frame Rate:** 30 fps minimum
- **Audio:** Clear microphone, no background noise
- **Browser:** Use Chrome or Firefox, maximize window
- **Recording Software:** OBS Studio, Camtasia, or similar

### Presentation Tips
1. **Pace:** Speak clearly and at a moderate pace
2. **Cursor:** Move cursor deliberately, don't rush
3. **Highlights:** Use cursor to point out important elements
4. **Pauses:** Brief pause after clicking buttons to show results
5. **Editing:** Edit out long wait times (like 60-second generation)

### What to Show
✓ **DO Show:**
- Clean, organized interface
- Successful operations
- Generated outputs
- Key features and benefits
- Source document references

✗ **DON'T Show:**
- Errors or failed operations (unless demonstrating error handling)
- Your API keys or sensitive info
- Unnecessary file system navigation
- Multiple failed attempts

### Time Management

If running short on time, **cut:**
- Second test case generation
- Multiple test case expansions
- Extended dashboard exploration

If you have extra time, **add:**
- Actually run a generated Selenium script
- Show the checkout.html in browser
- Demonstrate a second scenario
- Show export functionality

## Post-Recording Checklist

- [ ] Video is 5-10 minutes long
- [ ] All 4 main phases shown (upload, build KB, generate tests, generate script)
- [ ] Audio is clear
- [ ] No sensitive information visible
- [ ] Key features are highlighted
- [ ] Generated outputs are visible and readable
- [ ] Video demonstrates the full workflow

## Video Editing Notes

### Sections to Keep Short (Speed Up 1.5-2x)
- File upload process
- Long loading/generation times (keep 2-3 seconds)
- Scrolling through long documents

### Sections to Keep Normal Speed
- Explanations and narration
- Pointing out key features
- Showing generated test cases
- Showing generated scripts

### Add Annotations (Optional)
- Arrow pointing to "Grounded In" field
- Highlight key code sections in generated script
- Callout boxes for important messages
- Chapter markers for different sections

## Alternative: Recorded Demo With Voiceover

If you prefer, you can:
1. Record the screen without narration
2. Add voiceover later in editing
3. This allows for retakes and cleaner audio

## Sample Opening Script

"Hello, I'm presenting the Autonomous QA Agent - an intelligent system for generating test cases and Selenium scripts from project documentation.

This isn't just another code generator. The system uses Retrieval-Augmented Generation to ensure every test case is grounded in your actual documentation. No hallucinations, no made-up features - just accurate, comprehensive test coverage based on what you provide.

The system consists of three main components:
1. A FastAPI backend for document processing and AI orchestration
2. A ChromaDB vector database for semantic search
3. A Streamlit interface for intuitive interaction

Let's see it in action."

## Sample Closing Script

"As you've seen, the QA Agent provides an end-to-end solution for automated test generation. From uploading diverse document types, to building a searchable knowledge base, to generating structured test cases with full traceability, to producing executable Selenium scripts - all in a matter of minutes.

The system is designed to be:
- **Accurate** - All outputs are grounded in provided documentation
- **Flexible** - Supports multiple LLM providers and document formats
- **Professional** - Generates production-ready, well-structured code
- **Traceable** - Every test case references its source

The code is available in the repository along with comprehensive documentation for setup and usage. Thank you for your time."

## Common Issues During Demo

### Issue: Generation Takes Too Long
**Solution:** Edit the video to speed up the wait time. Keep 2-3 seconds of the spinner, then jump to the result.

### Issue: Generation Fails
**Solution:** Have a backup recording or restart. Make sure API key is valid and has quota.

### Issue: Script Not Perfect
**Solution:** This is actually fine - mention that "the script can be further refined, but shows the core structure and logic."

### Issue: Browser Window Too Small
**Solution:** Maximize the browser and zoom to 90% or 100% for optimal viewing.

## Export Settings

### For YouTube/Online
- Format: MP4 (H.264)
- Resolution: 1920x1080
- Bitrate: 5-8 Mbps
- Audio: AAC, 128-192 kbps

### For Local Submission
- Same as above, or
- Use the platform's recommended settings

## File Naming
- `qa_agent_demo_[your_name].mp4`
- `qa_agent_demonstration.mp4`
- Keep it professional and clear

---

Good luck with your demo! Remember: confidence, clarity, and showing the system's capabilities are key.
