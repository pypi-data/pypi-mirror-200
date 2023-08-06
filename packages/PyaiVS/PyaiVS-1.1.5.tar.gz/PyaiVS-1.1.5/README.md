# What is OCAICM ?
The tool can complete the construction of diffierent dataset classification models with only one line of code, and recommend the optimal model for virtual screening.  
The tool integrates multiple machine learning models, common molecular descriptors and three data set splitting methods.   
The tool integrates the virtual screening function and uses the optimal model to screen the quick screening of the compound library provided by users through a single code.



# How to use this tool ?

## 1 Bulid the environment

1. conda create -n envir_name python=3.8              
2. conda install rdkit rdkit             
3. conda install pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cudatoolkit=10.2 -c pytorch  # need to confirm your cuda>=10.2  
4. conda install -c dglteam dgl==0.4.3post2   
5. conda install **xgboost,hyperopt,mxnet,requests,mdtraj**    
6. pip install PyaiVS   

## 2 Bulid models

### 1 Submit a file in a given .csv format file(Simple single task only needs to provide two columns of content: Smiles and label)              
   such as  (The result output is the optimal model recommendation order considering AUC_ROC and F1_score):                
|Smiles |task1|task2|...|taskn|   
|smiles1|  0  |  0  |...|  1  |   
|smiles2|  0  |  1  |...|  1  |    
...         
|smilesm|  1  |  0  |...|  0  |     
Dataframe including smiles and labels. Can be loaded by pandas.read_csv(file_path). One column includes smiles and other columns for labels.Column names other than smiles column would be considered as task names.                      
    
    >>>from PyaiVS import model_bulid                                
    >>>model_bulid.running('submit_file.csv')                     
    auc_roc model    des   split  f1-score                                     
    1  0.871495   SVM  MACCS  random  0.783812                      
    
### 2 Parameter setting

model_bulid.running(file_name,out_dir = './',split=None,model=None,FP=None, cpus=4)         
* 1 file_name         
#the submitted file             
* 2 out_dir = './'            
#As the processing can generate some file , we need to give a dir to save this file. If there is no input,by default, it is in the same directory as the submission folder.         
* 3 split=None            
#There are three ways to partition data sets `['random','scaffold','cluster']`.If there is no input, only random will be used by default.          
* 4 model=None            
#There are nine methods for data set modeling `['SVM','RF','KNN','DNN','XGB','gcn','gat','attentivefp','mpnn']`. If there is no input, only SVM will be used by default.           
* 5 FP=None           
#Compound molecular fingerprint, there are four choices `['MACCS','ECFP4','2d-3d','pubchem']`.If there is no input, only MACCS will be used by default.            
* 6 cpus=4            
#When executing the traditional machine learning model algorithm, parallel computing can be selected. By default, 4 tasks are performed simultaneously.         
If a parameter task has been run, the modeling will not be performed again if the same parameter is entered.            
###### such as:  


    >>>from PyaiVS import model_bulid
    >>>model_bulid.running('Opioid_receptor_δ.csv',FP=['MACCS','ECFP4','pubchem'],model=['all'],split=['all'])
           model          des     split   auc_roc  f1_score      dist
    30   attentivefp  attentivefp    random  0.986480  0.967697  0.035018
    36   attentivefp  attentivefp   cluster  0.984862  0.966212  0.037024
    37   attentivefp  attentivefp  scaffold  0.984278  0.964374  0.038941
    35           gcn          gcn  scaffold  0.984983  0.963660  0.039321
    34           gcn          gcn    random  0.985115  0.963107  0.039782
    53           SVM        ECFP4    random  0.978375  0.964588  0.041492
    42           gcn          gcn   cluster  0.983298  0.961965  0.041540
    29           XGB        ECFP4    random  0.986725  0.958675  0.043405
    38           gat          gat    random  0.984019  0.957108  0.045772
    41           gat          gat   cluster  0.983390  0.955268  0.047716
    39           gat          gat  scaffold  0.983987  0.953511  0.049169
    48           XGB        MACCS    random  0.980382  0.944309  0.059045
    54           XGB        ECFP4   cluster  0.977971  0.943439  0.060699
    58           SVM        ECFP4   cluster  0.973957  0.943299  0.062396
    67           SVM        MACCS    random  0.966156  0.943412  0.065936
    64           XGB      pubchem   cluster  0.967548  0.937046  0.070826
    68           XGB        MACCS   cluster  0.965219  0.928265  0.079723
    72           KNN        ECFP4    random  0.964047  0.926797  0.081555
    82           SVM      pubchem   cluster  0.954311  0.930405  0.083252
    79           SVM        MACCS   cluster  0.955818  0.925836  0.086327
    73            RF        ECFP4    random  0.962057  0.921953  0.086781
    76            RF        ECFP4   cluster  0.961408  0.922007  0.087019
    77           KNN        MACCS    random  0.956867  0.919020  0.091751
    80           KNN        ECFP4   cluster  0.955816  0.915223  0.095600
    87            RF      pubchem   cluster  0.947577  0.904609  0.108847
    93            RF        MACCS   cluster  0.937535  0.906647  0.112323
    91           KNN        MACCS   cluster  0.941800  0.902867  0.113234
    105          XGB        ECFP4  scaffold  0.917542  0.903720  0.126764
    99           KNN      pubchem   cluster  0.925052  0.897299  0.127141
    106          SVM        ECFP4  scaffold  0.913976  0.899114  0.132582
    111          XGB        MACCS  scaffold  0.909663  0.901587  0.133589
    110           RF        MACCS  scaffold  0.909876  0.900669  0.134123
    113          KNN        ECFP4  scaffold  0.904415  0.905752  0.134236
    100           RF        MACCS    random  0.924256  0.883566  0.138903
    114           RF        ECFP4  scaffold  0.903923  0.892580  0.144117
    116          SVM        MACCS  scaffold  0.889971  0.885385  0.158880
    119          KNN        MACCS  scaffold  0.875938  0.865300  0.183127
    134          XGB      pubchem  scaffold  0.762263  0.858899  0.276457
    130          XGB      pubchem    random  0.782765  0.824306  0.279391
    131           RF      pubchem    random  0.779325  0.821290  0.283962
    137           RF      pubchem  scaffold  0.752757  0.857024  0.285607
    141          KNN      pubchem  scaffold  0.745604  0.851177  0.294730
    135          KNN      pubchem    random  0.759896  0.817813  0.301400
    140          SVM      pubchem    random  0.747886  0.817545  0.311210
    142          SVM      pubchem  scaffold  0.723828  0.837551  0.320407
    151          DNN        MACCS   cluster  0.500079  0.644619  0.613365
    148          DNN      pubchem  scaffold  0.503136  0.636747  0.615489
    149          DNN        MACCS    random  0.502265  0.617676  0.627624
    159          DNN        ECFP4   cluster  0.498636  0.616181  0.631413
    161          DNN        ECFP4    random  0.497590  0.611441  0.635133
    150          DNN      pubchem   cluster  0.501218  0.599697  0.639551
    153          DNN      pubchem    random  0.499805  0.598794  0.641218
    155          DNN        ECFP4  scaffold  0.498953  0.597844  0.642478
    158          DNN        MACCS  scaffold  0.498698  0.586520  0.649822
    (The result output is the optimal model recommendation order considering AUC_ROC and F1_score)

### 3 Generated Files


The process will generate a directory with the same name as the input file in the output location.  
submit_file     
>submit_file.csv                   // Copy of original document      
>> submit_file_pro.csv               // Modeling data after data preprocessing         
>> submit_file_auc.csv               // AUC-ROC numerical statistics results of all models     
>> model_save                        // Save folder of modeling model      
>>> KNN                           // Different algorithm models are saved separately            
>>> SVM             
>>>> cluster_cla_MACCS_SVM_bestModel.pkl     
>>>> random_cla_ECFP4_SVM_bestModel.pkl      
>>>> ...     

>>> GCN     
>>> ...   

>> result_save                       // Save folder of modeling data results       
>>> KNN                           // The results of different algorithms are saved separatel        
>>> SVM     
>>> RF      
>>>> random_RF_ECFP4_best.csv  // Model Results of Ten Times Random Seeds with Optimal Parameters        
>>>> random_RF_ECFP4_para.csv  // Saving model results under optimal parameters      
>>>> ...     

>> submit_file.smi                   // Intermediate file generated by padelpy descriptor calculation      
>> submit_file_23d.csv               // 2D-3D descriptor characteristic file       
>> submit_file_pro.bin               // Graph based feature file       
>> submit_file_punchem.csv           // Pubchem fingerprint file       

## 3 Virtual Screen     
model_screen(screen_file=None,model_dir=None,model=None,FP= None,split=None,prop = 0.5,sep = ',',smiles_col =None)
* 1 screen_file   # Compound library files used for screening 
* 2 model_dir # Model generated during modeling in the previous step_ Save location
* 3 model   # the best model recommended by model_bulid.py ,The default value is SVM.
* 4 FP      # the best FP recommended by model_bulid.py ,it can omit if model in graph model.The default value is MACCS.
* 5 split   # the best model recommended by model_bulid.py ,The default value is random.
* 6 prop    # When the prediction probability of the compound is greater than this value, the compound will be identified as an active compound,The default value is 0.5.
* 7 sep     # Content separator of compound library file ,The default value is ','.
* 8 smiles_col #  The column name of the smiles column in the compound library file,The default value is Smiles.

###### such as:       

    >>>from OCAICM import virtul_screen
    >>>virtul_screen.model_screen(model='attentivefp',FP= None,split='random',screen_file='/tmp/screen',prop = 0.5,sep = ',',
        model_dir='/tmp/Opioid_receptor_δ/model_save/',smiles_col=0)
    (Finally, folder screen will be generated under the set mdoel_dir peer directory to store the filtering results)


 

    
    
