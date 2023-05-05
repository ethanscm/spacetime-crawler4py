from collections import defaultdict

#   SimHash Object: initialized threshold (similarity % in decimals) and empty hashes set
#       self._threshold =   long between 0 through 1
#       self._hashes =      set of integer hashes representing crawled webpages
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
    #       hashes through taking the integer rep of each unicode char and summing them
    #       then multiplying by itself + 3 and finding the remainder over 65535
    def __hash(self,word:str)->int:
        num = sum(ord(c) for c in word)
        hash_val = (num*(num+3))%65535
        return hash_val

    # public methods
    #   given a token_dict (obtained in scraper.py), will return an assigned tokenHash
    def tokenHash(self, token_dict:dict)->int:         
        #   TOKEN to HASH (str -> int) to 16 bit BIN_NUM (int -> vector) with appropriate weights per word
        token_Vector = [0]*16
        for word,weight in token_dict.items():
                hash_val= self.__hash(word)
                bin_vect = [int(i) for i in format(hash_val, f'016b')]
                
                for j in range(0, 16):
                    if bin_vect[j] == 1:
                        token_Vector[j] += weight
                    else:
                        token_Vector[j] -= weight
                
        #   TURNS THE BIN_NUM (vector) INTO 0s and 1s (vector -> int) 
        for d in range(0,len(token_Vector)):
            if token_Vector[d] > 0:
                token_Vector[d] = 1
            else:
                token_Vector[d] = 0

        #   TURNS BINARY INT into regular int
        token = self.__binVector_to_int(token_Vector)
        return token

    #   computes token of given token_dict, then checks if similarly webpage already exists
    #       if all comparisons are under threshold:
    #           hash is added to the hashes set and returns FALSE
    #       if it does exceed threshold
    #           returns TRUE and hash is not added
    def similar(self, token_dict:dict)-> bool:
        token  = self.tokenHash(token_dict)        

        for i in self._hashes:
            xor_comp = format(token^i, f'016b')
            similarity = xor_comp.count('0')
            if similarity/16.0 >= self._threshold:
                return True

        self._hashes.add(token)
        hash_file = open("hashes.txt", 'a')
        hash_file.write(f'{token}\n')
        hash_file.close()
        return False
    
    #   will add the documented hashes back into the set upon restart
    def restore_simhashes(self):
        hash_file = open("hashes.txt", 'r')
        for line in hash_file:
            h = int(line)
            self._hashes.add(h)
    
    #   testing methods, returns threshold and hashes set respectively
    def threshold(self)->int:
        return self._threshold
    
    def hashes(self)->set:
        return self._hashes