function [ newpop ] = copyy( pop,objvalue )
%
totalfit=sum(objvalue);
fitvalue=objvalue/totalfit; % this is the probability that it will survive
[fittemp,pos]=sort(fitvalue);
[sx,sy,sz]=size(pop);
for i=1:sx
    poptemp(i,:,:)=pop(pos(i),:,:);
end
pop=poptemp;

select=rand(sx);
fit=1;
for i=1:sx
    if select(i)<fitvalue(sx+1-i)
        newpop(fit,:,:)=pop(i,:,:);
        fit=fit+1;
    end
end
if fit==1
    newpop=[];
end


end

