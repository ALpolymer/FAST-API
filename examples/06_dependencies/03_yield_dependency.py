import time
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI(title= "Yield Dependencies")

class FakeDatabase:
    def __init__(self):
        print("[DB] Opening connection")
        time.sleep(1)
        print("[DB] Connection opened")
    
    def query(self, sql:str):
        print(f"[DB] Running query")
        time.sleep(1)
        print(f"[DB] query completed")
        return f"Result of {sql}"
    
    def close(self):
        print(f"[DB] Closing connection")
        time.sleep(1)
        print("[DB] closed")

def get_db():
    """
    A yield dependency runs setup BEFORE the endpoint,
    and teardown AFTER the response is sent.
    Perfect for DB sessions, file handles, etc.

    Yield dependency.

    What it does:
    1. Creates/opens the resource (here: FakeDatabase)
    2. Provides it to the endpoint using yield
    3. After the endpoint finishes, executes the finally block
       and closes the resource

    This pattern is ideal for setup/teardown resource management.
    """
    print("\n" + "="*50)
    print("Step 1: SETUP — creating the resource")
    print("="*50)
    db = FakeDatabase()   # setup: open connection / create resource
    try:
        print("\nStep 2: YIELD — handing resource to the endpoint")
        print("-"*50)
        yield db          # execution pauses here and the db is passed to the endpoint
    finally:
        print("\nStep 3: TEARDOWN — cleaning up the resource")
        print("-"*50)
        db.close()         # teardown: always runs, even if an error occurs
        print("="*50 + "\n")



@app.get("/data")
def read_data(db: Annotated[FakeDatabase, Depends(get_db)]):
    """
    FastAPI will:
    - call get_db() first
    - get the db object from the yield
    - inject it into this function as an argument
    - after sending the response, return to get_db()
    and execute the finally block -> db.close()
    """
    print("  [ENDPOINT] 👉 Using the db inside the endpoint...")
    result = db.query("SELECT * FROM items")
    print("  [ENDPOINT] 👉 Sending response to client...")
    time.sleep(0.5)
    return {"result": result}