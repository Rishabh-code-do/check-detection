def parse_int(textnum, numwords={}):
    # create our default word-lists
    if not numwords:

      # singles
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      # tens
      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      # larger scales
      scales = ["hundred", "thousand", "lakh", "crore"]

      # divisors
      numwords["and"] = (1, 0)

      # perform our loops and start the swap
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     
        numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   
        if(idx==2):
            numwords[word] = (100000, 0) 
        elif(idx==3):
            numwords[word] = (100000000, 0) 
        else:
          numwords[word] = (10 ** (idx * 3 or 2), 0) 
        
    # primary loop
    current = result = 0
    # loop while splitting to break into individual words
    for word in textnum.replace("-"," ").split():
        # if problem then fail-safe
        if word.lower() not in numwords:
          return "invalid"

        # use the index by the multiplier
        scale, increment = numwords[word.lower()]
        current = current * scale + increment
        
        # if larger than 100 then push for a round 2
        if scale > 100:
            result += current
            current = 0

    # return the result plus the current
    return result + current
