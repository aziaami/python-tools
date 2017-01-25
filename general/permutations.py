import profile, os

#compute all permutations of an array

def somji_all_permutations(x,y,file="somji_perms.txt"):
    for i in range(len(y)):
        new_x = x + y[i]
        #print new_x
        write_to_file(new_x, file)
        new_y = y[:i] + y[i+1:]
        somji_all_permutations(new_x, new_y)

#########################################
def array_to_string(a):
    return ''.join(a)

def write_to_file(item, file):
    data = array_to_string(item) + "\n"
    #file = open(file, "a")
    #file.write(data)
    #file.close()

def swap (array, j, i):
    temp = array[j]
    array[j] = array[i]
    array[i] = temp

#given a set of letters - iteratively find all 
#rearrangements of those letters
def all_rearrangements(array,file):
    N = len(array)

    if N == 1:
        ##print array
        write_to_file(array,file)
        return

    p = []
    for index in range(N+1):
        p.append(index)
    
    i=1
    j=0

    #original array is valid arrangement
    ##print array
    write_to_file(array,file)

    while (i < N) :
        p[i] = p[i] - 1

        if (i % 2) == 1:
            j = p[i]
        else:
            j=0

        swap(array, j, i)

        i=1
        while (p[i] == 0):
            p[i] = i
            i += 1

        ##print array
        write_to_file(array,file)

#generate a set of combinations (order not important)
#of letters in the array. Move through the array taking
#off the first element, concat it with every combination 
#of the smaller array. Recursive  
def getCombinations(arr, n):
    ret = []
    if n == 1 :
        for e in arr:
            ret.append([e])
    else:
        for i in range(len(arr)):
            element = arr[i]
            new_arr = arr[i+1:]
            combos = getCombinations(new_arr , n-1)
            for k in range(len(combos)):
                combo = []
                combo.extend(element)
                combo.extend(combos[k])
                ret.append(combo)
    return ret


def aziz_all_permutations(array, file="aziz_perms.txt"):
    for n in range(1,len(array)+1):
        combos = getCombinations(array,n)
        for arr in combos:
            all_rearrangements(arr, file)

def string_to_array(s):
    return list(s)

def count_lines_in_text_file(file):
    f = open(file, 'r')
    count = 0
    for line in f:
        count += 1
    f.close()
    return count

#---------------------------
#this is executed when we run this script from commandline
if __name__ == "__main__":
    somjiFile = "somji_perms.txt"
    azizFile  = "aziz_perms.txt" 

    #delete the files if they exist so we can start fresh
    if os.path.isfile(somjiFile):
        os.remove(somjiFile)
    if os.path.isfile(azizFile):
        os.remove(azizFile)

    #define string to permute
    testStr = "abcdefghi"
    array = string_to_array(testStr)
    print "Finding all permutations of: ", testStr

    #all_rearrangements(["a","b","c","d"])
    #print getCombinations(array, 3)

    print 'Running somji_all_permutations ...'
    profile.run("somji_all_permutations('', array, somjiFile)")

    print 'Running aziz_all_permutations ...'
    profile.run("aziz_all_permutations(array, azizFile)")

    if os.path.isfile(somjiFile) and os.path.isfile(azizFile):
        somjiNum = count_lines_in_text_file(somjiFile)
        azizNum  = count_lines_in_text_file(azizFile)

        print "check same number of permutations..."
        print "somji number : ", somjiNum
        print "aziz number  : ", azizNum