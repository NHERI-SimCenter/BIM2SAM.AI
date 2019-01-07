% The goal of this procedure is to create new SAM files for walls. 
% The input parameters come from two sides: 1> parameters exited in the BIMs
% 2> predictions from Neural Network including (material parameters: Ap and Bn and geometry parameter N, the number of quads along the horizontal direction of the web part)

clc
clear
close all

%basePath = fullfile(pwd,'json');
basePath = fullfile(pwd,'Data','json');
folders = dir(basePath);
folderNames = {folders.name};
id = [folders.isdir] & ~ismember(folderNames,{'.','..'});
folderNames = folderNames(id);


flist=dir ([basePath,'/*/*ContinuumSAM_2.json']);
n=length(flist);
 %% 10 model ids. For these walls, we create the new SAM files.
PredIDs=[2 4 7 12 14 21 29 38 41 48]  
%% output of Neural Network
dn=[9 10 9 4 8 4 4 6 10 9]
aps=[0.41560218 0.42066967 0.46618402 0.35359 0.29063696 0.31456083 0.30781254 0.3287022  0.43574965 0.09797192]
bns=[0.654 0.663 0.843 0.785 0.434 0.726 0.707 0.827 0.570 0.797 ]

mIDsize=[];
for testi=1:10
    i=PredIDs(testi);
    f1=flist(i).folder;
    f2=flist(i).name;
    f = fullfile(f1,f2);
    str = fileread(f);
    data = jsondecode(str);  %% old SAM
    
    
    %% Parameters from BIM file.
    flistBIM=dir([flist(i).folder,'/*_BIM.json']);
    bimf1=flistBIM(1).folder;
    bimf2=flistBIM(1).name;
    f=fullfile(bimf1,bimf2);
    str = fileread(f);
    BIMdata = jsondecode(str);  %% BIM
    h=BIMdata.GeneralInformation.height;
    c=BIMdata.StructuralInformation.layout.clines(2).location;
    w=c(1);
    wb=BIMdata.StructuralInformation.properties.wallsections.boundaryElementLength;
    %w=w-2*wb
    
    level=BIMdata.GeneralInformation.stories;
    wbn=2;        %% number of quad on the wall boundary. (along horizontal direction) 
    wn=dn(testi); %% number of quad on the main part.     (along horizontal direction)
    hn=round(h/level/((w-2*wb)/wn))*level;   %% number of quad along vertial direction
    material=data.StructuralAnalysisModel.properties.ndMaterials;
    for k=1:length(material)
        mi=material{k};
        if strcmp(mi.type,'Concrete')
            mi.beta=0.370190655;
            mi.Ap=aps(testi);
            mi.An=3.45;
            mi.Bn=bns(testi);
            material{k}=mi;
            concreteID=k;
            break;
        end        
    end
    [nodes,elements]=wallModeling2D(w,h,wb,wn,hn,wbn,level,concreteID);
    %        nodes1=data.StructuralAnalysisModel.geometry.nodes;
    %     elements1=data.StructuralAnalysisModel.geometry.elements;
    pt=[];
    for i=1:length(nodes)
        crd=nodes(i).crd;
        crd=crd';
        pt=[pt;crd];
    end
    nodemap=nodeMapping(w,h,level,pt);
    
    data.StructuralAnalysisModel.geometry.nodes=nodes;
    data.StructuralAnalysisModel.geometry.elements=elements;
    data.StructuralAnalysisModel.nodeMapping=nodemap;

    data.StructuralAnalysisModel.properties.ndMaterials=material;
    
    oldField = 'StructuralAnalysisModel';
    newField = 'Structural Analysis Model';
   % data.Structural_0x20_Analysis_0x20_Model=data.(oldField);
   % [data.newField] = data.(oldField);
   % data = rmfield(data,oldField);
    
    dataout=jsonencode(data);
    newdataout=[char('{"Structural Analysis Model"'),dataout(27:end)];
    %address=[f1,'\',f2(1:end-5),'_new',num2str(wbn-1),'.json'];
    address=fullfile(f1,[f2(1:end-7),'.json']);
    fileID = fopen(address,'w');
    fprintf(fileID,newdataout);
    fclose(fileID);
    

    
    
 %% generating script for create TCL file and running opensees   
    string1=bimf2;
    string2=[f2(1:end-7),'.json'];
    string3=[bimf2(1:end-8),'EVT.json'];
    string4=[bimf2(1:end-8),'EDP.json'];
    string5=[bimf2(1:end-9),'.tcl'];
    address=fullfile(f1,'run.bat');
    fid = fopen(address,'wt');
    fprintf(fid, 'project1 %s %s %s %s %s', string1, string2, string3, string4, string5);
    fclose(fid);
    

    address=fullfile(f1,'run_opensees.bat');
    fid = fopen(address,'wt');
    fprintf(fid, 'OpenSees.exe %s',string5);
    fclose(fid);
    
end
