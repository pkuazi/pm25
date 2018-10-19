import numpy as np
from sklearn.cluster import KMeans

def prototype_initialize(num_class, x):
    
    n = proto_num
    kmeans = KMeans(n_clusters = n).fit(x)
    centers = kmeans.cluster_centers_
    centers = list(centers)
    
    return centers
        

    x_proto = []
    
    for i in range(0,num_class):
        x_train_class = []
        for j in range(len(x_train)):
            if y_train[j]==i:
                x_train_class.append(x_train[j])
        x = np.array(x_train_class, np.float32)
        
        kmeans = KMeans(n_clusters = n).fit(x)
        centers = kmeans.cluster_centers_
        centers = list(centers)
#     centers = prototype_initialize(x, proto_num)
        
        for j in range(proto_num):
            x_proto.append(centers[j])
               
    x_proto = np.array(x_proto, np.float32)
    
    return x_proto, y_proto