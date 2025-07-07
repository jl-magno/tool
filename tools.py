#!/usr/bin/env python3
# JL's Facebook Tool Suite - Error-Free Version
# Combines Share Boost and Profile Guard with modern UI

import os
import re
import json
import time
import random
import string
import uuid
import requests
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.text import Text
from rich.align import Align
from rich import box

# Initialize console
console = Console()

# Session object
ses = requests.Session()

# User agents
ua_list = [
    "Mozilla/5.0 (Linux; Android 10; Wildfire E Lite Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36[FBAN/EMA;FBLC/en_US;FBAV/298.0.0.10.115;]",
    "Mozilla/5.0 (Linux; Android 11; KINGKONG 5 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36[FBAN/EMA;FBLC/fr_FR;FBAV/320.0.0.12.108;]",
    "Mozilla/5.0 (Linux; Android 11; G91 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.126 Mobile Safari/537.36[FBAN/EMA;FBLC/fr_FR;FBAV/325.0.1.4.108;]"
]

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display application banner"""
    banner = Text("""
 ███████╗ █████╗  ██████╗███████╗██████╗  █████╗  ██████╗██╗  ██╗
 ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
 █████╗  ███████║██║     █████╗  ██████╔╝███████║██║     █████╔╝ 
 ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██╔══██║██║     ██╔═██╗ 
 ██║     ██║  ██║╚██████╗███████╗██████╔╝██║  ██║╚██████╗██║  ██╗
 ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
""", style="bold magenta")
    
    subtitle = Text("Facebook Tool Suite by JL Magno", style="cyan")
    console.print(Align.center(banner))
    console.print(Align.center(subtitle))
    console.print(Panel.fit("🛡️ Share Boost | Profile Guard | Account Tools", 
                         border_style="yellow", style="bold"))

def main_menu():
    """Display main menu"""
    while True:
        clear_screen()
        display_banner()
        
        menu = Table.grid(padding=(1, 3))
        menu.add_row("1", "🚀 Share Boost - Mass share posts")
        menu.add_row("2", "🛡️ Profile Guard - Protect profile")
        menu.add_row("3", "🔍 View Saved Credentials")
        menu.add_row("4", "🧹 Clear Saved Data")
        menu.add_row("5", "🚪 Exit")
        
        console.print(Panel.fit(menu, title="[bold green]MAIN MENU[/bold green]", 
                         border_style="blue", box=box.ROUNDED))
        
        choice = console.input("\n[bold cyan]🔢 Select option (1-5): [/bold cyan]").strip()
        
        if choice == "1":
            share_boost_menu()
        elif choice == "2":
            profile_guard_menu()
        elif choice == "3":
            check_credentials()
        elif choice == "4":
            delete_credentials()
        elif choice == "5":
            console.print(Panel("[bold green]👋 Thank you for using Facebook Tool Suite![/bold green]", 
                             style="bold green"))
            exit()
        else:
            console.print(Panel("[bold red]❌ Invalid choice[/bold red]", style="bold red"))
            time.sleep(1)

def share_boost_menu():
    """Share Boost menu"""
    while True:
        clear_screen()
        display_banner()
        
        if not (os.path.exists("token.txt") and os.path.exists("cookie.txt")):
            console.print(Panel("[bold yellow]⚠️ No saved credentials found[/bold yellow]", 
                             style="bold yellow"))
            time.sleep(1)
            return share_boost_login()
        
        menu = Table.grid(padding=(1, 3))
        menu.add_row("1", "📢 Start sharing posts")
        menu.add_row("2", "🔑 Re-authenticate")
        menu.add_row("3", "🔙 Back")
        
        console.print(Panel.fit(menu, title="[bold blue]SHARE BOOST[/bold blue]"))
        
        choice = console.input("\n[bold cyan]🔢 Select option (1-3): [/bold cyan]").strip()
        
        if choice == "1":
            start_sharing()
        elif choice == "2":
            share_boost_login()
        elif choice == "3":
            return
        else:
            console.print(Panel("[bold red]❌ Invalid choice[/bold red]", style="bold red"))
            time.sleep(1)

def share_boost_login():
    """Login for Share Boost"""
    clear_screen()
    display_banner()
    
    console.print(Panel("""
[bold yellow]🔑 LOGIN INSTRUCTIONS:[/bold yellow]
1. Go to [blue]Facebook.com[/blue]
2. Open Dev Tools ([green]F12[/green])
3. Go to [cyan]Application > Cookies[/cyan]
4. Copy cookie string
""", style="bold"))
    
    cookie = console.input("\n[bold cyan]📋 Paste Facebook cookie: [/bold cyan]").strip()
    
    if not cookie:
        console.print(Panel("[bold red]❌ Cookie required[/bold red]", style="bold red"))
        time.sleep(2)
        return share_boost_login()
    
    try:
        with console.status("[bold green]🔍 Verifying cookie...[/bold green]", spinner="dots"):
            ua = random.choice(ua_list)
            res = ses.get("https://business.facebook.com/business_locations", 
                         headers={"user-agent": ua}, 
                         cookies={i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")})
            
            token = re.search(r"(EAAG\w+)", res.text)
            if not token:
                raise ValueError("Token not found")
            
            with open("token.txt", "w") as f:
                f.write(token.group(1))
            with open("cookie.txt", "w") as f:
                f.write(cookie)
            
            console.print(Panel(f"[bold green]✅ Login successful! Token: {token.group(1)[:15]}...[/bold green]", 
                             style="bold green"))
            time.sleep(2)
            return share_boost_menu()
            
    except Exception as e:
        for f in ["token.txt", "cookie.txt"]:
            if os.path.exists(f): os.remove(f)
        console.print(Panel(f"[bold red]❌ Error: {str(e)}[/bold red]", style="bold red"))
        time.sleep(3)
        return share_boost_login()

def start_sharing():
    """Start sharing posts"""
    clear_screen()
    display_banner()
    
    try:
        token = open("token.txt").read()
        cookie = {i.split("=")[0]: i.split("=")[1] 
                for i in open("cookie.txt").read().split("; ")}
    except:
        console.print(Panel("[bold red]❌ Missing credentials[/bold red]", style="bold red"))
        time.sleep(2)
        return share_boost_login()
    
    console.print(Panel("""
[bold yellow]📢 SHARING INSTRUCTIONS:[/bold yellow]
Enter a post URL like:
[blue]https://www.facebook.com/username/posts/123456789[/blue]
""", style="bold"))
    
    url = console.input("\n[bold cyan]🔗 Post URL: [/bold cyan]").strip()
    if not url.startswith(("http://", "https://")):
        console.print(Panel("[bold red]❌ Invalid URL[/bold red]", style="bold red"))
        time.sleep(2)
        return start_sharing()
    
    try:
        count = int(console.input("[bold cyan]🔢 Number of shares: [/bold cyan]").strip())
        if count <= 0:
            raise ValueError
    except:
        console.print(Panel("[bold red]❌ Enter positive number[/bold red]", style="bold red"))
        time.sleep(2)
        return start_sharing()
    
    console.print(Panel("[bold green]🚀 Starting sharing...[/bold green]", style="bold green"))
    
    success = 0
    start = datetime.now()
    ua = random.choice(ua_list)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Sharing...", total=count)
        
        for i in range(1, count+1):
            try:
                res = ses.post(
                    f"https://graph.facebook.com/v13.0/me/feed?link={url}&published=0&access_token={token}",
                    headers={"user-agent": ua},
                    cookies=cookie
                ).json()
                
                if "id" in res:
                    success += 1
                    progress.update(task, advance=1, description=f"[green]✅ Shared {i}/{count}")
                else:
                    progress.update(task, advance=1, description=f"[red]❌ Failed {i}/{count}")
                
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                progress.update(task, advance=1, description=f"[red]⚠️ Error {i}/{count}")
                console.print(f"[yellow]Warning: {str(e)}[/yellow]")
    
    elapsed = str(datetime.now() - start).split('.')[0]
    console.print(Panel(f"""
[bold]📊 RESULTS:[/bold]
🔢 Attempted: [cyan]{count}[/cyan]
✅ Success: [green]{success}[/green]
⏱️ Elapsed: [yellow]{elapsed}[/yellow]
""", style="bold"))
    
    console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")
    share_boost_menu()

def profile_guard_menu():
    """Profile Guard menu"""
    while True:
        clear_screen()
        display_banner()
        
        menu = Table.grid(padding=(1, 3))
        menu.add_row("1", "🛡️ Activate Guard")
        menu.add_row("2", "⚠️ Deactivate Guard")
        menu.add_row("3", "🔙 Back")
        
        console.print(Panel.fit(menu, title="[bold blue]PROFILE GUARD[/bold blue]"))
        
        choice = console.input("\n[bold cyan]🔢 Select option (1-3): [/bold cyan]").strip()
        
        if choice == "1":
            toggle_shield(True)
        elif choice == "2":
            toggle_shield(False)
        elif choice == "3":
            return
        else:
            console.print(Panel("[bold red]❌ Invalid choice[/bold red]", style="bold red"))
            time.sleep(1)

def toggle_shield(enable):
    """Toggle profile shield"""
    clear_screen()
    display_banner()
    
    console.print(Panel("""
[bold yellow]🔐 LOGIN REQUIRED:[/bold yellow]
Enter Facebook credentials to manage Profile Guard.
Credentials are not stored.
""", style="bold"))
    
    email = console.input("\n[bold cyan]📧 Email: [/bold cyan]").strip()
    password = console.input("[bold cyan]🔑 Password: [/bold cyan]", password=True).strip()
    
    try:
        with console.status("[bold green]🔑 Authenticating...[/bold green]", spinner="dots"):
            headers = {
                'authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'content-type': 'application/x-www-form-urlencoded'
            }
            data = {
                'email': email,
                'password': password,
                'credentials_type': 'password'
            }
            res = requests.post('https://b-graph.facebook.com/auth/login', 
                              data=data, headers=headers).json()
            
            if 'access_token' not in res:
                raise ValueError("Login failed")
            
            token = res['access_token']
            uid = requests.get(f"https://graph.facebook.com/me?access_token={token}").json().get('id')
            if not uid:
                raise ValueError("Invalid token")
            
            # Toggle shield
            data = {
                'variables': json.dumps({
                    '0': {
                        'is_shielded': enable,
                        'actor_id': uid,
                        'client_mutation_id': str(uuid.uuid4())
                    }
                }),
                'doc_id': '1477043292367183'
            }
            res = requests.post('https://graph.facebook.com/graphql', 
                              json=data, 
                              headers={'Authorization': f"OAuth {token}"}).text
            
            if f'"is_shielded":{str(enable).lower()}' in res:
                status = "ACTIVATED" if enable else "DEACTIVATED"
                console.print(Panel(f"[bold green]✅ Profile Guard {status}[/bold green]", 
                               style="bold green"))
            else:
                raise ValueError("Failed to update shield status")
                
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error: {str(e)}[/bold red]", style="bold red"))
    
    console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")
    profile_guard_menu()

def check_credentials():
    """Check saved credentials"""
    clear_screen()
    display_banner()
    
    table = Table(title="[bold magenta]SAVED CREDENTIALS[/bold magenta]")
    table.add_column("Type", style="cyan")
    table.add_column("Value", style="yellow")
    
    try:
        token = open("token.txt").read()
        table.add_row("Token", f"{token[:15]}...")
    except:
        table.add_row("Token", "[red]Not found[/red]")
    
    try:
        cookie = open("cookie.txt").read()
        table.add_row("Cookie", f"{cookie[:30]}...")
    except:
        table.add_row("Cookie", "[red]Not found[/red]")
    
    console.print(table)
    console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")

def delete_credentials():
    """Delete saved data"""
    clear_screen()
    display_banner()
    
    deleted = False
    for f in ["token.txt", "cookie.txt"]:
        if os.path.exists(f):
            os.remove(f)
            console.print(f"[green]✓ {f} deleted[/green]")
            deleted = True
    
    if not deleted:
        console.print("[yellow]⚠️ No files to delete[/yellow]")
    
    console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]🚪 Exiting...[/bold red]")
        exit()