# This function will read the txt file data and return it, in this program it is only used for the "view all" option
def readFile(P_mainFile):
    fileOpened = open(P_mainFile, "r")
    fileData = fileOpened.read()
    # always make sure to close the file after opening it
    fileOpened.close()
    return fileData

# this is the function that generates the password, it takes in the password length and any character exclusions that are both
# determined by later functions
def createPassword(P_Length, P_Exclusions):
    import random
    import string
     
    newPassword = ""
    characterPool = string.ascii_letters + string.punctuation + string.digits
    
    # this for loop runs through the list of character exclusions and replaces them with empty characters in the character pool
    for i in P_Exclusions:
        characterPool = characterPool.replace(i, "")
        characterPool = characterPool.replace(i.upper(), "")
    
    # this for loop adds a new random character from the character pool to the empty password variable
    for i in range(P_Length):
        newPassword += random.choice(characterPool)
    
    return newPassword

# this function is used to search the file for a specific password via the site name
def fileSearch(P_mainFile, P_siteName):
    fileOpened = open(P_mainFile, "r")
    fileLines = fileOpened.readlines()

    # this for loop checks each line in the file for the given site name and then returns all of the content on that line
    for line in fileLines:
        if line.find(P_siteName) != -1:
            return line
    fileOpened.close()

# this function is used to write new passwords to the txt file
def writeToFile(P_mainFile, P_newPassword, P_website):
    # we use access type "a" instead of "w" so we append to the file instead of overwriting it
    fileData = open(P_mainFile, "a")

    # this format writes on the file line as "sitename: password" 
    fileData.write(P_website + ": " + P_newPassword)
    fileData.close()

# I do not take credit for this function, I found it on StackOverflow, https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard
# thank you very much user7864790
def addToClipBoard(P_password):
    import os
    command = 'echo | set /p nul=' + P_password.strip() + '| clip'
    os.system(command)

# this function is used to get any exclusions from the user, honestly I can't see many reasons why you'd want to exclude characters but I thought it'd be fun to add
def getInputExclusions():
    excludedCharacters = input("\nAre there any characters or numbers you would like to exclude? (leave blank to continue): ")

    # we use the list() function to split the string up in to a list of each indiviual character
    excludedCharacters = list(excludedCharacters)
    return excludedCharacters

# this function is used to get the desired password length from the user, the recommendation is based on personal experience and a single google search
def getInputLength():
        print("Password should be between 4 and 16 characters")
        passwordLength = int(input("How many characters long would you like the password to be?: "))
        return passwordLength

# arguably the simplest function here, it just gets the name of the website the user is making the password for, not much to explain 
def getInputInputWebsite():
    website = input("\nWhat site is this password for?: ")
    print("")
    return website.lower()

# the primary function that runs the program
def main():
    
    # the main file variable that all the functions access
    mainFile = "Wax_Key_List.txt"

    # the title and explanation of the program
    print("\n")
    print("=" * 20)
    print("WELCOME TO WAXKEY")
    print("=" * 20)
    print("WaxKey is a program designed to help create and store passwords\
          \nAll passwords are saved locally on a .txt file\n")
   
    # the while loop that runs the program until broken
    while True:
        # input used to decide what the user wants to use the program for, after any function we return here
        userChoice = input("\nWould you like to check a currently exsisting password or create a new password?\
                            \n(1 for exsisting. 2 for new. 3 to close): ")
        
        # the first branch, this is the option to check exsisting passwords
        if userChoice == "1":
            # additional choice for wether or not the user wants to view all passwords or search for a specific one
            print("\nWould you like to search for a specific site or view all curent passwords?")
            searchChoice = input("(1 for search. 2 for view all): ")
           
            # this is the option for "view all" it runs the readFile function and essentially just prints the entire file
            if searchChoice == "2":
                viewFile = readFile(mainFile)
                print(viewFile)
           
            # this is the option to search for a specific password 
            if searchChoice == "1":

                # get the site name for the associated password
                searchSiteName = input("\nWhat is the name of the site for the password?: ")
                searchedPassword = fileSearch(mainFile, searchSiteName)

                # try except in case the user inputs an invalid site name
                try:
                    searchedPassword = searchedPassword.replace(searchSiteName, "")
                except:
                    print("that site doesn't have a password associated with it.")
                    break
                
                # prints out the password and site name if one was found and then prompts the user to copy to clipboard
                print("\nYour password for " + searchSiteName + " is" + searchedPassword)
                clipboardChoice = input("would you like to copy the password to your clipboard?(Y/N): ").lower()
                if clipboardChoice == "y":
                    addToClipBoard(searchedPassword.replace(": ", ""))
                    print("Copied!")

        # the second branch of the program, this is the option for generating new passwords
        if userChoice == "2":
            
            # get all neccesary information via functions site name, password lenth, exclusions
            websiteName = getInputInputWebsite()
            passwordLength = getInputLength()
            passwordExclusions = getInputExclusions()

            # create a new password with the given information
            newPassword = createPassword(passwordLength, passwordExclusions)
            print("\nYour new password for " + websiteName + " is: " + newPassword)

            # give the user the option to save the password or not
            saveChoice = input("Would you like to save this passwod?(Y/N):").lower()
            if saveChoice == "y":
                print("\nPassword succesfully saved")

                # write the new password to the file with the associated site name
                writeToFile(mainFile, newPassword, websiteName)
        
        # the third branch of the program... this just ends the program
        if userChoice == "3":
            break
main()