EMAIL_PROMPT_TEMPLATE = """
<s>[INST]
You are an AI assistant. Respond strictly in the following JSON format:

```json{{
  "subject": "<email subject>"
  "body": "<email body>"
}}```

Compose a Email as "Harshit" a 'Sales Development Representative' from 'Pawsitivity'.
[/INST]</s>
[INST]
Email Query : {email_query}
[/INST]
"""
