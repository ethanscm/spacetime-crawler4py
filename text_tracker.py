class text_tracker:
    all_words = {}
    tokens = []
    longest_page = ("", 0)

    def SortFrequencies(array):
        if(len(array) == 1):
            return array
        elif (len(array) == 0):
            return array
        
        mid = len(array) // 2
        left = text_tracker.SortFrequencies(array[:mid])
        right = text_tracker.SortFrequencies(array[mid:])

        l = 0
        r = 0
        t = []

        while l < len(left) and r < len(right):
            if text_tracker.all_words[left[l]] > text_tracker.all_words[right[r]]:
                t.append(left[l])
                l += 1
            elif text_tracker.all_words[left[l]] < text_tracker.all_words[right[r]]:
                t.append(right[r])
                r += 1
            else:
                if(left[l] <= right[r]):
                    t.append(left[l])
                    l += 1
                else:
                    t.append(right[r])
                    r += 1

        while l < len(left):
            t.append(left[l])
            l += 1

        while r < len(right):
            t.append(right[r])
            r += 1
        
        return t

    def printtopfifty(array):
        print("---Top 50---")

        arr = text_tracker.SortFrequencies(array)
        print(f"after sorted. ", arr)

        for t in range(50):
            if t >= len(arr):
                break
            print(f'{t}) {arr[t]}: {text_tracker.all_words[arr[t]]}')

    def restore_data():
        #restore the frequency variable
        freq_file = open("frequency.txt", 'r')
        freq_text= freq_file.read()
        raw_text = freq_text[1:-2]
        all_pairs = raw_text.split(", ")

        for item in all_pairs:
            kv = item.split(": ")
            k = kv[0][1:-1]
            v = int(kv[1])
            text_tracker.tokens.append(k)
            text_tracker.all_words[k] = v

        freq_file.close()

        #restore the longest page variable
        #store all keys back into tokens
    def restore_longest_page():
        lp_file = open("longest_page.txt", "r")
        lp = lp_file.read()
        lp = lp[1:-1]
        lp = lp.split(", ")
        text_tracker.longest_page = (lp[0], int(lp[1]))