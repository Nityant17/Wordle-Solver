from nltk.corpus import words

count = 0
lst = []
for word in words.words():
    if word[0].isupper():
        continue
    if len(word)==5:
        count = count+1
        lst.append(word)
# print(count)

score = {}
for word in lst:
    score[word]=0.0
    for x in lst:
        score[word] = score[word] + (1.0*len(set(word).intersection(set(x)))/len(lst))
    # print(word," ",score[word])

val = max(score.values())
# print(val)
key = next((k for k, v in score.items() if v == val), None)
# print(key)

def word_finder(data, idx_char_pairs=None, exclude_letters=None, must_contain_letters=None, forbidden_indices=None, n=1):
    # Step 1: Filter keys based on indexed conditions
    if idx_char_pairs:
        data = {
            k: v for k, v in data.items()
            if all(len(k) > idx and k[idx] == char for idx, char in idx_char_pairs)
        }
    
    # Step 2: Remove keys containing specific letters
    if exclude_letters:
        data = {
            k: v for k, v in data.items()
            if not any(letter in k for letter in exclude_letters)
        }
    
    # Step 3: Remove keys that do not contain specific letters at allowed indices
    if must_contain_letters:
        data = {
            k: v for k, v in data.items()
            if all(
                letter in k and all(len(k) <= idx or k[idx] != letter for idx in forbidden_indices.get(letter, []))
                for letter in must_contain_letters
            )
        }

    # Step 4: Check if there are enough items to find the nth largest
    if len(data) < n:
        return None, None  # Not enough items

    # Step 5: Sort the filtered keys by value in descending order
    sorted_keys = sorted(data, key=data.get, reverse=True)
    
    # Step 6: Return the nth largest key and its value
    nth_key = sorted_keys[n - 1]
    return nth_key, data[nth_key]

print("To start the game enter arose")
guess = ['a','r','o','s','e']

index_char_conditions = []
exclude_letters = []
must_contain_letters = []
forbidden_indices = {}
m = 2
c = 'c'
while c == 'c':
    v = input("Did the previous word exist? y or n:")
    if v == 'y':
        m = 2
        print("Enter colour for each letter by entering g, b or y for green, black or yellow")
        l=[]
        for i in range(0,5):
            x = input("Enter colour:")
            l.append(x)
        # print(l)
        
        index_of_g = []
        index_of_b = []
        index_of_y = []
        for i in range(len(l)):
            if l[i] == 'g': 
                index_of_g.append(i)
            if l[i] == 'b': 
                index_of_b.append(i)
            if l[i] == 'y': 
                index_of_y.append(i)
        # print("green:",index_of_g)
        # print("black:",index_of_b)
        # print("yellow:",index_of_y)
        
        for i in index_of_g:
            index_char_conditions.append((i,guess[i]))
        for i in index_of_b:
            exclude_letters.append(guess[i])
        for i in index_of_y:
            must_contain_letters.append(guess[i])
            if guess[i] not in forbidden_indices:
                forbidden_indices[guess[i]] = []
            forbidden_indices[guess[i]].append(i)
        index_char_conditions = list(dict.fromkeys(index_char_conditions))
        must_contain_letters = list(dict.fromkeys(must_contain_letters))
        # print("Greened:",index_char_conditions)
        # print("Blacked:",exclude_letters)
        # print("Yellowed:",must_contain_letters)
        # print("Index of Yellow:",forbidden_indices)
        
        # Find the next word based on all conditions
        
        next_word, next_value = word_finder(
            score,
            idx_char_pairs=index_char_conditions,
            exclude_letters=exclude_letters,
            must_contain_letters=must_contain_letters,
            forbidden_indices=forbidden_indices,
            n=1 )
    
    elif v == 'n':
        next_word, next_value = word_finder(
            score,
            idx_char_pairs=index_char_conditions,
            exclude_letters=exclude_letters,
            must_contain_letters=must_contain_letters,
            forbidden_indices=forbidden_indices,
            n=m )
        m+=1
    
    print(f"Next word: {next_word}, Value: {next_value}")
    g = []
    for i in next_word:
        g.append(i)
    # print(g)
    guess = g
    c = input("Enter c to continue and end to end:")
    if c == "end":
        break

print("Byeee...")
