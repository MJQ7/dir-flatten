import os
from Config import Config
from src.flatten import flatten
from rich.prompt import Prompt

def main():
    Config.TLDN = Prompt.ask("Enter the directory to flatten:", default=os.getcwd())
    flatten()
    
if __name__ == "__main__":
    main()