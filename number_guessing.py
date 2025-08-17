import random
import time

def play_game():
    print("\n🎮 Welcome to the Number Guessing Game!")
    player_name = input("তোমার নাম বলো: ")

    # 🎯 Difficulty Level
    print("\nChoose Difficulty Level:")
    print("1. Easy (1 - 50)")
    print("2. Medium (1 - 100)")
    print("3. Hard (1 - 200)")
    choice = input("➡️ Enter 1/2/3: ")

    if choice == "1":
        secret_number = random.randint(1, 50)
        max_range = 50
    elif choice == "2":
        secret_number = random.randint(1, 100)
        max_range = 100
    else:
        secret_number = random.randint(1, 200)
        max_range = 200

    print(f"\nহ্যালো {player_name}! আমি ১ থেকে {max_range} এর মধ্যে একটি সংখ্যা ভেবেছি। তুমি সেটা ধরতে পারো কি?")

    guess = None
    attempts = 0

    # টাইম শুরু + Countdown Limit
    start_time = time.time()
    time_limit = 30   # ⏳ 30 সেকেন্ড

    while guess != secret_number:
        # চেক করা Countdown টাইম শেষ হয়েছে কিনা
        if time.time() - start_time > time_limit:
            print("\n⏳ সময় শেষ! তুমি হেরে গেছো।")
            print(f"🔢 সঠিক সংখ্যা ছিল: {secret_number}")
            return  # ফাংশন শেষ করে বের হয়ে যাবে

        try:
            guess = int(input("➡️ তোমার অনুমান করো: "))
            attempts += 1

            if guess > secret_number:
                print("🔻 Lower number please")
            elif guess < secret_number:
                print("🔺 Higher number please")
            else:
                end_time = time.time()
                total_time = round(end_time - start_time, 2)

                # 🏆 Score Formula (Improved)
                # Base = 100, কম ট্রাই + কম টাইম + Hard level = বেশি স্কোর
                difficulty_bonus = {"50": 5, "100": 10, "200": 20}[str(max_range)]
                score = max(100 + difficulty_bonus - (attempts * 2 + int(total_time)), 0)

                print(f"\n🎉 অভিনন্দন {player_name}! তুমি ঠিক ধরেছো ✅")
                print(f"🔢 সঠিক সংখ্যা ছিল: {secret_number}")
                print(f"⏱️ সময় লেগেছে: {total_time} সেকেন্ড")
                print(f"🔁 মোট চেষ্টা: {attempts} বার")
                print(f"🏆 তোমার স্কোর: {score} / 120")
                print("🔥 ধন্যবাদ খেলার জন্য!")
                break

            # 💡 Hint System (প্রতি ৩ বার ভুল হলে)
            if attempts % 3 == 0:
                if secret_number % 2 == 0:
                    print("💡 হিন্ট: সংখ্যা জোড়")
                else:
                    print("💡 হিন্ট: সংখ্যা বিজোড়")

        except ValueError:
            print("⚠️ দয়া করে একটি সঠিক সংখ্যা টাইপ করো!")

# 🔁 Play Again Loop
while True:
    play_game()
    play_again = input("\n🔁 আবার খেলতে চাও? (y/n): ")
    if play_again.lower() != "y":
        print("👋 গেম শেষ, আবার দেখা হবে!")
        break
