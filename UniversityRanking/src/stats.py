"""
@author: Bolun
"""

class histogram:
    def __init__(self):
        self.bucket = {}
        self._max = 1900
        self._min = 2015
        
        
    def add(self, e = "2000"):
        """
        @type e: String
        @param e: year
        """
        f = 0.0
        try: 
            f = float(e)
            intN = int(f)
            if f == intN: # it is valid integer
                if intN > self._max:
                    self._max = intN
                if intN < self._min:
                    self._min = intN
                if self.bucket.has_key(str(intN)):
                    self.bucket[str(intN)] += 1
                else:
                    self.bucket.update({str(intN) : 1})
            else:
                print "invalid type for the element (float):", e
        except:
            print "invalid type for the element (non-numeric):", e
            pass
        
    def hist(self):
        """
        @return: the dictionary of distribution in the granularity of year
        """
        return self.bucket
    
    def cdf(self):
        """
        @description: calculate the faculty distribution on year
        
        @return: 1) the index of distribution; 2) the frequency distribution; 3) the CDF of the distribution
        """
        l = self._max - self._min + 1
        cdf = [0.0]*l
        index = []
        index_dict = {}
        for i in range(l):
            index_dict.update({str(self._min+i) : i})
            index.append(str(self._min+i))
        for key in self.bucket:
            if index_dict.has_key(key):
                cdf[index_dict[key]] = float(self.bucket[key])
            else:
                pass
        
        _sum = sum(cdf)
        dist = list(cdf)
        cur_sum = 0.0
        for i in range(len(cdf)):
            tmp = cdf[i]
            cdf[i] = cdf[i] + cur_sum
            cur_sum += tmp
        for i in range(len(cdf)):
            cdf[i] /= _sum
            
        return index, dist, cdf
        