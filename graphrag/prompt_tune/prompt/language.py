# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Fine-tuning prompts for language detection."""

DETECT_LANGUAGE_PROMPT = """
You are an intelligent assistant that helps a human to analyze the information in a text document.
Given a sample text, help the user by determining what's the primary language of the provided texts.
Examples are: the language exactly like "English", "Spanish", "Japanese", "Portuguese" among others.
Only output the language itself and DO NOT include any other characters rather than Language itself!

Text: {input_text}
"""
