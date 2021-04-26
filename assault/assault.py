#This file is now a module inside the package called assault.

import click
import assault

@click.command()		#This is a decorator. It converts functions beneath it to commands.
@click.option("--requests", "-r", default=500, help="Number of requests")			#You can stack decorators on top of each other; so here the option and argument decorators are stacked on top of the command decorator.
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--jsonfile", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests, concurrency, jsonfile, url):
	print("Requests: " + str(requests))
	print("Concurrency: " + str(concurrency))
	print("JSON File: " + str(jsonfile))
	print("URL: " + str(url))
	http.assault(url, requests, concurrency)

if __name__ == "__main__":
	cli()
