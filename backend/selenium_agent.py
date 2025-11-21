"""
Selenium Script Generation Agent - Generates executable Selenium Python scripts from test cases.
"""

from typing import Dict, Any
from backend.llm_handler import LLMHandler
from backend.vector_db import VectorDatabase


class SeleniumScriptAgent:
    """Agent for generating Selenium test scripts"""
    
    def __init__(self, vector_db: VectorDatabase, llm_handler: LLMHandler):
        """
        Initialize Selenium script agent.
        
        Args:
            vector_db: Vector database instance
            llm_handler: LLM handler instance
        """
        self.vector_db = vector_db
        self.llm = llm_handler
    
    def generate_selenium_script(
        self,
        test_case: Dict[str, Any],
        html_content: str = None
    ) -> str:
        """
        Generate Selenium Python script from test case.
        
        Args:
            test_case: Test case dictionary
            html_content: HTML content of the target page
            
        Returns:
            Python Selenium script as string
        """
        # Retrieve HTML structure from vector DB if not provided
        if not html_content:
            html_results = self.vector_db.search("HTML structure checkout", top_k=3)
            html_content = "\n".join([chunk["content"] for chunk in html_results])
        
        # Get relevant documentation
        test_scenario = test_case.get("test_scenario", "")
        feature = test_case.get("feature", "")
        query = f"{feature} {test_scenario}"
        
        context_chunks = self.vector_db.search(query, top_k=5)
        
        # System prompt for Selenium generation
        system_prompt = """You are an expert Selenium test automation engineer with deep knowledge of Python and web testing.

Your task is to generate a complete, executable Selenium Python script based on the provided test case and HTML structure.

CRITICAL REQUIREMENTS:
1. Use actual element IDs, names, and CSS selectors from the HTML
2. Include proper imports (selenium, webdriver_manager, unittest, etc.)
3. Use explicit waits with WebDriverWait
4. Include proper assertions
5. Add error handling and teardown
6. Use unittest framework
7. Add comments explaining each step
8. Make the script runnable as-is
9. Use Chrome WebDriver with automatic driver management
10. Include setup and teardown methods

Code Quality Standards:
- Clean, readable, PEP 8 compliant code
- Proper exception handling
- Meaningful variable names
- Comprehensive assertions
- Screenshots on failure (optional but recommended)

Output Format:
Return ONLY the complete Python script. No explanations before or after.
The script should be ready to save as a .py file and execute."""
        
        # Create detailed prompt
        prompt = self._create_script_generation_prompt(test_case, html_content, context_chunks)
        
        try:
            script = self.llm.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # Lower temperature for more consistent code
                max_tokens=3000
            )
            
            # Clean up the script
            script = self._clean_script(script)
            
            return script
        except Exception as e:
            raise Exception(f"Error generating Selenium script: {str(e)}")
    
    def _create_script_generation_prompt(
        self,
        test_case: Dict[str, Any],
        html_content: str,
        context_chunks: list
    ) -> str:
        """Create detailed prompt for script generation"""
        
        # Format context
        context_text = "\n".join([
            f"Source: {chunk.get('metadata', {}).get('source', 'unknown')}\n{chunk.get('content', '')}"
            for chunk in context_chunks
        ])
        
        # Extract test case details
        test_id = test_case.get("test_id", "TC-001")
        feature = test_case.get("feature", "Unknown")
        scenario = test_case.get("test_scenario", "")
        test_steps = test_case.get("test_steps", [])
        expected_result = test_case.get("expected_result", "")
        preconditions = test_case.get("preconditions", "")
        
        prompt = f"""Generate a complete Selenium Python script for this test case:

TEST CASE DETAILS:
- Test ID: {test_id}
- Feature: {feature}
- Scenario: {scenario}
- Type: {test_case.get('test_type', 'positive')}

PRECONDITIONS:
{preconditions}

TEST STEPS:
{self._format_steps(test_steps)}

EXPECTED RESULT:
{expected_result}

---

HTML STRUCTURE (Use these exact selectors):
```html
{html_content[:5000]}  # Limit HTML length
```

---

DOCUMENTATION CONTEXT:
{context_text[:3000]}  # Limit context length

---

Generate a complete Selenium Python script that:
1. Sets up Chrome WebDriver using webdriver_manager
2. Opens the HTML file (assume it's at ./project_assets/checkout.html)
3. Executes all test steps
4. Performs assertions to verify the expected result
5. Includes proper error handling
6. Closes the browser in teardown

Use unittest.TestCase as the base class.
Include detailed comments for each step.
Make it production-ready and executable."""
        
        return prompt
    
    def _format_steps(self, steps: list) -> str:
        """Format test steps as numbered list"""
        if isinstance(steps, list):
            return "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        elif isinstance(steps, str):
            return steps
        return "No steps provided"
    
    def _clean_script(self, script: str) -> str:
        """Clean and format the generated script"""
        # Remove markdown code blocks if present
        if "```python" in script:
            script = script.split("```python")[1].split("```")[0]
        elif "```" in script:
            script = script.split("```")[1].split("```")[0]
        
        # Remove leading/trailing whitespace
        script = script.strip()
        
        # Ensure proper imports are at the top
        required_imports = [
            "import unittest",
            "from selenium import webdriver",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support.ui import WebDriverWait",
            "from selenium.webdriver.support import expected_conditions as EC"
        ]
        
        # Check if imports are present, if not add them
        if "import unittest" not in script:
            imports_block = "\n".join(required_imports) + "\n\n"
            script = imports_block + script
        
        return script
    
    def generate_test_suite(
        self,
        test_cases: list,
        html_content: str = None
    ) -> Dict[str, str]:
        """
        Generate multiple Selenium scripts for a test suite.
        
        Args:
            test_cases: List of test cases
            html_content: HTML content
            
        Returns:
            Dictionary mapping test_id to script
        """
        scripts = {}
        
        for test_case in test_cases:
            test_id = test_case.get("test_id", f"TC-{len(scripts)+1}")
            try:
                script = self.generate_selenium_script(test_case, html_content)
                scripts[test_id] = script
            except Exception as e:
                scripts[test_id] = f"# Error generating script: {str(e)}"
        
        return scripts
    
    def validate_script_syntax(self, script: str) -> Dict[str, Any]:
        """
        Validate Python syntax of generated script.
        
        Args:
            script: Python script to validate
            
        Returns:
            Validation result with 'valid' boolean and 'error' message if invalid
        """
        try:
            compile(script, '<string>', 'exec')
            return {
                "valid": True,
                "error": None
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error at line {e.lineno}: {e.msg}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
