function newpop=crossover(pop,pc,newpop1)
[sx sy sz]=size(pop);
[sx1 sy1 sz1]=size(newpop1);
% set parents
if sx1~=0
    temporder=randperm(sx);
    for i=1:1:sx1
        pop(temporder(i),:,:)=newpop1(i,:,:);
    end
end
% crossover
fit=1;
for i=1:sz
    for j=1:2:sx-1
        if rand<pc
            breakpoint=round(rand*(sy-1));
            newpop(fit,:,i)=[pop(j,1:breakpoint,i) pop(j+1,breakpoint+1:end,i)];
            newpop(fit+1,:,i)=[pop(j+1,1:breakpoint,i) pop(j,breakpoint+1:end,i)];
            fit=fit+2;
        end
       
    end
end
[xt,yt,zt]=size(newpop);
if zt~=sz
    newpop(:,:,sz)=zeros(xt,yt);
end
    
end

