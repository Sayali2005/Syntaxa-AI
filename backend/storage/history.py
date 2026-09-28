import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "syntaxa_history.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        document_name TEXT,
        mode TEXT,
        word_count INTEGER,
        score_before INTEGER,
        score_after INTEGER,
        errors_before INTEGER,
        errors_after INTEGER,
        category_breakdown TEXT,
        issue_types_json TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_analysis_entry(entry: Dict[str, Any]):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO analysis_history (
        id, timestamp, document_name, mode, word_count,
        score_before, score_after, errors_before, errors_after,
        category_breakdown, issue_types_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry["id"],
        entry.get("timestamp", datetime.now().isoformat()),
        entry.get("document_name", "Untitled Document"),
        entry.get("mode", "grammar_fix"),
        entry.get("word_count", 0),
        entry.get("score_before", 0),
        entry.get("score_after", 0),
        entry.get("errors_before", 0),
        entry.get("errors_after", 0),
        json.dumps(entry.get("category_breakdown", {})),
        json.dumps(entry.get("issue_types", {}))
    ))
    conn.commit()
    conn.close()

def get_history_entries(limit: int = 25) -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_history ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "document_name": r["document_name"],
            "mode": r["mode"],
            "word_count": r["word_count"],
            "score_before": r["score_before"],
            "score_after": r["score_after"],
            "errors_before": r["errors_before"],
            "errors_after": r["errors_after"],
            "category_breakdown": json.loads(r["category_breakdown"]) if r["category_breakdown"] else {},
            "issue_types": json.loads(r["issue_types_json"]) if r["issue_types_json"] else {}
        })
    conn.close()
    return results

def get_personalized_writing_profile() -> Dict[str, Any]:
    """
    Computes user's writing profile:
    - Recurring issues breakdown (percentages)
    - Score progress over chronological documents/sessions
    - Overall writing improvement statistics
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_history ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        # Default placeholder profile for new users
        return {
            "total_documents_analyzed": 0,
            "total_words_processed": 0,
            "average_score": 0,
            "average_score_improvement": 0,
            "most_common_issues": [],
            "score_timeline": [],
            "weakness_recommendation": "Analyze your first document to build your personalized writing profile."
        }

    total_docs = len(rows)
    total_words = sum(r["word_count"] for r in rows)
    avg_score = round(sum(r["score_before"] for r in rows) / total_docs, 1)
    avg_improvement = round(sum(r["score_after"] - r["score_before"] for r in rows) / total_docs, 1)

    # Aggregate issue types across history
    issue_type_counts: Dict[str, int] = {}
    for r in rows:
        types = json.loads(r["issue_types_json"]) if r["issue_types_json"] else {}
        for itype, count in types.items():
            issue_type_counts[itype] = issue_type_counts.get(itype, 0) + count

    total_issues = sum(issue_type_counts.values()) or 1
    sorted_issues = sorted(issue_type_counts.items(), key=lambda x: x[1], reverse=True)

    most_common_issues = [
        {
            "name": name,
            "count": count,
            "percentage": round((count / total_issues) * 100, 1)
        }
        for name, count in sorted_issues[:5]
    ]

    # Score timeline for progress charts
    score_timeline = [
        {
            "document": r["document_name"],
            "date": r["timestamp"][:10],
            "score_before": r["score_before"],
            "score_after": r["score_after"]
        }
        for r in rows
    ]

    # Recommendations
    top_issue = most_common_issues[0]["name"] if most_common_issues else "General Writing"
    recommendation = f"Focus area: Your most frequent pattern is '{top_issue}' ({most_common_issues[0]['percentage']}% of issues). Review targeted rules in the Explain tab." if most_common_issues else "Keep analyzing to refine your profile."

    return {
        "total_documents_analyzed": total_docs,
        "total_words_processed": total_words,
        "average_score": avg_score,
        "average_score_improvement": avg_improvement,
        "most_common_issues": most_common_issues,
        "score_timeline": score_timeline,
        "weakness_recommendation": recommendation
    }

def clear_all_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history")
    conn.commit()
    conn.close()
