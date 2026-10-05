from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_api_key():
    # TODO 1: read GEMINI_API_KEY from the environment
    # TODO 2: if it's missing or empty, raise a clear error
    #         (hint: raise ValueError("..."))
    # TODO 3: return the key
    pass

if __name__ == "__main__":
    try:
        api_key = get_api_key()
        print(f"Last 4 characters of the API key: {api_key[-4:]}")     
    except ValueError as e:
        print(f"Error: {e}")
    except TypeError as e:
        print(f"Type Error: {e}")
