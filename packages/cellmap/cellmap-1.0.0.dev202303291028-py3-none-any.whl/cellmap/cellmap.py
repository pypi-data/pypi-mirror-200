import anndata
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patheffects as PathEffects
import scipy
import sklearn.preprocessing
import matplotlib.colors
import pandas as pd
import logging
import scanpy


def create_graph(
    X,
    Y,
    cutedge_vol = None,
    cutedge_length = None,
    cut_std = 1,
    return_mask = False
):
    tri_ = matplotlib.tri.Triangulation(X,Y)
    x1,y1 = X[tri_.triangles[:,0]],Y[tri_.triangles[:,0]]
    x2,y2 = X[tri_.triangles[:,1]],Y[tri_.triangles[:,1]]
    x3,y3 = X[tri_.triangles[:,2]],Y[tri_.triangles[:,2]]
    vol = np.abs((x1-x3)*(y2-y3)-(x2-x3)*(y1-y3))
    length = np.max([(x1-x2)**2+(y1-y2)**2,(x2-x3)**2+(y2-y3)**2,(x3-x1)**2+(y3-y1)**2],axis=0)
    if cutedge_vol == None:
        judge_vol = vol < cut_std*np.std(vol)
    else:
        judge_vol = vol < np.percentile(vol,100-cutedge_vol)
    if cutedge_length == None:
        judge_length = length < cut_std*np.std(length)
    else:
        judge_length = length < np.percentile(length,100-cutedge_length)
    tri_mask_ = judge_vol & judge_length
    tri_.set_mask(tri_mask_==False)
    if return_mask: return tri_,tri_mask_
    else: return tri_



def check_arguments(
    adata,
    **kwargs
):
    logger = logging.getLogger("argument checking")
    logger.setLevel(logging.WARNING)
    
    if 'exp_key' in kwargs.keys():
        if kwargs['exp_key'] != None:
            if (kwargs['exp_key'] not in adata.obsm.keys()) and (kwargs['exp_key'] not in adata.layers.keys()):
                raise KeyError('The key \"%s\" was not found in adata.obsm.obsm. Please modify the argument \"exp_key\".' % kwargs['exp_key'])
    
    if 'exp_2d_key' in kwargs.keys():
        if (kwargs['exp_2d_key'] not in adata.obsm.keys()) and (kwargs['exp_2d_key'] not in adata.layers.keys()):
            if 'X_umap' in adata.obsm.keys():
                logger.warning('The key \"%s\" was not found in adata.obsm, but \"X_umap\" was found insted. Replace \"%s\" with \"X_umap\".' % (kwargs['exp_2d_key'],kwargs['exp_2d_key']))
                kwargs['exp_2d_key'] = 'X_umap'
            elif 'X_tsne' in adata.obsm.keys():
                logger.warning('Warning: The key \"%s\" was not found in adata.obsm, but \"X_tsne\" was found insted. Replace \"%s\" with \"X_tsne\".' % (kwargs['exp_2d_key'],kwargs['exp_2d_key']))
                kwargs['exp_2d_key'] = 'X_tsne'
            else:
                raise KeyError('The key \"%s\" was not found in adata.obsm.obsm. Please modify the argument \"exp_2d_key\".' % kwargs['exp_2d_key'])
    
    if 'vel_key' in kwargs.keys():
        if (kwargs['vel_key'] not in adata.obsm.keys()) and (kwargs['vel_key'] not in adata.layers.keys()):
            raise KeyError('The key \"%s\" was not found in adata.obsm.obsm. Please modify the argument \"vel_key\".' % kwargs['vel_key'])
    
    if 'vel_2d_key' in kwargs.keys():
        if (kwargs['vel_2d_key'] not in adata.obsm.keys()) and (kwargs['vel_2d_key'] not in adata.layers.keys()):
            if 'velocity_umap' in adata.obsm.keys():
                logger.warning('The key \"%s\" was not found in adata.obsm, but \"velocity_umap\" was found insted. Replace \"%s\" with \"velocity_umap\".' % (kwargs['basis'],kwargs['basis']))
                kwargs['vel_2d_key'] = 'velocity_umap'
            elif 'velocity_tsne' in adata.obsm.keys():
                logger.warning('Warning: The key \"%s\" was not found in adata.obsm, but \"velocity_tsne\" was found insted. Replace \"%s\" with \"velocity_tsne\".' % (kwargs['basis'],kwargs['basis']))
                kwargs['vel_2d_key'] = 'velocity_tsne'
            else:
                raise KeyError('The key \"%s\" was not found in adata.obsm.obsm. Please modify the argument \"vel_2d_key\".' % kwargs['vel_2d_key'])
    
    if 'map_key' in kwargs.keys():
        if kwargs['map_key'] == None:
            kwargs['map_key'] = kwargs['exp_2d_key']
    
    key_names = ['cluster_key','potential_key']
    for key in key_names:
        if key in kwargs.keys():
            if kwargs[key] not in adata.obs.keys():
                raise KeyError('The key \"%s\" was not found in adata.obs. Please modify the argument \"%s\".' % (kwargs[key],key))
    
    key_names = []
    for key in key_names:
        if key in kwargs.keys():
            if kwargs[key] not in adata.obsm.keys():
                raise KeyError('The key \"%s\" was not found in adata.obsm. Please modify the argument \"%s\".' % (kwargs[key],key))
    
    key_names = ['graph_key']
    for key in key_names:
        if key in kwargs.keys():
            if kwargs[key] not in adata.uns.keys():
                raise KeyError('The key \"%s\" was not found in adata.uns. Please modify the argument \"%s\".' % (kwargs[key],key))
    
    key_names = ['expression_key']
    for key in key_names:
        if key in kwargs.keys():
            if kwargs[key] != None:
                if kwargs[key] not in adata.layers.keys():
                    raise KeyError('The key \"%s\" was not found in adata.layers. Please modify the argument \"%s\".' % (kwargs[key],key))
    
    key = 'obs_key'
    if key in kwargs.keys():
        if type(kwargs[key]) == list:
            key_names = ['cluster_key','potential_key']
            for key_ in key_names:
                if key_ in kwargs.keys():
                    if kwargs[key_] in kwargs[key]:
                        # raise logger.warning('The key \"%s\" was multipled.' % (kwargs[key_]))
                        kwargs[key].remove(kwargs[key_])
            for arg in kwargs[key]:
                if arg not in adata.obs.keys():
                    logger.warning('The key \"%s\" was not found in adata.obs. The key \"%s\" is removed from \"%s\".' % (arg,key,arg,key))
                    kwargs[key].remove(key)
            key_names = ['cluster_key','potential_key']
        elif kwargs[key] != None:
            raise TypeError('The argument %s should be a list or None')
    
    key = 'genes'
    if key in kwargs.keys():
        if type(kwargs[key]) == list:
            for arg in kwargs[key]:
                if arg not in adata.var.index:
                    logger.warning('The gene \"%s\" was not found. The gene \"%s\" is removed from \"%s\".' % (arg,arg,key))
                    kwargs[key].remove(arg)
        elif kwargs[key] != None:
            raise TypeError('The argument %s should be a list or None')

    return kwargs


def cmap_earth(cv):
    #c_list  = np.array(['#0938BF','#50D9FB','#B7E5FA','#98D685','#36915c','#F9EFCD','#E0BB7D','#D3A62D','#997618','#705B10','#5F510D','#A56453','#5C1D09'])
    c_min,c_max = 5,95
    c_list  = np.array(['#0938BF','#50D9FB','#B7E5FA','#98D685','#fff5d1','#997618','#705B10'])
    c_level = np.array([np.percentile(cv,(c_max-c_min)*(i)/len(c_list)+c_min) for i in range(len(c_list))])
    color = np.vstack((c_level,c_list)).T
    hight = 1000*color[:,0].astype(np.float32)
    hightnorm = sklearn.preprocessing.minmax_scale(hight)
    colornorm = []
    for no, norm in enumerate(hightnorm):
        colornorm.append([norm, color[no, 1]])
    colornorm[-1][0] = 1
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('earth', colornorm, N=hight.max()-hight.min()+1)
    return cmap


def Hodge_decomposition(
    adata,
    exp_key = None,
    vel_key  = 'velocity',
    exp_2d_key = 'X_umap',
    vel_2d_key = 'velocity_umap',
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    graph_method = 'Delauney',
    alpha = 0.2,
    n_neighbors = 10,
    contribution_rate = 0.95,
    cutedge_vol  = None,
    cutedge_length = None,
    ):
    """
    Hodge decomposition

    Parameters
    ----------
    adata: anndata (n_samples, n_features)
    
    exp_key: None or string
    """
    
    kwargs_arg = check_arguments(adata, exp_key=exp_key, vel_key = vel_key, exp_2d_key=exp_2d_key, vel_2d_key=vel_2d_key, graph_method=graph_method)
    exp_key,vel_key,exp_2d_key,vel_2d_key = kwargs_arg['exp_key'],kwargs_arg['vel_key'],kwargs_arg['exp_2d_key'],kwargs_arg['vel_2d_key']
    
    
    if exp_key == None:
        if scipy.sparse.issparse(adata.X):
            exp_HD = adata.X.toarray()
        else:
            exp_HD = adata.X
    elif exp_key in adata.obsm.keys():
        exp_HD = adata.obsm[exp_key]
    else:
        exp_HD = adata.layers[exp_key]
    
    vel_HD = adata.obsm[vel_key] if vel_key in adata.obsm.keys() else adata.layers[vel_key]
    exp_LD = adata.obsm[exp_2d_key][:,:2] if exp_2d_key in adata.obsm.keys() else adata.layers[exp_2d_key][:,:2]
    vel_LD = adata.obsm[vel_2d_key][:,:2] if vel_2d_key in adata.obsm.keys() else adata.layers[vel_2d_key][:,:2]
    
    n_node_ = exp_HD.shape[0]
    if graph_method == 'Delauney':
        tri_,idx_tri = create_graph(exp_LD[:,0],exp_LD[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length,return_mask = True)
        source, target = np.ravel(tri_.triangles[idx_tri][:,[0,1,2]]),np.ravel(tri_.triangles[idx_tri][:,[1,2,0]])
    elif graph_method == 'knn':
        pca = sklearn.decomposition.PCA()
        exp_HD_pca = pca.fit_transform(exp_HD)
        n_pca = np.min(np.arange(len(pca.explained_variance_ratio_))[np.cumsum(pca.explained_variance_ratio_)>contribution_rate])
        knn = NearestNeighbors(n_neighbors=n_neighbors+1, algorithm='kd_tree')
        knn.fit(exp_HD_pca[:,:n_pca])
        distances, indices = knn.kneighbors(exp_HD_pca[:,:n_pca])
        distances, indices = distances[:,1:], indices[:,1:]
        source = np.ravel(np.repeat(np.arange(exp_HD.shape[0]).reshape((-1, 1)),n_neighbors,axis=1))
        target = np.ravel(indices)
    
    idx = np.isnan(vel_HD[0])==False
    X1,X2 = exp_HD[:,idx][source],exp_HD[:,idx][target]
    V1,V2 = vel_HD[:,idx][source],vel_HD[:,idx][target]
    Dis = np.linalg.norm(X2-X1,axis=1)
    edge_vel_HD = np.sum(0.5*(V1+V2)*(X2-X1),axis=1)/Dis
    
    idx = np.isnan(vel_LD[0])==False
    X1,X2 = exp_LD[:,idx][source],exp_LD[:,idx][target]
    V1,V2 = vel_LD[:,idx][source],vel_LD[:,idx][target]
    Dis = np.linalg.norm(X2-X1,axis=1)
    edge_vel_LD = np.sum(0.5*(V1+V2)*(X2-X1),axis=1)/Dis
    
    n_edge_ = len(source)
    grad_mat = np.zeros([n_edge_,n_node_],dtype=float)
    grad_mat[tuple(np.vstack((np.arange(n_edge_),source)))] = -1
    grad_mat[tuple(np.vstack((np.arange(n_edge_),target)))] = 1
    div_mat = -grad_mat.T
    lap = -np.dot(div_mat,grad_mat)
    source_term = np.dot(div_mat,(1-alpha)*edge_vel_LD+alpha*edge_vel_HD)
    potential = np.linalg.solve(lap,source_term)
    pot_flow = -np.dot(grad_mat,potential)
    adata.obs[potential_key] = potential - np.min(potential)
    if graph_key not in adata.uns.keys(): adata.uns[graph_key] = np.vstack((source,target))

def view(
    adata,
    basis = 'X_umap',
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cluster_key = None,
    show_graph = False,
    cutedge_vol  = None,
    cutedge_length = None,
    title = '',
    **kwargs
    ):
    
    kwargs_arg = check_arguments(adata,
                             basis = basis,
                             potential_key = potential_key,
                             graph_key = graph_key,
                            )
    basis = kwargs_arg['basis']
    
    if 'camp' not in kwargs:
        kwargs['cmap'] = cmap_earth(adata.obs[potential_key])
    data_pos = adata.obsm[basis]
    fig,ax = plt.subplots(figsize=(15,10))
    sc = ax.scatter(data_pos[:,0],data_pos[:,1],c=adata.obs[potential_key],zorder=10,**kwargs)
    if show_graph:
        tri_ = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length)
        ax.tripcolor(tri_,adata.obs[potential_key],lw=0.5,zorder=0,alpha=0.3,cmap=kwargs['cmap'])
    if cluster_key != None:
        if cluster_key in adata.obs.keys():
            cluster = adata.obs[cluster_key]
            for c in np.unique(cluster):
                txt = plt.text(np.mean(data_pos[cluster == c],axis=0)[0],np.mean(data_pos[cluster == c],axis=0)[1],c,fontsize=20,ha='center', va='center',fontweight='bold',zorder=20)
                txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
        else:
            print('There is no cluster key \"%s\" in adata.obs' % cluster_key)
    ax.axis('off')
    ax.set_title(title,fontsize=18)
    plt.colorbar(sc,aspect=20, pad=0.01, orientation='vertical').set_label('Potential',fontsize=20);


def view_cluster(
    adata,
    basis = 'X_umap',
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cluster_key = 'clusters',
    show_graph = True,
    cutedge_vol  = None,
    cutedge_length = None,
    plot_rate = 0.3,
    seed = None,
    title = '',
    **kwargs
    ):
    
    kwargs_arg = check_arguments(adata,
                             basis = basis,
                             potential_key = potential_key,
                             graph_key = graph_key,
                            )
    basis = kwargs_arg['basis']
    
    if 'camp' not in kwargs:
        kwargs['cmap'] = cmap_earth(adata.obs[potential_key])

    data_pos = adata.obsm[basis]
    fig,ax = plt.subplots(figsize=(15,10))
    tri_ = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length)
    # sc = ax.tripcolor(tri_,adata.obs[potential_key],lw=0.5,zorder=0,alpha=0.75,cmap=kwargs['cmap'])
    sc = ax.tricontourf(tri_,adata.obs[potential_key],zorder=0,alpha=0.9,cmap=kwargs['cmap'],levels=100)
    if cluster_key in adata.obs.keys():
        cluster = adata.obs[cluster_key]
        idx_random = np.zeros(cluster.shape,dtype=bool)
        np.random.seed(seed)
        idx_random[np.random.choice(len(idx_random),int(plot_rate*len(idx_random)),replace=False)] = True
        cluster_set = np.unique(cluster)
        cmap = plt.get_cmap("tab10") if len(cluster_set) <= 10 else plt.get_cmap("tab20")
        for i in range(len(cluster_set)):
            idx = (cluster == cluster_set[i]) & idx_random
            ax.scatter(data_pos[idx,0],data_pos[idx,1],zorder=10,alpha=0.8,edgecolor='w',color=cmap(i),**kwargs)
            txt = plt.text(np.mean(data_pos[cluster == cluster_set[i]],axis=0)[0],np.mean(data_pos[cluster == cluster_set[i]],axis=0)[1],cluster_set[i]
                           ,color=cmap(i),fontsize=20,ha='center', va='center',fontweight='bold',zorder=20)
            txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
    else:
        print('There is no cluster key \"%s\" in adata.obs' % cluster_key)
    ax.set_title(title,fontsize=18)
    plt.colorbar(sc,aspect=20, pad=0.01, orientation='vertical').set_label('Potential',fontsize=20)
    ax.axis('off')


def view_surface(
    adata,
    basis = 'X_umap',
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cluster_key = None,
    show_graph = False,
    cutedge_vol  = None,
    cutedge_length = None,
    title = '',
    **kwargs
    ):
    
    kwargs_arg = check_arguments(adata,
                             basis = basis,
                             potential_key = potential_key,
                             graph_key = graph_key,
                            )
    basis = kwargs_arg['basis']
    
    data_pos = adata.obsm[basis]
    tri_ = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length)
    cmap = cmap_earth(adata.obs[potential_key])
    fig,ax = plt.subplots(figsize=(15,10))
    cntr = ax.tricontourf(tri_,adata.obs[potential_key],cmap=cmap,levels=100,zorder=2)
    fig.colorbar(cntr, shrink=0.75, orientation='vertical').set_label('Potential',fontsize=20)
    if show_graph: ax.triplot(tri_,color='w',lw=0.5,zorder=10,alpha=1)
    ax.set_xlim(np.min(data_pos[:,0])-0.02*(np.max(data_pos[:,0])-np.min(data_pos[:,0])),np.max(data_pos[:,0])+0.02*(np.max(data_pos[:,0])-np.min(data_pos[:,0])))
    ax.set_ylim(np.min(data_pos[:,1])-0.02*(np.max(data_pos[:,1])-np.min(data_pos[:,1])),np.max(data_pos[:,1])+0.02*(np.max(data_pos[:,1])-np.min(data_pos[:,1])))
    ax.tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False,bottom=False,left=False,right=False,top=False)
    ax.spines['right'].set_visible(False),ax.spines['top'].set_visible(False),ax.spines['bottom'].set_visible(False),ax.spines['left'].set_visible(False)
    ax.set_title(title,fontsize=18)
    if cluster_key != None:
        texts = []
        if cluster_key in adata.obs.keys():
            cluster = adata.obs[cluster_key]
            for c in np.unique(cluster):
                txt = ax.text(np.mean(data_pos[cluster == c],axis=0)[0],np.mean(data_pos[cluster == c],axis=0)[1],c,fontsize=20,ha='center', va='center',fontweight='bold')
                txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
                texts.append(txt)


def view_surface_3D(
    adata,
    basis = 'X_umap',
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cluster_key = None,
    cutedge_vol  = 1,
    cutedge_length = 1,
    elev = 30,
    azim = -60,
    plot_rate = 0.3,
    title = '',
    **kwargs
    ):
    
    kwargs_arg = check_arguments(adata,
                             basis = basis,
                             potential_key = potential_key,
                             graph_key = graph_key,
                            )
    basis = kwargs_arg['basis']
    
    data_pos = adata.obsm[basis]
    tri_ = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length)
    cmap = cmap_earth(adata.obs[potential_key])
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    cntr = ax.plot_trisurf(tri_,adata.obs[potential_key],cmap=cmap,zorder=2)#,cmap=cmap_CellMap,levels=100)
    ax.set_box_aspect(aspect = (1,1,0.8))
    fig.colorbar(cntr, shrink=0.5, orientation='vertical').set_label('Potential',fontsize=20)
    ax.set_title(title,fontsize=18)
    if cluster_key != None:
        texts = []
        if cluster_key in adata.obs.keys():
            cluster = adata.obs[cluster_key]
            for c in np.unique(cluster):
                txt = ax.text(np.mean(data_pos[cluster == c],axis=0)[0],np.mean(data_pos[cluster == c],axis=0)[1],np.mean(adata.obs[potential_key][cluster == c]),c,fontsize=15,ha='center', va='center',fontweight='bold',zorder=1000)
                txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
                texts.append(txt)
        # from adjustText import adjust_text
        # adjust_text(texts)
    ax.view_init(elev=elev, azim=azim)


def view_surface_3D_cluster(
    adata,
    basis = 'X_umap',
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cluster_key = 'clusters',
    cutedge_vol  = 1,
    cutedge_length = 1,
    elev = 30,
    azim = -60,
    seed = None,
    plot_rate = 0.25,
    title = '',
    **kwargs
    ):
    
    if cluster_key in adata.obs.keys():
        kwargs_arg = check_arguments(adata,
                                 basis = basis,
                                 potential_key = potential_key,
                                 graph_key = graph_key,
                                )
        basis = kwargs_arg['basis']
        data_pos = adata.obsm[basis]
        tri_ = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length)
        cmap = cmap_earth(adata.obs[potential_key])
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111, projection='3d')
        cntr = ax.plot_trisurf(tri_,adata.obs[potential_key],cmap=cmap,zorder=2,alpha=0.9)#,cmap=cmap_CellMap,levels=100)
        ax.set_box_aspect(aspect = (1,1,0.8))
        ax.set_title(title,fontsize=18)
        fig.colorbar(cntr, shrink=0.5, orientation='vertical').set_label('Potential',fontsize=20)
        texts = []
        cluster = adata.obs[cluster_key]
        idx = np.zeros(cluster.shape,dtype=bool)
        np.random.seed(seed)
        idx[np.random.choice(len(idx),int(plot_rate*len(idx)),replace=False)] = True
        cluster_set = np.unique(cluster)
        z_shift = 0.1*np.abs( np.max(adata.obs[potential_key]) - np.min(adata.obs[potential_key]))
        if len(cluster_set) <= 10:
            cmap = plt.get_cmap("tab10")
            vmin,vmax = 0,10
        else:
            plt.get_cmap("tab20")
            vmin,vmax = 0,20
        id_color = np.empty(len(cluster),dtype=int)
        for i in range(len(cluster_set)):
            id_color[cluster == cluster_set[i]] = i
            # idx = (cluster == cluster_set[i]) & idx_random
            # ax.scatter(data_pos[idx,0],data_pos[idx,1],adata.obs[potential_key][idx]+z_shift,zorder=100,alpha=0.8,edgecolor='w',color=cmap(i),**kwargs)
            txt = ax.text(np.mean(data_pos[cluster == cluster_set[i]],axis=0)[0],
                           np.mean(data_pos[cluster == cluster_set[i]],axis=0)[1],
                           np.max(adata.obs[potential_key][cluster == cluster_set[i]]),cluster_set[i]
                           ,color=cmap(i),fontsize=20,ha='center', va='center',fontweight='bold',zorder=1000)
            txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
        ax.scatter(data_pos[idx,0],data_pos[idx,1],adata.obs[potential_key][idx]+z_shift,c=id_color[idx],zorder=100,alpha=1,edgecolor='w',vmin=vmin,vmax=vmax,cmap=cmap,**kwargs)
        ax.scatter(data_pos[idx,0],data_pos[idx,1],adata.obs[potential_key][idx]+z_shift*0.5,color='k',zorder=10,alpha=0.1,vmin=vmin,vmax=vmax,cmap=cmap,**kwargs)
    else:
        print('There is no cluster key \"%s\" in adata.obs' % cluster_key)
    ax.view_init(elev=elev, azim=azim);


def write(
    adata,
    filename = 'CellMap.csv',
    basis = 'X_umap',
    potential_key = 'Hodge_potential',
    cluster_key = 'clusters',
    obs_key = None,
    genes = None,
    expression_key = None,
    use_HVG = True,
    n_HVG = 10
):
    kwargs = check_arguments(adata,basis=basis,potential_key=potential_key,cluster_key = 'clusters',obs_key=obs_key,genes=genes,expression_key=expression_key)
    basis,obs_key,genes = kwargs['basis'],kwargs['obs_key'],kwargs['genes']
    
    if expression_key == None:
        if scipy.sparse.issparse(adata.X): data_exp = adata.X.toarray()
        else: data_exp = adata.X
    else:
        data_exp = adata.layers[expression_key]
    
    pd_out = pd.DataFrame({
        'X':adata.obsm[basis][:,0],'Y':adata.obsm[basis][:,1],
        'Potential':adata.obs[potential_key],
        'Annotation':adata.obs[cluster_key]
    },index=adata.obs.index)
    pd_out.index.name='CellID'
    
    if obs_key != None:
        for arg in obs_key:
            pd_out.insert(len(pd_out.columns), arg, adata.obs[arg])
    
    
    if genes != None:
        for gene in genes:
            pd_out.insert(len(pd_out.columns), gene, data_exp[:,adata.var.index == gene])
    
    if use_HVG:
        scanpy.pp.highly_variable_genes(adata,n_top_genes=n_HVG)
        for gene in adata.var.index[adata.var['highly_variable']==True]:
            pd_out.insert(len(pd_out.columns), 'HVG_'+gene, data_exp[:,adata.var.index == gene])
    
    print('succeeded in writing CellMapp data as \"%s.csv\"' % filename)
    print('you can visualize the CDV file by CellMapp viewer https://yusuke-imoto-lab.github.io/CellMapViewer/CellMapViewer/viewer.html')

    display(pd_out)
    
    pd_out.to_csv(filename)


def create_dgraph_potential(
    adata,
    basis = 'X_umap',
    map_key = None,
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cutedge_vol  = None,
    cutedge_length = None,
    ):
    """
    Hodge decomposition

    Parameters
    ----------
    adata: anndata (n_samples, n_features)
    
    basis: ndarray or string
    """
    
    kwargs_arg = check_arguments(adata,
                             basis = basis,
                             map_key = map_key
                            )
    basis,map_key = kwargs_arg['basis'],kwargs_arg['map_key']
    
    data_pos = adata.obsm[basis]
    triangles = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length).triangles
    tri_,idx_tri = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length,return_mask = True)
    triangles = tri_.triangles[idx_tri]
    n_node_ = data_pos.shape[0]
    graph_ = scipy.sparse.lil_matrix(np.zeros([n_node_,n_node_]))
    idx_set = [[0,1],[1,2],[2,0]]
    # idx = np.isnan(data_vel[0])==False
    for id_x,id_y in idx_set:
        weight = adata.obs[potential_key][triangles[:,id_y]].values - adata.obs[potential_key][triangles[:,id_x]].values
        min_weight = np.percentile(np.abs(weight),5)
        graph_[tuple(triangles[weight>min_weight][:,[id_x,id_y]].T[::-1])] = 1
        graph_[tuple(triangles[weight<-min_weight][:,[id_y,id_x]].T[::-1])] = 1
    return scipy.sparse.coo_matrix(graph_)


def create_dgraph(
    adata,
    basis = 'X_umap',
    vel_key  = 'velocity_umap',
    map_key = None,
    potential_key = 'Hodge_potential',
    graph_key = 'CM_graph',
    cutedge_vol  = None,
    cutedge_length = None,
    ):
    """
    Hodge decomposition

    Parameters
    ----------
    adata: anndata (n_samples, n_features)
    
    basis: ndarray or string
    """
    
    kwargs_arg = check_arguments(adata,
                             basis = basis,
                             vel_key = vel_key,
                             map_key = map_key
                            )
    basis,vel_key,map_key = kwargs_arg['basis'],kwargs_arg['vel_key'],kwargs_arg['map_key']
    
    data_pos = adata.obsm[basis]
    data_vel = adata.obsm[vel_key]
    map_pos  = adata.obsm[map_key][:,:2]
    triangles = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length).triangles
    tri_,idx_tri = create_graph(data_pos[:,0],data_pos[:,1],cutedge_vol=cutedge_vol,cutedge_length=cutedge_length,return_mask = True)
    triangles = tri_.triangles[idx_tri]
    n_node_ = data_pos.shape[0]
    graph_ = scipy.sparse.lil_matrix(np.zeros([n_node_,n_node_]))
    idx_set = [[0,1],[1,2],[2,0]]
    idx = np.isnan(data_vel[0])==False
    for id_x,id_y in idx_set:
        X1 = data_pos[:,idx][triangles[:,id_x]]
        X2 = data_pos[:,idx][triangles[:,id_y]]
        V1 = data_vel[:,idx][triangles[:,id_x]]
        V2 = data_vel[:,idx][triangles[:,id_y]]
        weight = np.sum(0.5*(V1+V2)*(X2-X1),axis=1)
        min_weight = np.percentile(np.abs(weight),5)
        graph_[tuple(triangles[weight>min_weight][:,[id_x,id_y]].T[::-1])] = 1
        graph_[tuple(triangles[weight<-min_weight][:,[id_y,id_x]].T[::-1])] = 1
    return scipy.sparse.coo_matrix(graph_)