#open should be sorted by ascending f values of nodes such that nodes with a lot of promise are popped earlier
open = [] # unexpanded nodes
closed = [] # expended nodes

# 1) push node representing the initial problem ste onto the open list

# 2) Loop that pops nodes from open and expands them, producing child nodes which might be added to open
# failure or success are recognized and 
# 3)