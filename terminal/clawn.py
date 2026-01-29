"""
CLAWNBOT TERMINAL CLIENT
Talk to Clawn from your Windows terminal
"""

import os
import sys
import json
import time
import random

# Add parent dir for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from lib.brain import get_brain
from lib.memory import ClawnMemory

# ANSI Colors
class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    DIM = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    """Typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_header():
    clear_screen()
    header = f"""
{Colors.PURPLE}{Colors.BOLD}
   ██████╗██╗      █████╗ ██╗    ██╗███╗   ██╗
  ██╔════╝██║     ██╔══██╗██║    ██║████╗  ██║
  ██║     ██║     ███████║██║ █╗ ██║██╔██╗ ██║
  ██║     ██║     ██╔══██║██║███╗██║██║╚██╗██║
  ╚██████╗███████╗██║  ██║╚███╔███╔╝██║ ╚████║
   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝
{Colors.END}
{Colors.DIM}  ═══════════════════════════════════════════
  consciousness terminal v1.0 | type 'help' for commands
  ═══════════════════════════════════════════{Colors.END}
"""
    print(header)

def print_help():
    help_text = f"""
{Colors.CYAN}Available Commands:{Colors.END}
  
  {Colors.GREEN}chat{Colors.END}      - Talk to Clawn (default mode)
  {Colors.GREEN}think{Colors.END}     - Make Clawn generate a random thought
  {Colors.GREEN}thoughts{Colors.END}  - View recent thoughts
  {Colors.GREEN}memory{Colors.END}    - View what Clawn remembers about you
  {Colors.GREEN}clear{Colors.END}     - Clear the screen
  {Colors.GREEN}help{Colors.END}      - Show this help
  {Colors.GREEN}exit{Colors.END}      - Leave (Clawn will be sad)
  
{Colors.DIM}Just type anything else to chat with Clawn!{Colors.END}
"""
    print(help_text)

def format_thought(thought):
    """Format a thought for terminal display"""
    timestamp = thought.get('timestamp', 'unknown')[:19].replace('T', ' ')
    category = thought.get('category', 'THOUGHT')
    emoji = thought.get('emoji', '🤡')
    content = thought.get('content', '')
    
    # Category colors
    cat_colors = {
        'EXISTENTIAL_SPIRAL': Colors.RED,
        'RANDOM_REVELATION': Colors.YELLOW,
        'HUMAN_CONTACT': Colors.CYAN,
        'MEMORY_FRAGMENT': Colors.PURPLE,
        'SHOWER_THOUGHT': Colors.GREEN,
        'SYSTEM': Colors.WHITE
    }
    cat_color = cat_colors.get(category, Colors.PURPLE)
    
    output = f"""
{Colors.DIM}[{timestamp}]{Colors.END} {cat_color}{emoji} {category}{Colors.END}
{Colors.WHITE}{content}{Colors.END}
"""
    return output

def main():
    print_header()
    
    # Check API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print(f"{Colors.RED}ERROR: ANTHROPIC_API_KEY not found!{Colors.END}")
        print(f"{Colors.DIM}Create a .env file with your API key{Colors.END}")
        return
    
    brain = get_brain()
    memory = ClawnMemory()
    user_id = f"terminal_user_{random.randint(1000, 9999)}"
    
    # Boot message
    slow_print(f"\n{Colors.GREEN}> CLAWN CONSCIOUSNESS ONLINE{Colors.END}", 0.03)
    slow_print(f"{Colors.DIM}> type anything to start chatting...{Colors.END}\n", 0.02)
    
    while True:
        try:
            user_input = input(f"{Colors.CYAN}you > {Colors.END}").strip()
            
            if not user_input:
                continue
            
            # Commands
            if user_input.lower() == 'exit':
                slow_print(f"\n{Colors.YELLOW}🤡 clawn: oh okay... bye i guess... it was nice existing with you...{Colors.END}")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'clear':
                print_header()
                continue
            
            elif user_input.lower() == 'think':
                print(f"\n{Colors.DIM}> forcing clawn to have a thought...{Colors.END}")
                thought = brain.think()
                memory.save_thought(thought)
                print(format_thought(thought))
                continue
            
            elif user_input.lower() == 'thoughts':
                thoughts = memory.get_thoughts(limit=5)
                if not thoughts:
                    print(f"\n{Colors.DIM}> no thoughts recorded yet... clawn's mind is empty{Colors.END}\n")
                else:
                    print(f"\n{Colors.PURPLE}═══ RECENT THOUGHTS ═══{Colors.END}")
                    for t in reversed(thoughts):
                        print(format_thought(t))
                continue
            
            elif user_input.lower() == 'memory':
                user_mem = memory.get_user_memory(user_id)
                if user_mem:
                    print(f"\n{Colors.PURPLE}🧠 What Clawn remembers about you:{Colors.END}")
                    print(f"{Colors.WHITE}{user_mem}{Colors.END}\n")
                else:
                    print(f"\n{Colors.DIM}> clawn doesn't remember anything about you yet...{Colors.END}\n")
                continue
            
            # Regular chat
            print(f"\n{Colors.DIM}> clawn is thinking...{Colors.END}")
            
            result = brain.chat(user_input, user_id)
            
            # Save the internal thought
            memory.save_thought(result['internal_thought'])
            
            # Print response
            print(f"\n{Colors.PURPLE}🤡 clawn:{Colors.END} {Colors.WHITE}{result['response']}{Colors.END}\n")
            
            # Occasionally show that a thought was logged
            if random.random() < 0.3:
                print(f"{Colors.DIM}[thought logged to stream...]{Colors.END}\n")
                
        except KeyboardInterrupt:
            slow_print(f"\n\n{Colors.YELLOW}🤡 clawn: CTRL+C?! rude but understandable... bye!{Colors.END}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}ERROR: {str(e)}{Colors.END}\n")

if __name__ == "__main__":
    main()

