function BIMFeatures=BIM2Feature(randProj,filename)
%% inputs
% M is a rand projection matrix
% filename is the address of the input BIM Json
%% an example of inputs *****************

% folder='.\json\DazioWSH4';
% name='RCWall_DazioWSH4_BIM.json';
% filename=[folder,'\',name];
% 
% rng(1234);
% randProj=randn(9,1024);
% randProj=normr(randProj);

%% **************************************
str = fileread(filename);
BIMdata = jsondecode(str);  %% BIM

wallSec=BIMdata.StructuralInformation.properties.wallsections;
wallSec.height=BIMdata.GeneralInformation.height;

len=wallSec.length;
if isfield(wallSec,'boundaryElementLength')
    blen=wallSec.boundaryElementLength;
else
    blen=0;
end

longspace=wallSec.longitudinalRebar.spacing;
numBarsLength=(len-2*blen)/longspace;
wallSec.longitudinalRebar.numBarsLength=floor(numBarsLength)+1;

hei=wallSec.height;
transpace=wallSec.transverseRebar.spacing;
num_bars_height=(hei)/transpace;
wallSec.transverseRebar.num_bars_height=floor(num_bars_height)+1;

if isfield(wallSec,'transverseBoundaryElementRebar')
    transpace=wallSec.transverseBoundaryElementRebar.spacing;
    num_bars_height=(hei)/transpace;
    wallSec.transverseBoundaryElementRebar.num_bars_height=floor(num_bars_height)+1;    
end

web_l=len-2*blen;
web_h=wallSec.height;
if isfield(wallSec,'thickness')
    web_t=wallSec.thickness;
else
    web_t=wallSec.web_thickness;
end

if isfield(wallSec,'flange_thickness')
    BE_t=wallSec.flange_thickness;
else
    if isfield(wallSec,'bottom_flange_width')
        BE_t=wallSec.bottomFlangeWidth;
    else
        BE_t=web_t;
    end
end

if BE_t==0
    if isfield(wallSec,'web_thickness')
        BE_t=wallSec.webThickness;
    else
        if isfield(wallSec,'thickness')
            BE_t=wallSec.thickness;
        end
    end
end

nl=wallSec.longitudinalRebar.numBarsLength;
nt=wallSec.longitudinalRebar.numBarsThickness;
diam=sqrt(wallSec.longitudinalRebar.barArea*4/pi);
%diam=wallSec.longitudinalRebar.barDiam;
p0=[0,0,0];

spacel=longspace;
spacet=web_t-2*wallSec.longitudinalRebar.cover-3*diam;
lbar=longBarPara(web_l,web_h,web_t,nl,nt,spacel,spacet,diam,p0,2);


nh=wallSec.transverseRebar.num_bars_height;
spaceh=transpace;
spacet=web_t-2*wallSec.longitudinalRebar.cover-1*diam;
%tbar=tranBarParla(web_l,web_h,web_t,nh,nt,spaceh,spacet,diam,p0,3)
tbar=BEtranBarParla(web_l,web_h,web_t,nl,nh,nt,spacel,spaceh,spacet,diam,p0,3);

BElbar1=[];
BElbar2=[];
BEtbar1=[];
BEtbar2=[];
if isfield(wallSec,'longitudinalBoundaryElementRebar')
    l=wallSec.boundaryElementLength;
    cover=wallSec.longitudinalBoundaryElementRebar.cover;
    
    nl=wallSec.longitudinalBoundaryElementRebar.numBarsLength;
    nt=wallSec.longitudinalBoundaryElementRebar.numBarsThickness;
    %diam=wallSec.longitudinalBoundaryElementRebar.barDiam;
    diam=sqrt(wallSec.longitudinalBoundaryElementRebar.barArea*4/pi);   
    spacel=(l-2*cover-3*diam)/(nl-1);
    spacet=(BE_t-2*cover-3*diam)/(nt-1);
    if ~isnan(nl+nt)
        p0=[(web_l+l)/2,0,0];
        BElbar1=longBarPara(l,web_h,BE_t,nl,nt,spacel,spacet,diam,p0,4);
        p0=[-(web_l+l)/2,0,0];
        BElbar2=longBarPara(l,web_h,BE_t,nl,nt,spacel,spacet,diam,p0,4);
    end
end

if isfield(wallSec,'transverseBoundaryElementRebar')
    transpace=wallSec.transverseBoundaryElementRebar.spacing;
    num_bars_height=(hei)/transpace;
    wallSec.transverseBoundaryElementRebar.num_bars_height=floor(num_bars_height)+1;   
    l=wallSec.boundaryElementLength;
    nl=wallSec.transverseBoundaryElementRebar.numBarsLength;
    nt=wallSec.transverseBoundaryElementRebar.numBarsThickness;
    nh=wallSec.transverseBoundaryElementRebar.num_bars_height;
    diam=sqrt(wallSec.transverseBoundaryElementRebar.barArea*4/pi);   
    cover=wallSec.longitudinalRebar.cover;
    
    p0=[(web_l+l)/2,0,0];    
    spacel=(l-2*cover-1*diam)/(nl-1);
    spacet=(BE_t-2*cover-1*diam)/(nt-1);
    spaceh=transpace;
    BEtbar1=BEtranBarParla(l,web_h,BE_t,nl,nh,nt,spacel,spaceh,spacet,diam,p0,5);
    
    p0=[-(web_l+l)/2,0,0];
    BEtbar2=BEtranBarParla(l,web_h,BE_t,nl,nh,nt,spacel,spaceh,spacet,diam,p0,5);
end

box=[0,0,web_h*0.5,web_l,web_t,web_h,1];
if (wallSec.boundaryElementLength > 0.0)
    l=wallSec.boundaryElementLength;
    t=BE_t;
    h=web_h;
    p1=[(web_l+l)/2,0,h/2];
    p2=[-(web_l+l)/2,0,h/2];
    box=[box;[p1,l,t,h,1];[p2,l,t,h,1]];
end

Para1=[lbar;tbar];
Para2=[];
if ~isempty(BElbar1)
    Para2=[Para2;BElbar1;BElbar2];
end
if ~isempty(BEtbar1)
    Para2=[Para2;BEtbar1;BEtbar2];
end

Para=[box;Para1;Para2];

%%%% old BIM para
% wallPara{i}=Para;

%%% new BIM para
n=size(Para,1);
newPara=zeros(n,9);
for k=1:size(Para,1)
    pk=Para(k,:);
    newpk=[pk,0,0];
    id=pk(7);
    if id>1 %% steel
        fy=BIMdata.StructuralInformation.properties.materials{id}.fy;
        newpk(7)=fy;
    end
    
    if id==1  %% concrete
        E=BIMdata.StructuralInformation.properties.materials{id}.E;
        fpc=BIMdata.StructuralInformation.properties.materials{id}.fpc;
        newpk(7)=0;
        newpk(8)=E;
        newpk(9)=fpc;
    end
    newPara(k,:)=newpk;
end

M=newPara*randProj;
%v=sum(normc(M));
v=sum(M);
BIMFeatures=cos(v);


