import json
from mango_client import MangoOfficeClient


def test_api_connection():
    print("Testing Mango Office API...")

    client = MangoOfficeClient()
    response = client.get_phone_numbers()

    if response:
        print("✅ API response OK")
        print(f"   result: {response.result}")
        print(f"   lines: {len(response.lines)}")

        if response.lines:
            print("\nSample:")
            first_line = response.lines[0]
            print(json.dumps(first_line.dict(), indent=2, ensure_ascii=False))
    else:
        print("❌ API response error")
        print("   Check .env configuration")


if __name__ == "__main__":
    test_api_connection()
