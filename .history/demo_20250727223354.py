#!/usr/bin/env python3
"""
Demo script for Real-Time Overlay Copilot
This script demonstrates the copilot's capabilities without requiring full setup.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import json
from typing import Dict, List

class CopilotDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Real-Time Overlay Copilot - Demo")
        self.root.geometry("800x600")
        
        # Demo data
        self.demo_contexts = [
            {
                "code_detected": True,
                "language": "python",
                "file_type": ".py",
                "error_indicators": ["SyntaxError", "IndentationError"],
                "suggestions_context": "Python code with syntax errors detected",
                "code_snippets": [
                    "def calculate_sum(a, b:\n    return a + b",
                    "if x > 0\n    print('Positive')",
                    "for i in range(10)\n    print(i)"
                ]
            },
            {
                "code_detected": True,
                "language": "javascript",
                "file_type": ".js",
                "error_indicators": ["ReferenceError", "TypeError"],
                "suggestions_context": "JavaScript code with reference errors",
                "code_snippets": [
                    "console.log(undefinedVariable);",
                    "const result = someFunction();",
                    "let arr = [1, 2, 3];\narr.push(4);"
                ]
            },
            {
                "code_detected": True,
                "language": "html",
                "file_type": ".html",
                "error_indicators": ["ValidationError"],
                "suggestions_context": "HTML with validation issues",
                "code_snippets": [
                    "<div>\n    <p>Unclosed paragraph\n</div>",
                    "<img src='image.jpg'>",
                    "<script>\n    console.log('Hello');\n</script>"
                ]
            }
        ]
        
        self.current_context_index = 0
        self.demo_suggestions = []
        
        self.setup_ui()
        self.generate_demo_suggestions()
        
    def setup_ui(self):
        """Setup the demo UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🚀 Real-Time Overlay Copilot Demo",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="This demo showcases the copilot's ability to analyze code and provide intelligent suggestions.",
            font=('Arial', 10),
            wraplength=700
        )
        desc_label.pack(pady=(0, 20))
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Context selector
        ttk.Label(control_frame, text="Select Demo Context:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.context_var = tk.StringVar(value="Python with Syntax Errors")
        context_combo = ttk.Combobox(
            control_frame,
            textvariable=self.context_var,
            values=[
                "Python with Syntax Errors",
                "JavaScript with Reference Errors", 
                "HTML with Validation Issues"
            ],
            state="readonly",
            width=30
        )
        context_combo.pack(side=tk.LEFT, padx=(0, 20))
        context_combo.bind('<<ComboboxSelected>>', self.on_context_change)
        
        # Generate button
        generate_btn = ttk.Button(
            control_frame,
            text="Generate Suggestions",
            command=self.generate_demo_suggestions
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Show overlay button
        overlay_btn = ttk.Button(
            control_frame,
            text="Show Overlay",
            command=self.show_overlay
        )
        overlay_btn.pack(side=tk.LEFT)
        
        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Context
        left_frame = ttk.LabelFrame(content_frame, text="Current Context", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.context_text = scrolledtext.ScrolledText(
            left_frame,
            height=15,
            width=40,
            font=('Courier', 9)
        )
        self.context_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Suggestions
        right_frame = ttk.LabelFrame(content_frame, text="AI Suggestions", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.suggestions_text = scrolledtext.ScrolledText(
            right_frame,
            height=15,
            width=40,
            font=('Arial', 9)
        )
        self.suggestions_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            foreground='#666666'
        )
        status_label.pack(pady=(10, 0))
        
        # Load initial context
        self.update_context_display()
        
    def on_context_change(self, event):
        """Handle context change"""
        selection = self.context_var.get()
        if "Python" in selection:
            self.current_context_index = 0
        elif "JavaScript" in selection:
            self.current_context_index = 1
        elif "HTML" in selection:
            self.current_context_index = 2
        
        self.update_context_display()
        self.generate_demo_suggestions()
        
    def update_context_display(self):
        """Update the context display"""
        context = self.demo_contexts[self.current_context_index]
        
        display_text = f"""Language: {context['language']}
File Type: {context['file_type']}
Error Indicators: {', '.join(context['error_indicators'])}
Context: {context['suggestions_context']}

Code Snippets:
"""
        
        for i, snippet in enumerate(context['code_snippets'], 1):
            display_text += f"\n--- Snippet {i} ---\n{snippet}\n"
        
        self.context_text.delete(1.0, tk.END)
        self.context_text.insert(1.0, display_text)
        
    def generate_demo_suggestions(self):
        """Generate demo suggestions based on current context"""
        context = self.demo_contexts[self.current_context_index]
        
        if context['language'] == 'python':
            self.demo_suggestions = [
                {
                    "type": "code_fix",
                    "title": "Fix Missing Colon",
                    "description": "Add missing colon after function definition and if statement",
                    "code": "def calculate_sum(a, b):\n    return a + b\n\nif x > 0:\n    print('Positive')",
                    "priority": "high"
                },
                {
                    "type": "code_fix", 
                    "title": "Fix Indentation",
                    "description": "Ensure proper indentation for the for loop",
                    "code": "for i in range(10):\n    print(i)",
                    "priority": "high"
                },
                {
                    "type": "best_practice",
                    "title": "Add Type Hints",
                    "description": "Consider adding type hints for better code documentation",
                    "code": "def calculate_sum(a: int, b: int) -> int:\n    return a + b",
                    "priority": "medium"
                }
            ]
        elif context['language'] == 'javascript':
            self.demo_suggestions = [
                {
                    "type": "code_fix",
                    "title": "Declare Variable",
                    "description": "Declare undefinedVariable before using it",
                    "code": "let undefinedVariable = 'some value';\nconsole.log(undefinedVariable);",
                    "priority": "high"
                },
                {
                    "type": "code_fix",
                    "title": "Define Function",
                    "description": "Define someFunction before calling it",
                    "code": "function someFunction() {\n    return 'Hello World';\n}\nconst result = someFunction();",
                    "priority": "high"
                },
                {
                    "type": "optimization",
                    "title": "Use Const for Array",
                    "description": "Use const for array declaration since it's not reassigned",
                    "code": "const arr = [1, 2, 3];\narr.push(4);",
                    "priority": "low"
                }
            ]
        else:  # HTML
            self.demo_suggestions = [
                {
                    "type": "code_fix",
                    "title": "Close Paragraph Tag",
                    "description": "Add closing paragraph tag",
                    "code": "<div>\n    <p>Unclosed paragraph</p>\n</div>",
                    "priority": "high"
                },
                {
                    "type": "code_fix",
                    "title": "Add Alt Attribute",
                    "description": "Add alt attribute for accessibility",
                    "code": "<img src='image.jpg' alt='Description'>",
                    "priority": "medium"
                },
                {
                    "type": "best_practice",
                    "title": "Add Type Attribute",
                    "description": "Add type attribute to script tag",
                    "code": "<script type='text/javascript'>\n    console.log('Hello');\n</script>",
                    "priority": "low"
                }
            ]
        
        self.update_suggestions_display()
        self.status_var.set(f"Generated {len(self.demo_suggestions)} suggestions")
        
    def update_suggestions_display(self):
        """Update the suggestions display"""
        display_text = ""
        
        for i, suggestion in enumerate(self.demo_suggestions, 1):
            display_text += f"🔧 Suggestion {i}: {suggestion['title']}\n"
            display_text += f"Type: {suggestion['type']}\n"
            display_text += f"Priority: {suggestion['priority']}\n"
            display_text += f"Description: {suggestion['description']}\n"
            if suggestion['code']:
                display_text += f"Code:\n{suggestion['code']}\n"
            display_text += "-" * 40 + "\n\n"
        
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, display_text)
        
    def show_overlay(self):
        """Show the overlay demo"""
        overlay_window = tk.Toplevel(self.root)
        overlay_window.title("🤖 AI Copilot Overlay")
        overlay_window.geometry("400x500")
        overlay_window.attributes('-topmost', True)
        
        # Configure overlay appearance
        overlay_window.configure(bg='#2D3748')
        
        # Main frame
        main_frame = ttk.Frame(overlay_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🤖 AI Copilot",
            font=('Arial', 12, 'bold'),
            foreground='#4299E1'
        )
        title_label.pack(pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Suggestions
        for suggestion in self.demo_suggestions:
            suggestion_frame = ttk.Frame(main_frame)
            suggestion_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Header
            header_frame = ttk.Frame(suggestion_frame)
            header_frame.pack(fill=tk.X)
            
            type_icon = "🔧" if suggestion['type'] == 'code_fix' else "⚡" if suggestion['type'] == 'optimization' else "✅"
            ttk.Label(header_frame, text=type_icon, font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Label(
                header_frame,
                text=suggestion['title'],
                font=('Arial', 10, 'bold'),
                foreground='#4ECDC4'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(
                header_frame,
                text=suggestion['priority'].upper(),
                font=('Arial', 7),
                foreground='#888888'
            ).pack(side=tk.RIGHT)
            
            # Description
            desc_text = scrolledtext.ScrolledText(
                suggestion_frame,
                height=3,
                wrap=tk.WORD,
                font=('Arial', 9),
                bg='#2D3748',
                fg='#FFFFFF',
                relief=tk.FLAT,
                borderwidth=0
            )
            desc_text.insert(tk.END, suggestion['description'])
            desc_text.configure(state=tk.DISABLED)
            desc_text.pack(fill=tk.X, pady=(2, 5))
            
            # Code (if available)
            if suggestion['code']:
                code_frame = ttk.Frame(suggestion_frame)
                code_frame.pack(fill=tk.X, pady=(0, 5))
                
                ttk.Label(
                    code_frame,
                    text="💻 Code:",
                    font=('Arial', 8, 'bold'),
                    foreground='#4299E1'
                ).pack(anchor=tk.W)
                
                code_text = scrolledtext.ScrolledText(
                    code_frame,
                    height=4,
                    wrap=tk.NONE,
                    font=('Courier', 8),
                    bg='#1A202C',
                    fg='#E2E8F0',
                    relief=tk.FLAT,
                    borderwidth=1
                )
                code_text.insert(tk.END, suggestion['code'])
                code_text.configure(state=tk.DISABLED)
                code_text.pack(fill=tk.X)
        
        # Status
        ttk.Label(
            main_frame,
            text=f"Found {len(self.demo_suggestions)} suggestions",
            font=('Arial', 8),
            foreground='#888888'
        ).pack(side=tk.LEFT, pady=(10, 0))
        
        ttk.Label(
            main_frame,
            text="Press ESC to close",
            font=('Arial', 8),
            foreground='#888888'
        ).pack(side=tk.RIGHT, pady=(10, 0))
        
        # Bind escape key
        overlay_window.bind('<Escape>', lambda e: overlay_window.destroy())
        
        self.status_var.set("Overlay displayed")
        
    def run(self):
        """Run the demo"""
        self.root.mainloop()

def main():
    """Main demo function"""
    print("🚀 Starting Real-Time Overlay Copilot Demo")
    print("This demo showcases the copilot's capabilities without requiring full setup.")
    print("=" * 60)
    
    demo = CopilotDemo()
    demo.run()

if __name__ == "__main__":
    main() 