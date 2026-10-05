import re
    
def cleanString(raw_str):
    cleanString = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[Email]", raw_str)
    return cleanString


if __name__ == "__main__":
    print(cleanString("user jane@onlinedoctor.ch sent a file, cc bob@test.com"))      