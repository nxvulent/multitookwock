import sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
import os, time, math, socket, threading, concurrent.futures
import requests
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
import urllib3
urllib3.disable_warnings()

console = Console()
TIMEOUT = 5

ASCII = r"""
    ██╗    ██╗ ██████╗  ██████╗██╗  ██╗    ██╗    ██╗███████╗██████╗ 
    ██║    ██║██╔═══██╗██╔════╝██║ ██╔╝    ██║    ██║██╔════╝██╔══██╗
    ██║ █╗ ██║██║   ██║██║     █████╔╝     ██║ █╗ ██║█████╗  ██████╔╝
    ██║███╗██║██║   ██║██║     ██╔═██╗     ██║███╗██║██╔══╝  ██╔══██╗
    ╚███╔███╔╝╚██████╔╝╚██████╗██║  ██╗    ╚███╔███╔╝███████╗██████╔╝
     ╚══╝╚══╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝ 
"""
SUBTITLE = " S U B D O M A I N   B R U T E F O R C E R "

def boot():
    if sys.platform.startswith("win"): os.system("title WOCK WEB // SUBDOMAIN BRUTEFORCER")
    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[?25l")
    lines = ASCII.strip("\n").split("\n")
    t0 = time.time()
    try:
        while time.time() - t0 < 1.4:
            t = time.time() - t0
            sys.stdout.write("\033[H\n")
            for line in lines:
                sys.stdout.write("  ")
                for c, ch in enumerate(line):
                    if ch == " ": sys.stdout.write(" ")
                    else:
                        v = max(40, min(255, int(100 + 155 * math.sin(t * 10 - c * 0.2))))
                        sys.stdout.write(f"\033[38;2;{v};0;0m{ch}")
                sys.stdout.write("\033[0m\n")
            sys.stdout.write(f"\n  \033[38;2;80;0;0m{SUBTITLE}\033[0m\n")
            sys.stdout.flush()
            time.sleep(0.025)
    finally:
        sys.stdout.write("\033[?25h\033[0m")
    os.system("cls" if os.name == "nt" else "clear")


SUBS = ["www", "dev", "test", "admin", "staging", "mail", "blog", "webmail", "server", "ns1", "ns2", "smtp", "secure", "vpn", "api", "portal", "beta", "web", "ftp", "cpanel", "shop", "forum", "support"]

def check_sub(dom, sub):
    target = f"{sub}.{dom}"
    try:
        ip = socket.gethostbyname(target)
        return target, ip
    except: return None

if __name__ == "__main__":
    try:
        boot()
        console.print(Align.center(Panel(
            Text.from_markup("[bold red]WOCK-MULTI[/]  [dim]//[/]  [white]WOCK WEB[/]  [dim]//[/]  [red]SUBOMAIN BRUTEFORCER[/]"),
            border_style="red", padding=(0, 6)
        )))
        console.print()
        console.print(" [bold red]┌─[[/][bold white] Target Domain (ex: site.com) [/][bold red]][/]")
        target = console.input(" [bold red]└─▶[/] [bold white]").strip()
        if target.startswith("http"): target = urlparse(target).netloc
        if not target: sys.exit(0)
        
        console.print()
        found = []
        with Progress(SpinnerColumn(spinner_name="point", style="red"), TextColumn("[dim white]{task.description}"), console=console, transient=True) as p:
            p.add_task(f"Bruteforcing {target}...", total=None)
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                futs = [ex.submit(check_sub, target, sub) for sub in SUBS]
                for f in concurrent.futures.as_completed(futs):
                    res = f.result()
                    if res:
                        found.append(res)
                        console.print(f" [bold red][+][/] [white]{res[0]}[/] [dim]({res[1]})[/]")
        
        console.print()
        console.print(f" [bold green][✓] Done. Found {len(found)} subdomains.[/]")
        console.input(" [dim]Press [bold red]ENTER[/] to exit...[/]")
    except (KeyboardInterrupt, EOFError): pass

