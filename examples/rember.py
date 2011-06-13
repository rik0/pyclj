import pyclj

@pyclj.clojure
def rember(a, lat):
    '''
    (defn rember 
      "Remove first occurrence of a from lat"
      [a lat]
      (cond
        (empty? lat) '()
        (= (first lat) a) (rest lat)
        :else (cons
          (first lat)
          (rember a (rest lat)))))
    '''


if __name__ == '__main__':
    print rember(2, range(4))
    help(rember)
