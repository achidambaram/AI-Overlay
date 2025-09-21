#!/usr/bin/env python3
"""
Demo script for the modern overlay UI
"""

import tkinter as tk
from overlay_ui import OverlayUI
import time
import threading

def create_demo_suggestions():
    """Create demo suggestions to showcase the modern UI"""
    return [
        {
            "type": "code_fix",
            "title": "Fix Memory Leak",
            "priority": "high",
            "description": "The current implementation has a potential memory leak in the data processing loop. Consider adding proper cleanup and using context managers.",
            "code": "def process_data(data):\n    result = []\n    for item in data:\n        # Process item\n        result.append(transform(item))\n    return result\n\n# Fixed version:\ndef process_data(data):\n    with DataProcessor() as processor:\n        return [processor.transform(item) for item in data]"
        },
        {
            "type": "optimization",
            "title": "Optimize Database Query",
            "priority": "medium",
            "description": "The current query can be optimized by adding proper indexing and reducing the number of joins.",
            "code": "# Current query (slow)\nSELECT * FROM users u\nJOIN orders o ON u.id = o.user_id\nJOIN products p ON o.product_id = p.id\nWHERE u.status = 'active'\n\n# Optimized query\nSELECT u.id, u.name, o.total, p.name\nFROM users u\nJOIN orders o ON u.id = o.user_id\nJOIN products p ON o.product_id = p.id\nWHERE u.status = 'active'\nAND u.last_login > DATE_SUB(NOW(), INTERVAL 30 DAY)"
        },
        {
            "type": "best_practice",
            "title": "Add Error Handling",
            "priority": "medium",
            "description": "Consider adding comprehensive error handling to improve user experience and debugging capabilities.",
            "code": "try:\n    result = risky_operation()\nexcept SpecificException as e:\n    logger.error(f\"Operation failed: {e}\")\n    return handle_error(e)\nexcept Exception as e:\n    logger.critical(f\"Unexpected error: {e}\")\n    raise"
        },
        {
            "type": "security",
            "title": "Security Vulnerability",
            "priority": "high",
            "description": "SQL injection vulnerability detected. Use parameterized queries instead of string concatenation.",
            "code": "# Vulnerable code\nquery = f\"SELECT * FROM users WHERE name = '{username}'\"\n\n# Secure code\nquery = \"SELECT * FROM users WHERE name = %s\"\ncursor.execute(query, (username,))"
        },
        {
            "type": "documentation",
            "title": "Add API Documentation",
            "priority": "low",
            "description": "The API endpoints lack proper documentation. Consider adding OpenAPI/Swagger documentation.",
            "code": "@app.route('/api/users/<int:user_id>', methods=['GET'])\ndef get_user(user_id):\n    \"\"\"\n    Get user by ID\n    \n    :param user_id: The user ID\n    :return: User object\n    \"\"\"\n    return user_service.get_user(user_id)"
        }
    ]

def demo_suggestion_click(suggestion):
    """Demo callback for suggestion clicks"""
    print(f"Clicked on suggestion: {suggestion['title']}")

def demo_close():
    """Demo callback for close button"""
    print("Overlay closed")

def main():
    """Main demo function"""
    print("Starting Modern Overlay UI Demo...")
    
    # Create overlay instance
    overlay = OverlayUI()
    
    # Set callbacks
    overlay.set_callbacks(
        on_suggestion_click=demo_suggestion_click,
        on_close=demo_close
    )
    
    # Create demo suggestions
    suggestions = create_demo_suggestions()
    
    # Show overlay
    overlay.create_overlay(suggestions)
    
    # Add some demo interactions
    def update_demo():
        time.sleep(3)
        print("Updating suggestions...")
        new_suggestions = suggestions[:3]  # Show only first 3
        overlay.update_suggestions(new_suggestions)
        
        time.sleep(3)
        print("Adding more suggestions...")
        overlay.update_suggestions(suggestions)
    
    # Start update thread
    update_thread = threading.Thread(target=update_demo, daemon=True)
    update_thread.start()
    
    # Run the demo
    try:
        if overlay.root:
            overlay.root.mainloop()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    finally:
        overlay.destroy()
        print("Demo finished")

if __name__ == "__main__":
    main()
