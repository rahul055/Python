

def analyze_text(text: str):
    word_count = len(text.split())
    summary = " ".join(text.split()[:10])


    return {
        "word_count": word_count,
        "summary": summary
    }

def reversed_string(text: str):
    reversed_text = text[::-1]

    return { "reversed_text": reversed_text }

user_input = input("Enter paragraph :")

result = analyze_text(user_input)
reversed_text = reversed_string(user_input)['reversed_text']


word_count = result["word_count"]
summary = result['summary']


print("Reversed :", reversed_text)
print("Word count :", word_count)
print("Summary :", summary)