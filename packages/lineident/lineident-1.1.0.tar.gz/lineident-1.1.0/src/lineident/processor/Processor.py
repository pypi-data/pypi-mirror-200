class Processor():
    def __init__(self, path, method, words) -> None:
        self.path = path
        self.method = method
        self.words = words.split(",")

    def process(self):
        matches = []
        lineCount = 1
        with open(self.path, "r") as f:
            while True:
                next_line = f.readline()

                if not next_line:
                    break

                line = next_line.strip()
                
                if(self.method == "or"):
                    for word in self.words:
                        if(word in line):
                            matches.append((lineCount, line))
                            break
                elif(self.method == "and"):
                    andCount = 0
                    
                    for word in self.words:
                        if(word in line):
                            andCount += 1

                    if(andCount == len(self.words)):        
                        matches.append((lineCount, line))

                lineCount+=1
        return matches