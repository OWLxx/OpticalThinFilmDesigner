function [ handles] = generationalgorithm( handles )
global Nooflayer;
global Noofgen;
cla(handles.axes1);
cla(handles.axes2);
cla(handles.axes3);
% parameter of GA
popsize=100; %size of population
chromlength=8; % In general, the resolution is high enough for coating
pc=0.15; % probability of cross over
pm=0.0018; % probability of mutation

%% Initialize
handles.meritvalue=1e10*ones(1,Noofgen);
pop=round(rand(popsize,chromlength,Nooflayer));
handles.recipe=zeros(Noofgen,Nooflayer);
%% Generation Algorithm
for i=1:Noofgen
    tic;
    % Calculate current merit value
    pop2=bin2no(pop);  % this is the normalized thickness
    objvalue=meritcalc(pop2,handles); % this is merit value
    %%
    [minmv, minp]=max(objvalue); % for plotting
    %%
    handles.recipe(i,:)=pop2(minp,:);
    handles.meritvalue(i)=minmv;
   
    newpop1=copyy(pop,objvalue);  % copy, duplicate
    newpop2=crossover(pop,pc,newpop1); % crossover
    newpop=mutation(pop,pm,popsize,newpop1,newpop2,handles); %mutation, population for next generation
    pop=newpop;
    disp(strcat('Generation ',num2str(i)));
    toc;
end
    axes(handles.axes3);
    plot(1:i,handles.meritvalue,'b*');
    title('meritvalue vs generation');
    xlabel('generation');
    ylabel('meritvalue');

%% Find best one among all the generation, plot it 
[finalmv,finalpos]=max(handles.meritvalue);
%%
finalrecipe=handles.recipe(finalpos,:);
[~,int1]=meritcalc(finalrecipe,handles,1);
handles.int=int1;
handles.int2=int1;
%% save weak simulation
Dataset= struct;
[fn,~]=tagcreate(handles);
load('dataset.mat');
if isfield(Dataset,fn)
    dataorder=length(Dataset.(fn).mvalue);
else 
    dataorder=0;
end
count=round(Noofgen/5);
if count~=0
    mvaluetemp=sort(handles.meritvalue);
    for i=1:count
        temp=find(mvaluetemp(i)==handles.meritvalue);
        tempgen(i,:)=temp(1); % find which generation will be saved
        Dataset.(fn).recipe(dataorder+i,:)=handles.recipe(tempgen(i),:);
        Dataset.(fn).mvalue(dataorder+i,:)=handles.meritvalue(tempgen(i));     
    end 
   save ('dataset.mat','Dataset');
   disp(['Dataset now has ',num2str(length(Dataset.(fn).mvalue)),' data']);
   set(handles.fn,'String',fn);
   [~,ord]=sort(Dataset.(fn).mvalue);
   set(handles.ds,'Data',[sort(Dataset.(fn).mvalue)   Dataset.(fn).recipe(ord,:)]);
end

end


