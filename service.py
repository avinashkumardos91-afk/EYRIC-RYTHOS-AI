import os
import time
from app.core.agent import build_agent


def main():
    agent = build_agent()
    print('EYRIC RYTHOS AI service started. Press Ctrl+C to stop.')
    while True:
        time.sleep(60)
        agent.analyze_message('background security heartbeat')


if __name__ == '__main__':
    main()
