
# Take user input → print reversed string
# normal way

user_input = input('Enter a string  ')

reversed_string = user_input[::-1]

print("Reversed string " + reversed_string)


# using loop

string_to_be_reversed = ""

for char in user_input:
    string_to_be_reversed = char + string_to_be_reversed


print("using loop " + string_to_be_reversed)


# Count words in a sentence

words_in_sentence = len(user_input.split())
print("words in sentence", words_in_sentence)

# store 5 users in list of dicts

list_of_users = [ {"name": "rahul", 'age' : 29}, {"name": "pranali", "age": 24} ]

print("users :",  list_of_users )


# Filter users by age
list_of_users.sort(key= lambda u : u["age"])

print("normal way", list_of_users)

sorted_users = sorted(list_of_users, key= lambda u : u ['age'])

print("using sorted", sorted_users)