array = ['one','two','three']
string = '\n'.join(array)

data = open('data.txt','w')
data.write(string)
data.close()


f = open('data.txt','r')
print(f.read().split('\n'))
f.close()

