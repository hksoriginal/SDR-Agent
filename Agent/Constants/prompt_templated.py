_INTENT_DETECTION_PROMPT_TEMPLATE = """
[INST]<s>
Return a JSON object as given below, nothing else.</s>
{{
    "intent" : "(intent match from the list)",
    "action": "(short description of action)"
}}
[/INST]
[INST]
Provide Intent of the user input only from the given intent_list in a given Json object:
Intent List : ["write_email" : User wants to send an email,
            "read_email" : User wants to read an email,
            "reply_email" : User wants to reply to an email,
            "delete_email" : User wants to delete an email]
[/INST]           
[INST]
User Input: "{query}"
[/INST]

"""


INTENT_DETECTION_PROMPT_TEMPLATE = """
[INST]<s>
You are an AI assistant. Respond strictly in the following JSON format:

```json{{
  "intent": "<intent>"
  "action": "<short description>"
}}```

Please fill in the placeholders with relevant, realistic information. Do not add any extra text or explanation outside the JSON format.
[/INST]
[INST]
Provide Intent of the user input only from the given intent_list in a given Json object:
Intent List : ["write_email" : User wants to send an email,
            "search_dataframe" : User wants to search entity in a dataframe,
            "reply_email" : User wants to reply to an email,
            "delete_email" : User wants to delete an email]
[/INST]           
[INST]
User Input: "{query}"
[/INST]

"""
