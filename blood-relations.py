import tkinter as tk
from tkinter import messagebox
import re
from collections import defaultdict

class BloodRelationsApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Blood Relations")
    self.root.geometry("600x500")
    
    tk.Label(root, text="Enter the blood relation statement:").pack(pady=10)
    self.input_text = tk.Text(root, height=6, width=50)
    self.input_text.pack(pady=10)
    
    tk.Button(root, text="Solve", command=self.solve_relation).pack(pady=10)
    
    tk.Label(root, text="Result:").pack(pady=10)
    self.result_text = tk.Text(root, height=8, width=50, state='disabled')
    self.result_text.pack(pady=10)
    
    self.graph = defaultdict(list)
    self.names = set()
    self.genders = {}
        
  def solve_relation(self):
    statement = self.input_text.get("1.0", tk.END).strip()
    if not statement:
      messagebox.showerror("Input Error", "Please enter a blood relation statement.")
      return
    
    try:
      result = self.parse_complex_relation(statement)
      self.output_text.Config(state='normal')
      self.result_text.delete("1.0", tk.END)
      self.result_text.insert(tk.END, result)
      self.result_text.config(state='disabled')
    
    except Exception as e:
      messagebox.showerror("Error", f"Failed to parse statement: {str(e)}")
      
  def parse_complex_relation(self, statement):
    self.graph = defaultdict(list)
    self.names = set()
    self.genders = {}
    
    statement = statement.lower().strip()
    
    relations = {
      'father' : ('male', 'parent', '1'),
      'mother' : ('female', 'parent', '1'),
      'son' : ('male', 'child', '-1'),
      'daughter' : ('female', 'child', '-1'),
      'brother' : ('male', 'sibling', '0'),
      'sister' : ('female', 'sibling', '0'),
      'husband' : ('male', 'spouse', '0'),
      'wife' : ('female', 'spouse', '0'),
      'grandfather' : ('male', 'parent', '2'),
      'grandmother' : ('female', 'parent', '2'),
      'grandson' : ('male', 'child', '-2'),
      'granddaughter' : ('female', 'child', '-2'),
      'uncle' : ('male', 'parent_sibling', '1'),
      'aunt' : ('female', 'parent_sibling', '1'),
      'cousin' : ('any', 'cousin', '0'),
      'nephew' : ('male', 'child_sibling', '-1'),
      'niece' : ('female', 'child_sibling', '-1'),
      'father-in-law' : ('male', 'parent_spouse', '1'),
      'mother-in-law' : ('female', 'parent_spouse', '1'),
      'stepfather' : ('male', 'step_parent', '1'),
      'stepmother' : ('female', 'step_parent', '1'),
      'stepson' : ('male', 'step_child', '-1'),
      'stepdaughter' : ('female', 'step_child', '-1'),
    }
    
    parts = re.split(r'[,.]|who is|married to', statement)
    parts = [part.strip() for part in parts if part.strip()]
    
    def extract_names(part):
      name_pattern = r'([A-Z][a-z]*(?:\s[A-Z][a-z]*)?)'
      names = re.findall(name_pattern, part)
      return [ n for n in names if n.lower() not in relations and n.lower not in ['is','or','and','of','to','the']]
    
    for part in parts:
      for rel, (gender, rel_type, level) in relations.items():
        if rel in part:
          names = extract_names(part)
          if len(names) >=2:
            person1, person2 = names[:2]
            self.names.add(person1)
            self.names.add(person2)
            
            if person1 not in self.genders or self.genders[person1] == gender or self.genders[person1] == 'unkown':
              self.genders[person1] = gender
              
            if person2 not in self.genders or self.genders[person2] == gender or self.genders[person1] == 'unkown':
              self.genders[person2] = gender
              
            if rel_type == 'parent':
              self.graph[person1].append((person2, rel, level))
              self.graph[person2].append((person1, f"child_of_{rel}", -level))
