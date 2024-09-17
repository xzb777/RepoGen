
start
eval always

# to use function store the return location in reg5
label fn # print 10 to output 
10
copy 0 6
# function returns to value in reg5
copy 5 0
eval always


label start


# do random program stuff
copy 1 0
copy 0 1


# set up return in reg5
return
copy 0 5
#call function
fn
eval always
label return


copy 0 1
copy 1 0
