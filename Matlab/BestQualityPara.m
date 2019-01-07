clc
clear all
load('data/L2.mat');
load('data/cosSimilarity.mat');
load('data/para64.mat')
load('data/CC.mat');

variables=[variables(:,1), variables(:,3)]; %%% the most import one is Ap and Bn

CS=cosSimilarity;
n=size(CS,1)
paraCS=[];
paraL2=[];
paraCC=[];
VCS=[];
VL2=[];
VCC=[];
for k=1:n
    x=1:1:64;
    y=1:9;
    for i=1:64
        for j=1:9
            MCS(i,j)=CS(k,i,j);
            ML2(i,j)=L2(k,i,j);
            MCC(i,j)=CC(k,i,j);
        end
    end
    %% method 1
    method=1;
    if method==1
        maximum = max(max(MCS));
        [x1,y1]=find(MCS==maximum)
        paraCS=[paraCS;variables(x1,:),y1];
        
        minimum = min(min(ML2));
        [x2,y2]=find(ML2==minimum);
        paraL2=[paraL2;variables(x2,:),y2];
        
   %     labelM=[labelM;x1,y1,x2,y2];
        maximum = max(max(MCC));
        [x3,y3]=find(MCC==maximum);
        paraCC=[paraCC;variables(x3,:),y3];
        VCC=[VCC;MCC(:)];
        VL2=[VL2;ML2(:)];
        VCS=[VCS;MCS(:)];

    end
end



NewVL2=VL2;
for i=1:51
    i1=i*576-575;i2=i*576;
    V=VL2(i1:i2);
    maxv=max(V);minv=min(V);
    newV=(V-minv)/(maxv-minv);
    NewVL2(i1:i2)=newV;
end


para=paraL2';
csvwrite(['bestParaL2.txt'],para);

para=paraCS';
csvwrite(['bestParaCS.txt'],para);

para=paraCC';
csvwrite(['bestParaCC.txt'],para);
