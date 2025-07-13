import os

lorem_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 400  # ~100 chars x 400 = 40,000 chars
)

with open("calculator/lorem.txt", "w", encoding="utf-8") as f:
    f.write(lorem_text)

print("✅ lorem.txt with 40,000+ characters created in calculator/")