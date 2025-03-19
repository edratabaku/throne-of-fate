import unittest
from unittest.mock import patch, mock_open
from ai.ollama_ai import generate_scenario


class TestGenerateScenario(unittest.TestCase):
    def test_generate_scenario_with_valid_inputs(self):
        """Test generate_scenario with valid inputs and no previous events."""
        economy, military, public_appeal, diplomacy = 50, 60, 70, 80
        previous_events = ["A rebellion was suppressed.", "Trade routes were disrupted."]
        
        with patch("ai.ollama_ai.ollama.generate") as mock_generate:
            mock_generate.return_value.response = """
            {
                "scenario": "A neighboring kingdom demands tribute.",
                "options": [
                    {"text": "Pay the tribute.", "effects": {"economy": -10, "military": 0, "public_appeal": 5, "diplomacy": 10}},
                    {"text": "Refuse and prepare for war.", "effects": {"economy": -5, "military": -10, "public_appeal": -5, "diplomacy": -10}},
                    {"text": "Negotiate a compromise.", "effects": {"economy": -5, "military": 0, "public_appeal": 5, "diplomacy": 5}}
                ]
            }
            """
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy, previous_events)
            self.assertEqual(scenario, "A neighboring kingdom demands tribute.")
            self.assertEqual(len(options), 3)

    def test_generate_scenario_with_no_previous_events(self):
        """Test generate_scenario when previous_events is None."""
        economy, military, public_appeal, diplomacy = 50, 60, 70, 80
        
        with patch("ai.ollama_ai.ollama.generate") as mock_generate:
            mock_generate.return_value.response = """
            {
                "scenario": "A drought threatens the kingdom's food supply.",
                "options": [
                    {"text": "Ration food supplies.", "effects": {"economy": -5, "military": 0, "public_appeal": -5, "diplomacy": 0}},
                    {"text": "Import food from neighbors.", "effects": {"economy": -10, "military": 0, "public_appeal": 5, "diplomacy": 5}},
                    {"text": "Do nothing.", "effects": {"economy": 0, "military": 0, "public_appeal": -10, "diplomacy": 0}}
                ]
            }
            """
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy)
            self.assertEqual(scenario, "A drought threatens the kingdom's food supply.")
            self.assertEqual(len(options), 3)

    @patch("builtins.open", new_callable=mock_open, read_data='{"scenario": "A test scenario.", "options": []}')
    def test_generate_scenario_with_load_from_file(self, mock_file):
        """Test generate_scenario with load_from_file parameter."""
        economy, military, public_appeal, diplomacy = 50, 60, 70, 80
        scenario, options = generate_scenario(economy, military, public_appeal, diplomacy, load_from_file="assets/scenario.json")
        self.assertEqual(scenario, "A test scenario.")
        self.assertEqual(options, [])

    def test_generate_scenario_with_ai_failure(self):
        """Test fallback behavior when AI fails to generate a scenario."""
        economy, military, public_appeal, diplomacy = 50, 60, 70, 80
        
        with patch("ai.ollama_ai.ollama.generate", side_effect=Exception("AI error")):
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy)
            self.assertEqual(scenario, "A crisis emerges!")
            self.assertEqual(len(options), 3)

    def test_generate_scenario_with_no_file_and_ai_failure(self):
        """Test fallback behavior when no file is loaded and AI fails."""
        economy, military, public_appeal, diplomacy = 50, 50, 50, 50
        
        with patch("ai.ollama_ai.ollama.generate", side_effect=Exception("AI error")):
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy, load_from_file=None)
            self.assertEqual(scenario, "A crisis emerges!")
            self.assertEqual(len(options), 3)

    def test_generate_scenario_with_extreme_values(self):
        """Test generate_scenario with extreme values for stats."""
        economy, military, public_appeal, diplomacy = 0, 100, -50, 200
        previous_events = ["A neighboring kingdom declared war.", "A famine struck the southern provinces."]
        
        with patch("ai.ollama_ai.ollama.generate") as mock_generate:
            mock_generate.return_value.response = """
            {
                "scenario": "The kingdom faces a dire threat from an invading army.",
                "options": [
                    {"text": "Mobilize the army.", "effects": {"economy": -20, "military": -10, "public_appeal": 5, "diplomacy": -5}},
                    {"text": "Seek peace negotiations.", "effects": {"economy": -5, "military": 0, "public_appeal": 10, "diplomacy": 15}},
                    {"text": "Fortify defenses.", "effects": {"economy": -15, "military": 10, "public_appeal": 0, "diplomacy": -10}}
                ]
            }
            """
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy, previous_events)
            self.assertEqual(scenario, "The kingdom faces a dire threat from an invading army.")
            self.assertEqual(len(options), 3)

    @patch("builtins.open", new_callable=mock_open, read_data="INVALID_JSON")
    def test_generate_scenario_with_corrupted_file(self, mock_file):
        """Test generate_scenario with a corrupted file."""
        economy, military, public_appeal, diplomacy = 50, 50, 50, 50
        scenario, options = generate_scenario(economy, military, public_appeal, diplomacy, load_from_file="assets/scenario.json")
        self.assertEqual(scenario, "A crisis emerges!")
        self.assertEqual(len(options), 3)

    def test_generate_scenario_with_empty_options(self):
        """Test generate_scenario when the AI response contains no options."""
        economy, military, public_appeal, diplomacy = 50, 50, 50, 50
        
        with patch("ai.ollama_ai.ollama.generate") as mock_generate:
            mock_generate.return_value.response = """
            {
                "scenario": "A neighboring kingdom offers an alliance.",
                "options": []
            }
            """
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy)
            self.assertEqual(scenario, "A neighboring kingdom offers an alliance.")
            self.assertEqual(len(options), 0)

    def test_generate_scenario_with_missing_fields(self):
        """Test generate_scenario when the AI response is missing required fields."""
        economy, military, public_appeal, diplomacy = 50, 50, 50, 50
        
        with patch("ai.ollama_ai.ollama.generate") as mock_generate:
            mock_generate.return_value.response = """
            {
                "options": [
                    {"text": "Do something.", "effects": {"economy": 0, "military": 0, "public_appeal": 0, "diplomacy": 0}}
                ]
            }
            """
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy)
            self.assertEqual(scenario, "A crisis emerges!")
            self.assertEqual(len(options), 3)

    def test_generate_scenario_with_large_previous_events(self):
        """Test generate_scenario with a large list of previous events."""
        economy, military, public_appeal, diplomacy = 50, 50, 50, 50
        previous_events = [f"Event {i}" for i in range(100)]  # Generate 100 previous events
        
        with patch("ai.ollama_ai.ollama.generate") as mock_generate:
            mock_generate.return_value.response = """
            {
                "scenario": "The kingdom faces unrest due to past decisions.",
                "options": [
                    {"text": "Appease the people.", "effects": {"economy": -10, "military": 0, "public_appeal": 10, "diplomacy": 0}},
                    {"text": "Ignore the unrest.", "effects": {"economy": 0, "military": 0, "public_appeal": -10, "diplomacy": 0}},
                    {"text": "Enforce strict laws.", "effects": {"economy": 0, "military": 10, "public_appeal": -5, "diplomacy": 0}}
                ]
            }
            """
            scenario, options = generate_scenario(economy, military, public_appeal, diplomacy, previous_events)
            self.assertEqual(scenario, "The kingdom faces unrest due to past decisions.")
            self.assertEqual(len(options), 3)


if __name__ == "__main__":
    unittest.main()