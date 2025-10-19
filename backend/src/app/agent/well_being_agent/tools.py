"""Tools for the Well Being Agent."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from langchain_core.tools import tool
from app.core.db import get_connection
from ddgs import DDGS

# Lazy load transformers to avoid slow startup
_tokenizer = None
_model = None

def get_sentiment_model():
    """Lazy load sentiment analysis model (TDD-friendly singleton)."""
    global _tokenizer, _model
    
    if _tokenizer is None or _model is None:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
        
        # Using DistilBERT for sentiment (fast, accurate, well-supported)
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Set to eval mode
        _model.eval()
    
    return _tokenizer, _model

@tool
def update_sentiment_snapshot(
    employee_id: str,
    sentiment_label: str,
    sentiment_score: float,
    message_id: Optional[int] = None
) -> Dict[str, str]:
    """
    Record significant sentiment data to database for tracking mood patterns over time.
    
    Call this tool ONLY when analyze_message_sentiment indicates is_significant=True.
    The agent should use analyze_message_sentiment first, then call this to record the data.
    
    Args:
        employee_id: The employee's unique identifier
        sentiment_label: Sentiment category from analyze_message_sentiment
        sentiment_score: Sentiment score from analyze_message_sentiment (-1.0 to 1.0)
        message_id: Optional reference to the wellbeing message that triggered this
    
    Returns:
        Dict with status confirming the sentiment was recorded
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    current_time = datetime.now(timezone.utc).isoformat()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Record detailed sentiment message
    if message_id:
        cursor.execute(
            """
            INSERT INTO sentiment_messages (message_id, label, score, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (message_id, sentiment_label, sentiment_score, abs(sentiment_score), current_time)
        )
    
    # Update or create daily snapshot with rolling average
    cursor.execute(
        """
        SELECT id, average_score, messages_count 
        FROM sentiment_snapshots 
        WHERE employee_id = ? AND day = ?
        """,
        (employee_id, today)
    )
    existing = cursor.fetchone()
    
    if existing:
        snapshot_id, avg_score, msg_count = existing
        new_count = msg_count + 1
        new_avg = ((avg_score * msg_count) + sentiment_score) / new_count
        
        cursor.execute(
            """
            UPDATE sentiment_snapshots 
            SET average_score = ?, messages_count = ?, label = ?, created_at = ?
            WHERE id = ?
            """,
            (new_avg, new_count, sentiment_label, current_time, snapshot_id)
        )
    else:
        cursor.execute(
            """
            INSERT INTO sentiment_snapshots 
            (employee_id, anon_session_id, day, label, average_score, messages_count, created_at)
            VALUES (?, NULL, ?, ?, ?, 1, ?)
            """,
            (employee_id, today, sentiment_label, sentiment_score, current_time)
        )
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "message": f"Sentiment recorded for {employee_id}",
        "label": sentiment_label,
        "score": sentiment_score
    }

def get_past_sentiment_history(
    employee_id: str,
    days_back: int = 7
) -> Dict[str, any]:
    """
    Retrieve past sentiment history for an employee to understand mood patterns over time.
    
    Use this tool to:
    - Understand the employee's emotional trajectory
    - Identify patterns in mood changes
    - Provide context-aware support based on historical data
    - Detect if current state is unusual compared to baseline
    
    Args:
        employee_id: The employee's unique identifier
        days_back: Number of days to look back (default: 7 days)
    
    Returns:
        Dict containing sentiment history with daily snapshots and recent messages
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get daily sentiment snapshots
    cursor.execute(
        """
        SELECT day, label, average_score, messages_count, created_at
        FROM sentiment_snapshots
        WHERE employee_id = ?
        ORDER BY day DESC
        LIMIT ?
        """,
        (employee_id, days_back)
    )
    
    snapshots = []
    for row in cursor.fetchall():
        snapshots.append({
            "day": row[0],
            "label": row[1],
            "average_score": row[2],
            "messages_count": row[3],
            "created_at": row[4]
        })
    
    # Get recent detailed sentiment messages
    cursor.execute(
        """
        SELECT sm.label, sm.score, sm.confidence, sm.created_at, wm.content
        FROM sentiment_messages sm
        JOIN wellbeing_messages wm ON sm.message_id = wm.id
        WHERE wm.employee_id = ?
        ORDER BY sm.created_at DESC
        LIMIT 10
        """,
        (employee_id,)
    )
    
    recent_sentiments = []
    for row in cursor.fetchall():
        recent_sentiments.append({
            "label": row[0],
            "score": row[1],
            "confidence": row[2],
            "created_at": row[3],
            "message_preview": row[4][:100] if row[4] else ""
        })
    
    conn.close()
    
    # Calculate summary statistics
    if snapshots:
        avg_overall = sum(s["average_score"] for s in snapshots) / len(snapshots)
        trend = "improving" if len(snapshots) >= 2 and snapshots[0]["average_score"] > snapshots[-1]["average_score"] else "declining" if len(snapshots) >= 2 else "stable"
    else:
        avg_overall = 0.0
        trend = "no_data"
    
    return {
        "employee_id": employee_id,
        "days_analyzed": days_back,
        "daily_snapshots": snapshots,
        "recent_sentiments": recent_sentiments,
        "summary": {
            "average_sentiment_score": round(avg_overall, 2),
            "trend": trend,
            "total_snapshots": len(snapshots),
            "data_available": len(snapshots) > 0
        }
    }

@tool
def analyze_message_sentiment(message_content: str, employee_id: str) -> Dict[str, any]:
    """
    Analyze sentiment of a user message using transformer-based AI model.
    
    Use this tool to:
    - Determine sentiment score before updating snapshot
    - Compare current sentiment to historical baseline
    - Decide if mood change is significant enough to record
    
    Args:
        message_content: The user's message text
        employee_id: The employee's unique identifier (needed to compare with baseline)
    
    Returns:
        Dict with sentiment label, score, confidence, and analysis
    """
    
    import torch
    
    tokenizer, model = get_sentiment_model()
    
    # Tokenize input
    inputs = tokenizer(
        message_content,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )
    
    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # DistilBERT SST-2 returns: [negative_score, positive_score]
    negative_prob = predictions[0][0].item()
    positive_prob = predictions[0][1].item()
    
    # Convert to sentiment score (-1 to +1 range)
    # sentiment_score = (positive - negative)
    sentiment_score = positive_prob - negative_prob
    
    # Determine label based on score
    if sentiment_score <= -0.6:
        label = "distressed"
    elif sentiment_score <= -0.3:
        label = "concerned"
    elif sentiment_score <= -0.1:
        label = "slightly_negative"
    elif sentiment_score <= 0.1:
        label = "neutral"
    elif sentiment_score <= 0.3:
        label = "slightly_positive"
    elif sentiment_score <= 0.6:
        label = "positive"
    else:
        label = "very_positive"
    
    # Confidence is the max probability
    confidence = max(positive_prob, negative_prob)
    
    # Get historical baseline to compare
    past_sentiment = get_past_sentiment_history(employee_id, days_back=7)
    baseline_score = past_sentiment["summary"]["average_sentiment_score"]
    
    # Calculate sentiment change: new - baseline
    sentiment_change = sentiment_score - baseline_score
    
    # Determine if significant based on:
    # 1. Absolute change threshold (±0.3 or more indicates notable mood shift)
    # 2. Extreme states (distressed always significant for safety)
    # 3. Has historical data to compare against
    CHANGE_THRESHOLD = 0.3
    
    if past_sentiment["summary"]["data_available"]:
        # Compare against baseline
        is_significant = (
            abs(sentiment_change) >= CHANGE_THRESHOLD or 
            label == "distressed"  # Always track distress for safety
        )
    else:
        # No baseline yet - record if sentiment is notably positive or negative
        is_significant = abs(sentiment_score) >= 0.4 or label in ["distressed", "very_positive"]
    
    return {
        "sentiment_label": label,
        "sentiment_score": round(sentiment_score, 2),
        "confidence": round(confidence, 2),
        "positive_probability": round(positive_prob, 2),
        "negative_probability": round(negative_prob, 2),
        "baseline_score": round(baseline_score, 2),
        "sentiment_change": round(sentiment_change, 2),
        "is_significant": is_significant,
        "has_baseline": past_sentiment["summary"]["data_available"],
        "analysis_method": "transformer_distilbert_sst2"
    }
    

@tool
def search_wellbeing_resources(
    query: str,
    max_results: int = 5
) -> Dict[str, any]:
    """
    Search the web for wellbeing resources, mental health support, and self-care information.
    
    Use this tool to:
    - Find external resources for mental health support
    - Discover wellbeing articles, guides, and tips
    - Locate professional help services
    - Search for specific wellness topics (stress management, mindfulness, etc.)
    - Find company-specific or regional support resources
    
    Args:
        query: Search query (e.g., "therapist directory Singapore", "stress management techniques")
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Dict with search results including titles, URLs, and descriptions
    """
    
    results = []
    query_lower = query.lower()
    
    # Smart region detection:
    # Local services (clinics, psychiatrists, hospitals, hotlines) → Singapore region
    # General resources (articles, guides, tips) → Worldwide
    local_service_keywords = ['clinic', 'hospital', 'psychiatrist', 'psychologist', 
                              'therapist', 'counsellor', 'counselor', 'counselling', 'counseling',
                              'hotline', 'helpline', 'emergency', 'crisis', 'directory', 
                              'find', 'near me', 'appointment']
    
    is_local_service = any(keyword in query_lower for keyword in local_service_keywords)
    region = 'sg-en' if is_local_service else 'wt-wt'
    
    # Initialize DuckDuckGo search
    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=max_results,
            region=region,
            safesearch='moderate'
        )
        
        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "description": result.get("body", ""),
                "source": result.get("href", "").split('/')[2] if result.get("href") else ""
            })
    
    return {
        "query": query,
        "results_count": len(results),
        "results": results,
        "search_engine": "DuckDuckGo",
        "region": region,
    }


