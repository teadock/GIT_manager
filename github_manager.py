#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os
import platform
from datetime import datetime

# Detect operating system and set appropriate paths
SYSTEM = platform.system()

def find_gh_path():
    """Find the GitHub CLI executable path"""
    if SYSTEM == 'Windows':
        # Try common Windows locations in order of likelihood
        possible_paths = [
            r'C:\Program Files\GitHub CLI\gh.exe',
            r'C:\Program Files (x86)\GitHub CLI\gh.exe',
            os.path.expanduser(r'~\AppData\Local\Programs\GitHub CLI\gh.exe'),
            os.path.expanduser(r'~\scoop\shims\gh.exe'),  # Scoop package manager
        ]
        
        # Check common installation paths first
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # If not found in common paths, try using 'where' command
        try:
            result = subprocess.run(['where', 'gh'], capture_output=True, text=True, shell=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        
        return 'gh'  # Fallback
    elif SYSTEM == 'Darwin':  # macOS
        os.environ['PATH'] = '/opt/homebrew/bin:/usr/local/bin:' + os.environ.get('PATH', '')
        return '/opt/homebrew/bin/gh'
    else:  # Linux
        return 'gh'

GH_PATH = find_gh_path()

class GitHubManager:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repository Manager")
        self.root.geometry("700x600")
        self.root.configure(bg='#f5f5f7')
        
        # macOS style colors
        self.bg_color = '#f5f5f7'
        self.button_color = '#007AFF'
        self.delete_color = '#FF3B30'
        self.item_bg = '#FFFFFF'
        
        self.create_ui()
        self.load_repositories()
    
    def create_ui(self):
        # Top section - Create New Repository
        top_frame = tk.Frame(self.root, bg=self.bg_color, pady=20, padx=20)
        top_frame.pack(fill=tk.X)
        
        # Entry field with rounded corners effect
        entry_container = tk.Frame(top_frame, bg='white', 
                                   highlightbackground='#d1d1d6',
                                   highlightthickness=1)
        entry_container.pack(fill=tk.X)
        
        self.name_entry = tk.Entry(entry_container, font=('SF Pro Text', 14), 
                                   relief=tk.FLAT, borderwidth=0,
                                   bg='white', fg='#1d1d1f')
        self.name_entry.pack(fill=tk.X, ipady=8, padx=8)
        self.name_entry.insert(0, "")
        self.name_entry.bind('<Return>', lambda e: self.create_repository())
        
        # Create button - BLUE with rounded corners
        btn_container = tk.Frame(top_frame, bg=self.button_color,
                                highlightthickness=0)
        btn_container.pack(pady=(10, 0))
        
        create_btn = tk.Button(btn_container, text="Create New", 
                              font=('SF Pro Text', 13, 'bold'),
                              bg=self.button_color, fg='white',
                              activebackground='#0051D5',
                              activeforeground='white',
                              relief=tk.FLAT, cursor='hand2',
                              command=self.create_repository,
                              borderwidth=0,
                              padx=20, pady=10)
        create_btn.pack()
        
        # Separator
        separator = tk.Frame(self.root, height=1, bg='#d1d1d6')
        separator.pack(fill=tk.X, padx=20)
        
        # Repository list
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(list_frame, bg=self.bg_color, 
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                 command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, 
                                 anchor="nw", width=640)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        # Windows reports delta in multiples of 120
        if SYSTEM == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta)), "units")
    
    def load_repositories(self):
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get repository data
            result = subprocess.run(
                [GH_PATH, 'repo', 'list', '--limit', '100', 
                 '--json', 'name,diskUsage,pushedAt,isPrivate'],
                capture_output=True, text=True, check=True
            )
            repos = json.loads(result.stdout)
            
            # Sort by pushedAt (newest first)
            repos.sort(key=lambda x: x['pushedAt'], reverse=True)
            
            # Create repository items
            for repo in repos:
                self.create_repo_item(repo)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load repositories:\n{str(e)}")
    
    def create_repo_item(self, repo):
        # Container for each repo (looks like a card/button with rounded corners)
        item_frame = tk.Frame(self.scrollable_frame, bg=self.item_bg,
                             relief=tk.FLAT, borderwidth=0,
                             highlightbackground='#e5e5ea',
                             highlightthickness=1)
        item_frame.pack(fill=tk.X, pady=5, ipady=10, ipadx=15)
        
        # Left side - repo info
        info_frame = tk.Frame(item_frame, bg=self.item_bg)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Name row with copy button
        name_row = tk.Frame(info_frame, bg=self.item_bg)
        name_row.pack(fill=tk.X, pady=(0, 5))
        
        # Name (larger, bold)
        name_label = tk.Label(name_row, text=repo['name'],
                             font=('SF Pro Text', 15, 'bold'),
                             bg=self.item_bg, fg='#1d1d1f',
                             anchor='w')
        name_label.pack(side=tk.LEFT)
        
        # Copy button (small icon next to name)
        copy_btn = tk.Button(name_row, text="📋",
                            font=('SF Pro Text', 12),
                            bg=self.item_bg, fg='#007AFF',
                            activebackground=self.item_bg,
                            activeforeground='#0051D5',
                            relief=tk.FLAT, cursor='hand2',
                            borderwidth=0,
                            command=lambda: self.copy_repo_name(repo['name']),
                            padx=5, pady=0)
        copy_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Details row
        details_frame = tk.Frame(info_frame, bg=self.item_bg)
        details_frame.pack(fill=tk.X)
        
        # Size
        size_kb = repo['diskUsage']
        if size_kb < 1024:
            size_str = f"{size_kb} KB"
        elif size_kb < 1048576:
            size_str = f"{size_kb // 1024} MB"
        else:
            size_str = f"{size_kb // 1048576} GB"
        
        size_label = tk.Label(details_frame, text=f"📦 {size_str}",
                             font=('SF Pro Text', 12),
                             bg=self.item_bg, fg='#86868b')
        size_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Date
        try:
            date_obj = datetime.fromisoformat(repo['pushedAt'].replace('Z', '+00:00'))
            date_str = date_obj.strftime('%Y-%m-%d')
        except:
            date_str = repo['pushedAt'][:10]
        
        date_label = tk.Label(details_frame, text=f"📅 {date_str}",
                             font=('SF Pro Text', 12),
                             bg=self.item_bg, fg='#86868b')
        date_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Privacy
        privacy_icon = "🔒 Private" if repo['isPrivate'] else "🌍 Public"
        privacy_label = tk.Label(details_frame, text=privacy_icon,
                                font=('SF Pro Text', 12),
                                bg=self.item_bg, fg='#86868b')
        privacy_label.pack(side=tk.LEFT)
        
        # Right side - Delete button (RED, 30px more to left)
        delete_btn = tk.Button(item_frame, text="Delete",
                              font=('SF Pro Text', 12),
                              bg=self.delete_color, fg='white',
                              activebackground='#CC2E24',
                              activeforeground='white',
                              relief=tk.FLAT, cursor='hand2',
                              borderwidth=0,
                              command=lambda: self.delete_repository(repo['name']),
                              padx=15, pady=5)
        delete_btn.pack(side=tk.RIGHT, padx=(10, 30))
    
    def copy_repo_name(self, name):
        """Copy repository name to clipboard"""
        try:
            if SYSTEM == 'Windows':
                subprocess.run(['clip'], input=name.encode(), shell=True)
            elif SYSTEM == 'Darwin':  # macOS
                subprocess.run(['pbcopy'], input=name.encode())
            else:  # Linux
                try:
                    subprocess.run(['xclip', '-selection', 'clipboard'], input=name.encode())
                except FileNotFoundError:
                    subprocess.run(['xsel', '--clipboard', '--input'], input=name.encode())
            
            # Optional: Show a brief feedback (you could also use a tooltip or status bar)
            # For now, we'll keep it silent for a clean UX
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard:\n{str(e)}")
    
    def create_repository(self):
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Empty Name", "Please enter a repository name.")
            return
        
        # Validate name
        if not all(c.isalnum() or c in '-_' for c in name):
            messagebox.showerror("Invalid Name", 
                               "Repository name can only contain letters, numbers, hyphens, and underscores.")
            return
        
        try:
            # Create repository
            subprocess.run(
                [GH_PATH, 'repo', 'create', name, '--private'],
                check=True, capture_output=True
            )
            
            # Copy to clipboard (platform-specific)
            try:
                if SYSTEM == 'Windows':
                    subprocess.run(['clip'], input=name.encode(), shell=True)
                elif SYSTEM == 'Darwin':  # macOS
                    subprocess.run(['pbcopy'], input=name.encode())
                else:  # Linux
                    try:
                        subprocess.run(['xclip', '-selection', 'clipboard'], input=name.encode())
                    except FileNotFoundError:
                        subprocess.run(['xsel', '--clipboard', '--input'], input=name.encode())
            except Exception:
                pass  # Clipboard copy is optional
            
            # Clear entry
            self.name_entry.delete(0, tk.END)
            
            # Show success
            messagebox.showinfo("Success", 
                              f"✅ Repository '{name}' created!\n\nType: Private\nProtocol: SSH\n\nName copied to clipboard!")
            
            # Refresh list
            self.load_repositories()
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create repository:\n{e.stderr.decode()}")
    
    def delete_repository(self, name):
        # Confirmation
        response = messagebox.askyesno(
            "Confirm Deletion",
            f"⚠️ Delete '{name}'?\n\nThis action CANNOT be undone!\nAll code, issues, and history will be permanently deleted.",
            icon='warning'
        )
        
        if response:
            try:
                # Get the authenticated username dynamically
                username_result = subprocess.run(
                    [GH_PATH, 'api', 'user', '-q', '.login'],
                    capture_output=True, text=True, check=True
                )
                username = username_result.stdout.strip()
                
                # Delete repository
                subprocess.run(
                    [GH_PATH, 'repo', 'delete', f'{username}/{name}', '--yes'],
                    check=True, capture_output=True
                )
                
                messagebox.showinfo("Deleted", f"✅ Repository '{name}' has been deleted.")
                
                # Refresh list
                self.load_repositories()
                
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode()
                
                # Check if error is due to missing delete_repo scope
                if 'delete_repo' in error_msg or 'admin rights' in error_msg.lower():
                    messagebox.showerror(
                        "Permission Required",
                        "The GitHub CLI needs the 'delete_repo' permission.\n\n"
                        "Please run this command in Terminal once:\n\n"
                        "gh auth refresh -h github.com -s delete_repo\n\n"
                        "Then try again.",
                        icon='error'
                    )
                else:
                    messagebox.showerror("Error", f"Failed to delete repository:\n{error_msg}")

if __name__ == '__main__':
    root = tk.Tk()
    app = GitHubManager(root)
    root.mainloop()
