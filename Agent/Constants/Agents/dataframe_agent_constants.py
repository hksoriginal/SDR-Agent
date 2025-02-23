DATAFRAME_AGENT_PROMPT_TEMPLATE = """
<s>[INST]
You are an AI assistant. Respond strictly in the following JSON format:
```json{{
  "column": "<column name>",
  "condition": "<condition for boolean search>"
}}```[/INST]
[INST]
Example : get the data where 'Company' is university, from the data
```json{{
  "column": "Company",
  "condition": "university"
}}```
[/INST]
[INST]
Extract the column name and the condition from the Query below.

Data filter : {data_query}
[/INST]
"""
