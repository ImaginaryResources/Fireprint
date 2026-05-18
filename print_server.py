"""
ESC/POS print server for Star TSP100 thermal printers.

Listens on port 9100 for raw ESC/POS data and prints it via py-star-tsp.
Run this first, then send ESC/POS data from fireprint.py or any
ESC/POS-compatible tool.

    python print_server.py
"""

import asyncio
import logging
import argparse

from py_star_tsp import StarTSP100
from py_star_tsp.escpos import PRESET_EPSON_TM_T88
from py_star_tsp.server import EscposServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


def on_print(raster_set):
    with StarTSP100() as printer:
        printer.find_device()
        printer.print_speed = 2
        printer.raster_print_quality = 2
        for block in raster_set.blocks:
            printer.add_raster(block)
        printer.print()


async def main(host="0.0.0.0", port=9100):
    server = EscposServer(host=host, port=port, preset=PRESET_EPSON_TM_T88, on_print=on_print)
    print(f"Print server listening on {host}:{port}")
    await server.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ESC/POS print server for Star TSP100")
    parser.add_argument("--host", default="0.0.0.0", help="host to bind to")
    parser.add_argument("--port", type=int, default=9100, help="port to listen on")
    args = parser.parse_args()

    asyncio.run(main(host=args.host, port=args.port))
