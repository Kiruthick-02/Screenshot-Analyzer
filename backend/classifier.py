from transformers import pipeline

# Load a reliable zero-shot classifier
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

def classify_and_suggest(text):
    text_lower = text.lower()
    
    # --- 1. KEYWORD BACKUP (Rule-Based) ---
    # This ensures common screenshots are caught even if AI confidence is low
    if any(word in text_lower for word in ["total", "amount", "order", "price", "tax", "invoice", "bill", "qty"]):
        return "Invoice/Bill", 0.95, "Insight: Detected financial keywords. Verified as an Invoice/Bill."
    
    if any(word in text_lower for word in ["error", "exception", "traceback", "failed", "warning", "stack", "line"]):
        return "Error Message", 0.95, "Suggestion: This looks like a system error. Check the stack trace or logs."
    
    if any(word in text_lower for word in ["def ", "class ", "import ", "void ", "{", "public ", "print("]):
        return "Code Snippet", 0.95, "Suggestion: Detected programming syntax. Review logic and closed brackets."

    if any(word in text_lower for word in ["certificate", "recognition", "presented", "awarded"]):
        return "Certificate", 0.95, "Insight: Formal document recognized as a Certificate."

    # --- 2. AI CLASSIFICATION (Fallback) ---
    labels = ["Error Message", "Chat Conversation", "Code Snippet", "Invoice/Bill", "Certificate"]
    
    try:
        result = classifier(text[:512], candidate_labels=labels)
        category = result['labels'][0]
        score = result['scores'][0]
        
        # If AI is very unsure, call it a "General Document"
        if score < 0.35:
            return "General Document", score, "Insight: General text detected with no specific category."

        insights = {
            "Error Message": "Suggestion: Check system documentation for this error.",
            "Chat Conversation": "Insight: Natural language conversation detected.",
            "Code Snippet": "Suggestion: Programming code detected. Check for syntax errors.",
            "Invoice/Bill": "Insight: Financial document. Please verify the total amount.",
            "Certificate": "Insight: This is a formal document of recognition."
        }
        
        return category, score, insights.get(category, "No specific suggestion.")
        
    except Exception as e:
        return "Unclassified", 0.0, f"Error in AI analysis: {str(e)}"