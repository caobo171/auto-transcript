# lis returns length of the longest increasing subsequence 
# in arr of size n 
def LIS(arr): 
    n = len(arr) 
    print(arr , n)
  
    # Declare the list (array) for LIS and initialize LIS 
    # values for all indexes 
    lis = [1]*n 

    trace = [0] * n

    return_array = [-1]*n
  
    # Compute optimized LIS values in bottom up manner 
    for i in range (1 , n): 
        for j in range(0 , i): 
            if arr[i] > arr[j] and lis[i]< lis[j] + 1 : 
                lis[i] = lis[j]+1
                trace[i] = j
  
    # Initialize maximum to 0 to get the maximum of all 
    # LIS 
    maximum = 0
  
    # Pick maximum of all LIS values 
    for i in range(n): 
        if(lis[i] >= maximum):
            maximum = lis[i]
            found_index = i
    
    while(found_index != 0 ):
    
        return_array[found_index] = arr[found_index]
        found_index = trace[found_index]
  
    return return_array 
# end of lis function 

