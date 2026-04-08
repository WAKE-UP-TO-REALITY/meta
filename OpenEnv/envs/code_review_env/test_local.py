import asyncio
from client import CodeReviewEnv
from models import CodeReviewAction

async def main():
    print("Connecting to local CodeReviewEnv...")
    async with CodeReviewEnv(base_url="http://localhost:8000") as client:
        print("✅ Connected!")
        
        print("\n🔄 Resetting environment...")
        result = await client.reset()
        print(f"Initial Observation: {result.observation.echoed_message}")
        
        print("\n▶️ Taking a step (Action = 'Testing my new environment!')...")
        action = CodeReviewAction(message="Testing my new environment!")
        result = await client.step(action)
        
        print(f"Response: {result.observation.echoed_message}")
        print(f"Reward received: {result.reward}")

if __name__ == "__main__":
    asyncio.run(main())
