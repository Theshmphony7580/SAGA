# 💬 NLQ Engine

Converts user natural language queries into executable pandas code.

### Process
1. Receive query.
2. Send dataset schema & examples to GPT-4.
3. LLM returns structured JSON with code and summary.
4. Code runs in sandbox.

### Example
```
User: "Top 10 products by sales"
Response: df.groupby('Product')['Sales'].sum().nlargest(10)
```

### Rules
- Validate output JSON.
- Allow only whitelisted columns.
- Abort after 5 seconds of runtime.
