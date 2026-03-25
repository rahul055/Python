

def analyze_text(text: str):
    word = text.split()
    word_count = len(word)
    text_summary = " ".join(word[:10])


    return { "word_count": word_count, "text_summary": text_summary }


def reverse_string(string: str):
    return string[::-1]


def main():
    user_input = input('Enter your text : ')


    reversed_string = reverse_string(user_input)
    result = analyze_text(user_input)
    word_count = result['word_count']
    text_summary = result['text_summary']


    print("Output : ")

    print('Reversed string : ', reversed_string)
    print('Words count : ', word_count)
    print('Summary : ', text_summary + "...")



if __name__ == "__main__":
    main()