"""
Modern Overlay UI module for displaying AI suggestions
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, font
import threading
import time
import math
from typing import Dict, List, Optional, Callable
import logging
from config import Config

class OverlayUI:
    def __init__(self):
        self.root = None
        self.is_visible = False
        self.current_suggestions = []
        self.logger = logging.getLogger(__name__)
        
        # UI elements
        self.title_label = None
        self.suggestions_frame = None
        self.status_label = None
        self.close_button = None
        self.header_frame = None
        self.content_frame = None
        
        # Callbacks
        self.on_suggestion_click = None
        self.on_close = None
        
        # Animation and effects
        self.fade_thread = None
        self.fade_direction = 1  # 1 for fade in, -1 for fade out
        self.animation_running = False
        self.hover_widgets = {}  # Track hover states
        
        # Modern styling
        self.setup_modern_styles()
        
    def setup_modern_styles(self):
        """Setup modern ttk styles"""
        self.styles = {
            'modern_frame': {
                'background': Config.OVERLAY_COLOR,
                'relief': 'flat',
                'borderwidth': 0
            },
            'modern_button': {
                'background': Config.OVERLAY_ACCENT_COLOR,
                'foreground': '#FFFFFF',
                'relief': 'flat',
                'borderwidth': 0,
                'font': (Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_BODY, 'bold')
            },
            'modern_label': {
                'background': Config.OVERLAY_COLOR,
                'foreground': Config.OVERLAY_TEXT_COLOR,
                'font': (Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_BODY)
            },
            'title_label': {
                'background': Config.OVERLAY_COLOR,
                'foreground': Config.OVERLAY_BORDER_COLOR,
                'font': (Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_TITLE, Config.OVERLAY_FONT_WEIGHT_TITLE)
            },
            'suggestion_frame': {
                'background': '#2A2A2A',
                'relief': 'flat',
                'borderwidth': 1
            }
        }
        
    def create_overlay(self, suggestions: List[Dict], position: Dict = None):
        """Create and show the modern overlay with suggestions"""
        try:
            # Destroy existing window if any
            if self.root:
                self.root.destroy()
            
            # Create new window
            self.root = tk.Tk()
            self.root.title("AI Copilot")
            
            # Configure window properties with modern styling
            self._configure_modern_window(position)
            
            # Create modern UI elements
            self._create_modern_ui_elements(suggestions)
            
            # Show window with animation
            self.is_visible = True
            self.root.deiconify()
            
            # Start modern fade-in animation
            self._start_modern_fade_animation(1)
            
            # Set up auto-hide timer
            self._setup_auto_hide()
            
            self.logger.info("Modern overlay created and shown")
            
        except Exception as e:
            self.logger.error(f"Error creating overlay: {e}")
    
    def _configure_modern_window(self, position: Dict = None):
        """Configure modern window properties with enhanced styling"""
        # Get position
        if position is None:
            position = Config.get_overlay_position()
        
        # Window configuration with modern settings
        self.root.geometry(f"{Config.OVERLAY_WIDTH}x{Config.OVERLAY_HEIGHT}+{position['x']}+{position['y']}")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep on top
        self.root.attributes('-alpha', Config.OVERLAY_OPACITY)  # Set transparency
        
        # Modern window styling
        self.root.configure(bg=Config.OVERLAY_COLOR)
        
        # Configure modern appearance with rounded corners effect
        self.root.option_add('*TFrame*background', Config.OVERLAY_COLOR)
        self.root.option_add('*TLabel*background', Config.OVERLAY_COLOR)
        self.root.option_add('*TLabel*foreground', Config.OVERLAY_TEXT_COLOR)
        self.root.option_add('*TButton*background', Config.OVERLAY_ACCENT_COLOR)
        self.root.option_add('*TButton*foreground', '#FFFFFF')
        
        # Enhanced event bindings
        self.root.bind('<Escape>', self._on_escape)
        self.root.bind('<Button-1>', self._on_click)
        self.root.bind('<Motion>', self._on_mouse_move)
        self.root.bind('<Enter>', self._on_mouse_enter)
        self.root.bind('<Leave>', self._on_mouse_leave)
        
        # Make window draggable with modern feel
        self.root.bind('<Button-1>', self._start_drag)
        self.root.bind('<B1-Motion>', self._on_drag)
        
        # Add keyboard shortcuts
        self.root.bind('<Control-q>', self._on_escape)
        self.root.bind('<Control-w>', self._on_escape)
    
    def _create_modern_ui_elements(self, suggestions: List[Dict]):
        """Create modern UI elements with enhanced styling"""
        # Main container with modern styling
        self.main_frame = tk.Frame(self.root, **self.styles['modern_frame'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Header section with modern design
        self._create_modern_header()
        
        # Content area with modern styling
        self._create_modern_content_area(suggestions)
        
        # Footer with status and controls
        self._create_modern_footer()
    
    def _create_modern_header(self):
        """Create modern header with gradient-like effect"""
        self.header_frame = tk.Frame(self.main_frame, **self.styles['modern_frame'])
        self.header_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Title with modern styling
        self.title_label = tk.Label(
            self.header_frame,
            text="🤖 AI Copilot",
            **self.styles['title_label']
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Close button with modern styling
        self.close_button = tk.Button(
            self.header_frame,
            text="✕",
            width=2,
            height=1,
            **self.styles['modern_button'],
            command=self._on_close_click
        )
        self.close_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Add hover effects
        self._add_hover_effect(self.close_button, Config.OVERLAY_ERROR_COLOR)
        
        # Modern separator line
        separator = tk.Frame(self.header_frame, height=1, bg=Config.OVERLAY_BORDER_COLOR)
        separator.pack(fill=tk.X, pady=(8, 0))
    
    def _create_modern_content_area(self, suggestions: List[Dict]):
        """Create modern content area with enhanced scrolling"""
        # Content frame
        self.content_frame = tk.Frame(self.main_frame, **self.styles['modern_frame'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        # Create scrollable canvas for modern feel
        self.canvas = tk.Canvas(
            self.content_frame,
            bg=Config.OVERLAY_COLOR,
            highlightthickness=0,
            relief='flat'
        )
        
        # Modern scrollbar
        self.scrollbar = tk.Scrollbar(
            self.content_frame,
            orient="vertical",
            command=self.canvas.yview,
            bg=Config.OVERLAY_COLOR,
            troughcolor='#3A3A3A',
            activebackground=Config.OVERLAY_ACCENT_COLOR
        )
        
        # Scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, **self.styles['modern_frame'])
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Add mousewheel scrolling
        self._bind_mousewheel()
        
        # Add suggestions
        self._add_modern_suggestions(suggestions)
    
    def _create_modern_footer(self):
        """Create modern footer with status and instructions"""
        footer_frame = tk.Frame(self.main_frame, **self.styles['modern_frame'])
        footer_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Status label with modern styling
        self.status_label = tk.Label(
            footer_frame,
            text="Ready",
            **self.styles['modern_label']
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Instructions with modern styling
        instructions_label = tk.Label(
            footer_frame,
            text="ESC to close • Drag to move",
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_SMALL),
            foreground='#888888',
            background=Config.OVERLAY_COLOR
        )
        instructions_label.pack(side=tk.RIGHT)
    
    def _add_modern_suggestions(self, suggestions: List[Dict]):
        """Add modern suggestion widgets with enhanced styling"""
        # Clear existing suggestions
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.current_suggestions = suggestions
        
        if not suggestions:
            self._create_empty_state()
            return
        
        # Add modern suggestion cards
        for i, suggestion in enumerate(suggestions):
            suggestion_card = self._create_modern_suggestion_card(suggestion, i)
            suggestion_card.pack(fill=tk.X, pady=(0, 8))
    
    def _create_empty_state(self):
        """Create modern empty state"""
        empty_frame = tk.Frame(self.scrollable_frame, **self.styles['modern_frame'])
        empty_frame.pack(expand=True, fill=tk.BOTH, pady=40)
        
        # Empty state icon
        icon_label = tk.Label(
            empty_frame,
            text="💡",
            font=('Arial', 24),
            **self.styles['modern_label']
        )
        icon_label.pack(pady=(0, 10))
        
        # Empty state text
        text_label = tk.Label(
            empty_frame,
            text="No suggestions available\nTry asking a question or\nproviding more context",
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_BODY),
            foreground='#888888',
            background=Config.OVERLAY_COLOR,
            justify=tk.CENTER
        )
        text_label.pack()
    
    def _create_modern_suggestion_card(self, suggestion: Dict, index: int) -> tk.Frame:
        """Create a modern suggestion card with enhanced styling"""
        # Main card frame with modern styling
        card_frame = tk.Frame(
            self.scrollable_frame,
            bg='#2A2A2A',
            relief='flat',
            borderwidth=1
        )
        
        # Add padding and rounded corners effect
        inner_frame = tk.Frame(card_frame, bg='#2A2A2A')
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # Header with type icon and title
        header_frame = tk.Frame(inner_frame, bg='#2A2A2A')
        header_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Type icon with modern styling
        type_icon = self._get_type_icon(suggestion.get("type", "general"))
        icon_label = tk.Label(
            header_frame,
            text=type_icon,
            font=('Arial', 14),
            bg='#2A2A2A',
            fg=self._get_priority_color(suggestion.get("priority", "medium"))
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Title with modern typography
        title_label = tk.Label(
            header_frame,
            text=suggestion.get("title", "Suggestion"),
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_BODY, 'bold'),
            bg='#2A2A2A',
            fg=Config.OVERLAY_TEXT_COLOR,
            anchor='w'
        )
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Priority badge with modern styling
        priority_color = self._get_priority_color(suggestion.get("priority", "medium"))
        priority_label = tk.Label(
            header_frame,
            text=suggestion.get("priority", "medium").upper(),
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], 8, 'bold'),
            bg=priority_color,
            fg='#FFFFFF',
            padx=6,
            pady=2
        )
        priority_label.pack(side=tk.RIGHT)
        
        # Description with modern text styling
        description_text = scrolledtext.ScrolledText(
            inner_frame,
            height=3,
            wrap=tk.WORD,
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], Config.OVERLAY_FONT_SIZE_BODY),
            bg='#2A2A2A',
            fg=Config.OVERLAY_TEXT_COLOR,
            insertbackground=Config.OVERLAY_TEXT_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        description_text.insert(tk.END, suggestion.get("description", ""))
        description_text.configure(state=tk.DISABLED)
        description_text.pack(fill=tk.X, pady=(0, 8))
        
        # Code snippet with modern code styling
        if suggestion.get("code"):
            self._add_modern_code_snippet(inner_frame, suggestion["code"])
        
        # Action buttons with modern styling
        self._add_modern_action_buttons(inner_frame, suggestion)
        
        # Add hover effects to the card
        self._add_card_hover_effects(card_frame, inner_frame)
        
        # Bind click event
        card_frame.bind('<Button-1>', lambda e, s=suggestion: self._on_suggestion_click(s))
        
        return card_frame
    
    def _add_modern_code_snippet(self, parent, code: str):
        """Add modern code snippet with syntax highlighting effect"""
        # Code header
        code_header = tk.Frame(parent, bg='#2A2A2A')
        code_header.pack(fill=tk.X, pady=(0, 4))
        
        code_label = tk.Label(
            code_header,
            text="💻 Code:",
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], 9, 'bold'),
            bg='#2A2A2A',
            fg=Config.OVERLAY_ACCENT_COLOR
        )
        code_label.pack(anchor=tk.W)
        
        # Code text with modern styling
        code_text = scrolledtext.ScrolledText(
            parent,
            height=4,
            wrap=tk.NONE,
            font=('Monaco', 9),
            bg='#1A1A1A',
            fg='#E2E8F0',
            insertbackground='#E2E8F0',
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0
        )
        code_text.insert(tk.END, code)
        code_text.configure(state=tk.DISABLED)
        code_text.pack(fill=tk.X, pady=(0, 8))
    
    def _add_modern_action_buttons(self, parent, suggestion: Dict):
        """Add modern action buttons with enhanced styling"""
        button_frame = tk.Frame(parent, bg='#2A2A2A')
        button_frame.pack(fill=tk.X, pady=(4, 0))
        
        # Copy button with modern styling
        copy_button = tk.Button(
            button_frame,
            text="📋 Copy",
            width=10,
            height=1,
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], 9, 'bold'),
            bg=Config.OVERLAY_INFO_COLOR,
            fg='#FFFFFF',
            relief=tk.FLAT,
            borderwidth=0,
            command=lambda: self._copy_suggestion(suggestion)
        )
        copy_button.pack(side=tk.LEFT, padx=(0, 8))
        
        # Apply button with modern styling
        apply_button = tk.Button(
            button_frame,
            text="✅ Apply",
            width=10,
            height=1,
            font=(Config.OVERLAY_FONT_FAMILY.split(',')[0], 9, 'bold'),
            bg=Config.OVERLAY_SUCCESS_COLOR,
            fg='#FFFFFF',
            relief=tk.FLAT,
            borderwidth=0,
            command=lambda: self._apply_suggestion(suggestion)
        )
        apply_button.pack(side=tk.LEFT)
        
        # Add hover effects
        self._add_hover_effect(copy_button, '#2563EB')
        self._add_hover_effect(apply_button, '#059669')
    
    def _add_hover_effect(self, widget, hover_color):
        """Add modern hover effect to widget"""
        original_color = widget.cget('bg')
        
        def on_enter(event):
            widget.configure(bg=hover_color)
        
        def on_leave(event):
            widget.configure(bg=original_color)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def _add_card_hover_effects(self, card_frame, inner_frame):
        """Add modern hover effects to suggestion cards"""
        original_bg = card_frame.cget('bg')
        hover_bg = '#3A3A3A'
        
        def on_enter(event):
            card_frame.configure(bg=hover_bg)
            inner_frame.configure(bg=hover_bg)
            # Update all child widgets
            for child in inner_frame.winfo_children():
                if hasattr(child, 'configure') and 'bg' in str(child.configure()):
                    try:
                        child.configure(bg=hover_bg)
                    except:
                        pass
        
        def on_leave(event):
            card_frame.configure(bg=original_bg)
            inner_frame.configure(bg=original_bg)
            # Reset all child widgets
            for child in inner_frame.winfo_children():
                if hasattr(child, 'configure') and 'bg' in str(child.configure()):
                    try:
                        if '2A2A2A' in str(child.configure()):
                            child.configure(bg='#2A2A2A')
                    except:
                        pass
        
        card_frame.bind('<Enter>', on_enter)
        card_frame.bind('<Leave>', on_leave)
    
    def _bind_mousewheel(self):
        """Bind mousewheel scrolling to canvas"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    def _start_modern_fade_animation(self, direction: int):
        """Start modern fade animation with smooth transitions"""
        self.fade_direction = direction
        if self.animation_running:
            return
        
        self.animation_running = True
        self.fade_thread = threading.Thread(target=self._modern_fade_animation, daemon=True)
        self.fade_thread.start()
    
    def _modern_fade_animation(self):
        """Modern fade animation with smooth easing"""
        try:
            current_alpha = self.root.attributes('-alpha')
            target_alpha = Config.OVERLAY_OPACITY if self.fade_direction == 1 else 0.0
            duration = Config.OVERLAY_FADE_DURATION
            fps = 60
            steps = int(duration * fps)
            
            for i in range(steps):
                if not self.animation_running:
                    break
                
                # Smooth easing function (ease-out)
                progress = i / steps
                eased_progress = 1 - (1 - progress) ** 3
                
                if self.fade_direction == 1:
                    new_alpha = current_alpha + (target_alpha - current_alpha) * eased_progress
                else:
                    new_alpha = current_alpha - (current_alpha - target_alpha) * eased_progress
                
                self.root.attributes('-alpha', new_alpha)
                time.sleep(1 / fps)
            
            self.root.attributes('-alpha', target_alpha)
            
            if self.fade_direction == -1:
                self.root.withdraw()
                self.is_visible = False
            
            self.animation_running = False
            
        except Exception as e:
            self.logger.error(f"Error in modern fade animation: {e}")
            self.animation_running = False
    
    def _on_mouse_enter(self, event):
        """Handle mouse enter with modern effects"""
        # Could add subtle glow effect or scale animation
        pass
    
    def _on_mouse_leave(self, event):
        """Handle mouse leave with modern effects"""
        # Reset any hover effects
        pass
    
    def _configure_window(self, position: Dict = None):
        """Configure window properties"""
        # Get position
        if position is None:
            position = Config.get_overlay_position()
        
        # Window configuration
        self.root.geometry(f"{Config.OVERLAY_WIDTH}x{Config.OVERLAY_HEIGHT}+{position['x']}+{position['y']}")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep on top
        self.root.attributes('-alpha', Config.OVERLAY_OPACITY)  # Set transparency
        
        # Configure appearance
        self.root.configure(bg=Config.OVERLAY_COLOR)
        self.root.option_add('*TFrame*background', Config.OVERLAY_COLOR)
        self.root.option_add('*TLabel*background', Config.OVERLAY_COLOR)
        self.root.option_add('*TLabel*foreground', Config.OVERLAY_TEXT_COLOR)
        
        # Bind events
        self.root.bind('<Escape>', self._on_escape)
        self.root.bind('<Button-1>', self._on_click)
        self.root.bind('<Motion>', self._on_mouse_move)
        
        # Make window draggable
        self.root.bind('<Button-1>', self._start_drag)
        self.root.bind('<B1-Motion>', self._on_drag)
    
    def _create_ui_elements(self, suggestions: List[Dict]):
        """Create UI elements"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        self.title_label = ttk.Label(
            title_frame, 
            text="🤖 AI Copilot", 
            font=('Arial', 12, 'bold'),
            foreground=Config.OVERLAY_BORDER_COLOR
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Close button
        self.close_button = ttk.Button(
            title_frame,
            text="✕",
            width=3,
            command=self._on_close_click
        )
        self.close_button.pack(side=tk.RIGHT)
        
        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Suggestions area
        self.suggestions_frame = ttk.Frame(main_frame)
        self.suggestions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add suggestions
        self._add_suggestions(suggestions)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text=f"Found {len(suggestions)} suggestions",
            font=('Arial', 8),
            foreground='#888888'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Instructions
        instructions_label = ttk.Label(
            status_frame,
            text="Press ESC to close",
            font=('Arial', 8),
            foreground='#888888'
        )
        instructions_label.pack(side=tk.RIGHT)
    
    def _add_suggestions(self, suggestions: List[Dict]):
        """Add suggestion widgets to the frame"""
        # Clear existing suggestions
        for widget in self.suggestions_frame.winfo_children():
            widget.destroy()
        
        self.current_suggestions = suggestions
        
        if not suggestions:
            # No suggestions
            no_suggestions_label = ttk.Label(
                self.suggestions_frame,
                text="No suggestions available",
                font=('Arial', 10),
                foreground='#888888'
            )
            no_suggestions_label.pack(pady=20)
            return
        
        # Create scrollable frame for suggestions
        canvas = tk.Canvas(self.suggestions_frame, bg=Config.OVERLAY_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.suggestions_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add suggestions
        for i, suggestion in enumerate(suggestions):
            suggestion_widget = self._create_suggestion_widget(scrollable_frame, suggestion, i)
            suggestion_widget.pack(fill=tk.X, pady=(0, 5))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_suggestion_widget(self, parent, suggestion: Dict, index: int) -> ttk.Frame:
        """Create a widget for a single suggestion"""
        # Main frame
        suggestion_frame = ttk.Frame(parent)
        suggestion_frame.configure(style='Suggestion.TFrame')
        
        # Header frame
        header_frame = ttk.Frame(suggestion_frame)
        header_frame.pack(fill=tk.X, pady=(5, 2))
        
        # Type icon and title
        type_icon = self._get_type_icon(suggestion.get("type", "general"))
        type_label = ttk.Label(
            header_frame,
            text=type_icon,
            font=('Arial', 12)
        )
        type_label.pack(side=tk.LEFT, padx=(0, 5))
        
        title_label = ttk.Label(
            header_frame,
            text=suggestion.get("title", "Suggestion"),
            font=('Arial', 10, 'bold'),
            foreground=self._get_priority_color(suggestion.get("priority", "medium"))
        )
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Priority badge
        priority_label = ttk.Label(
            header_frame,
            text=suggestion.get("priority", "medium").upper(),
            font=('Arial', 7),
            foreground='#888888'
        )
        priority_label.pack(side=tk.RIGHT)
        
        # Description
        description_text = scrolledtext.ScrolledText(
            suggestion_frame,
            height=3,
            wrap=tk.WORD,
            font=('Arial', 9),
            bg=Config.OVERLAY_COLOR,
            fg=Config.OVERLAY_TEXT_COLOR,
            insertbackground=Config.OVERLAY_TEXT_COLOR,
            relief=tk.FLAT,
            borderwidth=0
        )
        description_text.insert(tk.END, suggestion.get("description", ""))
        description_text.configure(state=tk.DISABLED)
        description_text.pack(fill=tk.X, pady=(2, 5))
        
        # Code snippet (if available)
        if suggestion.get("code"):
            code_frame = ttk.Frame(suggestion_frame)
            code_frame.pack(fill=tk.X, pady=(0, 5))
            
            code_label = ttk.Label(
                code_frame,
                text="💻 Code:",
                font=('Arial', 8, 'bold'),
                foreground=Config.OVERLAY_BORDER_COLOR
            )
            code_label.pack(anchor=tk.W)
            
            code_text = scrolledtext.ScrolledText(
                code_frame,
                height=4,
                wrap=tk.NONE,
                font=('Courier', 8),
                bg='#1A202C',
                fg='#E2E8F0',
                insertbackground='#E2E8F0',
                relief=tk.FLAT,
                borderwidth=1
            )
            code_text.insert(tk.END, suggestion["code"])
            code_text.configure(state=tk.DISABLED)
            code_text.pack(fill=tk.X)
        
        # Action buttons
        button_frame = ttk.Frame(suggestion_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        copy_button = ttk.Button(
            button_frame,
            text="Copy",
            width=8,
            command=lambda: self._copy_suggestion(suggestion)
        )
        copy_button.pack(side=tk.LEFT, padx=(0, 5))
        
        apply_button = ttk.Button(
            button_frame,
            text="Apply",
            width=8,
            command=lambda: self._apply_suggestion(suggestion)
        )
        apply_button.pack(side=tk.LEFT)
        
        # Bind click event
        suggestion_frame.bind('<Button-1>', lambda e, s=suggestion: self._on_suggestion_click(s))
        
        return suggestion_frame
    
    def _get_type_icon(self, suggestion_type: str) -> str:
        """Get icon for suggestion type"""
        icons = {
            "code_fix": "🔧",
            "optimization": "⚡",
            "best_practice": "✅",
            "security": "🔒",
            "documentation": "📝",
            "general": "💡"
        }
        return icons.get(suggestion_type, "💡")
    
    def _get_priority_color(self, priority: str) -> str:
        """Get color for priority level"""
        colors = {
            "high": "#FF6B6B",
            "medium": "#4ECDC4",
            "low": "#45B7D1"
        }
        return colors.get(priority, "#4ECDC4")
    
    def _copy_suggestion(self, suggestion: Dict):
        """Copy suggestion to clipboard"""
        try:
            self.root.clipboard_clear()
            if suggestion.get("code"):
                self.root.clipboard_append(suggestion["code"])
            else:
                self.root.clipboard_append(suggestion.get("description", ""))
            
            self._show_status("Copied to clipboard!")
            self.logger.info("Suggestion copied to clipboard")
        except Exception as e:
            self.logger.error(f"Error copying to clipboard: {e}")
    
    def _apply_suggestion(self, suggestion: Dict):
        """Apply suggestion (callback to main application)"""
        if self.on_suggestion_click:
            self.on_suggestion_click(suggestion)
        self._show_status("Suggestion applied!")
    
    def _on_suggestion_click(self, suggestion: Dict):
        """Handle suggestion click"""
        if self.on_suggestion_click:
            self.on_suggestion_click(suggestion)
    
    def _on_close_click(self):
        """Handle close button click"""
        self.hide_overlay()
        if self.on_close:
            self.on_close()
    
    def _on_escape(self, event):
        """Handle escape key"""
        self.hide_overlay()
    
    def _on_click(self, event):
        """Handle window click"""
        pass  # Prevent window from closing on click
    
    def _on_mouse_move(self, event):
        """Handle mouse movement"""
        pass  # Could be used for hover effects
    
    def _start_drag(self, event):
        """Start window drag"""
        self.root.x = event.x
        self.root.y = event.y
    
    def _on_drag(self, event):
        """Handle window drag"""
        deltax = event.x - self.root.x
        deltay = event.y - self.root.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def _start_fade_animation(self, direction: int):
        """Start fade animation"""
        self.fade_direction = direction
        if self.fade_thread and self.fade_thread.is_alive():
            return
        
        self.fade_thread = threading.Thread(target=self._fade_animation, daemon=True)
        self.fade_thread.start()
    
    def _fade_animation(self):
        """Fade animation thread"""
        try:
            current_alpha = self.root.attributes('-alpha')
            target_alpha = Config.OVERLAY_OPACITY if self.fade_direction == 1 else 0.0
            step = 0.05
            
            while abs(current_alpha - target_alpha) > step:
                if self.fade_direction == 1:
                    current_alpha = min(current_alpha + step, target_alpha)
                else:
                    current_alpha = max(current_alpha - step, target_alpha)
                
                self.root.attributes('-alpha', current_alpha)
                time.sleep(0.02)
            
            self.root.attributes('-alpha', target_alpha)
            
            if self.fade_direction == -1:
                self.root.withdraw()
                self.is_visible = False
            
        except Exception as e:
            self.logger.error(f"Error in fade animation: {e}")
    
    def _setup_auto_hide(self):
        """Setup auto-hide timer"""
        def auto_hide():
            time.sleep(30)  # Auto-hide after 30 seconds
            if self.is_visible:
                self.hide_overlay()
        
        auto_hide_thread = threading.Thread(target=auto_hide, daemon=True)
        auto_hide_thread.start()
    
    def _show_status(self, message: str):
        """Show status message"""
        if self.status_label:
            self.status_label.configure(text=message)
            # Reset status after 3 seconds
            threading.Timer(3.0, lambda: self.status_label.configure(text="")).start()
    
    def update_suggestions(self, suggestions: List[Dict]):
        """Update suggestions in the overlay"""
        if self.is_visible and self.suggestions_frame:
            self._add_suggestions(suggestions)
            self._show_status(f"Updated with {len(suggestions)} suggestions")
    
    def hide_overlay(self):
        """Hide the overlay with fade animation"""
        if self.is_visible:
            self._start_fade_animation(-1)
    
    def show_overlay(self):
        """Show the overlay with fade animation"""
        if self.root and not self.is_visible:
            self.root.deiconify()
            self.is_visible = True
            self._start_fade_animation(1)
    
    def set_callbacks(self, on_suggestion_click: Optional[Callable] = None, 
                     on_close: Optional[Callable] = None):
        """Set callback functions"""
        self.on_suggestion_click = on_suggestion_click
        self.on_close = on_close
    
    def destroy(self):
        """Destroy the overlay window"""
        if self.root:
            self.root.destroy()
            self.root = None
        self.is_visible = False 