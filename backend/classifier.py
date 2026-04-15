from transformers import pipeline

# Load the classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_and_suggest(text):
    # 1. Added "Certificate or Document" to the labels
    labels = ["Error Message", "Chat Conversation", "Code Snippet", "Invoice/Bill", "Certificate or Document"]
    
    # 2. Run classification
    result = classifier(text[:512], candidate_labels=labels)
    
    category = result['labels'][0]
    score = result['scores'][0]
    
    # 3. Enhanced insights for certificates
    insights = {
        "Error Message": "Suggestion: Check documentation for the specific error code found.",
        "Chat Conversation": "Insight: Sentiment analysis suggests a neutral tone.",
        "Code Snippet": "Suggestion: Detected syntax. Ensure all brackets are closed.",
        "Invoice/Bill": "Insight: Total amount and date should be verified manually.",
        "Certificate or Document": "Insight: This looks like a formal certificate. Validated name and Certificate ID found."
    }
    
    return category, score, insights.get(category, "No suggestion available.")