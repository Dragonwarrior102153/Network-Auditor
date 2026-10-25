"""Application entry point for the interactive network auditor."""

import ipaddress

from scanTarget import ScanTarget
from discoverDevices import DiscoverDevices
from cli import CLI

def main():
    # Start the interactive command-line interface.
    cli = CLI()

    
if (__name__ == "__main__"):
    main()