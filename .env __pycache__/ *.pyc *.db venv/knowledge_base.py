"""
Knowledge Base Module

Handles retrieval of attendance-related information.

This module provides a simple interface:
    query_knowledge_base(collection, query)

The AgentExecutor uses this function to retrieve
relevant information before sending it to the LLM.
"""

import sqlite3

import config


def query_knowledge_base(collection, query: str):
    """
    Search attendance records based on a user query.

    Args:
        collection:
            Reserved for future vector database support.
            Kept because AgentExecutor expects it.

        query:
            User question/search query.

    Returns:
        List of matching attendance records.
    """

    results = []

    try:
        connection = sqlite3.connect(
            config.DATABASE_PATH
        )

        cursor = connection.cursor()

        # Simple keyword-based search
        cursor.execute(
            """
            SELECT
                student_id,
                student_name,
                subject,
                date,
                status
            FROM attendance
            WHERE
                student_name LIKE ?
                OR subject LIKE ?
                OR student_id LIKE ?
            LIMIT 10
            """,
            (
                f"%{query}%",
                f"%{query}%",
                f"%{query}%"
            )
        )

        rows = cursor.fetchall()

        for row in rows:
            results.append(
                {
                    "student_id": row[0],
                    "student_name": row[1],
                    "subject": row[2],
                    "date": row[3],
                    "status": row[4],
                }
            )

        connection.close()

    except sqlite3.Error as error:
        print(
            f"Knowledge base error: {error}"
        )

    return results
