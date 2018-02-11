function newpop=mutation(pop,pm,popsize,newpop1,newpop2,handles)
[sx sy sz]=size(pop);
[sx1 sy1 sz1]=size(newpop1);
[sx2 sy2 sz2]=size(newpop2);
%% set the number of population
if isempty(newpop1)
    poptemp=[newpop2];
else if isempty(newpop2)
        poptemp=[newpop1];
    else
        poptemp=[newpop1;newpop2];
    end
end

if (sx1+sx2)>0.8*popsize
    pop1=bin2no(newpop1);
    pop2=bin2no(newpop2);
    mtemp=meritcalc([pop1;pop2],handles);
    [~, pos]=sort(mtemp);
    for i=1:0.8*popsize
        poptemp2(i,:,:)=poptemp(pos(i),:,:);
    end
    pad=round(rand(0.2*popsize,sy,sz));
    poptemp2=[poptemp2;pad];
end

if (sx1+sx2)<=0.8*popsize
    padx=popsize-sx1-sx2;
    pad2=round(rand(padx,sy,sz));
    poptemp2=[poptemp;pad2];   
end
%%mutation
for i=1:sz
    for j=1:popsize
        for k=1:sy
            if rand<pm
                poptemp2(j,k,i)=1-poptemp2(j,k,i);
            end
        end
    end
end
newpop=poptemp2;

end

