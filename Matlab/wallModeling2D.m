 function [nodes,elements]=wallModeling2D(w,h,wb,wn,hn,wbn,level,start_mid)
% w=5;
% wb=1;
% h=10;
% wn=20;
% hn=40;
% wbn=3;
% level=2;

x1=[-w/2:(wb/wbn):-w/2+wb];
x2=[-w/2+wb:(w-2*wb)/wn:w/2-wb];
x3=[w/2-wb:(wb/wbn):w/2];

if wb>0
    x=[x1,x2(2:end-1),x3]+w/2;  %% add w/2;
else
    x=x2+w/2;
end
y=0:h/hn:h;

crd=[];
for yi=0:1:hn
    yc=y(yi+1)*ones((wn+2*wbn+1),1);
    xc=x';
    zc=zeros((wn+2*wbn+1),1);
    crd=[crd;xc,zc,yc];
    
%     for xi=0:1:(wn+2*wbn)       
%     end
end
f=[];
for yi=0:hn-1
    N=wn+2*wbn;
    fx=1:N;
    fx1=fx'+(yi)*(N+1);
    fx2=fx1+1;
    fx3=fx1+(N+1);
    fx4=fx2+(N+1);
    f=[f;fx1,fx2,fx4,fx3];   
end

flag=[ones(1,wbn),zeros(1,wn),ones(1,wbn)];
Tflag=repmat(flag,1,hn);
mainflag=find(Tflag==0);
bflag=find(Tflag==1);

v=0:round(hn/level):hn;
mainv=v*wn;
bv=v*(2*wbn);

fmflag=zeros(1,length(f)); %% face material flag;

mid=start_mid; 
for i=1:level
        mid=mid+1;
    j1=mainv(i)+1:mainv(i+1);
    fmflag(mainflag(j1))=mid;  
    
    mid=mid+1;
    j1=bv(i)+1:bv(i+1);
    fmflag(bflag(j1))=mid;
    

end


% for i=1:length(crd)
%     nodes(i).name=i;
%     nodes(i).ndf=3;
%     crdi=crd(i,:);
%     nodes(i).crd=crdi';
% end

for i=1:length(crd)
    nodes(i).name=i;
    nodes(i).ndf=2;
    crdi=[crd(i,1),crd(i,3)];
    nodes(i).crd=crdi';
end

for i=1:length(f)
    elements(i).name=i-1;
    elements(i).type='FourNodeQuad';
    elements(i).nodes=[f(i,:)]';
    elements(i).material=fmflag(i);
end




