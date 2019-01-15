clc;
clear all;
% folder='.\json\DazioWSH4';
% name='RCWall_DazioWSH4_BIM.json';
% filename=[folder,'\',name];

rng(1234);
randProj=randn(9,1024);
randProj=normr(randProj);

flist=dir ('../Data/json/*/*BIM.json');
HWT51=[];
BIMfeature51=[];
for i=1:length(flist)
    f1=flist(i).folder;
    f2=flist(i).name;
    filename=[f1,'/',f2];    
    Features1=BIM2Feature(randProj,filename);
    Features2=BIM2Feature_simpleversion(filename);
    
    BIMfeature51=[BIMfeature51;Features1];
    HWT51=[HWT51;Features2];    
end

csvwrite(['wall_fe51v1.txt'],BIMfeature51);

%% processing the simple version of BIM feature. 
para=HWT51;
%[h w t E fpc]
para(:,4)=para(:,4)/max(para(:,4));
para(:,5)=para(:,5)/max(para(:,5));
para(:,1:3)=para(:,1:3)/176;
csvwrite(['wallHWT51.txt'],para);
