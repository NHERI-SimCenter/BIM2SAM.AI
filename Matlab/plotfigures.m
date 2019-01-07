clear;
close all;
clc;

output = {'JoshOutput','MaekawaOutput','Josh_Reg','Maekawa_Reg'};


basePath = fullfile(pwd,'Data','ConcreteShearWallBeamcolumn','For AI-M');
folders = dir(basePath);
folderNames = {folders.name};
id = [folders.isdir] & ~ismember(folderNames,{'.','..'});
folderNames = folderNames(id);
for i=1:length(folderNames)
    

    name=folderNames{i};
    
    
    
    cd(fullfile(basePath,folderNames{i}));
    
%     for j=5:2:9
%     cd([name,'nInt',num2str(j)]);
%     !rm Elem*.out
%     !rm base*.out
%     !rm Section*.out
%     cd('..')
%     end
%     continue
    
    
    fprintf(1,'Running analyses for model %s\n',folderNames{i});
    %[status, result] = dos('opensees.exe wallDriver.tcl', '-echo');
    
    
    
    try
        DTop5 = load(['nInt5','/outputs','/Dtop.out']);
        RBase5 = load(['nInt5','/outputs','/RBase.out']);
        DTop7 = load(['nInt7','/outputs','/Dtop.out']);
        RBase7 = load(['nInt7','/outputs','/RBase.out']);
        DTop9 = load(['nInt9','/outputs','/Dtop.out']);
        RBase9 = load(['nInt9','/outputs','/RBase.out']);
        
        edpfile = fullfile(['RCWall_',name, '_EDP.json']);
        edpdata = loadjson(edpfile);
        if isfield(edpdata.EngineeringDemandParameters{1}.responses{1},'data')
            
            figure
            hold on
            title(name)
            
            force_exp = edpdata.EngineeringDemandParameters{1}.responses{1}.data;
            evtfile = fullfile(['RCWall_',name, '_EVT.json']);
            evtdata = loadjson(evtfile);
            d_exp = evtdata.Events{1}.timeSeries{end}.values;
            plot(d_exp,force_exp,'k-o')
            plot(DTop5(:,1),-RBase5(:,1),'r-')
            plot(DTop7(:,1),-RBase7(:,1),'g-')
            plot(DTop9(:,1),-RBase9(:,1),'b-')
            xlabel('Displacement at top')
            ylabel('Shear force')
            legend('Experiment','Simulation - nInt5','Simulation - nInt7','Simulation - nInt9','Location','northwest')
            
            box on
            grid on
            print(['../../../../Figures/',name,'.png'],'-dpng')
            close all
            
            
%             figure
%             plot(d_exp)
%             figure
%             plot(DTop5(:,1))
%             figure
%             plot(force_exp)
%             figure
%             plot(-RBase5(:,1))
%             close all
            
        end
    catch
        i
    end
    
end
