clear all
clc

addpath('../jsonlab-1.5')
basePath = fullfile(pwd,'json-pv');
folders = dir(basePath);
folderNames = {folders.name};
id = [folders.isdir] & ~ismember(folderNames,{'.','..'});
folderNames = folderNames(id);

for expID=1:length(folderNames)
    resultFileName = ['json-pv/',folderNames{expID},'/dakota/dakotaTab.dat'];
    data = importdata(resultFileName);
    variables = data.data(:,1:4);
    results = data.data(:,5:end);
    
    for i=expID
        resultLength = size(results,2);
        name = folderNames{i};
        
        resultsData = results;
        resultsData = resultsData(:,1:end);
        
        % experiment data
        EVT = loadjson(['json-pv/',name,'/RCWall_',name,'_EVT.json']);
        EVT = EVT.Events{1};
        disp = EVT.timeSeries{end}.values;
        disp=disp(3:end);
        EDP = loadjson(['json-pv/',name,'/RCWall_',name,'_EDP.json']);
        forceEXP = EDP.EngineeringDemandParameters{1}.responses{1}.data;
        forceEXP = forceEXP(3:end);
        
        
        for j=1:size(resultsData,1)
            for k=1:9
                forceSIM = resultsData(j,(1:length(disp))+length(disp)*(k-1));
                forceEXP(forceEXP==0)=0.001;
                L2_tmp = norm((forceEXP-forceSIM)./length(forceEXP));
                cosSimilarity_tmp = dot(forceEXP,forceSIM)/norm(forceEXP)/norm(forceSIM);
                
                if isinf(L2_tmp) || isinf(cosSimilarity_tmp)
                    fprintf('stop because Inf exits.\n')
                    return;
                end
                L2(expID,j,k) = L2_tmp;                        % L2 norm
                cosSimilarity(expID,j,k) = cosSimilarity_tmp;  % cos similarity
                C1=cov(forceEXP,forceSIM);
                C2=C1(1,2)*C1(2,1)/(C1(1,1)*C1(2,2))
                CC(expID,j,k)=C2;                              % correlation coefficient
            end
        end
        
    end
end

save('data/L2.mat','L2');
save('data/cosSimilarity.mat','cosSimilarity');
save('data/CC.mat','CC');

