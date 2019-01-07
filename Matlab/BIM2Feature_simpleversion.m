function BIMFeatures=BIM2Feature_simpleversion(filename)
%% inputs
% filename is the address of the input BIM Json
%% output is a simple version of BIM feature, the concrete parameters of the given wall.
%% an example of inputs *****************

% folder='.\json\DazioWSH4';
% name='RCWall_DazioWSH4_BIM.json';
% filename=[folder,'\',name];

%% **************************************
str = fileread(filename);
BIMdata = jsondecode(str);  %% BIM


h=BIMdata.GeneralInformation.height;
w=BIMdata.StructuralInformation.properties.wallsections.length;
t=BIMdata.StructuralInformation.properties.wallsections.thickness;
E=0;
fpc=0;
material=BIMdata.StructuralInformation.properties.materials;
for i=1:length(material)
    if strcmp(material{i}.type,'concrete')
        E=material{i}.E;
        fpc=material{i}.fpc;       
        break;
    end
end
BIMFeatures=[h w t E fpc];



