function handles=boosting(handles)


Dataset=struct;
load('dataset.mat');
validlayer=[];

%% create tag
[~,fntemp]=tagcreate(handles);
%% sort data
for i=2:1:20  %find valid layers
    if isfield(Dataset,strcat(fntemp,num2str(i)))==1,
        validlayer=[validlayer i];

    end
end
datapool=zeros(9999,max(validlayer)+1);
count=1;
for i=validlayer
    [tempdata,~]=size(Dataset.(strcat(fntemp,num2str(i))).recipe);
    datapool(count:count+tempdata-1,2:i+1)=Dataset.(strcat(fntemp,num2str(i))).recipe;
    
    count=count+tempdata;
end
datapool(~any(datapool,2),:)=[];  %remove zero
datapool(:,1)=meritcalc(datapool(:,2:end),handles);
[data,layer]=size(datapool);
if layer>=4
    for i=1:data
        for j=3:layer-1
            if(datapool(i,j))==0
                datapool(i,j-1)=datapool(i,j-1)+datapool(i,j+1);
                datapool(i,j+1)=0;
            end
        end
    end
end
[~,order]=sort(datapool(:,1));
set(handles.ds,'Data',datapool(order,:));
[~,int1]=meritcalc(datapool(order(1),2:end),handles,1);
handles.int=int1;
handles.int2=int1;

end



