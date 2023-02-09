import asyncio
import time
import websockets
from collections import deque

# Denote the pair
pair = 'xrpusdt'

# Define the URI for the Binance WebSocket API
uri = f"wss://stream.binance.com:9443/ws/{pair}@aggTrade"

# Define a deque to store the tuples with the request time and price
prices = deque()


async def read_price():
    async with websockets.connect(uri) as websocket:
        while True:
            # Receive the message from the WebSocket
            message = await websocket.recv()

            # Extract the price from the message
            price = float(message.split('"p":"')[1].split('","')[0])

            # Append a tuple with the request time and price to the prices deque
            request_time = int(time.time() * 1000)
            prices.append((request_time, price))

            # If the price is less by 1 percent than the maximum price from prices, display a message
            if len(prices) > 1 and price < 0.99 * max(p[1] for p in prices):
                print("ATTENTION! THE PRICE HAS DROPPED!")


async def remove_old_prices():
    while True:
        await asyncio.sleep(0.1)
        current_time = int(time.time() * 1000)
        one_hour = current_time - 60 * 60 * 1000

        # Remove tuples containing request time less than the current time minus 1 hour
        while len(prices) > 0 and prices[0][0] < one_hour:
            prices.popleft()


async def main():
    # Start the read_price and remove_old_prices tasks
    read_price_task = asyncio.create_task(read_price())
    remove_old_prices_task = asyncio.create_task(remove_old_prices())

    # Wait for both tasks to complete
    await asyncio.gather(read_price_task, remove_old_prices_task)

# Run the main function
asyncio.run(main())
