from collections import defaultdict

#   creates SimHash object with a threshold (similarity %) and hashes set
#       self._threshold =   long between 0 through 1
#       self._hashes =      set of integer hashes representing already crawled webpages
class SimHash:
    def __init__(self, threshold):
        self._threshold = threshold
        self._hashes = set()

    # private methods
    #   turns binary vector into an int
    #       ex: [1,0,1] = 5
    def __binVector_to_int(self, binVector:list)->int:
        binString = ''.join(map(str,binVector))
        return int(binString,2)
    
    #   simple hash method that converts word into an 16-bit hash number
    def __hash(self,word:str)->int:
        num = sum(ord(c) for c in word)
        hash_val = (num*(num+3))%65535
        return hash_val

    # public methods
    #   given a token_dict (obtained in scraper.py), will return an assigned tokenHash
    def tokenHash(self, token_dict:dict)->int:         
        #   STEP 2: TOKEN to HASH (int) to BIN_NUM (binary_num) then add appropriate weight
        token_Vector = [0]*16
        for word,weight in token_dict.items():
                #idk if it work like that but
                hash_val= self.__hash(word)
                bin_vect = [int(i) for i in format(hash_val, f'016b')]
                
                for j in range(0, 16):
                    if bin_vect[j] == 1:
                        token_Vector[j] += weight
                    else:
                        token_Vector[j] -= weight
                
        #   STEP 3: TURN THE VECTOR INTO 0s and 1s  (0s just stay the same ig)
        for d in range(0,len(token_Vector)):
            if token_Vector[d] > 0:
                token_Vector[d] = 1
            else:
                token_Vector[d] = 0

        #   STEP 4: TURNS IT INTO AN INT
        token = self.__binVector_to_int(token_Vector)
        return token

    #   returns if there is too similar site
    #       true for "yea"
    #       false for.. "no" will also add the token to the set for future use
    def similar(self, token_dict:dict)-> bool:
        token  = self.tokenHash(token_dict)        

        for i in self._hashes:
            xor_comp = format(token^i, f'016b')
            similarity = xor_comp.count('0')
            if similarity/16.0 >= self._threshold:
                return True

        self._hashes.add(token)
        return False
    
    #   testing methods, returns threshold and hashes set respectively
    def threshold(self)->int:
        return self._threshold
    
    def hashes(self)->set:
        return self._hashes