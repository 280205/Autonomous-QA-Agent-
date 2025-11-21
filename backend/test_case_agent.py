"""
Test Case Generation Agent - Generates comprehensive test cases from documentation.
"""

import json
from typing import List, Dict, Any
from backend.llm_handler import LLMHandler
from backend.vector_db import VectorDatabase


class TestCaseAgent:
    """Agent for generating test cases from documentation"""
    
    def __init__(self, vector_db: VectorDatabase, llm_handler: LLMHandler):
        """
        Initialize test case agent.
        
        Args:
            vector_db: Vector database instance
            llm_handler: LLM handler instance
        """
        self.vector_db = vector_db
        self.llm = llm_handler
    
    def generate_test_cases(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate test cases based on user query and documentation.
        
        Args:
            query: User's test case request
            top_k: Number of context chunks to retrieve
            
        Returns:
            List of test cases
        """
        # Retrieve relevant context
        context_chunks = self.vector_db.search(query, top_k=top_k)
        
        if not context_chunks:
            raise Exception("No relevant documentation found. Please ensure documents are uploaded.")
        
        # System prompt for test case generation
        system_prompt = """You are an expert QA engineer specializing in test case design.

Your task is to generate comprehensive, well-structured test cases based STRICTLY on the provided documentation.

CRITICAL RULES:
1. ALL test cases MUST be grounded in the provided documentation
2. Reference the source document for each test case
3. Do NOT invent features, behaviors, or requirements not in the documentation
4. If information is missing, state it explicitly
5. Generate both positive and negative test cases where applicable

Output Format:
Return ONLY a valid JSON array of test cases. Each test case must have this exact structure:
{
  "test_id": "TC-XXX",
  "feature": "Feature name",
  "test_scenario": "Clear description of what is being tested",
  "test_type": "positive" or "negative",
  "preconditions": "Prerequisites before test execution",
  "test_steps": ["Step 1", "Step 2", "Step 3"],
  "expected_result": "What should happen",
  "grounded_in": "source_document.ext",
  "priority": "high", "medium", or "low"
}

Generate multiple comprehensive test cases covering different aspects of the feature."""
        
        # Generate test cases
        try:
            response = self.llm.generate_with_context(
                query=query,
                context_chunks=context_chunks,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=3000
            )
            
            # Parse JSON response
            test_cases = self._parse_test_cases(response)
            
            return test_cases
        except Exception as e:
            raise Exception(f"Error generating test cases: {str(e)}")
    
    def _parse_test_cases(self, response: str) -> List[Dict[str, Any]]:
        """Parse test cases from LLM response"""
        # Try to extract JSON from response
        try:
            # Find JSON array in response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response[start_idx:end_idx]
            test_cases = json.loads(json_str)
            
            # Validate test cases
            validated_cases = []
            for tc in test_cases:
                if self._validate_test_case(tc):
                    validated_cases.append(tc)
            
            return validated_cases
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to create structured output from text
            return self._fallback_parse(response)
    
    def _validate_test_case(self, test_case: Dict[str, Any]) -> bool:
        """Validate test case structure"""
        required_fields = [
            "test_id", "feature", "test_scenario",
            "expected_result", "grounded_in"
        ]
        
        for field in required_fields:
            if field not in test_case:
                return False
        
        return True
    
    def _fallback_parse(self, response: str) -> List[Dict[str, Any]]:
        """Fallback parser for non-JSON responses"""
        # Create a single test case from the response
        return [{
            "test_id": "TC-001",
            "feature": "Generated from query",
            "test_scenario": "See full response",
            "test_type": "positive",
            "preconditions": "N/A",
            "test_steps": ["See full response"],
            "expected_result": response,
            "grounded_in": "documentation",
            "priority": "medium",
            "note": "This is a fallback parse. Please review the full response."
        }]
    
    def generate_test_plan(
        self,
        features: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive test plan.
        
        Args:
            features: List of features to test (optional)
            
        Returns:
            Complete test plan
        """
        if features:
            query = f"Generate a comprehensive test plan for these features: {', '.join(features)}"
        else:
            query = "Generate a comprehensive test plan covering all features in the application"
        
        test_cases = self.generate_test_cases(query, top_k=10)
        
        # Organize test plan
        test_plan = {
            "test_plan_id": "TP-001",
            "title": "Automated Test Plan",
            "total_test_cases": len(test_cases),
            "test_cases": test_cases,
            "coverage": {
                "positive_tests": len([tc for tc in test_cases if tc.get("test_type") == "positive"]),
                "negative_tests": len([tc for tc in test_cases if tc.get("test_type") == "negative"]),
                "high_priority": len([tc for tc in test_cases if tc.get("priority") == "high"]),
                "medium_priority": len([tc for tc in test_cases if tc.get("priority") == "medium"]),
                "low_priority": len([tc for tc in test_cases if tc.get("priority") == "low"])
            }
        }
        
        return test_plan
    
    def suggest_test_scenarios(self) -> List[str]:
        """
        Suggest test scenarios based on uploaded documentation.
        
        Returns:
            List of suggested test scenario queries
        """
        # Get sample documents to understand what's available
        all_docs = self.vector_db.get_all_documents()
        
        if not all_docs:
            return [
                "Generate test cases for form validation",
                "Generate test cases for shopping cart functionality",
                "Generate test cases for discount code feature",
                "Generate test cases for payment processing"
            ]
        
        # Extract unique sources
        sources = set()
        for doc in all_docs[:10]:  # Sample first 10
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "")
            if source:
                sources.add(source)
        
        # Generate suggestions based on sources
        suggestions = [
            "Generate all positive and negative test cases",
            "Generate test cases for all critical features",
            "Generate test cases for form validation",
            "Generate test cases for user interactions"
        ]
        
        return suggestions
