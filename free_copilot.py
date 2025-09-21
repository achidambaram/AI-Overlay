#!/usr/bin/env python3
"""
Free Real-Time Overlay Copilot
Uses local AI models and rule-based suggestions - No API costs!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import re
import json
from typing import Dict, List, Optional
import logging

class FreeCopilot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Free Real-Time Overlay Copilot")
        self.root.geometry("800x600")
        
        # Rule-based suggestion engine
        self.suggestion_rules = self._load_suggestion_rules()
        
        # Demo contexts
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
        
    def _load_suggestion_rules(self) -> Dict:
        """Load rule-based suggestion patterns"""
        return {
            "python": {
                "syntax_errors": [
                    {
                        "pattern": r"def\s+\w+\s*\([^)]*\)\s*[^:]",
                        "fix": lambda m: m.group(0) + ":",
                        "title": "Missing Colon",
                        "description": "Add missing colon after function definition",
                        "priority": "high"
                    },
                    {
                        "pattern": r"if\s+[^:]+[^:]$",
                        "fix": lambda m: m.group(0) + ":",
                        "title": "Missing Colon",
                        "description": "Add missing colon after if statement",
                        "priority": "high"
                    },
                    {
                        "pattern": r"for\s+[^:]+[^:]$",
                        "fix": lambda m: m.group(0) + ":",
                        "title": "Missing Colon",
                        "description": "Add missing colon after for loop",
                        "priority": "high"
                    }
                ],
                "best_practices": [
                    {
                        "pattern": r"def\s+(\w+)\s*\(([^)]*)\):",
                        "suggestion": lambda m: f"def {m.group(1)}({m.group(2)}) -> Any:",
                        "title": "Add Type Hints",
                        "description": "Consider adding type hints for better code documentation",
                        "priority": "medium"
                    },
                    {
                        "pattern": r"print\s*\(",
                        "suggestion": "Use logging instead of print for production code",
                        "title": "Use Logging",
                        "description": "Replace print statements with proper logging",
                        "priority": "medium"
                    }
                ]
            },
            "javascript": {
                "reference_errors": [
                    {
                        "pattern": r"console\.log\((\w+)\)",
                        "check": lambda m: f"let {m.group(1)} = 'value';",
                        "title": "Declare Variable",
                        "description": "Variable is used before declaration",
                        "priority": "high"
                    },
                    {
                        "pattern": r"(\w+)\(\)",
                        "check": lambda m: f"function {m.group(1)}() {{\n    return 'Hello';\n}}",
                        "title": "Define Function",
                        "description": "Function is called but not defined",
                        "priority": "high"
                    }
                ],
                "best_practices": [
                    {
                        "pattern": r"var\s+(\w+)",
                        "suggestion": lambda m: f"const {m.group(1)}",
                        "title": "Use Const/Let",
                        "description": "Use const/let instead of var for better scoping",
                        "priority": "medium"
                    }
                ]
            },
            "html": {
                "validation_errors": [
                    {
                        "pattern": r"<p>([^<]*)",
                        "check": lambda m: f"<p>{m.group(1)}</p>",
                        "title": "Close Tags",
                        "description": "HTML tags should be properly closed",
                        "priority": "high"
                    },
                    {
                        "pattern": r"<img\s+[^>]*>",
                        "check": lambda m: m.group(0).replace(">", ' alt="description">'),
                        "title": "Add Alt Attribute",
                        "description": "Images should have alt attributes for accessibility",
                        "priority": "medium"
                    }
                ]
            }
        }
    
    def analyze_code(self, code: str, language: str) -> List[Dict]:
        """Analyze code using rule-based patterns"""
        suggestions = []
        
        if language not in self.suggestion_rules:
            return suggestions
        
        rules = self.suggestion_rules[language]
        
        # Check for syntax errors
        if "syntax_errors" in rules:
            for rule in rules["syntax_errors"]:
                matches = re.finditer(rule["pattern"], code, re.MULTILINE)
                for match in matches:
                    suggestions.append({
                        "type": "code_fix",
                        "title": rule["title"],
                        "description": rule["description"],
                        "code": rule["fix"](match),
                        "priority": rule["priority"]
                    })
        
        # Check for best practices
        if "best_practices" in rules:
            for rule in rules["best_practices"]:
                matches = re.finditer(rule["pattern"], code, re.MULTILINE)
                for match in matches:
                    if "suggestion" in rule:
                        if callable(rule["suggestion"]):
                            suggested_code = rule["suggestion"](match)
                        else:
                            suggested_code = rule["suggestion"]
                    else:
                        suggested_code = ""
                    
                    suggestions.append({
                        "type": "best_practice",
                        "title": rule["title"],
                        "description": rule["description"],
                        "code": suggested_code,
                        "priority": rule["priority"]
                    })
        
        # Check for reference errors
        if "reference_errors" in rules:
            for rule in rules["reference_errors"]:
                matches = re.finditer(rule["pattern"], code, re.MULTILINE)
                for match in matches:
                    if "check" in rule:
                        suggested_code = rule["check"](match)
                    else:
                        suggested_code = ""
                    
                    suggestions.append({
                        "type": "code_fix",
                        "title": rule["title"],
                        "description": rule["description"],
                        "code": suggested_code,
                        "priority": rule["priority"]
                    })
        
        # Check for validation errors
        if "validation_errors" in rules:
            for rule in rules["validation_errors"]:
                matches = re.finditer(rule["pattern"], code, re.MULTILINE)
                for match in matches:
                    if "check" in rule:
                        suggested_code = rule["check"](match)
                    else:
                        suggested_code = ""
                    
                    suggestions.append({
                        "type": "code_fix",
                        "title": rule["title"],
                        "description": rule["description"],
                        "code": suggested_code,
                        "priority": rule["priority"]
                    })
        
        return suggestions
    
    def setup_ui(self):
        """Setup the demo UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🚀 Free Real-Time Overlay Copilot",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="💰 No API costs - Uses local rule-based analysis",
            font=('Arial', 12),
            foreground='#4CAF50'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="This free version uses pattern matching and rule-based analysis to provide code suggestions without any API costs.",
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
            text="Analyze Code",
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
        left_frame = ttk.LabelFrame(content_frame, text="Code to Analyze", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.context_text = scrolledtext.ScrolledText(
            left_frame,
            height=15,
            width=40,
            font=('Courier', 9)
        )
        self.context_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Suggestions
        right_frame = ttk.LabelFrame(content_frame, text="Free AI Suggestions", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.suggestions_text = scrolledtext.ScrolledText(
            right_frame,
            height=15,
            width=40,
            font=('Arial', 9)
        )
        self.suggestions_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - No API costs!")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            foreground='#4CAF50'
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

Code Snippets to Analyze:
"""
        
        for i, snippet in enumerate(context['code_snippets'], 1):
            display_text += f"\n--- Snippet {i} ---\n{snippet}\n"
        
        self.context_text.delete(1.0, tk.END)
        self.context_text.insert(1.0, display_text)
        
    def generate_demo_suggestions(self):
        """Generate suggestions based on current context"""
        context = self.demo_contexts[self.current_context_index]
        language = context['language']
        
        # Analyze each code snippet
        all_suggestions = []
        for snippet in context['code_snippets']:
            suggestions = self.analyze_code(snippet, language)
            all_suggestions.extend(suggestions)
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_suggestions = []
        for suggestion in all_suggestions:
            if suggestion['title'] not in seen_titles:
                seen_titles.add(suggestion['title'])
                unique_suggestions.append(suggestion)
        
        self.demo_suggestions = unique_suggestions
        self.update_suggestions_display()
        self.status_var.set(f"Generated {len(self.demo_suggestions)} free suggestions - No API costs!")
        
    def update_suggestions_display(self):
        """Update the suggestions display"""
        display_text = ""
        
        if not self.demo_suggestions:
            display_text = "No issues found in the code! 🎉"
        else:
            for i, suggestion in enumerate(self.demo_suggestions, 1):
                display_text += f"🔧 Suggestion {i}: {suggestion['title']}\n"
                display_text += f"Type: {suggestion['type']}\n"
                display_text += f"Priority: {suggestion['priority']}\n"
                display_text += f"Description: {suggestion['description']}\n"
                if suggestion['code']:
                    display_text += f"Suggested Fix:\n{suggestion['code']}\n"
                display_text += "-" * 40 + "\n\n"
        
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, display_text)
        
    def show_overlay(self):
        """Show the overlay demo"""
        overlay_window = tk.Toplevel(self.root)
        overlay_window.title("🤖 Free AI Copilot Overlay")
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
            text="🤖 Free AI Copilot",
            font=('Arial', 12, 'bold'),
            foreground='#4CAF50'
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="💰 No API costs - Local analysis",
            font=('Arial', 8),
            foreground='#4CAF50'
        )
        subtitle_label.pack(pady=(0, 10))
        
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
            
            type_icon = "🔧" if suggestion['type'] == 'code_fix' else "✅"
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
                    text="💻 Suggested Fix:",
                    font=('Arial', 8, 'bold'),
                    foreground='#4CAF50'
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
            text=f"Found {len(self.demo_suggestions)} suggestions - FREE!",
            font=('Arial', 8),
            foreground='#4CAF50'
        ).pack(side=tk.LEFT, pady=(10, 0))
        
        ttk.Label(
            main_frame,
            text="Press ESC to close",
            font=('Arial', 8),
            foreground='#888888'
        ).pack(side=tk.RIGHT, pady=(10, 0))
        
        # Bind escape key
        overlay_window.bind('<Escape>', lambda e: overlay_window.destroy())
        
        self.status_var.set("Free overlay displayed - No costs!")
        
    def run(self):
        """Run the demo"""
        self.root.mainloop()

def main():
    """Main demo function"""
    print("🚀 Starting Free Real-Time Overlay Copilot")
    print("💰 No API costs - Uses local rule-based analysis")
    print("=" * 60)
    
    demo = FreeCopilot()
    demo.run()

if __name__ == "__main__":
    main() 