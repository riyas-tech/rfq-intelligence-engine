from src.pipeline.pipeline import process_message

def main():
    samples = [
        "quote 10m eurusd spot",
        "buy 5m gbpusd tomorrow",
        "need price 3m usdjpy",
        "sell 2m eurusd next week",
        "price 7m cable"
    ]

    for msg in samples:
        result = process_message(msg)
        print("\n Input :", msg)
        print("Output :", result.model_dump())

if __name__ == "__main__":
    main()        