from collections import defaultdict


class SimHash:

    def __init__(self, threshold: int):
        self._threshold = threshold
        self._binarys = list()

    #   given a text file, will open it and split into groups of n grams each 
    #       selects hash values using mod 4 to be fingerprint
    def tokenHash(self, text_file_path: str): 
        token_dict = defaultdict(int)
        try:
            with open(text_file_path) as text_file:
                for line in text_file:
                    for word in line.rstrip('\n'): #split to read word by word , add to split alphanumerically
                        if word != '':
                            token_dict[word] += 1
        except:
            print("Error")
        
        token_Vector = list(8)
        for tokenPair in token_dict.items():
                #idk if it work like that but
                bin_num = list( map(int, str( bin(hash(tokenPair)).replace("0b", "")  ) ) ) 
                
                for i in range(0,len(bin_num)):
                    if bin_num[i] == 1:
                        token_Vector[i] += 1
                    else:
                        token_Vector[i] -= 1
                
        for d in range(0,len(token_Vector)):
            if d >= 0:
                token_Vector[d] = 1
            else:
                token_Vector[d] = 0
        
        #turn token vector into uhhhhh uhhhh a binary ?! !??!?!/!???!?1/?!?/1/?/1??/!/?!1/
        return token_Vector


    def similar(self, text_file_path)-> bool:
        #ideally token is actually some binary thing not whatever I set it as 
        token   = self.tokenHash(text_file_path)
        #   check file/list to see what % is same to each num
        #       if exceeds threshold, die ig
        #   store in list or file if not similar to stuff
        self._binarys.append(token)
        return True